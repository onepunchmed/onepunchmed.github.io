#!/usr/bin/env python3
"""Add the Cloudflare Web Analytics beacon to every page that lacks it.

Usage:
    python3 _dev/add_beacon.py            # repo root = cwd
    python3 _dev/add_beacon.py --root path/to/repo

Inserts one line before </body>, indented like </body>. Pages that already
have the beacon are left alone, so it is safe to run any time.
Owner approved the beacon on 2026-11-21 (cookieless, Cloudflare Web Analytics).
Standard library only.
"""
import argparse
import re
from pathlib import Path

TOKEN = "28f7e614b4e242bf952ea885535cab68"
SNIPPET = ("<!-- Cloudflare Web Analytics --><script type='module' "
           "src='https://static.cloudflareinsights.com/beacon.min.js' "
           "data-cf-beacon='{\"token\": \"" + TOKEN + "\"}'></script>"
           "<!-- End Cloudflare Web Analytics -->")
EXCLUDE = {"_dev"}


def pages(root):
    return sorted(p for p in root.rglob("*.html")
                  if not any(part in EXCLUDE or part.startswith(".")
                             for part in p.relative_to(root).parts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    added, skipped = [], []
    for p in pages(root):
        text = p.read_text(encoding="utf-8")
        if TOKEN in text:
            continue
        m = list(re.finditer(r"^([ \t]*)</body>", text, re.M))
        if len(m) != 1:
            skipped.append(p.relative_to(root).as_posix())
            continue
        i = m[0].start()
        p.write_text(text[:i] + m[0].group(1) + SNIPPET + "\n" + text[i:], encoding="utf-8")
        added.append(p.relative_to(root).as_posix())
    for rel in added:
        print(f"added  {rel}")
    for rel in skipped:
        print(f"SKIP   {rel} (needs exactly one </body> on its own line)")
    print(f"{len(added)} added, {len(skipped)} skipped")
    return 1 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
