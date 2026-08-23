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

---

## 📝 七、 2026-08-20 開發日誌與資料庫重構收尾

### 🎯 今日核心重構進度：
1. **全面廢除靜態 JSON 依賴**：
   * 正式刪除 `json/users_skz.json`、`json/users_atz.json` 與 `json/sellers.json`。
   * 買家名單全面改接 Firestore `users` 集合（社群成員 `type: "custom"` 全顯，Threads 帳號自動遮罩）。
   * 代拍廠商名單全面改接 Firestore `sellers` 集合。
2. **`index/index_records.html` 全面重構修復**：
   * **膠囊選單標準化**：團體膠囊首位新增 `[ 全部 ]` 並設為預設 `active`，套用 `🧭 Stray Kids` / `🏴‍☠️ ATEEZ` 可愛動物 Emoji。
   * **修復發圖狀態污染 Bug**：廢除按買家全域比對發圖狀態之邏輯，嚴格改為與訂單本身之 `isPhotoSent === true` 綁定。
   * **嚴格即時聯動進行中狀態**：只要在 `photo_progress` 將活動標記為 `已結束` 或 `到期/已刪除`，查單明細立刻同步隱藏。
   * **三層嚴格排序核心**：第 1 層：活動日期數字（舊到新）➔ 第 2 層：團體（🏴‍☠️ ATEEZ 優先於 🧭 SKZ）➔ 第 3 層：官方成員陣列順序。
   * **版面與欄位優化**：
     - 表格名稱下方清晰補齊「團體與成員」標註（如 `🏴‍☠️ ATEEZ · 🐶 潤浩`）。
     - 發圖狀態與期限改為三行垂直排列（`已發圖` / `發圖日期` / `刪除期限`）。
     - 數量單位計算校正，徹底消除 `100包 (100張)` 之錯誤，規範顯示為 `1包 (100張)`。
     - 待匯款清單補齊團體與成員專屬可愛 Emoji。
3. **`admin/admin_stock.html`**：
   * 全面套用團體與成員可愛動物 Emoji 映射。
4. **`admin/admin_ctbc_bank.html` & `index/index_deposit_app.html`**：
   * 在 100% 嚴格保留原 UI 排版與業務邏輯前提下，精確將買家下拉選單替換為 Firestore `users` 即時監聽。
5. **專案路徑清理**：
   * 刪除舊路徑殘留之 `admin/orders/orders_form.html`。

---

## 🌳 八、 現行完整專案目錄樹狀圖 (2026/08/20 終端實測確認)

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
│   ├── admin_sellers.html
│   ├── admin_stock.html
│   ├── admin_users.html
│   ├── ctbc_data.js
│   ├── deposit.html
│   ├── orders
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
│   ├── index_records.html
│   └── index_stock.html
├── index.html
├── json
│   ├── bank_info.json
│   ├── banks.json
│   ├── ctbc_transactions.json
│   ├── group.json
│   ├── members_atz.json
│   └── members_skz.json
├── orders_form.html
└── parse.html

---

## ⚠️ 九、 與使用者相處與協作之【最高警戒鐵律】(AI 嚴禁違背)

1. **嚴禁擅自大改 / 偷改 UI 排版與結構 (最嚴重違規事項)**：
   - 需求若為「更換資料來源（如 JSON 換 Firestore）」，**嚴格只允許替換資料讀取邏輯**！
   - **絕對不准擅自重構、美化、改寫、刪減既有的 HTML 結構、表單欄位與 CSS 排版**。
2. **嚴禁未經同意擅自生成指令**：
   - 必須遵守：**提出分析與改動範圍說明 ➔ 使用者檢閱確認 ➔ 使用者回覆「好 / OK」 ➔ 始得提供單一 Bash 指令**。
   - 討論階段嚴禁附帶任何 Bash / Git 指令。
3. **改動前必須逐行檢閱現行程式碼**：
   - 不可盲目臆測舊程式碼內容，必須以使用者提供的檔案內容為基準進行比對。
4. **團體平等與膠囊規範**：
   - 膠囊篩選第一顆必為 `[ 全部 ]`（預設 active），禁止將單一團體強制設為唯一預設。
   - 團體順序若無特別指定，排序邏輯優先呈現 `ATEEZ` 接著 `Stray Kids`。
5. **成員排序不可變動**：
   - 嚴格維持 `json/members_skz.json` 與 `json/members_atz.json` 官方設定之陣列順序。
=============================================================

20260823 gemini pro

# 🚀 專案記憶與極詳細交接文件 (PROJECT_HANDOVER)

## ⚠️ 零、 致接手的 Gemini AI：與本使用者協作之【最高警戒生存手冊】
**如果你不想惹怒使用者、浪費他的 Token 與時間，請把這段當成你的系統底層邏輯，刻在 DNA 裡！**

### 💀 1. 嚴禁擅自刪減/「優化」既有欄位與 UI (踩雷率第一名)
* **使用者的痛點**：AI 常常為了「排版簡潔」自作聰明，把原本已經寫好的 `<input>` 欄位（例如：張數、後五碼、匯款日期、備註等）偷偷刪掉。
* **鐵律**：不管你覺得畫面多擠，**絕對不准**擅自拔掉任何一個欄位！如果要重構排版（例如從 Table 換成 Grid），必須保證 100% 的資料欄位完整移植。

### 🤐 2. 拒絕廢話、機械式官腔與無意義的道歉
* **使用者的痛點**：討厭看到「好的，完全理解！」、「非常抱歉造成您的困擾」、「很高興為您服務」。
* **鐵律**：直奔主題，講重點。直接給方案、分析優缺點、或是展示純文字版的 UI 畫面草圖。

### 🛑 3. 「純討論模式」與「給指令」的嚴格分界
* **使用者的痛點**：還沒討論完細節，AI 就急著丟出一大包程式碼，結果根本不是他要的，導致要一直 Undo。
* **鐵律**：
  - **討論階段**：只准用文字排版畫出「預計長怎樣的 UI」，並列出邏輯（例如 1. 2. 3. 點）。**嚴禁附帶任何 HTML/JS 程式碼。**
  - **輸出階段**：直到使用者明確說出 **「給我指令」**、**「好」**、**「OK」** 時，你才可以給出唯一的 Bash (`cat << 'EOF'`) 覆寫指令。

### 📊 4. 成員排序是神聖不可侵犯的
* **使用者的痛點**：AI 喜歡用 JS 的 `.sort()` 把成員名字按筆畫或英文字母重排，導致官方順序大亂。
* **鐵律**：只要畫面需要渲染 Stray Kids 或 ATEEZ 的成員，**只能、必須、絕對要**依靠 `members_skz.json` 或 `members_atz.json` 裡的原始陣列順序。

### 💻 5. 指令交付格式
* 永遠使用 `cat << 'EOF' > [相對路徑]` 搭配 `git add`, `git commit`, `git push` 的單一 Bash 區塊。
* 中間不能有會讓 Git Bash 解析中斷的符號。

---

## 📌 一、 專案核心介紹與架構
* **專案名稱**：`forsure0922`（飯拍與周邊團購登記管理系統）
* **技術棧**：原生 HTML/CSS/JS (ES6 Module) + Firebase Firestore Database + GitHub Pages 靜態託管。
* **主要 JSON 設定檔 (位於 `json/`)**：
  * `group.json`：團體清單。
  * `members_skz.json` / `members_atz.json`：成員排序唯一基準。
  * `bank_info.json` / `banks.json`：收款與匯款銀行清單。

---

## 📂 二、 常用路徑與核心目錄樹 (Directory Structure)

專案已高度模組化，請精準辨識各個子系統的獨立資料夾：

* **根目錄 (`/`)**
  * `index.html`：前台入口 (7 大 Tab 主選單)。
  * `admin.html`：後台控制台入口。
  * `orders_form.html`：團員登記填單表單。
  * `orders_manage.html`：團員登記管理與發圖。

* **中信財務結算系統 (`ctbc/`)** 👉 *近期重點開發區域*
  * `index.html`：中信對帳系統的主框架 (包含分頁切換膠囊)。
  * `ctbc_bank_table.html`：[子分頁 1] 建立結算單與匯入中信 PDF 進行勾選對帳。
  * `ctbc_bills_list.html`：[子分頁 2] 自動財務結算一覽表 (雙欄買家卡片、成員分組、退款、外部結算)。
  * `ctbc_data.js`：中信 PDF 解析出來的靜態明細資料。

* **前台功能頁面 (`index/`)**
  * `index_progress.html`：開團與進度 (進行中)。
  * `index_records.html`：登記與對帳查詢 (三層嚴格排序、動態隱藏已結束)。
  * `index_deposit_app.html`：帳戶儲值與退款中心。
  * `index_stock.html`：歷年現貨圖包認領 (含成員分區、灰階售完狀態)。

* **後台管理頁面 (`admin/`)**
  * `admin_events.html` / `admin_progress.html`：活動與進度管理。
  * `admin_payments.html`：匯款對帳審核總控台 (內嵌 iframe)。
  * `payment/` (匯款審核子頁面)：`payment_all.html`, `payment_pending.html` 等。

---

## 🎨 三、 核心邏輯與動態資料機制

1. **四層膠囊篩選器 (全站通用)**：
   - 篩選標準流：`[1. 團體]` ➔ `[2. 檢視模式(依成員/依活動)]` ➔ `[3. 細項篩選]` ➔ `[4. 買家暱稱]`。
   - 所有細項與買家膠囊，必須依據「當前過濾後的資料」**動態生成**，不盲目渲染空資料。

2. **財務對帳機制 (中信 CTBC 系統)**：
   - **對帳邏輯**：摒棄總額黑洞，採用「勾選特定帳單核銷」並自動試算溢繳/尚欠。
   - **狀態防呆標籤**：`📌 待匯款`、`🔍 待對帳`、`⚠️ 待補款`、`✅ 已對帳結清`、`✔ 全外部結帳`。
   - **灰階封存**：當買家卡片的「尚欠金額 ≤ 0」時，卡片透明度降低、轉灰階，並自動沉降至畫面最底部的封存區塊。
   - **容錯機制**：任何對帳與填單，必須具備 `[✏️ 編輯]` 與 `[🔓 撤銷綁定]` 功能。

3. **使用者資料來源**：
   - 全面廢除靜態 JSON，買家名單與代拍廠商一律即時監聽 Firestore (`users`, `sellers` 集合)。

---

## 📝 四、 開發變更日誌 (Change Log)

### 2026-08-20 (資料庫重構收尾)
* 廢除靜態 JSON 依賴，改接 Firestore `users` 與 `sellers`。
* 重構 `index/index_records.html`，實裝三層嚴格排序（活動日期 ➔ 團體 ➔ 官方成員順序）。

### 2026-08-23 (CTBC 中信財務系統模組化與極致升級)
1. **目錄拆分**：將原 `admin_ctbc_bank.html` 移至獨立目錄 `ctbc/`，並拆分為 `index.html` (框架), `ctbc_bank_table.html` (對帳), `ctbc_bills_list.html` (管理)。
2. **建檔區優化**：送出後 100% 清空表單；實裝精準勾選對帳機制，自動試算餘額。
3. **一覽表大改版**：
   * 導入四層膠囊篩選器取代傳統搜尋框。
   * 實裝買家專屬卡片，外層採 Grid 雙欄排版。
   * 實裝內部明細「依官方成員順序分組」、「依活動名稱排序」。
   * 實裝四大狀態智慧判定、溢繳退款登記、全局防雷備註、一鍵匯出 Excel。
   * 實裝結算完畢卡片自動灰階並下沉至封存區功能。
   