// Progressive enhancement: only the engine table is filtered.
const filters = document.querySelector('.subset-filters');
const rows = document.querySelectorAll('#engine-table tbody tr');
if (filters && rows.length) {
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-subset]');
    if (!button || !filters.contains(button)) return;
    filters.querySelectorAll('button').forEach(item => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    rows.forEach(row => {
      row.hidden = button.dataset.subset !== 'all' && row.cells[0].textContent !== button.dataset.subset;
    });
  });
}
