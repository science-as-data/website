(() => {
  const search = document.getElementById('arxiv-category-search');
  if (!search) return;
  const groups = [...document.querySelectorAll('.category-group')];
  const rows = groups.flatMap(group => [...group.querySelectorAll('tbody tr')]);
  search.closest('label').hidden = false;
  search.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    groups.forEach(group => {
      const groupName = group.querySelector('summary').textContent.toLowerCase();
      let matches = 0;
      group.querySelectorAll('tbody tr').forEach(row => {
        row.hidden = !!query && !`${groupName} ${row.textContent}`.toLowerCase().includes(query);
        if (!row.hidden) matches++;
      });
      group.hidden = matches === 0;
      group.open = !!query && matches > 0;
      visible += matches;
    });
    document.getElementById('arxiv-category-status').textContent = `${visible} of ${rows.length} category codes shown`;
  });
})();
