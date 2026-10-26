# onepunchmed.github.io SEO／GEO 計畫

研究日期：2026-10-26。根據 repo 原始碼盤點、Google 官方文件，以及台灣繁中搜尋結果實際打開的頁面整理。沒有付費工具，也沒有搜尋量資料；文中「難度」是用 10 點量表評的相對分數，不是工具數字。

## 1. 已定案的方向（站長 2026-10-26 選定）

| 項目 | 決定 | 對規格的影響 |
|---|---|---|
| AI 爬蟲 | 擋訓練、放搜尋 | robots.txt 改寫（見 §4.2），拿掉 `noai, noimageai` meta |
| 範圍 | 英文學術頁與 Markets 繁中區都做 | 兩區目標不同，見 §5、§6 |
| 網域 | 會買自訂網域（尚未決定名稱） | 先在 github.io 上完成站內修正，網域到手後跑搬站流程（TASKS Phase 3） |
| 作者身分 | 只用英文名 Chun Jui Lu | 不另做中文作者頁、不在 Markets 文章加醫師頭銜；byline 與 schema 一律用 `Chun Jui Lu`，連到既有的英文個人頁 |

## 2. 現況盤點（repo 原始碼，2026-10-26）

- 12 個 HTML 頁，手寫靜態 HTML，無建置流程，有 `.nojekyll`。
- 每頁都有 `<title>`、meta description、viewport、`lang`（英文頁 `en`，Markets 頁 `zh-Hant`）。
- **全站沒有**：canonical、Open Graph、Twitter card、JSON-LD、sitemap.xml、Search Console 驗證。
- 每頁有 `<meta name="robots" content="noai, noimageai">`：Google 支援的 robots 規則清單沒有這兩個值，對 Google 沒有作用。
- robots.txt 擋了 ChatGPT-User、PerplexityBot（兩者是搜尋／即時抓取，不是訓練），也擋了 Anthropic 現行文件已不使用的 `anthropic-ai`；沒有 `Sitemap:` 行。
- Markets 文章有可見的 `<time datetime>` 發布日，但**沒有作者署名**；作者名只出現在站名。YMYL 頁沒有負責人資訊，品質評分指南會給最低評等。
- 英文首頁 `index.html` 已有姓名、職稱、學歷、ORCID、GitHub；中文摘要段落包在 `lang="en"` 頁面裡，沒有標 `lang="zh-Hant"`。
- 用 `"Chun Jui Lu"` 搜尋，前 10 名沒有本站（同名或近似名的人很多），推測尚未被充分索引或權重不足。
- 執行 `python3 _dev/seo/seo_check.py`：目前 95 個 FAIL，即 TASKS 的驗收基線。

## 3. 關鍵字研究（Markets 區）

### 3.1 候選詞

| 文章 | 候選詞 |
|---|---|
| backtest-checklist | 回測 過度擬合、回測陷阱、前瞻偏誤、存活者偏差、回測績效可信嗎、回測 實盤 落差、樣本外測試、多重比較 回測 |
| tw-arbitrage | 期現貨套利、正價差 逆價差、台積電 ADR 溢價、ADR 為什麼比台股貴、散戶 套利 可行嗎 |
| tsmc-taiex-hedge | 台積電 超跌 買進、乖離率 策略 回測、台積電 波段 vs 長期持有、walk-forward、參數最佳化 |
| tw-hedge-backtest | 微型台指 避險、股票期貨 避險、避險 有用嗎、避險 vs 買進持有 |
| tsmc-valuation | 台積電 估值、台積電 DCF、反向 DCF、隱含成長率、股票估值 怎麼算 |
| pre-ipo-valuation | Pre-IPO 估值、未上市股票 估值、Anthropic IPO、宇樹 估值、宇樹 流通盤 |

### 3.2 難度（10 點量表，0–3 易、4–6 中、7–10 難）

搜尋工具看不到精選摘要與 AI 摘要，這兩項一律計 0，實際難度可能略高。

| 主要詞 | 分數 | 前排狀況 | 本站機會 |
|---|---|---|---|
| 回測 過度擬合 | 2 易 | 匿名部落格、假設數字、無原創數據 | 用 120 組參數與 walk-forward 實證，加臨床試驗類比 |
| 期現貨套利／正逆價差 | 3 易 | 股感寫成「無風險套利」沒算稅費；PTT 有散戶自己算成本 | 6.8 年期交所資料、逐項成本 |
| 反向 DCF | 1 易 | 中文只有一篇，數字是假設的 | 台積電真實數據 |
| 微型台指 避險 | 3（券商主導） | 玉山、群益只講規格保證金，沒有回測 | 走「避險有用嗎」回測角度，不搶規格詞 |
| 台積電 ADR 溢價 | 4 中 | 6 家媒體，只報導不分析可行性 | 回歸是否成立、散戶能否套利 |
| 台積電 波段／超跌 回測 | 4 中（只開 1 頁） | 理財周刊有 2016–2026 均線回測 | 20 年資料、樣本內外 |
| 台積電 合理價 本益比 | 5 中 | 商周具名專家、券商目標價新聞洗版、波動高 | 不搶單一價位；主打「估值方法與區間」 |
| Anthropic 股票 怎麼買 | 4 中、波動高 | 券商頁、編譯文；IPO 消息會讓結果頁大洗牌 | 只寫估值方法，不寫購買管道 |

來源頁（研究時實際打開）：ctyeh.com/finance/15092、blog.wistock.ai/?p=32947、udn.com/news/story/6811/9459796、esunsec.com.tw/article/post/348、school.gugu.fund/blog/gugu_knowledge/6182156539、stockfeel.com.tw/?p=267404、ctyeh.com/finance/15121、disp.cc/b/Stock/i71V、moneyweekly.com.tw/_Article?AID=230109、esunsec.com.tw/article/post/143、nstock.tw/author/article?id=1132、ctee.com.tw/news/20260729701011-430202、smart.businessweekly.com.tw/Reading/IndepArticle.aspx?ID=6004275、school.gugu.fund/blog/invest-proper-noun/1058877870、blog.wistock.ai/?p=30049、ctyeh.com/finance/12847、futureaitw.substack.com/p/anthropic-965b-ipo-ai、grenade.tw/blog/pre-ipo-gold-rush/、inside.com.tw/article/42033-unitree-ipo-pricing-star-market-valuation

### 3.3 缺口

**核心缺口**（前 3 名都有，本站沒有或不明顯）
- 段首直接回答、FAQ 區塊
- 「X 是什麼？」定義型 H2（前瞻偏誤是什麼、正價差是什麼、反向 DCF 是什麼）
- 「自己怎麼查」的指引（期交所價差資料、ADR 溢價資料來源）

**機會缺口**（沒人寫但有人問，本站已有資料）
1. 散戶套利的真實成本：PTT 有人逐項算，媒體與教學站都沒做
2. 避險後報酬與買進持有的比較：微台相關頁只講規格
3. 用真實回測示範方法論：競品案例都是假設數字
4. 反向 DCF 真實數據
5. 宇樹流通盤小對估值的影響

### 3.4 下一批文章候選（需站長決定是否寫）

| 題目 | 主要詞 | 連回 |
|---|---|---|
| 台積電 ADR 溢價會回歸嗎？用歷史數據看 | 台積電 ADR 溢價 | tw-arbitrage、tsmc-taiex-hedge |
| 波段操作 vs 長期持有：台股 20 年回測 | 波段 長期持有 回測 | tsmc-taiex-hedge、tw-hedge-backtest、backtest-checklist |
| 夏普值、最大回撤怎麼看：像讀臨床試驗終點一樣讀策略績效 | 夏普值 最大回撤 | backtest-checklist、tw-hedge-backtest |
| 反向 DCF 實作：台積電股價隱含幾 % 成長 | 反向 DCF | tsmc-valuation |
| 定期定額 vs 逢低加碼：0050 回測（競爭度未評） | 定期定額 逢低加碼 回測 | tsmc-taiex-hedge、backtest-checklist |

### 3.5 不正面搶的詞（YMYL／券商主導）

微型台指開戶與保證金、股票手續費怎麼算、Anthropic 怎麼買、台積電目標價。做法：寫成內文附表或連到官方來源，不獨立成篇，不給單一價位，不寫購買管道。

## 4. 技術規範（依 Google 官方文件）

### 4.1 每頁 `<head>`

- `<link rel="canonical">`：絕對網址、指向自己。
- Open Graph：`og:title`、`og:description`、`og:url`（= canonical）、`og:type`（文章 `article`，其他 `website`）、`og:site_name`（`Chun Jui Lu`）、`og:locale`（`zh_TW` 或 `en_US`）；有圖再加 `og:image`。
- `twitter:card`：`summary`（沒圖）或 `summary_large_image`（有圖）。
- 刪除 `<meta name="robots" content="noai, noimageai">`。
- 英文頁裡的中文段落標 `lang="zh-Hant"`。
- **不加 hreflang**：英文頁和中文頁不是互譯版本。
- **不做 llms.txt**：Google 文件明說出現在 AI Overviews／AI Mode 沒有額外要求。

### 4.2 robots.txt（擋訓練、放搜尋）

```
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: meta-externalagent
User-agent: CCBot
User-agent: Bytespider
Disallow: /

User-agent: *
Allow: /
Disallow: /_dev/

Sitemap: https://onepunchmed.github.io/sitemap.xml
```

- OAI-SearchBot、ChatGPT-User、Claude-SearchBot、Claude-User、PerplexityBot、Meta-WebIndexer 落到 `*` 被放行。
- Google-Extended 只管 Gemini 訓練與 grounding，不影響 Google 搜尋收錄。
- 限制：Perplexity-User、Meta-ExternalFetcher 官方表示可能不理 robots.txt。
- `/_dev/` 只擋爬蟲，檔案仍可被直接開啟；不要在這個資料夾放機密。

### 4.3 結構化資料（JSON-LD）

- **Markets 文章**：`Article`，含 `headline`（= H1）、`datePublished`（= 可見 `<time>`）、`dateModified`（內容有實質修改才更新）、`author: {"@type":"Person","name":"Chun Jui Lu","url":"<site>/"}`、`inLanguage: "zh-Hant"`、`publisher` 同作者；另加 `BreadcrumbList`（About › Markets › 文章）。
- **index.html**：`ProfilePage`，`mainEntity` 為 `Person`：`name`、`description`（取頁面上已寫的職稱與學歷）、`sameAs`（ORCID、GitHub）、`url`。結構化資料只能描述頁面上看得到的內容。
- **markets/index.html**：`CollectionPage` 或只加 `BreadcrumbList`。
- FAQPage：Google 已大幅限縮 FAQ 複合式結果的顯示範圍（此點未在本輪重新查證），不列為必要；如果文章加 FAQ 區塊，以可見內容為主。

### 4.4 sitemap.xml

只列 canonical 網址；`lastmod` 只在內容實質變動時更新；不用 `priority`、`changefreq`。手寫即可，12 頁不需要產生器；之後頁數變多再寫小腳本。

### 4.5 作者署名（E-E-A-T，依站長選擇只用英文名）

每篇 Markets 文章在 `article-meta` 加可見署名：`<a rel="author" href="../index.html">Chun Jui Lu</a>`。英文個人頁已有學歷與職稱，署名連過去即可，不在中文文章加頭銜。

## 5. 英文學術頁目標

- 主題詞（positive-unlabeled learning、undiagnosed diabetes primary care）的搜尋結果由 arXiv、PMC 等學術來源主導，不設排名目標。
- 目標改為**姓名搜尋**：`Chun Jui Lu` 同名者多，靠 ProfilePage、ORCID／GitHub `sameAs`、一致的姓名寫法，讓 Google 把本站認成這個人的主頁。
- 反向連結：ORCID 個人檔案的網址欄、GitHub profile 網址欄、日後論文作者資訊都填本站網址（站長手動）。

## 6. Markets 區目標

- 用 §3 的易、中難度詞取得排名；套利成本、避險回測、回測方法論是本站最有利的三題。
- 內容調整（需站長逐篇核可，不由開發自動改寫）：
  - `<title>` 前置關鍵字，H1 保持原樣。
  - 補「X 是什麼」定義段與「自己怎麼查」段。
  - 段首 2–4 句直接回答。
- 站外：PTT Stock、Mobile01 貼摘要並附連結（站長自行發）。

### 6.1 `<title>` 建議（只改 title tag，H1 不動；需站長核可）

| 檔案 | 現在 | 建議 |
|---|---|---|
| backtest-checklist | 用讀臨床試驗的方式讀回測：十個問題 | 回測可信嗎？用讀臨床試驗的方式檢查前瞻偏誤、過度擬合與存活者偏誤 |
| tw-arbitrage | 台股套利為什麼對散戶不成立：用 6.8 年期貨資料算一次 | 台股期現貨套利與台積電 ADR 溢價：扣完成本散戶還剩多少（6.8 年資料） |
| tsmc-taiex-hedge | 台積電超跌加碼、台指超漲放空：20 年回測只有一半成立 | 台積電超跌買進、台指超漲放空回測：20 年、120 組參數與 walk-forward |
| tw-hedge-backtest | 三組多空避險策略回測 2022–2026：…全部輸給買進持有 | 微型台指與股票期貨多空避險回測 2022–2026：三組都輸給買進持有 |
| tsmc-valuation | 用台積電練估值：四個方法、三個情境… | 台積電估值怎麼做：本益比、DCF、反向 DCF 與三情境敏感度 |
| pre-ipo-valuation | 沒有正常價格時怎麼估值：… | Pre-IPO 估值怎麼做：Anthropic 盤前合約與宇樹 7% 流通盤案例 |

## 7. 量測

- Google Search Console：github.io 只能用「網址前置字元」資源，以 HTML 驗證檔或首頁 meta tag 驗證；換網域後要重新驗證新網域。
- Bing Webmaster Tools：可從 Search Console 匯入；Copilot 引用另有 AI Performance 報表。
- IndexNow：放金鑰檔即可，Google 不參與，屬選配。
- AI 引用率：每月用 10–20 題的台灣使用者說法題組，在 ChatGPT、Perplexity、Google 各問 3–5 次，由站長在自己登入的瀏覽器執行並記錄。

## 8. 主要來源

- Article：https://developers.google.com/search/docs/appearance/structured-data/article
- ProfilePage：https://developers.google.com/search/docs/appearance/structured-data/profile-page
- Breadcrumb：https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Sitemap：https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Canonical：https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Robots meta：https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- AI 功能：https://developers.google.com/search/docs/appearance/ai-features
- Google 爬蟲（Google-Extended）：https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- 搬站：https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- 有用內容與 E-E-A-T：https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- OpenAI 爬蟲：https://developers.openai.com/api/docs/bots
- Anthropic 爬蟲：https://support.claude.com/en/articles/8896518
- Perplexity 爬蟲：https://docs.perplexity.ai/docs/resources/perplexity-crawlers.md
- Meta 爬蟲：https://developers.facebook.com/docs/sharing/webmasters/web-crawlers
- Apple：https://support.apple.com/HT204683
- GitHub Pages 網域驗證：https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- GitHub Pages 自訂網域：https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Search Console 驗證：https://support.google.com/webmasters/answer/9008080
- IndexNow：https://www.indexnow.org/documentation
- 開源方法參考：AgriciDaniel/claude-seo（MIT）、inhouseseo/superseo-skills（Apache-2.0）、coreyhaines31/marketingskills（MIT）
