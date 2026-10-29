# SEO 開發任務

依據：`_dev/seo/SEO_PLAN.md`。驗收：`python3 _dev/seo/seo_check.py` 回 0。
分工依站長的模型原則：Opus 規劃（已完成）→ Sonnet 執行 → 另一個沒看過產出過程的 Opus 驗證。

標記：🧑 站長親自做｜🤖 Claude Code 做｜✅ 需站長核可才能合併

---

## Phase 0　站長準備（🧑，可與 Phase 1 平行）

- [x] 買網域：onepunchmed.com（2026-10-29，Cloudflare Registrar）
- [x] Google Search Console 新增「網址前置字元」資源 `https://onepunchmed.github.io/`，選「HTML 標記」，把 meta tag 的 content 值交給 Claude Code（放進 `index.html`）（PR #3）
- [x] Bing Webmaster Tools：Search Console 驗證完成後，從 GSC 匯入（2026-10-29 匯入成功，sitemap 已重新提交）
- [x] ORCID、GitHub profile 的網站欄填 `https://onepunchmed.github.io/`（換網域後改新網址）（2026-10-29 確認兩邊都已填）

## Phase 1　技術基礎（🤖 Sonnet medium）

在 `seo-handoff` 分支上做，一個項目一個 commit。不改任何內文文字與數字。全部範圍＝12 個 HTML 頁：`index.html`、`research.html`、`data.html`、`notes.html`、`disclosure.html`、`markets/index.html`，以及 6 篇 `markets/*.html` 文章。

1. **robots.txt**：照 SEO_PLAN §4.2 逐字改寫。
2. **移除**所有頁面的 `<meta name="robots" content="noai, noimageai">`。
3. **canonical**：每頁加一個絕對網址 canonical。
   - `index.html` → `https://onepunchmed.github.io/`
   - `markets/index.html` → `https://onepunchmed.github.io/markets/`
   - 其他 → 檔案路徑
4. **站內連結改指 canonical**：導覽列與內文中所有 `href="index.html"` 改成 `./`，`href="../index.html"` 改成 `../`。只動 href，連結文字不動。
5. **Open Graph／Twitter**：每頁加以下標籤：
   - `og:title`、`og:description`：沿用該頁 `<title>` 與 meta description
   - `og:url`：等於 canonical
   - `og:type`：6 篇文章用 `article`，其他 6 頁（含 `markets/index.html`）用 `website`
   - `og:site_name`：`Chun Jui Lu`
   - `og:locale`：`lang="zh-Hant"` 的頁用 `zh_TW`，其他用 `en_US`
   - `twitter:card`：`summary`
6. **JSON-LD**：每頁一個 `<script type="application/ld+json">`，用 `{"@context":"https://schema.org","@graph":[...]}`。
   - **6 篇文章**：`Article` 加 `BreadcrumbList`（About › Markets › 文章）。`Article` 的欄位：
     - `headline`：逐字等於 H1 文字
     - `datePublished`、`dateModified`：都等於頁面上的 `<time datetime>`
     - `author` 與 `publisher`：同一個 `{"@type":"Person","name":"Chun Jui Lu","url":"https://onepunchmed.github.io/"}`，不加任何其他欄位
     - `inLanguage`：`zh-Hant`
     - `mainEntityOfPage`：canonical
   - **`index.html`**：`ProfilePage`，`mainEntity` 為 `Person`，欄位如下：
     - `name`：`Chun Jui Lu`
     - `url`：`https://onepunchmed.github.io/`
     - `description`：逐字照抄頁面上職稱與學歷那一行
     - `sameAs`：ORCID 與 GitHub 兩個網址，從頁面上的連結抄
   - **`markets/index.html`**：`BreadcrumbList`（About › Markets）。
   - 結構化資料只能描述頁面上看得到的內容。
7. **作者署名**：6 篇文章的 `<p class="article-meta">` 開頭加 `<a rel="author" href="../">Chun Jui Lu</a> · `。連結文字只能是英文名，不加頭銜。
8. **語系標記**：
   - `index.html`、`research.html`、`data.html`、`disclosure.html`、`notes.html` 裡的中文段落，在包住它的元素加 `lang="zh-Hant"`。
   - `markets/index.html` 裡的英文段落 `<div class="zh">` 加 `lang="en"`。
9. **sitemap.xml**：手寫，列 12 個 canonical 網址（跟第 3 項同一組），`lastmod` 一律 `2026-10-26`，不用 `priority`、`changefreq`。
10. **CI**：把 `_dev/seo/seo-check.yml` 移到 `.github/workflows/seo-check.yml`。push 若因 token 沒有 workflow 權限被拒，就把這個 commit 留在本機，並告訴站長由他手動推。
11. **GSC 驗證 meta**：拿到站長提供的值才加，沒拿到就跳過，不要自己編。

**驗收**
- `python3 _dev/seo/seo_check.py` 結果為 0 FAIL。WARN 只允許「no og:image」。
- lychee 無斷鏈。
- 用瀏覽器開每頁，版面與修改前一致（署名那一行除外）。

## Phase 2　內容調整（✅ 每項需站長逐篇核可）

起草：🤖 Opus high（對外文案）。核可：🧑。

1. 6 篇文章的 `<title>`，依 SEO_PLAN §6.1 建議。H1 不動，JSON-LD `headline` 維持等於 H1；`og:title` 跟著新 title 改。
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

**狀態（2026-10-29）：** 1–5 完成（PR #10）；6 已新增 `sc-domain:onepunchmed.com` 並提交 sitemap，舊資源的「網址變更」工具可用，尚未送出；Bing 已從 GSC 匯入 onepunchmed.com 並提交 sitemap；7 GitHub 已改，ORCID 待改。實測結果見 `_dev/seo/CHANGELOG.md`。

## Phase 4　追蹤（每月）

- 🧑 讀 GSC：排名 4–20、曝光高但點擊低的頁 → 回 Phase 2 調 title 與 description
- 🧑 AI 引用率題組，見 SEO_PLAN §7
- 🤖 Haiku low：把當月數字整理進 `_dev/seo/LOG.md`
- 新文章題目見 SEO_PLAN §3.4；每篇另開研究任務（Opus high），寫作與核可由站長負責

## 驗證（每個 Phase 結束時）

另開一個 Opus high 子代理，不給它開發過程，只給以下四樣：
1. CLAUDE.md
2. SEO_PLAN.md
3. 本檔
4. diff

它要檢查：
- seo_check 是否通過
- 結構化資料是否只描述可見內容
- 內文數字有沒有被動到
- robots 規則是否符合 §4.2
