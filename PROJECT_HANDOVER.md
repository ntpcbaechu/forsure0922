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

5. **成員排序鐵律**：
   - 無論哪個頁面渲染成員，**嚴格遵循 `members_skz.json` / `members_atz.json` 原始陣列順序**，絕不自動按 Alphabet 排序。

---

## 🎨 三、 核心邏輯與篩選架構

1. **全站雙區域膠囊篩選與動態 IF 機制**：
   - **區域 A（團體與場次細分）**：
     - 第一層：`[Stray Kids]` / `[ATEEZ]` 膠囊切換。
     - 第二層：`[依成員]` / `[依活動]` 檢視模式切換。
     - 第三層：動態細項膠囊（**動態 IF 條件：下方明細中真的有資料才渲染**）。
   - **區域 B（社群暱稱獨立篩選）**：
     - 買家暱稱膠囊（**動態 IF 條件：當前篩選下真的有喊單才渲染**）。

2. **`index_records.html` 雙檢視呈現模式**：
   - **全站/多買家檢視**：按活動場次區分，採緊湊表格展示。
   - **單一買家獨立檢視**：頂部顯示**彩色高對比個人統計卡**（大字區分「應付總額」、「已對帳付清」、「待匯款金額」），下方接該買家全表緊湊明細。
   - **🚨 僅顯示待匯款模式**：採**「按買家暱稱分組歸戶」**，小卡標頭帶出該買家欠款總額與明細。

3. **`index_deposit_app.html` 銀行連動**：
   - 選擇台銀、樂天、中信時，下方即時自動彈出黃色提示框，帶出 `bank_info.json` 的對應轉帳帳號。

---

## 📂 四、 完整檔案樹狀圖 (PROJECT STRUCTURE)

* `/forsure0922`
  * `index.html` (前台總控與 Tab 主選單)
  * `admin.html` (後台總控控制台)
  * `orders_form.html` (團員登記填單表單)
  * `orders_manage.html` (團員登記管理與一鍵發圖)
  * `deposit.html` (存款交易明細對帳表)
  * `PROJECT_HANDOVER.md` (專案極詳細交接與記憶文件)
  * `index/` (前台功能頁面)
    * `index_progress.html` (開團與進度)
    * `index_notice.html` (注意事項)
    * `index_payment.html` (匯款表單)
    * `index_records.html` (登記與對帳查詢 - 待匯款暱稱歸戶 + 彩色統計卡)
    * `index_deposit_app.html` (帳戶儲值與退款中心 - 自動帶出銀行帳號)
    * `index_lottery.html` (抽獎結果公告)
  * `admin/` (後台管理頁面)
    * `admin_events.html` (活動單價與成本設定)
    * `admin_progress.html` (發佈與更新發圖進度)
    * `admin_lottery.html` (抽獎活動管理)
    * `admin_deposit.html` (預存儲值與抵用金管理)
    * `admin_payments.html` (匯款對帳審核總控台)
    * `admin_ctbc_bank.html` (中信存款交易明細對帳系統)
    * `payment/` (匯款審核 4 大子頁面)
      * `payment_pending.html` (未對帳)
      * `payment_ok.html` (已對帳 - 自動連動扣款)
      * `payment_error.html` (帳有問題)
      * `payment_photosent.html` (已發圖專區)
  * `json/` (系統靜態設定檔)
    * `group.json` / `members_skz.json` / `members_atz.json` / `users.json` / `bank_info.json` / `banks.json` / `sellers.json`
