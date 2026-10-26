# 貼給 Claude Code 的開工指令

在 Claude Code 開啟 `onepunchmed/onepunchmed.github.io`，切到 `seo-handoff` 分支，貼上：

```
讀 CLAUDE.md、_dev/seo/SEO_PLAN.md、_dev/seo/TASKS.md。
執行 TASKS.md 的 Phase 1，第 1 到 10 項。第 11 項等我提供 GSC token。
每項一個 commit，每個 commit 後跑 python3 _dev/seo/seo_check.py。
全部完成後：
1. 回報 seo_check 結果與 diff 摘要。
2. 另開一個沒看過開發過程的 Opus 子代理，照 TASKS.md「驗證」一節檢查。
3. 開 PR 到 main，不要合併。
```

Phase 2 的指令（Phase 1 合併之後再下）：

```
執行 TASKS.md Phase 2。先只產出 6 篇的 title、description、定義段草稿，放在 _dev/seo/phase2-drafts.md 給我核可，不要直接改 HTML。
```
