#!/usr/bin/env python3
"""Offline SEO acceptance check for onepunchmed.github.io.

Usage:
    python3 _dev/seo/seo_check.py            # check repo root (default)
    python3 _dev/seo/seo_check.py --root .   # explicit root
    python3 _dev/seo/seo_check.py --site https://example.com  # after domain move

Exit code 0 = all checks pass, 1 = at least one FAIL.
Standard library only, so it runs in CI and on any machine.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_SITE = "https://onepunchmed.github.io"

# Pages excluded from sitemap / canonical checks (none yet). Paths are repo-relative.
EXCLUDE = {"_dev"}

# Robots policy chosen by the owner on 2026-10-26: block training, allow search.
MUST_BLOCK = ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
              "meta-externalagent", "CCBot", "Bytespider"]
MUST_NOT_BLOCK = ["OAI-SearchBot", "ChatGPT-User", "Claude-SearchBot", "Claude-User",
                  "PerplexityBot", "Perplexity-User", "Googlebot", "Bingbot",
                  "Meta-WebIndexer"]


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title = None
        self._in_title = False
        self._svg_depth = 0
        self.metas = []
        self.links = []
        self.jsonld = []
        self._in_jsonld = False
        self._buf = []
        self.h1 = 0
        self.hrefs = []
        self.times = []
        self.author_links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "svg":
            self._svg_depth += 1
        elif tag == "title" and self._svg_depth == 0 and self.title is None:
            self._in_title = True
            self._buf = []
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._buf = []
        elif tag == "h1":
            self.h1 += 1
        elif tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
            if "author" in (a.get("rel") or "").split():
                self.author_links.append(a["href"])
        elif tag == "time" and a.get("datetime"):
            self.times.append(a["datetime"])

    def handle_endtag(self, tag):
        if tag == "svg" and self._svg_depth:
            self._svg_depth -= 1
        elif tag == "title" and self._in_title:
            self.title = "".join(self._buf).strip()
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            self.jsonld.append("".join(self._buf))
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title or self._in_jsonld:
            self._buf.append(data)

    def meta(self, key, val):
        for m in self.metas:
            if m.get(key) == val:
                return m.get("content")
        return None

    def link(self, rel):
        for l in self.links:
            if rel in (l.get("rel") or "").split():
                return l.get("href")
        return None


def url_for(path: Path, root: Path, site: str) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return site + "/"
    if rel.endswith("/index.html"):
        return f"{site}/{rel[:-len('index.html')]}"
    return f"{site}/{rel}"


def is_article(rel: str) -> bool:
    return rel.startswith("markets/") and not rel.endswith("index.html")


def iter_types(node):
    if isinstance(node, dict):
        t = node.get("@type")
        if t:
            yield from (t if isinstance(t, list) else [t])
        for v in node.values():
            yield from iter_types(v)
    elif isinstance(node, list):
        for v in node:
            yield from iter_types(v)


def parse_robots(text):
    groups, agents, rules = [], [], []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, v = (s.strip() for s in line.split(":", 1))
        k = k.lower()
        if k == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(v.lower())
        elif k in ("allow", "disallow"):
            rules.append((k, v))
    if agents:
        groups.append((agents, rules))
    return groups


def blocked_root(groups, ua):
    ua = ua.lower()
    chosen = None
    for agents, rules in groups:
        if ua in agents:
            chosen = rules
            break
    if chosen is None:
        for agents, rules in groups:
            if "*" in agents:
                chosen = rules
                break
    if not chosen:
        return False
    return any(k == "disallow" and v == "/" for k, v in chosen)


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
    expected_urls = set()
    titles = {}

    for p in pages:
        rel = p.relative_to(root).as_posix()
        hp = HeadParser()
        hp.feed(p.read_text(encoding="utf-8"))
        url = url_for(p, root, site)
        expected_urls.add(url)
        tag = f"[{rel}]"

        if not hp.html_lang:
            fails.append(f"{tag} <html> missing lang")
        if not hp.title:
            fails.append(f"{tag} missing <title>")
        else:
            titles.setdefault(hp.title, []).append(rel)
        desc = hp.meta("name", "description")
        if not desc:
            fails.append(f"{tag} missing meta description")
        if hp.h1 != 1:
            fails.append(f"{tag} expected exactly 1 <h1>, found {hp.h1}")

        robots_meta = (hp.meta("name", "robots") or "").lower()
        if "noai" in robots_meta or "noimageai" in robots_meta:
            fails.append(f"{tag} still has non-standard noai/noimageai robots meta")
        if "noindex" in robots_meta:
            fails.append(f"{tag} is noindex")

        canon = hp.link("canonical")
        if canon != url:
            fails.append(f"{tag} canonical should be {url}, got {canon}")

        for prop in ("og:title", "og:description", "og:url", "og:type", "og:site_name"):
            if not hp.meta("property", prop):
                fails.append(f"{tag} missing {prop}")
        if hp.meta("property", "og:url") not in (None, url):
            fails.append(f"{tag} og:url should equal canonical")
        if not hp.meta("property", "og:image"):
            warns.append(f"{tag} no og:image (social shares will have no picture)")
        if not hp.meta("name", "twitter:card"):
            warns.append(f"{tag} no twitter:card")

        types = []
        for raw in hp.jsonld:
            try:
                data = json.loads(raw)
            except json.JSONDecodeError as e:
                fails.append(f"{tag} invalid JSON-LD: {e}")
                continue
            types.extend(iter_types(data))
            if is_article(rel):
                arts = [n for n in (data.get("@graph", [data]) if isinstance(data, dict) else data)
                        if isinstance(n, dict) and n.get("@type") in ("Article", "BlogPosting")]
                for a in arts:
                    for k in ("headline", "datePublished", "dateModified", "author"):
                        if k not in a:
                            fails.append(f"{tag} Article missing {k}")
                    au = a.get("author", {})
                    au = au[0] if isinstance(au, list) and au else au
                    if isinstance(au, dict) and au.get("name") != "Chun Jui Lu":
                        fails.append(f"{tag} Article author.name must be 'Chun Jui Lu'")
                    dp = a.get("datePublished", "")
                    if hp.times and dp and not dp.startswith(hp.times[0][:10]):
                        fails.append(f"{tag} datePublished {dp} != visible <time> {hp.times[0]}")
        if is_article(rel):
            if not any(t in ("Article", "BlogPosting") for t in types):
                fails.append(f"{tag} missing Article JSON-LD")
            if "BreadcrumbList" not in types:
                warns.append(f"{tag} no BreadcrumbList JSON-LD")
            if not any(re.search(r"(^|/)\.\./(index\.html)?$", h) for h in hp.author_links):
                fails.append(f"{tag} no visible byline <a rel=\"author\" href=\"../index.html\">")
        if rel == "index.html" and "ProfilePage" not in types:
            fails.append(f"{tag} missing ProfilePage JSON-LD")

        if len(desc or "") > 160:
            warns.append(f"{tag} description {len(desc)} chars; may be truncated in results")

    for t, rels in titles.items():
        if len(rels) > 1:
            fails.append(f"duplicate <title> '{t}' on {rels}")

    # sitemap
    sm = root / "sitemap.xml"
    if not sm.exists():
        fails.append("sitemap.xml missing")
    else:
        try:
            tree = ET.parse(sm)
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = {e.text.strip() for e in tree.getroot().findall("s:url/s:loc", ns)}
            for u in sorted(expected_urls - locs):
                fails.append(f"sitemap.xml missing {u}")
            for u in sorted(locs - expected_urls):
                fails.append(f"sitemap.xml lists unknown/non-canonical {u}")
        except ET.ParseError as e:
            fails.append(f"sitemap.xml invalid XML: {e}")

    # robots
    rb = root / "robots.txt"
    if not rb.exists():
        fails.append("robots.txt missing")
    else:
        text = rb.read_text(encoding="utf-8")
        groups = parse_robots(text)
        for ua in MUST_BLOCK:
            if not blocked_root(groups, ua):
                fails.append(f"robots.txt should block training crawler {ua}")
        for ua in MUST_NOT_BLOCK:
            if blocked_root(groups, ua):
                fails.append(f"robots.txt must not block search crawler {ua}")
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
