async function loadRollData() {
  if (window.rollData) return window.rollData;
  const response = await fetch('data/rolls.json');
  if (!response.ok) {
    throw new Error('無法讀取肉桂捲資料');
  }
  const data = await response.json();
  window.rollData = data;
  return data;
}

function formatBadgeValue(value) {
  return value && value !== '·' ? value : '';
}

function buildRollCard(record, headers) {
  const card = document.createElement('article');
  card.className = 'roll-card';

  const image = document.createElement('img');
  image.loading = 'lazy';
  image.alt = record._title;
  const imageSrc = record[headers[10]];
  image.src = imageSrc || 'https://via.placeholder.com/200x200?text=Cinnamon+Roll';
  card.appendChild(image);

  const meta = document.createElement('div');
  meta.className = 'roll-meta';

  const title = document.createElement('h3');
  title.className = 'roll-title';
  const detailLink = document.createElement('a');
  detailLink.href = `roll.html?id=${record._id}`;
  detailLink.textContent = record._title;
  title.appendChild(detailLink);
  meta.appendChild(title);

  const badges = document.createElement('div');
  badges.className = 'badges';

  const rating = formatBadgeValue(record[headers[2]]);
  const reviews = formatBadgeValue(record[headers[3]]);
  const status = formatBadgeValue(record[headers[6]]);
  const category = formatBadgeValue(record[headers[4]]);

  [rating && `⭐️ ${rating}`, reviews, status, category].forEach((value) => {
    if (!value) return;
    const badge = document.createElement('span');
    badge.className = 'badge';
    badge.textContent = value;
    badges.appendChild(badge);
  });

  if (badges.children.length) {
    meta.appendChild(badges);
  }

  const address = formatBadgeValue(record[headers[5]]);
  if (address) {
    const addressEl = document.createElement('p');
    addressEl.className = 'roll-address';
    addressEl.textContent = address;
    meta.appendChild(addressEl);
  }

  const phone = formatBadgeValue(record[headers[9]]);
  if (phone) {
    const phoneEl = document.createElement('p');
    phoneEl.className = 'roll-address';
    phoneEl.textContent = `電話：${phone}`;
    meta.appendChild(phoneEl);
  }

  card.appendChild(meta);
  return card;
}

async function renderIndex() {
  const list = document.getElementById('roll-list');
  const searchInput = document.getElementById('search');
  const { headers, rows } = await loadRollData();

  function filterRows(keyword) {
    const query = keyword.trim().toLowerCase();
    if (!query) return rows;
    return rows.filter((item) => {
      return (
        item._title.toLowerCase().includes(query) ||
        (item[headers[5]] || '').toLowerCase().includes(query) ||
        (item[headers[4]] || '').toLowerCase().includes(query)
      );
    });
  }

  function render(data) {
    list.innerHTML = '';
    if (!data.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = '沒有符合搜尋的肉桂捲，換個關鍵字試試看吧！';
      list.appendChild(empty);
      return;
    }

    data.forEach((record) => {
      const card = buildRollCard(record, headers);
      list.appendChild(card);
    });
  }

  render(rows);
  searchInput.addEventListener('input', (event) => {
    render(filterRows(event.target.value));
  });
}

async function renderDetail() {
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  const container = document.getElementById('roll-detail');
  const { headers, rows } = await loadRollData();
  const record = rows.find((item) => item._id === id);

  if (!record) {
    container.innerHTML = '<div class="empty-state">找不到指定的肉桂捲，請回到首頁查看列表。</div>';
    return;
  }

  const hero = document.createElement('section');
  hero.className = 'details roll-hero';

  const info = document.createElement('div');
  const title = document.createElement('h2');
  title.textContent = record._title;
  info.appendChild(title);

  const actions = document.createElement('div');
  actions.className = 'badges';

  const mapUrl = record[headers[0]];
  if (mapUrl) {
    const link = document.createElement('a');
    link.href = mapUrl;
    link.className = 'badge';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = '查看地圖';
    actions.appendChild(link);
  }

  const orderLink = record[headers[13]];
  if (orderLink) {
    const link = document.createElement('a');
    link.href = orderLink;
    link.className = 'badge';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = '線上訂購';
    actions.appendChild(link);
  }

  if (actions.children.length) {
    info.appendChild(actions);
  }

  const metaList = document.createElement('ul');
  metaList.className = 'meta-list';

  const metaFields = [
    [headers[4], record[headers[4]]],
    ['地址', record[headers[5]]],
    ['營業狀態', record[headers[6]]],
    ['電話', record[headers[9]]],
    ['評分', record[headers[2]]],
    ['評論數', record[headers[3]]],
  ];

  metaFields.forEach(([label, value]) => {
    if (!value) return;
    const item = document.createElement('li');
    item.className = 'meta-item';
    const labelEl = document.createElement('span');
    labelEl.className = 'meta-label';
    labelEl.textContent = label;
    const valueEl = document.createElement('span');
    valueEl.className = 'meta-value';
    valueEl.textContent = value;
    item.appendChild(labelEl);
    item.appendChild(valueEl);
    metaList.appendChild(item);
  });

  if (metaList.children.length) {
    info.appendChild(metaList);
  }

  hero.appendChild(info);

  const heroImage = document.createElement('img');
  heroImage.alt = record._title;
  heroImage.src = record[headers[10]] || 'https://via.placeholder.com/640x360?text=Cinnamon+Roll';
  hero.appendChild(heroImage);

  container.appendChild(hero);

  const tableWrapper = document.createElement('section');
  tableWrapper.className = 'details';
  const tableTitle = document.createElement('h3');
  tableTitle.textContent = '原始欄位資料';
  tableWrapper.appendChild(tableTitle);

  const table = document.createElement('table');
  table.className = 'data-table';
  const tbody = document.createElement('tbody');

  headers.forEach((header) => {
    const value = record[header];
    if (!value) return;
    const row = document.createElement('tr');
    const th = document.createElement('th');
    th.textContent = header;
    const td = document.createElement('td');
    td.textContent = value;
    row.appendChild(th);
    row.appendChild(td);
    tbody.appendChild(row);
  });

  table.appendChild(tbody);
  tableWrapper.appendChild(table);
  container.appendChild(tableWrapper);
}

window.addEventListener('DOMContentLoaded', () => {
  if (document.body.dataset.page === 'index') {
    renderIndex().catch((error) => {
      document.getElementById('roll-list').innerHTML = `<div class="empty-state">${error.message}</div>`;
    });
  }

  if (document.body.dataset.page === 'detail') {
    renderDetail().catch((error) => {
      document.getElementById('roll-detail').innerHTML = `<div class="empty-state">${error.message}</div>`;
    });
  }
});
