# CLAUDE.md — onepunchmed.github.io

Personal site of Chun Jui Lu, branded **onepunchmed**: English academic profile (clinical machine learning) plus a Traditional Chinese `markets/` section of investment-research articles. Hand-written static HTML on GitHub Pages. No build step (`.nojekyll`).

Article-writing rules (compliance, structure, evidence, checklist): `~/Claude/onepunchmed-site/docs/WRITING_GUIDE.md`. SEO plan and tasks: `_dev/seo/SEO_PLAN.md`, `_dev/seo/TASKS.md`.

## Branches, merge and "done"

- One task per branch in its own worktree (`git worktree add -b <branch> ~/Claude/opm-<name> origin/main`); one article or change per PR. Never edit the shared checkout's branch from another session.
- Merging to `main` publishes the live site: only after the owner approves the PR.
- Integration check before asking to merge: `git fetch` and rebase the branch onto the latest `origin/main` (resolve `sitemap.xml`, `health/index.html`, `markets/index.html` list conflicts by keeping both entries), then rerun `python3 _dev/seo/seo_check.py`; it must exit 0 on the rebased branch, not only on the original base.
- Report the four states separately: committed (branch + commit), checked (seo_check / fact-check result), approved (owner said merge), live (curl of the live URL returns 200 with the new text). "Merged" is not "live" until the curl check passes.

## Fact-check results

Every factual claim gets one of three results: **verified** (source found and read, link recorded), **contradicted** (fix or delete), **inconclusive** (no source found or source not readable). Inconclusive is not a pass: rewrite it as a stated condition or limitation, or remove it. Verification must read the source (WebSearch/WebFetch or NCBI eutils), never memory.

## Hard rules

- Never change numbers, results, or claims in article bodies. Content edits (Phase 2) need the owner's per-article approval.
- Site brand and author byline is `onepunchmed` (owner decision 2026-11-03): site name, page-title suffix, bylines, og:site_name and Article author/publisher. The About page h1 and its Person JSON-LD (ORCID) keep the real name `Chun Jui Lu` with `alternateName: onepunchmed`. Do not add a Chinese author page, a Chinese name, or titles/credentials to `markets/` pages. Structured data may describe only what is visible on the page.
- Keep every investment disclaimer ("不構成投資建議", 免責聲明, 持有揭露) intact.
- Robots policy: block training crawlers, allow search crawlers (exact file in SEO_PLAN §4.2).
- Do not invent the Search Console verification token or the custom domain; ask the owner.
- Keep existing HTML style: same indentation, same CSS classes, no frameworks, no new JS.
- Chinese text: Traditional Chinese (zh-Hant, Taiwan usage); keep the site's existing punctuation style.

## Workflow (owner's model policy)

- Routine implementation from this spec: Sonnet, medium effort.
- Copy that will be published (titles, descriptions, new paragraphs): Opus, high effort, then owner review.
- After each phase: a separate Opus subagent that has not seen the work reviews the diff against SEO_PLAN.md and TASKS.md.
