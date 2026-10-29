#!/usr/bin/env python3
"""Offline SEO acceptance check for onepunchmed.github.io.

Usage:
    python3 _dev/seo/seo_check.py                              # repo root = cwd
    python3 _dev/seo/seo_check.py --root path/to/repo
    python3 _dev/seo/seo_check.py --site https://example.com   # after domain move

Exit code 0 = all checks pass, 1 = at least one FAIL.
Standard library only.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_SITE = "https://onepunchmed.com"
AUTHOR_NAME = "Chun Jui Lu"
EXCLUDE = {"_dev"}

# Owner decision 2026-10-26: block training crawlers, allow search crawlers.
MUST_BLOCK = ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
              "meta-externalagent", "CCBot", "Bytespider"]
MUST_NOT_BLOCK = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User",
                  "PerplexityBot", "Perplexity-User", "Googlebot", "Bingbot",
                  "Meta-WebIndexer"]
# Paths search crawlers may be disallowed from.
ALLOWED_DISALLOWS = {"/_dev/"}

# Author identity: English name only, no titles/credentials on articles.
FORBIDDEN_AUTHOR_KEYS = {"jobTitle", "honorificPrefix", "honorificSuffix",
                         "alumniOf", "hasCredential", "alternateName"}
TITLE_PATTERN = re.compile(r"醫師|博士|\bM\.?D\b|\bDr\b", re.I)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title = None
        self.metas, self.links, self.jsonld = [], [], []
        self.h1_texts = []
        self.hrefs, self.times = [], []
        self.author_links = []          # (href, text)
        self._svg = 0
        self._mode = None               # "title" | "jsonld" | "h1" | "author"
        self._buf = []
        self._author_href = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "svg":
            self._svg += 1
        elif tag == "title" and not self._svg and self.title is None:
            self._mode, self._buf = "title", []
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._mode, self._buf = "jsonld", []
        elif tag == "h1":
            self._mode, self._buf = "h1", []
        elif tag == "a" and a.get("href") is not None:
            self.hrefs.append(a["href"])
            if "author" in (a.get("rel") or "").split():
                self._mode, self._buf, self._author_href = "author", [], a["href"]
        elif tag == "time" and a.get("datetime"):
            self.times.append(a["datetime"])

    def handle_endtag(self, tag):
        text = "".join(self._buf).strip()
        if tag == "svg" and self._svg:
            self._svg -= 1
        elif tag == "title" and self._mode == "title":
            self.title, self._mode = text, None
        elif tag == "script" and self._mode == "jsonld":
            self.jsonld.append("".join(self._buf))
            self._mode = None
        elif tag == "h1" and self._mode == "h1":
            self.h1_texts.append(re.sub(r"\s+", " ", text))
            self._mode = None
        elif tag == "a" and self._mode == "author":
            self.author_links.append((self._author_href, re.sub(r"\s+", " ", text)))
            self._mode = None

    def handle_data(self, data):
        if self._mode:
            self._buf.append(data)

    def meta(self, key, val):
        for m in self.metas:
            if m.get(key) == val:
                return m.get("content")
        return None

    def link_all(self, rel):
        return [l.get("href") for l in self.links if rel in (l.get("rel") or "").split()]


def url_for(rel, site):
    if rel == "index.html":
        return site + "/"
    if rel.endswith("/index.html"):
        return f"{site}/{rel[:-len('index.html')]}"
    return f"{site}/{rel}"


def is_article(rel):
    return rel.startswith("markets/") and not rel.endswith("index.html")


def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def nodes(data):
    """Yield every dict node in a JSON-LD document."""
    if isinstance(data, dict):
        yield data
        for v in data.values():
            yield from nodes(v)
    elif isinstance(data, list):
        for v in data:
            yield from nodes(v)


def has_type(node, *types):
    return any(t in types for t in as_list(node.get("@type")))


# ---------- robots.txt (RFC 9309 subset) ----------

def parse_robots(text):
    groups, agents, rules, last = [], [], [], None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = (s.strip() for s in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if last != "user-agent" and (agents or rules):
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(v.lower())
        elif k in ("allow", "disallow"):
            rules.append((k, v))
        last = k
    if agents:
        groups.append((agents, rules))
    return groups


def rules_for(groups, ua):
    ua = ua.lower()
    specific = [r for a, rs in groups if ua in a for r in rs]
    if any(ua in a for a, _ in groups):
        return specific
    return [r for a, rs in groups if "*" in a for r in rs]


def _match_len(pattern, path):
    if pattern == "":
        return -1
    rx = "^" + re.escape(pattern).replace(r"\*", ".*")
    if rx.endswith(r"\$"):
        rx = rx[:-2] + "$"
    return len(pattern) if re.match(rx, path) else -1


def allowed(rules, path):
    best_len, verdict = -1, True
    for k, v in rules:
        n = _match_len(v, path)
        if n > best_len or (n == best_len and n >= 0 and k == "allow"):
            best_len, verdict = n, (k == "allow")
    return verdict


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--site", default=DEFAULT_SITE)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    site = args.site.rstrip("/")

    fails, warns = [], []
    pages = sorted(p for p in root.rglob("*.html")
                   if not any(part in EXCLUDE or part.startswith(".")
                              for part in p.relative_to(root).parts))
    expected, titles, canon_seen = set(), {}, {}

    for p in pages:
        rel = p.relative_to(root).as_posix()
        url = url_for(rel, site)
        expected.add(url)
        tag = f"[{rel}]"
        pp = PageParser()
        pp.feed(p.read_text(encoding="utf-8"))
        art = is_article(rel)

        if not pp.html_lang:
            fails.append(f"{tag} <html> missing lang")
        if not pp.title:
            fails.append(f"{tag} missing <title>")
        else:
            titles.setdefault(pp.title, []).append(rel)
        desc = pp.meta("name", "description")
        if not desc:
            fails.append(f"{tag} missing meta description")
        elif len(desc) > 160:
            warns.append(f"{tag} description is {len(desc)} chars")
        if len(pp.h1_texts) != 1:
            fails.append(f"{tag} expected exactly 1 <h1>, found {len(pp.h1_texts)}")
        h1 = pp.h1_texts[0] if pp.h1_texts else None

        robots_meta = (pp.meta("name", "robots") or "").lower()
        if "noai" in robots_meta or "noimageai" in robots_meta:
            fails.append(f"{tag} still has noai/noimageai robots meta")
        if "noindex" in robots_meta:
            fails.append(f"{tag} is noindex")

        canons = pp.link_all("canonical")
        if len(canons) != 1 or canons[0] != url:
            fails.append(f"{tag} need exactly one canonical = {url}, got {canons}")
        else:
            canon_seen.setdefault(url, []).append(rel)

        # Internal links must point at canonical URLs (no explicit index.html)
        for h in pp.hrefs:
            if re.search(r"(^|/)index\.html(#.*)?$", h) and not h.startswith(("http:", "https:")):
                fails.append(f"{tag} link '{h}' points at index.html; use the directory URL (e.g. '../', './')")
                break

        # Open Graph
        for prop in ("og:title", "og:description", "og:url", "og:type", "og:site_name", "og:locale"):
            if not pp.meta("property", prop):
                fails.append(f"{tag} missing {prop}")
        if pp.meta("property", "og:url") not in (None, url):
            fails.append(f"{tag} og:url must equal canonical")
        want_type = "article" if art else "website"
        if pp.meta("property", "og:type") not in (None, want_type):
            fails.append(f"{tag} og:type should be '{want_type}'")
        want_locale = "zh_TW" if pp.html_lang == "zh-Hant" else "en_US"
        if pp.meta("property", "og:locale") not in (None, want_locale):
            fails.append(f"{tag} og:locale should be '{want_locale}'")
        if pp.meta("property", "og:site_name") not in (None, AUTHOR_NAME):
            fails.append(f"{tag} og:site_name should be '{AUTHOR_NAME}'")
        if not pp.meta("name", "twitter:card"):
            fails.append(f"{tag} missing twitter:card")
        if not pp.meta("property", "og:image"):
            warns.append(f"{tag} no og:image")

        # JSON-LD
        all_nodes = []
        for raw in pp.jsonld:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                fails.append(f"{tag} invalid JSON-LD: {e}")
                continue
            if not isinstance(data, (dict, list)):
                fails.append(f"{tag} JSON-LD top level must be an object or array")
                continue
            all_nodes.extend(nodes(data))

        articles = [n for n in all_nodes if has_type(n, "Article", "BlogPosting")]
        if art:
            if not articles:
                fails.append(f"{tag} missing Article JSON-LD")
            for a in articles:
                for k in ("headline", "datePublished", "dateModified", "author",
                          "inLanguage", "publisher"):
                    if k not in a:
                        fails.append(f"{tag} Article missing {k}")
                if h1 and a.get("headline") not in (None, h1):
                    fails.append(f"{tag} Article headline must equal <h1> text")
                if a.get("inLanguage") not in (None, "zh-Hant"):
                    fails.append(f"{tag} Article inLanguage should be 'zh-Hant'")
                for au in as_list(a.get("author")):
                    if not isinstance(au, dict) or not has_type(au, "Person"):
                        fails.append(f"{tag} Article author must be a Person object")
                        continue
                    if au.get("name") != AUTHOR_NAME:
                        fails.append(f"{tag} author.name must be '{AUTHOR_NAME}'")
                    if au.get("url") != site + "/":
                        fails.append(f"{tag} author.url must be '{site}/'")
                    bad = FORBIDDEN_AUTHOR_KEYS & au.keys()
                    if bad or "description" in au:
                        fails.append(f"{tag} author must not carry titles/credentials: {sorted(bad | ({'description'} & au.keys()))}")
                dp = str(a.get("datePublished", ""))
                if pp.times and dp and not dp.startswith(pp.times[0][:10]):
                    fails.append(f"{tag} datePublished {dp} != visible <time> {pp.times[0]}")
            if not any(has_type(n, "BreadcrumbList") for n in all_nodes):
                fails.append(f"{tag} missing BreadcrumbList JSON-LD")
            if not pp.author_links:
                fails.append(f"{tag} missing visible byline <a rel=\"author\" href=\"../\">{AUTHOR_NAME}</a>")
            for href, text in pp.author_links:
                if href not in ("../", site + "/"):
                    fails.append(f"{tag} byline href should be '../', got '{href}'")
                if text != AUTHOR_NAME:
                    fails.append(f"{tag} byline text must be exactly '{AUTHOR_NAME}', got '{text}'")
            # Defense in depth: no Chinese name or titles in byline area
            for _, text in pp.author_links:
                if TITLE_PATTERN.search(text):
                    fails.append(f"{tag} byline contains a title or Chinese name")
        if rel == "index.html":
            profiles = [n for n in all_nodes if has_type(n, "ProfilePage")]
            persons = [n for n in all_nodes if has_type(n, "Person")]
            if not profiles:
                fails.append(f"{tag} missing ProfilePage JSON-LD")
            if not any(p_.get("name") == AUTHOR_NAME for p_ in persons):
                fails.append(f"{tag} Person.name must be '{AUTHOR_NAME}'")
            if not any(as_list(p_.get("sameAs")) for p_ in persons):
                fails.append(f"{tag} Person missing sameAs (ORCID, GitHub)")
        if rel == "markets/index.html" and not any(has_type(n, "BreadcrumbList") for n in all_nodes):
            fails.append(f"{tag} missing BreadcrumbList JSON-LD")

    for t, rels in titles.items():
        if len(rels) > 1:
            fails.append(f"duplicate <title> '{t}' on {rels}")
    for u, rels in canon_seen.items():
        if len(rels) > 1:
            fails.append(f"duplicate canonical {u} on {rels}")

    # sitemap.xml
    sm = root / "sitemap.xml"
    if not sm.exists():
        fails.append("sitemap.xml missing")
    else:
        try:
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = ET.parse(sm).getroot().findall("s:url", ns)
            locs = set()
            for u in urls:
                loc = (u.findtext("s:loc", default="", namespaces=ns) or "").strip()
                if not loc:
                    fails.append("sitemap.xml has an empty <loc>")
                    continue
                locs.add(loc)
                lm = (u.findtext("s:lastmod", default="", namespaces=ns) or "").strip()
                if lm and not re.fullmatch(r"\d{4}-\d{2}-\d{2}(T[\d:.+\-Z]+)?", lm):
                    fails.append(f"sitemap.xml bad lastmod '{lm}' for {loc}")
                if u.find("s:priority", ns) is not None or u.find("s:changefreq", ns) is not None:
                    warns.append(f"sitemap.xml uses priority/changefreq (ignored by Google) for {loc}")
            for u in sorted(expected - locs):
                fails.append(f"sitemap.xml missing {u}")
            for u in sorted(locs - expected):
                fails.append(f"sitemap.xml lists unknown/non-canonical {u}")
        except ET.ParseError as e:
            fails.append(f"sitemap.xml invalid XML: {e}")

    # robots.txt
    rb = root / "robots.txt"
    if not rb.exists():
        fails.append("robots.txt missing")
    else:
        text = rb.read_text(encoding="utf-8")
        groups = parse_robots(text)
        for ua in MUST_BLOCK:
            if allowed(rules_for(groups, ua), "/"):
                fails.append(f"robots.txt should block training crawler {ua}")
        for ua in MUST_NOT_BLOCK:
            rs = rules_for(groups, ua)
            for path in ("/", "/markets/", "/markets/backtest-checklist.html", "/research.html"):
                if not allowed(rs, path):
                    fails.append(f"robots.txt blocks search crawler {ua} from {path}")
                    break
            extra = {v for k, v in rs if k == "disallow" and v and v not in ALLOWED_DISALLOWS}
            if extra:
                fails.append(f"robots.txt disallows {sorted(extra)} for search crawler {ua}")
        if f"Sitemap: {site}/sitemap.xml" not in text:
            fails.append(f"robots.txt missing 'Sitemap: {site}/sitemap.xml'")

    for w in warns:
        print("WARN ", w)
    for f in fails:
        print("FAIL ", f)
    print(f"\n{len(pages)} pages checked: {len(fails)} FAIL, {len(warns)} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
