# SEO Phase 2 草稿（待站長逐項核可）

機密 CONFIDENTIAL · https://onepunchmed.github.io

起草日期：2026-10-29。依據：`_dev/seo/TASKS.md` Phase 2、`_dev/seo/SEO_PLAN.md` §3.3、§6.1。

**這份檔案只是草稿，沒有改任何 HTML。** 請在每一項的「核可」欄寫「可」、「不要」或修改後的文字。核可的項目會另開一個 PR 實作；實作時同步更新該頁的 `dateModified`、sitemap `lastmod` 與頁尾「Last updated」（TASKS Phase 2 第 6 項）。

共同規則（TASKS Phase 2 規範）：
- 數字一律不改。定義段只引用該篇已經寫出的數字。
- H1 不動；JSON-LD `headline` 維持等於 H1；只改 `<title>` 與 `og:title`。
- 不寫「保證」「穩賺」「首創」「唯一」，不給買賣建議、單一目標價或購買管道。
- 標點與斷行沿用全站風格。

## 總表

| # | 文章 | 標題 | 描述 | 定義段 | 自己怎麼查 | 延伸閱讀 |
|---|---|---|---|---|---|---|
| 1 | backtest-checklist | 改 | 不動 | 3 段 | — | 補 2 篇 |
| 2 | tw-arbitrage | 改 | 不動 | 2 段 | 新增 | 補 3 篇 |
| 3 | tsmc-taiex-hedge | 改 | 不動 | — | — | 補 3 篇 |
| 4 | tw-hedge-backtest | 改 | 不動 | — | — | 補 3 篇 |
| 5 | tsmc-valuation | 改 | 不動 | 1 段 | — | 補 3 篇 |
| 6 | pre-ipo-valuation | 改 | 不動 | — | — | 補 3 篇 |
| 7 | night-session、sharpe-drawdown、dca-vs-dip-0050 | 不動 | 不動 | — | — | 各補 1–2 篇 |

**描述（TASKS 第 2 項）：** 9 篇的 meta description 目前都在 160 字以內（最長是 tsmc-valuation 的 150 字），也都保留了「不構成投資建議」，依規格不需要縮短。

---

## 1. `<title>` 建議（TASKS 第 1 項，依 SEO_PLAN §6.1）

站名後綴「 | Chun Jui Lu」保留。Google 搜尋結果大約顯示前 30 個中文字左右，所以關鍵字放在最前面。

| 文章 | 現在 | 建議 | 核可 |
|---|---|---|---|
| backtest-checklist | 用讀臨床試驗的方式讀回測：十個問題 | 回測可信嗎？用讀臨床試驗的方式檢查前瞻偏誤、過度擬合與存活者偏誤 | |
| tw-arbitrage | 台股套利為什麼對散戶不成立：用 6.8 年期貨資料算一次 | 台股期現貨套利與台積電 ADR 溢價：扣完成本散戶還剩多少（6.8 年資料） | |
| tsmc-taiex-hedge | 台積電超跌加碼、台指超漲放空：20 年回測只有一半成立 | 台積電超跌做多、台指超漲放空回測：20 年、120 組參數與 walk-forward | |
| tw-hedge-backtest | 三組多空避險策略回測 2022–2026：把選股判斷寫成規則之後，全部輸給買進持有 | 微型台指與股票期貨多空避險回測 2022–2026：三組都輸給買進持有 | |
| tsmc-valuation | 用台積電練估值：四個方法、三個情境，答案的區間比答案重要 | 台積電估值怎麼做：本益比、DCF、反向 DCF 與三情境敏感度 | |
| pre-ipo-valuation | 沒有正常價格時怎麼估值：Anthropic 的盤前合約與宇樹的 7% 流通盤 | Pre-IPO 估值怎麼做：Anthropic 盤前合約與宇樹 7% 流通盤案例 | |

和 §6.1 原建議的差異只有一處：tsmc-taiex-hedge 把「超跌買進」改成「超跌做多」，和內文用語一致，也避免讀起來像買進建議。

---

## 2. 定義段（TASKS 第 3 項）

每段 2–3 句，可以被單獨引用。放在指定 H2 的第一段之前，以 `<p>` 呈現，不另加小標。

### 2.1 backtest-checklist

**前瞻偏誤**　放在「一、時間：最容易犯、也最難察覺」底下：

> 前瞻偏誤（look-ahead bias）是回測在做決定的時點，用到了當時還拿不到的資料。最常見的來源是收盤時間差：台股 13:30 收盤，美股收盤在台北隔天清晨，用兩者一起算出的訊號，等於先偷看了答案。本站的套利回測修正這一點之後，每筆平均報酬從 +6.4% 掉到 +1.5%。

核可：

**過度擬合**　放在「二、多重比較：參數最佳化就是 p-hacking」底下：

> 過度擬合（overfitting）是參數被調得太貼合過去的資料，學到的是那段期間的雜訊，而不是會重複出現的規律，所以樣本內很漂亮、換一段資料就變差。檢查的方法是把資料切成樣本內和樣本外：本站一篇回測裡，樣本內夏普值最高的參數組合是 0.42，到樣本外變成 −0.54。

核可：

**存活者偏誤**　放在「四、樣本與證據等級」底下：

> 存活者偏誤（survivorship bias）是只用今天還存在的股票、基金或契約去回推過去，期間下市、被剔除或清算的樣本都消失了，結果通常偏樂觀。這和只追蹤還在門診回診的病人會高估療效，是同一種偏誤。

核可：

### 2.2 tw-arbitrage

**正價差與逆價差**　放在「一、理論價很準，成本才是重點」底下：

> 期貨價格高於現貨叫正價差，低於現貨叫逆價差。股票期貨的理論價是「現貨 ×（1 + 資金成本 × 剩餘天數 ÷ 365）」，所以沒有股利影響時，理論上會有小幅正價差；只有偏離理論價的幅度大過一趟來回成本，才有套利空間。本文測得台積電股期偏離的 95 分位只有 +0.70%，低於一趟約 0.89% 的成本。

核可：

**ADR 溢價**　放在「三、台積電 ADR 溢價為什麼不會收斂」底下：

> ADR（美國存託憑證）是外國公司在美國掛牌交易的憑證，台積電 ADR 的代號是 TSM。ADR 溢價是 ADR 價格換算回新台幣、再按換股比例比較之後，比台股貴多少。台積電因為台股轉成 ADR 有額度限制，2020 年後平均溢價 11.7%，這是制度造成的結構，不是錯價。

核可：

### 2.3 tsmc-valuation

**反向 DCF**　放在「4.4 反向 DCF」小節的第一段之前：

> 一般的 DCF 是先假設成長率，再算公司值多少；反向 DCF 倒過來，固定折現率、利潤率與永續成長率，問現在的市價隱含了多少成長。本文的答案是 2027 到 2030 年每年約 22.1%，非常接近基準情境的 20.8%。

核可：

---

## 3. tw-arbitrage「自己怎麼查」（TASKS 第 4 項）

放在「方法與限制」之前，新增一節 `<section>`，H2 為「自己怎麼查」。下列連結都在 2026-10-29 確認可以開啟。

> 本文的期貨資料來自期交所，現貨、ADR 與匯率用 Yahoo Finance 日線。想自己核對，官方或第一手的來源如下：
> - 股票期貨每日結算價：期交所「期貨每日交易行情查詢」 https://www.taifex.com.tw/cht/3/futDailyMarketReport ，或「每日行情下載」 https://www.taifex.com.tw/cht/3/dlFutDailyMarketView
> - 現股每日收盤價：證交所「個股日成交資訊」 https://www.twse.com.tw/zh/trading/historical/stock-day.html
> - 除息日與除息參考價：證交所「除權除息計算結果表」 https://www.twse.com.tw/zh/announcement/ex-right/twt49u.html
> - 台積電 ADR（TSM）價格：紐約證交所 https://www.nyse.com/quote/XNYS:TSM
> - 新台幣兌美元匯率：臺灣銀行「歷史匯率」 https://rate.bot.com.tw/xrt/history
> - ADR 換股比例：台積電向美國證管會提交的 2025 年度 20-F，每單位 ADR 代表 5 股普通股 https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm
>
> 計算順序：先把 ADR 價格除以換股比例、乘以匯率，換算成每股新台幣，再和同一天的台股收盤相比。注意美股收盤比台股晚了一個晚上，這正是第四節講的時差陷阱。

核可：

（備註：換股比例已在 2026-10-29 於上述 20-F 原文核對，原句為 "each ADS represents five (5) common shares"。）

---

## 4. 延伸閱讀（TASKS 第 5 項）

放在「方法與限制」之後、免責聲明之前，新增一節 `<section>`，H2 為「延伸閱讀」，每篇 3 個連結，各附一句說明。下表「補」是目前內文沒有連過去的；已經在內文連過的不重複放。

| 文章 | 目前內文已連 | 建議延伸閱讀（補） | 核可 |
|---|---|---|---|
| tw-arbitrage | 無 | night-session（夜盤與 ADR 的時差）、backtest-checklist（時差陷阱是第 1 題）、sharpe-drawdown（勝率 100% 為什麼是警訊） | |
| tw-hedge-backtest | 無 | tsmc-taiex-hedge（同樣是多空結構）、backtest-checklist（換倉日敏感度與多重比較）、sharpe-drawdown（這篇的夏普值信賴區間） | |
| tsmc-taiex-hedge | 無 | tw-hedge-backtest（另一組多空回測）、backtest-checklist（參數最佳化的例子）、sharpe-drawdown（樣本內外夏普值） | |
| tsmc-valuation | 無 | pre-ipo-valuation（沒有市價時的估值）、backtest-checklist（區間而非點估計）、tsmc-taiex-hedge（同一檔股票的回測） | |
| pre-ipo-valuation | 無 | tsmc-valuation（上市公司版的同一套方法）、backtest-checklist（證據等級）、sharpe-drawdown（區間與樣本數） | |
| backtest-checklist | 5 篇 | sharpe-drawdown（續篇）、dca-vs-dip-0050（預先登記的實例） | |
| night-session | tw-arbitrage | tsmc-taiex-hedge、backtest-checklist | |
| sharpe-drawdown | 3 篇 | backtest-checklist（前篇）、dca-vs-dip-0050（同一套讀法用在新回測） | |
| dca-vs-dip-0050 | 2 篇 | tw-hedge-backtest（另一個輸給買進持有的例子） | |

各篇的連結說明文字，會在核可後實作時照上表括號內容寫成一句話，不加新的數字。

---

## 5. 實作時一起改的東西（不需另外核可）

- 改過的頁面：`dateModified`、sitemap `lastmod`、頁尾「Last updated」更新為實作當天。
- `og:title` 跟著新 `<title>`；JSON-LD `headline` 不動。
- 實作後跑 `python3 _dev/seo/seo_check.py`，必須 0 FAIL；另外逐頁比對可見文字，確認除了核可的段落之外沒有其他變動。
