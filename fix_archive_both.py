import os

# 1. 歷年開團進度歸檔 HTML
progress_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <title>歷年開團進度歸檔</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 0; margin: 0; background: transparent; color: #333; }
    
    .filter-card { background: #fff; border: 1px solid #e4e7ed; border-radius: 12px; padding: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 8px; }
    .filter-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
    .filter-label { font-size: 12px; font-weight: bold; color: #606266; min-width: 80px; }

    .capsule-group { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .capsule-filter-btn { background: #f4f4f5; color: #606266; border: 1px solid #dcdfe6; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: bold; cursor: pointer; transition: all 0.2s; outline: none; }
    .capsule-filter-btn:hover { background: #ecf5ff; color: #409eff; border-color: #c6e2ff; }
    .capsule-filter-btn.active { background: #409eff; color: #fff; border-color: #409eff; box-shadow: 0 2px 6px rgba(64,158,255,0.25); }
    .capsule-filter-btn.sub-active { background: #e6a23c; color: #fff; border-color: #e6a23c; box-shadow: 0 2px 6px rgba(230,162,60,0.25); }

    /* 強制寫死 3 欄式，防止單一卡片拉寬 */
    #progressList { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; align-items: start; }
    @media (max-width: 900px) { #progressList { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 600px) { #progressList { grid-template-columns: 1fr; } }

    .event-group-card { background: #fff; border: 1px solid #e4e7ed; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.02); display: flex; flex-direction: column; }
    .event-group-header { background: #f4f4f5; border-left: 4px solid #909399; color: #606266; font-size: 15px; font-weight: bold; padding: 10px 14px; display: flex; align-items: center; gap: 6px; }

    .progress-list-box { padding: 12px 14px; display: flex; flex-direction: column; gap: 12px; }
    .member-block { display: flex; flex-direction: column; gap: 6px; border-bottom: 1px dashed #ebeef5; padding-bottom: 10px; }
    .member-block:last-child { border-bottom: none; padding-bottom: 0; }

    .member-box-card { background: #f8f9fa; border: 1px solid #e4e7ed; border-radius: 8px; padding: 8px 12px; display: flex; flex-direction: column; gap: 4px; }
    .member-header-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; font-weight: bold; color: #303133; }
    .buyer-row { display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #606266; padding-left: 12px; margin-top: 2px; }
    .buyer-status-group { display: flex; align-items: center; gap: 6px; }

    .status-badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; white-space: nowrap; }
    .status-done { background: #f4f4f5; color: #909399; border: 1px solid #e4e7ed; }
  </style>
</head>
<body>

  <div class="filter-card">
    <div class="filter-row">
      <span class="filter-label">1. 團體：</span>
      <div id="groupCapsules" class="capsule-group"></div>
    </div>

    <div class="filter-row">
      <span class="filter-label">2. 檢視模式：</span>
      <div id="modeCapsules" class="capsule-group">
        <button class="capsule-filter-btn active" onclick="setModeFilter('member', this)">👥 依成員</button>
        <button class="capsule-filter-btn" onclick="setModeFilter('event', this)">🗓️ 依活動</button>
      </div>
    </div>

    <div class="filter-row">
      <span class="filter-label">3. 細項篩選：</span>
      <div id="detailCapsules" class="capsule-group"></div>
    </div>

    <div class="filter-row">
      <span class="filter-label">👤 買家暱稱：</span>
      <div id="buyerCapsules" class="capsule-group"></div>
    </div>
  </div>

  <div id="progressList">載入中...</div>

  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
    import { getFirestore, collection, onSnapshot } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

    const firebaseConfig = {
      apiKey: "AIzaSyDF7QySG1Jj4gdZvXwMRaKjRmI-lFKpj7k",
      authDomain: "forsure0922.firebaseapp.com",
      databaseURL: "https://forsure0922-default-rtdb.firebaseio.com",
      projectId: "forsure0922",
      storageBucket: "forsure0922.firebasestorage.app",
      messagingSenderId: "817449290174",
      appId: "1:817449290174:web:6b4ec1d36c171ff97011ef"
    };

    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);

    let rawProgress = [];
    let ordersCache = {};
    
    let activeGroup = 'Stray Kids';
    let activeMode = 'member';
    let activeDetail = 'ALL';
    let activeBuyer = 'ALL';

    let groupList = [];
    let memberMap = {};

    document.addEventListener('DOMContentLoaded', async () => {
      try {
        let basePath = location.pathname.includes('/archive/') ? '../../json/' : '../json/';
        const gRes = await fetch(basePath + 'group.json');
        groupList = await gRes.json();

        for (const g of groupList) {
          const file = (g === 'Stray Kids') ? 'members_skz.json' : (g === 'ATEEZ' ? 'members_atz.json' : '');
          if (file) {
            const mRes = await fetch(basePath + file);
            memberMap[g] = await mRes.json();
          }
        }
      } catch(e) {}

      renderGroupCapsules();

      onSnapshot(collection(db, "orders"), snap => {
        ordersCache = {};
        snap.forEach(d => { ordersCache[d.id] = { id: d.id, ...d.data(), group: d.data().group || 'Stray Kids' }; });
        updateDetailCapsules();
        renderView();
      });

      onSnapshot(collection(db, "photo_progress"), snap => {
        rawProgress = [];
        snap.forEach(d => {
          const data = d.data();
          if (data.status === '已結束' || data.status === '到期/已刪除') {
            rawProgress.push({ id: d.id, group: 'Stray Kids', ...data });
          }
        });
        updateDetailCapsules();
        renderView();
      });
    });

    function renderGroupCapsules() {
      const container = document.getElementById('groupCapsules');
      container.innerHTML = '';
      groupList.forEach(g => {
        const btn = document.createElement('button');
        btn.className = `capsule-filter-btn ${activeGroup === g ? 'active' : ''}`;
        btn.textContent = g;
        btn.onclick = () => {
          activeGroup = g;
          document.querySelectorAll('#groupCapsules .capsule-filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeDetail = 'ALL';
          activeBuyer = 'ALL';
          updateDetailCapsules();
          renderView();
        };
        container.appendChild(btn);
      });
    }

    window.setModeFilter = (mode, btn) => {
      activeMode = mode;
      document.querySelectorAll('#modeCapsules .capsule-filter-btn').forEach(b => b.classList.remove('active'));
      if(btn) btn.classList.add('active');
      activeDetail = 'ALL';
      activeBuyer = 'ALL';
      updateDetailCapsules();
      renderView();
    };

    function updateDetailCapsules() {
      const container = document.getElementById('detailCapsules');
      container.innerHTML = '';

      const allBtn = document.createElement('button');
      allBtn.className = `capsule-filter-btn ${activeDetail === 'ALL' ? 'active' : ''}`;
      allBtn.textContent = '全部顯示';
      allBtn.onclick = () => {
        activeDetail = 'ALL';
        activeBuyer = 'ALL';
        updateDetailCapsules();
        renderView();
      };
      container.appendChild(allBtn);

      const filteredProgress = rawProgress.filter(i => i.group === activeGroup);

      if (activeMode === 'member') {
        const membersInJson = memberMap[activeGroup] || [];
        const activeMembers = new Set(filteredProgress.map(i => i.member).filter(Boolean));

        membersInJson.forEach(m => {
          if (activeMembers.has(m)) {
            const btn = document.createElement('button');
            btn.className = `capsule-filter-btn ${activeDetail === m ? 'active' : ''}`;
            btn.textContent = m;
            btn.onclick = () => {
              activeDetail = m;
              activeBuyer = 'ALL';
              updateDetailCapsules();
              renderView();
            };
            container.appendChild(btn);
          }
        });
      } else {
        const eventsSet = new Set(filteredProgress.map(i => i.eventName || i.event).filter(Boolean));
        Array.from(eventsSet).sort().forEach(ev => {
          const btn = document.createElement('button');
          btn.className = `capsule-filter-btn ${activeDetail === ev ? 'active' : ''}`;
          btn.textContent = ev;
          btn.onclick = () => {
            activeDetail = ev;
            activeBuyer = 'ALL';
            updateDetailCapsules();
            renderView();
          };
          container.appendChild(btn);
        });
      }

      updateBuyerCapsules();
    }

    /* 從當前符合條件的訂單中，擷取買家暱稱並去除前綴符號 */
    function updateBuyerCapsules() {
      const container = document.getElementById('buyerCapsules');
      container.innerHTML = '';

      const buyersSet = new Set();
      Object.values(ordersCache).forEach(ord => {
        if (ord.group === activeGroup) {
          const eName = ord.event || ord.eventName;
          const mName = ord.member;

          if (activeDetail !== 'ALL') {
            if (activeMode === 'member' && mName !== activeDetail) return;
            if (activeMode === 'event' && eName !== activeDetail) return;
          }

          let rawName = ord.buyerName || ord.user || ord.nickname || '';
          let cleanName = rawName.replace(/^[-\s]+/, '').trim();
          if (cleanName) buyersSet.add(cleanName);
        }
      });

      const allBtn = document.createElement('button');
      allBtn.className = `capsule-filter-btn ${activeBuyer === 'ALL' ? 'sub-active' : ''}`;
      allBtn.textContent = '全部買家';
      allBtn.onclick = () => {
        activeBuyer = 'ALL';
        document.querySelectorAll('#buyerCapsules .capsule-filter-btn').forEach(b => b.classList.remove('sub-active'));
        allBtn.classList.add('sub-active');
        renderView();
      };
      container.appendChild(allBtn);

      Array.from(buyersSet).sort().forEach(bName => {
        const btn = document.createElement('button');
        btn.className = `capsule-filter-btn ${activeBuyer === bName ? 'sub-active' : ''}`;
        btn.textContent = bName;
        btn.onclick = () => {
          activeBuyer = bName;
          document.querySelectorAll('#buyerCapsules .capsule-filter-btn').forEach(b => b.classList.remove('sub-active'));
          btn.classList.add('sub-active');
          renderView();
        };
        container.appendChild(btn);
      });
    }

    function renderView() {
      const container = document.getElementById('progressList');
      container.innerHTML = '';

      let list = rawProgress.filter(i => i.group === activeGroup);

      if (activeDetail !== 'ALL') {
        if (activeMode === 'member') list = list.filter(i => i.member === activeDetail);
        else if (activeMode === 'event') list = list.filter(i => (i.eventName || i.event) === activeDetail);
      }

      if (list.length === 0) {
        container.innerHTML = '<p style="color:#909399; font-size:14px; grid-column: 1 / -1;">目前尚無符合條件的歸檔紀錄。</p>';
        notifyHeight();
        return;
      }

      const eventGroups = {};
      list.forEach(item => {
        const eTitle = item.eventName || item.event || '未命名活動';
        if (!eventGroups[eTitle]) eventGroups[eTitle] = [];
        eventGroups[eTitle].push(item);
      });

      let htmlContent = '';
      const currentMemberList = memberMap[activeGroup] || [];

      Object.keys(eventGroups).sort().forEach(eventName => {
        const items = eventGroups[eventName];

        items.sort((a, b) => {
          let idxA = currentMemberList.indexOf(a.member || '');
          let idxB = currentMemberList.indexOf(b.member || '');
          return (idxA === -1 ? 99 : idxA) - (idxB === -1 ? 99 : idxB);
        });

        const memberMapObj = {};
        items.forEach(item => {
          const m = item.member || '全體';
          if (!memberMapObj[m]) memberMapObj[m] = [];
          memberMapObj[m].push(item);
        });

        let membersHtml = '';

        Object.keys(memberMapObj).forEach(mName => {
          const mItems = memberMapObj[mName];

          let buyersHtml = '';
          Object.values(ordersCache).forEach(ord => {
            if (ord.group === activeGroup && (ord.event || ord.eventName) === eventName && ord.member === mName) {
              let rawName = ord.buyerName || ord.user || ord.nickname || '';
              let cleanName = rawName.replace(/^[-\s]+/, '').trim();

              if (activeBuyer === 'ALL' || activeBuyer === cleanName) {
                if (cleanName) {
                  buyersHtml += `
                    <div class="buyer-row">
                      <span>- ${cleanName}</span>
                      <div class="buyer-status-group">
                        <span class="status-badge status-done">⚫ 已結案</span>
                        <span class="status-badge status-done">⚪ 已發圖</span>
                      </div>
                    </div>
                  `;
                }
              }
            }
          });

          if (activeBuyer !== 'ALL' && !buyersHtml) return;

          const st = mItems[0].status || '已結束';

          membersHtml += `
            <div class="member-block">
              <div class="member-box-card">
                <div class="member-header-row">
                  <span>👤 ${mName}</span>
                  <span class="status-badge status-done">${st}</span>
                </div>
              </div>
              ${buyersHtml}
            </div>
          `;
        });

        if (membersHtml) {
          htmlContent += `
            <div class="event-group-card">
              <div class="event-group-header">📦 [${activeGroup}] ${eventName} (已歸檔)</div>
              <div class="progress-list-box">${membersHtml}</div>
            </div>
          `;
        }
      });

      container.innerHTML = htmlContent || '<p style="color:#909399; font-size:14px; grid-column: 1 / -1;">目前尚無符合條件的歸檔紀錄。</p>';
      notifyHeight();
    }

    function notifyHeight() {
      setTimeout(() => {
        window.parent.postMessage({ frameHeight: document.body.scrollHeight }, '*');
      }, 100);
    }
  </script>
</body>
</html>'''


# 2. 歷年喊單與對帳紀錄歸檔 HTML
records_html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <title>歷年喊單與對帳紀錄歸檔</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 0; margin: 0; background: transparent; color: #333; }
    
    .filter-card { background: #fff; border: 1px solid #e4e7ed; border-radius: 12px; padding: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 8px; }
    .filter-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
    .filter-label { font-size: 12px; font-weight: bold; color: #606266; min-width: 80px; }

    .capsule-group { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
    .capsule-filter-btn { background: #f4f4f5; color: #606266; border: 1px solid #dcdfe6; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: bold; cursor: pointer; transition: all 0.2s; outline: none; }
    .capsule-filter-btn:hover { background: #ecf5ff; color: #409eff; border-color: #c6e2ff; }
    .capsule-filter-btn.active { background: #409eff; color: #fff; border-color: #409eff; box-shadow: 0 2px 6px rgba(64,158,255,0.25); }
    .capsule-filter-btn.sub-active { background: #e6a23c; color: #fff; border-color: #e6a23c; box-shadow: 0 2px 6px rgba(230,162,60,0.25); }

    .compact-table-card { background: #fff; border: 1px solid #e4e7ed; border-radius: 12px; padding: 14px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
    table.compact-records-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    table.compact-records-table th, table.compact-records-table td { padding: 10px 8px; border-bottom: 1px solid #ebeef5; text-align: left; vertical-align: middle; }
    table.compact-records-table th { background: #f8f9fa; color: #606266; font-weight: bold; white-space: nowrap; }

    /* 強制寫死 2 欄式，防止單一卡片拉寬 */
    #recordsListGrid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; align-items: start; }
    @media (max-width: 768px) { #recordsListGrid { grid-template-columns: 1fr; } }

    .event-section { background: #fff; border: 1px solid #e4e7ed; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); display: flex; flex-direction: column; }
    .event-header { font-size: 15px; font-weight: bold; color: #303133; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f2f5; padding-bottom: 8px; }
    .event-meta { font-size: 12px; color: #909399; background: #f4f4f5; padding: 4px 8px; border-radius: 6px; font-weight: bold; }

    .status-badge { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; display: inline-block; white-space: nowrap; }
    .status-paid { background: #f0f9eb; color: #67c23a; border: 1px solid #e1f3d8; }
    .photo-badge-sent { background: #f4f4f5; color: #909399; border: 1px solid #e4e7ed; }
  </style>
</head>
<body>

  <div class="filter-card">
    <div class="filter-row">
      <span class="filter-label">1. 團體：</span>
      <div id="groupCapsules" class="capsule-group"></div>
    </div>

    <div class="filter-row">
      <span class="filter-label">2. 檢視模式：</span>
      <div id="modeCapsules" class="capsule-group">
        <button class="capsule-filter-btn active" onclick="setModeFilter('member', this)">👥 依成員</button>
        <button class="capsule-filter-btn" onclick="setModeFilter('event', this)">🗓️ 依活動</button>
      </div>
    </div>

    <div class="filter-row">
      <span class="filter-label">3. 細項篩選：</span>
      <div id="detailCapsules" class="capsule-group"></div>
    </div>

    <div class="filter-row">
      <span class="filter-label">👤 買家暱稱：</span>
      <div id="buyerCapsules" class="capsule-group"></div>
    </div>
  </div>

  <div id="recordsList">載入中...</div>

  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
    import { getFirestore, collection, onSnapshot } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

    const firebaseConfig = {
      apiKey: "AIzaSyDF7QySG1Jj4gdZvXwMRaKjRmI-lFKpj7k",
      authDomain: "forsure0922.firebaseapp.com",
      databaseURL: "https://forsure0922-default-rtdb.firebaseio.com",
      projectId: "forsure0922",
      storageBucket: "forsure0922.firebasestorage.app",
      messagingSenderId: "817449290174",
      appId: "1:817449290174:web:6b4ec1d36c171ff97011ef"
    };

    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);

    let allOrders = [];
    let progressMap = {};
    let eventSettingsMap = {};

    let activeGroup = 'Stray Kids';
    let activeMode = 'member';
    let activeDetail = 'ALL';
    let activeBuyer = 'ALL';

    let groupList = [];
    let memberMap = {};

    document.addEventListener('DOMContentLoaded', async () => {
      try {
        let basePath = location.pathname.includes('/archive/') ? '../../json/' : '../json/';
        const gRes = await fetch(basePath + 'group.json');
        groupList = await gRes.json();

        for (const g of groupList) {
          const file = (g === 'Stray Kids') ? 'members_skz.json' : (g === 'ATEEZ' ? 'members_atz.json' : '');
          if (file) {
            const mRes = await fetch(basePath + file);
            memberMap[g] = await mRes.json();
          }
        }
      } catch(e) {}

      renderGroupCapsules();

      onSnapshot(collection(db, "photo_progress"), snap => {
        progressMap = {};
        snap.forEach(d => {
          const data = d.data();
          const key = (data.eventName || data.event || '') + '_' + (data.member || '');
          progressMap[key] = data.status || '';
        });
        updateDetailCapsules();
        renderRecords();
      });

      onSnapshot(collection(db, "event_settings"), snap => {
        eventSettingsMap = {};
        snap.forEach(d => {
          const data = d.data();
          const key = (data.name || data.rawName) + '_' + (data.member || '');
          eventSettingsMap[key] = {
            price: Number(data.actualPrice || data.price || data.estimatedPrice || data.unitPrice) || 0,
            packQty: Number(data.packQty) || 1,
            actVideo: Number(data.actVideo) || 0
          };
        });
        renderRecords();
      });

      onSnapshot(collection(db, "orders"), snap => {
        const ordersMap = new Map();
        snap.forEach(d => {
          const data = d.data();
          ordersMap.set(d.id, { id: d.id, ...data, group: data.group || "Stray Kids" });
        });
        allOrders = Array.from(ordersMap.values());
        updateDetailCapsules();
        renderRecords();
      });
    });

    function isArchivedOrder(ord) {
      const key = (ord.event || ord.eventName || '') + '_' + (ord.member || '');
      const st = progressMap[key] || '';
      return st === '已結束' || st === '到期/已刪除';
    }

    function renderGroupCapsules() {
      const container = document.getElementById('groupCapsules');
      container.innerHTML = '';
      groupList.forEach(g => {
        const btn = document.createElement('button');
        btn.className = `capsule-filter-btn ${activeGroup === g ? 'active' : ''}`;
        btn.textContent = g;
        btn.onclick = () => {
          activeGroup = g;
          document.querySelectorAll('#groupCapsules .capsule-filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          activeDetail = 'ALL';
          activeBuyer = 'ALL';
          updateDetailCapsules();
          renderRecords();
        };
        container.appendChild(btn);
      });
    }

    window.setModeFilter = (mode, btn) => {
      activeMode = mode;
      document.querySelectorAll('#modeCapsules .capsule-filter-btn').forEach(b => b.classList.remove('active'));
      if(btn) btn.classList.add('active');
      activeDetail = 'ALL';
      activeBuyer = 'ALL';
      updateDetailCapsules();
      renderRecords();
    };

    function updateDetailCapsules() {
      const container = document.getElementById('detailCapsules');
      container.innerHTML = '';

      const allBtn = document.createElement('button');
      allBtn.className = `capsule-filter-btn ${activeDetail === 'ALL' ? 'active' : ''}`;
      allBtn.textContent = '全部顯示';
      allBtn.onclick = () => {
        activeDetail = 'ALL';
        activeBuyer = 'ALL';
        updateDetailCapsules();
        renderRecords();
      };
      container.appendChild(allBtn);

      const filtered = allOrders.filter(o => o.group === activeGroup && isArchivedOrder(o));

      if (activeMode === 'member') {
        const membersInJson = memberMap[activeGroup] || [];
        const activeMembersWithData = new Set(filtered.map(o => o.member).filter(Boolean));

        membersInJson.forEach(m => {
          if (activeMembersWithData.has(m)) {
            const btn = document.createElement('button');
            btn.className = `capsule-filter-btn ${activeDetail === m ? 'active' : ''}`;
            btn.textContent = m;
            btn.onclick = () => {
              activeDetail = m;
              activeBuyer = 'ALL';
              updateDetailCapsules();
              renderRecords();
            };
            container.appendChild(btn);
          }
        });
      } else if (activeMode === 'event') {
        const eventsSet = new Set();
        filtered.forEach(o => {
          if (o.event || o.eventName) eventsSet.add(o.event || o.eventName);
        });
        Array.from(eventsSet).sort().forEach(ev => {
          const btn = document.createElement('button');
          btn.className = `capsule-filter-btn ${activeDetail === ev ? 'active' : ''}`;
          btn.textContent = ev;
          btn.onclick = () => {
            activeDetail = ev;
            activeBuyer = 'ALL';
            updateDetailCapsules();
            renderRecords();
          };
          container.appendChild(btn);
        });
      }

      updateBuyerCapsules();
    }

    /* 從當前符合條件的歷史訂單中，擷取買家暱稱並去除前綴符號 */
    function updateBuyerCapsules() {
      const container = document.getElementById('buyerCapsules');
      container.innerHTML = '';

      const filtered = allOrders.filter(o => o.group === activeGroup && isArchivedOrder(o));
      const buyersSet = new Set();

      filtered.forEach(ord => {
        if (activeDetail !== 'ALL') {
          if (activeMode === 'member' && ord.member !== activeDetail) return;
          if (activeMode === 'event' && (ord.event || ord.eventName) !== activeDetail) return;
        }

        let rawName = ord.user || ord.buyerName || ord.nickname || '';
        let cleanName = rawName.replace(/^[-\s]+/, '').trim();
        if (cleanName) buyersSet.add(cleanName);
      });

      const allBtn = document.createElement('button');
      allBtn.className = `capsule-filter-btn ${activeBuyer === 'ALL' ? 'sub-active' : ''}`;
      allBtn.textContent = '全部買家';
      allBtn.onclick = () => {
        activeBuyer = 'ALL';
        document.querySelectorAll('#buyerCapsules .capsule-filter-btn').forEach(b => b.classList.remove('sub-active'));
        allBtn.classList.add('sub-active');
        renderRecords();
      };
      container.appendChild(allBtn);

      Array.from(buyersSet).sort().forEach(bName => {
        const btn = document.createElement('button');
        btn.className = `capsule-filter-btn ${activeBuyer === bName ? 'sub-active' : ''}`;
        btn.textContent = bName;
        btn.onclick = () => {
          activeBuyer = bName;
          document.querySelectorAll('#buyerCapsules .capsule-filter-btn').forEach(b => b.classList.remove('sub-active'));
          btn.classList.add('sub-active');
          renderRecords();
        };
        container.appendChild(btn);
      });
    }

    function getItemPriceAndUnit(item) {
      const eventName = item.event || item.eventName || '';
      const member = item.member || '';
      const key = eventName + '_' + member;
      const setting = eventSettingsMap[key] || {};
      
      const pricePerPack = setting.price || Number(item.price) || 0;
      const packQty = setting.packQty || 1;
      const qty = Number(item.quantity) || Number(item.qty) || 0;
      const packs = (packQty > 0) ? Math.round(qty / packQty) : 1;
      const totalPrice = packs * pricePerPack;

      const unitLabel = setting.actVideo > 0 ? '個' : '張';
      const qtyText = `${packs}包 (${qty}${unitLabel})`;

      return { totalPrice, qtyText };
    }

    function renderRecords() {
      const recordsList = document.getElementById('recordsList');
      recordsList.innerHTML = '';

      let list = allOrders.filter(o => o.group === activeGroup && isArchivedOrder(o));

      if (activeDetail !== 'ALL') {
        if (activeMode === 'member') list = list.filter(o => o.member === activeDetail);
        else if (activeMode === 'event') list = list.filter(o => (o.event || o.eventName) === activeDetail);
      }

      if (activeBuyer !== 'ALL') {
        list = list.filter(o => {
          let rawName = o.user || o.buyerName || o.nickname || '';
          let cleanName = rawName.replace(/^[-\s]+/, '').trim();
          return cleanName === activeBuyer;
        });
      }

      if (list.length === 0) {
        recordsList.innerHTML = '<p style="color:#909399; padding:20px 0; text-align:center;">目前無符合條件的歷史歸檔紀錄。</p>';
        notifyHeight();
        return;
      }

      const groups = {};
      list.forEach(o => {
        const key = `[${activeGroup}] ` + (o.event || o.eventName || '未分類活動') + (o.member ? ' - ' + o.member : '');
        if (!groups[key]) groups[key] = [];
        groups[key].push(o);
      });

      let gridHtml = '<div id="recordsListGrid">';
      for (const [title, listItems] of Object.entries(groups)) {
        const totalPacks = listItems.reduce((sum, item) => sum + (Number(item.quantity) || Number(item.qty) || 1), 0);

        let rowsHtml = '';
        listItems.forEach((ord, idx) => {
          let rawName = ord.user || ord.buyerName || ord.nickname || '未知';
          let cleanName = rawName.replace(/^[-\s]+/, '').trim();
          const info = getItemPriceAndUnit(ord);

          rowsHtml += `
            <tr>
              <td>#${idx + 1}</td>
              <td><b>${cleanName}</b></td>
              <td>${info.qtyText}</td>
              <td><b>$${info.totalPrice.toLocaleString()}</b></td>
              <td><span class="status-badge status-paid">🟢 已結案</span></td>
              <td><span class="status-badge photo-badge-sent">📦 歷史歸檔</span></td>
            </tr>
          `;
        });

        gridHtml += `
          <div class="event-section">
            <div class="event-header">
              <span>📦 ${title} (歷史歸檔)</span>
              <span class="event-meta">共 ${listItems.length} 筆 / ${totalPacks} 份</span>
            </div>
            <table class="compact-records-table">
              <thead>
                <tr>
                  <th style="width:5%;">#</th>
                  <th style="width:25%;">買家暱稱</th>
                  <th style="width:20%;">喊單數量</th>
                  <th style="width:15%;">小計</th>
                  <th style="width:15%;">對帳狀態</th>
                  <th style="width:20%;">發圖與歸檔狀態</th>
                </tr>
              </thead>
              <tbody>${rowsHtml}</tbody>
            </table>
          </div>
        `;
      }
      gridHtml += '</div>';
      recordsList.innerHTML = gridHtml;
      notifyHeight();
    }

    function notifyHeight() {
      setTimeout(() => {
        window.parent.postMessage({ frameHeight: document.body.scrollHeight }, '*');
      }, 200);
    }
  </script>
</body>
</html>'''

# 覆寫所有的目標路徑
files = {
    'index/archive/index_archive_progress.html': progress_html,
    'index/index_archive_progress.html': progress_html,
    'index/archive/index_archive_records.html': records_html,
    'index/index_archive_records.html': records_html
}

for path, content in files.items():
    if os.path.exists(os.path.dirname(path)):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ 已覆寫成功:", path)

