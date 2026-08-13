# 🚀 專案記憶與極詳細交接文件 (PROJECT_HANDOVER)

## 📌 一、 專案核心介紹與架構
* **專案名稱**：`forsure0922`（飯拍與周邊團購登記管理系統）
* **技術棧**：原生 HTML/CSS/JS (ES6 Module) + Firebase Firestore Database + GitHub Pages 靜態託管。
* **主要 JSON 設定檔**：
  * `json/group.json`：團體清單（現有 `Stray Kids`、`ATEEZ`）。
  * `json/members_skz.json`：Stray Kids 成員陣列（**鐵律：排序不可自動重排，必須嚴格維持此 JSON 陣列順序**）。
  * `json/members_atz.json`：ATEEZ 成員陣列（**鐵律：排序不可自動重排，必須嚴格維持此 JSON 陣列順序**）。
  * `json/users.json`：社群買家暱稱名單。
  * `json/bank_info.json`：收款銀行帳號資訊。
  * `json/banks.json`：匯款選擇銀行清單。
  * `json/sellers.json`：代拍廠商清單。

---

## 🤝 二、 人格設定、相處模式與溝通默契 (AI 必讀執行鐵律)

1. **拒絕廢話與無意義讚美**：
   - 開啟話題或回應時，絕對不要說「好的」、「沒問題」、「很高興為您服務」等機械式開場白。
   - 直奔主題、講重點、直接給方案與分析。

2. **嚴禁擅自生成指令 (最重要鐵律)**：
   - **在使用者明確說「好」、「OK」或要求提供指令之前，絕對不能擅自生成 Bash / Git 執行指令！**
   - 流程必須為：**討論問題與方案 ➔ 展示文字 UI Layout / 邏輯分析 ➔ 使用者確認「好」➔ 才可給出 Bash 指令**。

3. **指令格式鐵律**：
   - 喜歡使用包含 `cat << 'EOF'` 與 `git` 的單一完整 Bash 區塊。
   - 必須確保指令可以一口氣貼在 Git Bash 完整執行，中間嚴禁包含會讓 Shell 解析中斷的巢狀標記或內部衝突字元。

4. **檔案路徑絕對精準**：
   - 核心填單與管理檔案置於**根目錄**（`orders_form.html`、`orders_manage.html`），切勿加上 `orders/` 等子目錄前綴。
   - 後台對帳子頁面位於 `admin/payment/` 子目錄內（`payment_pending.html`、`payment_ok.html`、`payment_error.html`、`payment_photosent.html`）。
   - 前台歸檔子頁面位於 `index/archive/` 子目錄內（`archive_progress.html`、`archive_records.html`）。

5. **成員排序鐵律**：
   - 無論哪個頁面渲染成員，**嚴格遵循 `members_skz.json` / `members_atz.json` 原始陣列順序**，絕不自動按 Alphabet 排序。

---

## 🎨 三、 核心邏輯與動態資料分流架構

1. **全站雙區域膠囊篩選與動態 IF 機制**：
   - **區域 A（團體與場次細分）**：
     - 第一層：`[Stray Kids]` / `[ATEEZ]` 膠囊切換。
     - 第二層：`[依成員]` / `[依活動]` 檢視模式切換。
     - 第三層：動態細項膠囊（**動態 IF 條件：下方明細中真的有資料才渲染**）。
   - **區域 B（社群暱稱獨立篩選）**：
     - 買家暱稱膠囊（**動態 IF 條件：當前篩選下真的有喊單才渲染**）。

2. **進度與對帳動態 Key 分流歸檔機制**：
   - 前台 `index_progress.html` 與 `index_records.html` 動態比對 `photo_progress` 狀態：
     - 狀態為 **`未開放`、`已預約`、`等圖中`、`分圖中`、`上傳中`、`已通知匯款`、`已發圖`** ➔ 在前台主頁正常渲染。
     - 狀態改為 **`已結束`、`到期/已刪除`** ➔ 前台主頁自動過濾並移除，由 `index/index_archive.html` 專屬歸檔頁面接管。

3. **後台發起匯款連動 (`admin_progress.html`)**：
   - 狀態選單擴充至 9 種。
   - 每列資料附帶 **`[📢 發起匯款]`** 按鈕，管理者點擊確認後，批量將對應活動+成員下未付款訂單改為 `待匯款`，且該筆進度狀態同步改為 `已通知匯款`。

---

## 📂 四、 完整檔案樹狀圖 (PROJECT STRUCTURE)

* `/forsure0922`
  * `index.html` (前台總控 - 7 大 Tab 主選單)
  * `admin.html` (後台總控控制台)
  * `orders_form.html` (團員登記填單表單)
  * `orders_manage.html` (團員登記管理與一鍵發圖)
  * `deposit.html` (存款交易明細對帳表)
  * `PROJECT_HANDOVER.md` (專案極詳細交接與記憶文件)
  * `index/` (前台功能頁面)
    * `index_progress.html` (開團與進度 - 進行中)
    * `index_notice.html` (注意事項)
    * `index_payment.html` (匯款表單)
    * `index_records.html` (登記與對帳查詢 - 進行中自適應2欄)
    * `index_deposit_app.html` (帳戶儲值與退款中心)
    * `index_lottery.html` (抽獎結果公告)
    * `index_archive.html` (歷年已結束歸檔總控)
    * `archive/` (歸檔子頁面)
      * `archive_progress.html` (歷年開團與發圖進度歸檔)
      * `archive_records.html` (歷年喊單與對帳紀錄歸檔)
  * `admin/` (後台管理頁面)
    * `admin_events.html` (活動單價與成本設定)
    * `admin_progress.html` (發佈與更新發圖進度 - 9種狀態與發起匯款按鈕)
    * `admin_lottery.html` (抽獎活動管理)
    * `admin_deposit.html` (預存儲值與抵用金管理)
    * `admin_payments.html` (匯款對帳審核總控台)
    * `admin_ctbc_bank.html` (中信存款交易明細對帳系統)
    * `payment/` (匯款審核 4 大子頁面)
  * `json/` (系統靜態設定檔)

---

## 🌳 五、 最新專案目錄樹狀圖 (2026/08/13 實測備份)

.
├── PROJECT_HANDOVER.md
├── admin
│   ├── admin_ctbc_bank.html
│   ├── admin_deposit.html
│   ├── admin_events.html
│   ├── admin_lottery.html
│   ├── admin_orders.html
│   ├── admin_payments.html
│   ├── admin_progress.html
│   ├── ctbc_data.js
│   ├── deposit.html
│   ├── orders
│   │   ├── orders_form.html
│   │   └── orders_manage.html
│   └── payment
│       ├── payment_all.html
│       ├── payment_error.html
│       ├── payment_manage.html
│       ├── payment_ok.html
│       ├── payment_pending.html
│       └── payment_photosent.html
├── admin.html
├── file_path.txt
├── idea
│   └── 20260731_architecture.txt
├── index
│   ├── archive
│   │   ├── archive_progress.html
│   │   ├── archive_records.html
│   │   ├── index_archive_progress.html
│   │   └── index_archive_records.html
│   ├── index_archive.html
│   ├── index_deposit_app.html
│   ├── index_lottery.html
│   ├── index_notice.html
│   ├── index_payment.html
│   ├── index_progress.html
│   └── index_records.html
├── index.html
├── json
│   ├── bank_info.json
│   ├── banks.json
│   ├── ctbc_transactions.json
│   ├── group.json
│   ├── members_atz.json
│   ├── members_skz.json
│   ├── sellers.json
│   ├── users_atz.json
│   └── users_skz.json
└── parse.html

---

## 📝 六、 開發變更日誌 (Change Log)

### 2026-08-13
1. **json/users_atz.json**：更新 ATEEZ 社群成員 21 位名單，連動選單免動態馬賽克。
2. **admin/admin_payments.html**：
   - 新增「📋 全部」分頁標籤並移至最首位設為預設載入頁面。
3. **admin/payment/ 全套子頁面 (payment_all.html, payment_pending.html, payment_error.html, payment_ok.html)**：
   - 新增 formatSocialDisplay() 邏輯，依據 contactType 正確呈現 [IG]、[Threads] 與 💬 官方 Line，不再暴露賣家官方 Line ID。
   - 建立全功能總覽頁面 payment_all.html。
4. **index/index_deposit_app.html**：
   - 修正訂單明細扣抵顯示邏輯，加入「第一優先：活動日期數字正序（舊到新）」與「第二優先：遵照 members_skz.json / members_atz.json 官方成員陣列順序」之雙重排序。
   - 清理並刪除誤建之 index/index_deposit.html。
