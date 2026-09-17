(() => {
  const chart = document.querySelector('.annual-chart');
  if (chart) {
    const slider = chart.querySelector('input[type="range"]');
    const output = chart.querySelector('output');
    const bars = [...chart.querySelectorAll('.chart-bar')];
    const selectYear = year => {
      const bar = bars.find(p => p.dataset.year === String(year));
      if (!bar) return;
      bars.forEach(p => p.classList.toggle('is-selected', p === bar));
      slider.value = bar.dataset.year;
      slider.setAttribute('aria-valuetext', bar.dataset.label);
      output.textContent = bar.dataset.label;
    };
    slider.addEventListener('input', () => selectYear(slider.value));
    bars.forEach(bar => {
      bar.addEventListener('barerenter', () => selectYear(bar.dataset.year));
      bar.addEventListener('click', () => selectYear(bar.dataset.year));
    });
    chart.querySelector('.chart-inspector').hidden = false;
    selectYear(slider.value);
  }

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
