# SEO CHANGELOG

## 2026-10-29　換網域到 onepunchmed.com（Phase 3）

- 網域在 Cloudflare Registrar 註冊，DNS 也在 Cloudflare。根網域 4 筆 A、4 筆 AAAA 指向 GitHub Pages，`www` CNAME 指向 `onepunchmed.github.io`，全部 DNS only（不經 Cloudflare proxy）。
- GitHub 帳號層級驗證網域（TXT `_github-pages-challenge-onepunchmed`），驗證記錄保留。
- PR #10 加 `CNAME`，全站 canonical、og:url、JSON-LD、sitemap、robots 改為 `https://onepunchmed.com`。
- GitHub Pages 憑證：approved，涵蓋 onepunchmed.com 與 www.onepunchmed.com，到期 2027-01-27（自動續期）。Enforce HTTPS 已開。
- 轉址實測（curl）：
  - `https://onepunchmed.github.io/markets/backtest-checklist.html` → 301 → `http://onepunchmed.com/markets/backtest-checklist.html` → 301 → `https://...`（同路徑保留）
  - `https://www.onepunchmed.com/` → 301 → `https://onepunchmed.com/`
  - `http://onepunchmed.com/` → 301 → `https://onepunchmed.com/`
- Search Console：新增「網域」資源 `onepunchmed.com`（DNS TXT 驗證，記錄要保留），提交 `https://onepunchmed.com/sitemap.xml`。
- Bing Webmaster：從 GSC 匯入 onepunchmed.com，提交新 sitemap。
- GitHub 個人頁與 ORCID 的網站欄改為 https://onepunchmed.com 。
