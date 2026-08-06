# 🚀 專案記憶與交接文件 (PROJECT_HANDOVER)

## 📌 一、 專案核心介紹與架構
* 專案名稱：forsure0922（飯拍與周邊團購登記管理系統）
* 技術棧：原生 HTML/CSS/JS (ES6 Module) + Firebase Firestore Database + GitHub Pages 靜態託管。
* 主要 JSON 設定檔：
  - json/group.json：團體清單（Stray Kids、ATEEZ）。
  - json/members_skz.json：Stray Kids 成員陣列（嚴格維持 JSON 原始順序，絕不自動排序）。
  - json/members_atz.json：ATEEZ 成員陣列（嚴格維持 JSON 原始順序，絕不自動排序）。
  - json/users.json：社群買家暱稱名單。

---

## 🎨 二、 前後台統一「雙區域膠囊篩選」架構
全站（除 Deposit 儲值金系列頁面外）統一篩選規則：
- 區域 A（團體與場次細分）：
  1. 第一層：[Stray Kids] / [ATEEZ] 膠囊切換。
  2. 第二層：[依成員] / [依活動] 模式切換。
  3. 第三層：動態細項膠囊（成員依 JSON 原始順序排列）。
- 區域 B（社群暱稱獨立篩選）：
  - 買家暱稱獨立膠囊，按 A-Z、0-9 系統順序排列。

---

## 📂 三、 已重構與維護的 HTML 檔案清單
1. 核心元件與表單：
   - orders_form.html：限制 max-width: 600px 置中。
   - orders_manage.html：修復 $0 金額 BUG（即時連動 event_settings 計算總價）；新增高對比彩色狀態標籤。
2. 後台管理頁面（已套用雙區域篩選）：
   - admin/admin_events.html
   - admin/admin_progress.html
   - admin/admin_lottery.html
3. 前台查詢頁面（已套用雙區域篩選 + Doc ID 去重）：
   - index/index_progress.html
   - index/index_records.html
   - index/index_lottery.html
4. 獨立邏輯頁面（保持現狀）：
   - deposit.html / admin/admin_deposit.html / index/index_deposit_app.html

---

## 🤝 四、 相處模式與溝通默契
1. 拒絕廢話與無意義讚美，直接給方案。
2. 務實且嚴謹排查，不盲目猜測。
3. 成員排序鐵律：所有頁面列出成員時，絕對嚴格遵循 members_skz.json / members_atz.json 的原始陣列順序。
