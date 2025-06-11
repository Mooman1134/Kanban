async function loadCards() {
  const res = await fetch('/api/cards');
  const cards = await res.json();
  displayCards(cards);
}

function displayCards(cards) {
  const tbody = document.querySelector('#card-table tbody');
  tbody.innerHTML = '';
  for (const c of cards) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${c.name}</td><td>${c.set_name}</td><td>$${c.price.toFixed(2)}</td>`;
    tr.addEventListener('click', () => loadHistory(c.id, c.name));
    tbody.appendChild(tr);
  }
  document.getElementById('search').addEventListener('input', e => {
    const term = e.target.value.toLowerCase();
    for (const row of tbody.rows) {
      const name = row.cells[0].textContent.toLowerCase();
      row.style.display = name.includes(term) ? '' : 'none';
    }
  });
}

async function loadHistory(cardId, name) {
  const res = await fetch(`/api/cards/${cardId}/history`);
  const history = await res.json();
  const labels = history.map(h => new Date(h.fetched_at).toLocaleDateString());
  const data = history.map(h => h.price);
  if (window.chart) window.chart.destroy();
  const ctx = document.getElementById('history-chart').getContext('2d');
  window.chart = new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: name, data, borderColor: 'red' }] },
    options: { responsive: true }
  });
}

loadCards();
