# 🚀 專案記憶與交接文件 (PROJECT_HANDOVER)

## 📌 一、 專案核心介紹與架構
* **專案名稱**：`forsure0922`（飯拍與周邊團購登記管理系統）
* **技術棧**：原生 HTML/CSS/JS (ES6 Module) + Firebase Firestore Database + GitHub Pages 靜態託管。
* **主要 JSON 設定檔**：
  * `json/group.json`：團體清單（現有 `Stray Kids`、`ATEEZ`）。
  * `json/members_skz.json`：Stray Kids 成員陣列（嚴格維護原始順序，不按 Alphabet 排序）。
  * `json/members_atz.json`：ATEEZ 成員陣列（嚴格維護原始順序，不按 Alphabet 排序）。
  * `json/users.json`：社群買家暱稱名單。
  * `json/bank_info.json`：收款銀行帳號資訊。

---

## 🎨 二、 前後台統一「雙區域膠囊篩選」與動態 IF 隱藏機制
全站（除 Deposit 儲值金系列頁面外）統一採用以下篩選規則：
1. **區域 A（團體與場次細分）**：
   - 第一層：[Stray Kids] / [ATEEZ] 膠囊切換。
   - 第二層：[依成員] / [依活動] 檢視模式切換。
   - 第三層：動態細項膠囊（加上 IF 條件：下方明細中真的有資料才渲染，成員嚴格維持 JSON 順序）。
2. **區域 B（社群暱稱獨立篩選）**：
   - 買家暱稱獨立膠囊（加上 IF 條件：當前篩選下真的有喊單才渲染，按 A-Z、0-9 順序排列）。

---

## 📂 三、 專案架構流程圖比對 (歷史原版 vs 重構升級版)

### 1. 歷史原版架構圖 (留存比對)
========================================================================
index.html (前台總控與 Tab 主選單)
├── 透過 iframe 切換 6 大功能頁面：
│   ├── 1. index/index_progress.html (開團與進度)
│   ├── 2. index/index_notice.html (注意事項)
│   ├── 3. index/index_payment.html (匯款表單)
│   ├── 4. index/index_records.html (登記與對帳進度查詢)
│   ├── 5. index/index_deposit_app.html (帳戶儲值與退款中心)
│   └── 6. index/index_lottery.html (抽獎結果公告)

admin.html (後台總控 / 各獨立管理頁面進入點)
├── admin_deposit.html (預存儲值與抵用金管理)
├── admin_progress.html (發佈與更新發圖進度)
├── admin_orders.html (內嵌 orders/orders_form.html 與 orders/orders_manage.html)
├── admin_lottery.html (抽獎活動管理與結果發佈)
├── admin_events.html (活動單價與成本設定)
├── admin_payments.html (內嵌 payment/ payment_pending/ok/error/photosent.html)
└── admin_ctbc_bank.html (中信存款交易明細對帳系統)
========================================================================

### 2. 重構升級版全站架構圖 (當前最新實案)
========================================================================
index.html (前台總控與 Tab 主選單)
├── 1. index/index_progress.html
│   └── (新增動態 IF 隱藏無資料膠囊)
├── 2. index/index_notice.html
├── 3. index/index_payment.html
├── 4. index/index_records.html
│   └── (新增待匯款紅色膠囊、彙總卡片、UI雙欄改版、動態 IF 膠囊)
├── 5. index/index_deposit_app.html
│   └── (新增台銀/樂天/中信銀行帳號自動帶出提示)
└── 6. index/index_lottery.html
    └── (新增動態 IF 隱藏無資料膠囊)

admin.html (後台總控 / 各獨立管理頁面進入點)
├── admin/admin_deposit.html (預存儲值與抵用金管理)
├── admin/admin_progress.html (新增動態 IF 隱藏無資料膠囊)
├── orders_manage.html (位於根目錄，修復 $0 總價 BUG + 高對比彩色標籤 + 動態 IF 膠囊)
├── orders_form.html (位於根目錄，優化 max-width: 600px 置中)
├── admin/admin_lottery.html (新增動態 IF 隱藏無資料膠囊)
├── admin/admin_events.html (新增動態 IF 隱藏無資料膠囊)
├── admin/admin_payments.html
│   └── 內嵌 admin/payment/ (payment_pending, payment_ok, payment_error, payment_photosent)
└── deposit.html (存款交易明細對帳表)
========================================================================

---

## 🤝 四、 專案相處模式與溝通默契
1. **拒絕廢話與無意義讚美**：開啟新話題時不說「好的」、「沒問題」，直接講重點或給方案。
2. **務實且嚴謹排查**：不盲目猜測，獨立審視程式碼與算式後才給出結論。被指出錯誤時直接承認並快速修正。
3. **檔案路徑絕不能出錯**：
   - 核心填單/管理檔置於根目錄：`orders_form.html`、`orders_manage.html`。
   - 後台對帳子頁面位於：`admin/payment/payment_*.html`。
4. **成員排序鐵律**：無論哪一個頁面，只要列出成員，**嚴格遵循 `members_skz.json` / `members_atz.json` 的原始陣列順序**，絕不自動按 Alphabet 排序。
