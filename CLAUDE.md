# CLAUDE.md — onepunchmed.github.io

Personal site of Chun Jui Lu: English academic profile (clinical machine learning) plus a Traditional Chinese `markets/` section of investment-research articles. Hand-written static HTML on GitHub Pages. No build step (`.nojekyll`).

## Current work: SEO / GEO

- Plan and research: `_dev/seo/SEO_PLAN.md`
- Tasks and phases: `_dev/seo/TASKS.md`
- Acceptance: `python3 _dev/seo/seo_check.py` must exit 0

Work on branch `seo-handoff`, one task per commit. Do not merge to `main` (merging publishes the live site) until the owner approves.

## Hard rules

- Never change numbers, results, or claims in article bodies. Content edits (Phase 2) need the owner's per-article approval.
- Author identity is the English name `Chun Jui Lu` only. Do not add a Chinese author page, a Chinese name, or titles/credentials to `markets/` pages. Structured data may describe only what is visible on the page.
- Keep every investment disclaimer ("不構成投資建議", 免責聲明, 持有揭露) intact.
- Robots policy: block training crawlers, allow search crawlers (exact file in SEO_PLAN §4.2).
- Do not invent the Search Console verification token or the custom domain; ask the owner.
- Keep existing HTML style: same indentation, same CSS classes, no frameworks, no new JS.
- Chinese text: Traditional Chinese (zh-Hant, Taiwan usage); keep the site's existing punctuation style.

## Workflow (owner's model policy)

- Routine implementation from this spec: Sonnet, medium effort.
- Copy that will be published (titles, descriptions, new paragraphs): Opus, high effort, then owner review.
- After each phase: a separate Opus subagent that has not seen the work reviews the diff against SEO_PLAN.md and TASKS.md.
