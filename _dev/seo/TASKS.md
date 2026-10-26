# SEO 開發任務

依據：`_dev/seo/SEO_PLAN.md`。驗收：`python3 _dev/seo/seo_check.py` 回 0。
分工依站長的模型原則：Opus 規劃（已完成）→ Sonnet 執行 → 另一個沒看過產出過程的 Opus 驗證。

標記：🧑 站長親自做｜🤖 Claude Code 做｜✅ 需站長核可才能合併

---

## Phase 0　站長準備（🧑，可與 Phase 1 平行）

- [ ] 買網域，把網域名稱告訴 Claude Code（Phase 3 才需要）
- [ ] Google Search Console 新增「網址前置字元」資源 `https://onepunchmed.github.io/`，選「HTML 標記」，把 meta tag 的 content 值交給 Claude Code（放進 `index.html`）
- [ ] Bing Webmaster Tools：Search Console 驗證完成後，從 GSC 匯入
- [ ] ORCID、GitHub profile 的網站欄填 `https://onepunchmed.github.io/`（換網域後改新網址）

## Phase 1　技術基礎（🤖 Sonnet medium）

在 `seo-handoff` 分支上做，一個項目一個 commit。不改任何內文文字與數字。

1. **robots.txt**：照 SEO_PLAN §4.2 改寫。
2. **移除** 所有頁面的 `<meta name="robots" content="noai, noimageai">`。
3. **canonical**：每頁加絕對網址 canonical。
   - `index.html` → `https://onepunchmed.github.io/`
   - `markets/index.html` → `https://onepunchmed.github.io/markets/`
   - 其他 → 檔案路徑
4. **Open Graph／Twitter**：每頁加 SEO_PLAN §4.1 的標籤。`og:title`、`og:description` 沿用現有 title 與 description；`og:locale`：英文頁 `en_US`，Markets `zh_TW`。
5. **JSON-LD**：
   - 6 篇 Markets 文章：`Article` + `BreadcrumbList`，用 `@graph` 放在同一個 script。`datePublished` 等於頁面 `<time datetime>`，`dateModified` 先等於 `datePublished`。
   - `index.html`：`ProfilePage` + `Person`。description 只能用頁面上已寫的文字：Researcher in clinical machine learning; Director of Research at a community primary care clinic in New Taipei City, Taiwan; M.D., Chang Gung University。`sameAs`：ORCID、GitHub。
   - `markets/index.html`：`BreadcrumbList`。
6. **作者署名**：6 篇文章的 `<p class="article-meta">` 開頭加 `<a rel="author" href="../index.html">Chun Jui Lu</a> · `。只用英文名，不加頭銜。
7. **語系**：`index.html` 等英文頁內的中文段落加 `lang="zh-Hant"`。
8. **sitemap.xml**：手寫，列 12 個 canonical 網址，`lastmod` 用各頁 git 最後實質修改日，不用 `priority`／`changefreq`。
9. **CI**：啟用 `_dev/seo/seo-check.yml`（搬到 `.github/workflows/`），PR 與 push 時跑 seo_check 與 lychee 斷鏈檢查。
10. **GSC 驗證 meta**：拿到站長提供的值才加，沒拿到就跳過，不要自己編。

**驗收**：`seo_check.py` 0 FAIL；lychee 無斷鏈；用瀏覽器開每頁，版面與修改前一致。

## Phase 2　內容調整（✅ 每項需站長逐篇核可）

起草：🤖 Opus high（對外文案）。核可：🧑。

1. 6 篇文章的 `<title>`，依 SEO_PLAN §6.1 建議。H1 不動。改了 title 要同步改 `og:title` 與 JSON-LD `headline`，或維持 headline 等於 H1，二擇一並在全站一致。
2. meta description 超過 160 字的縮短；保留「不構成投資建議」字樣。
3. 每篇補一段「X 是什麼」定義段，放在第一個相關 H2 底下，2–3 句，可被引用。
   - backtest-checklist：前瞻偏誤、存活者偏誤、過度擬合
   - tw-arbitrage：正價差／逆價差、ADR 溢價
   - tsmc-valuation：反向 DCF
4. tw-arbitrage 補「自己怎麼查」：期交所與 ADR 資料的原始來源連結。
5. 每篇文末「延伸閱讀」：同系列 3 篇。目前 6 篇彼此的連結已不少，只補缺的。
6. 改任何文字後，`dateModified` 與 sitemap `lastmod` 一起更新，頁面上的「Last updated」也同步。

**規範**
- 數字一律不改，只能引用各篇已有的數字。
- 不寫「保證」「穩賺」「首創」「唯一」，不給買賣建議、單一目標價或購買管道。
- 標點與斷行沿用全站現有風格。

## Phase 3　換網域（網域到手後，🤖 Sonnet medium + 🧑）

1. 🧑 GitHub repo Settings → Pages → Custom domain：先新增並驗證網域，加 TXT 記錄 `_github-pages-challenge-onepunchmed.<網域>`，驗證後保留。
2. 🧑 DNS 設定：
   - 根網域 A 記錄指向 185.199.108.153、185.199.109.153、185.199.110.153、185.199.111.153
   - 選用 AAAA 記錄指向 2606:50c0:8000::153 到 2606:50c0:8003::153
   - `www` 設 CNAME 指向 `onepunchmed.github.io`
   - 不設萬用字元 DNS；有 CAA 記錄的話要包含 letsencrypt.org
3. 🤖 全站把 `https://onepunchmed.github.io` 換成新網域：canonical、og:url、JSON-LD、sitemap、robots 的 Sitemap 行。改 `seo_check.py` 的 `DEFAULT_SITE`，或執行時加 `--site`。
4. 🧑 等 DNS 生效後開 Enforce HTTPS，最多 24 小時。
5. 🤖 驗證 `https://onepunchmed.github.io/markets/backtest-checklist.html` 會 301 轉到新網域同路徑。GitHub 官方文件沒保證這點，一定要實測，並把結果寫進 CHANGELOG。
6. 🧑 Search Console 新增新網域的「網域」資源（DNS 驗證）。舊資源用「網址變更」工具，如果不支援 github.io，改為只提交新 sitemap。
7. 🧑 ORCID、GitHub profile 改填新網址。

## Phase 4　追蹤（每月）

- 🧑 讀 GSC：排名 4–20、曝光高但點擊低的頁 → 回 Phase 2 調 title 與 description
- 🧑 AI 引用率題組，見 SEO_PLAN §7
- 🤖 Haiku low：把當月數字整理進 `_dev/seo/LOG.md`
- 新文章題目見 SEO_PLAN §3.4；每篇另開研究任務（Opus high），寫作與核可由站長負責

## 驗證（每個 Phase 結束時）

另開一個 Opus high 子代理，不給它開發過程，只給以下三樣：
1. SEO_PLAN.md
2. 本檔
3. diff

它要檢查：
- seo_check 是否通過
- 結構化資料是否只描述可見內容
- 內文數字有沒有被動到
- robots 規則是否符合 §4.2
