(() => {
  'use strict';
  const source = document.getElementById('preview-dataset');
  if (!source) return;
  const dataset = JSON.parse(source.textContent);
  const tables = dataset.tables;
  const select = document.getElementById('preview-table');
  const search = document.getElementById('preview-search');
  const table = document.getElementById('preview-records');
  const detail = document.getElementById('preview-detail');
  const csv = document.getElementById('preview-csv');
  const csvBase = csv.getAttribute('href').replace(/works\.csv$/, '');
  const pageSize = 10;
  const format = new Intl.NumberFormat('en');
  let name = 'works';
  let page = 0;
  let sort = null;
  let direction = 1;
  let selectedWork = null;

  const el = (tag, text, className) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  };
  const shortID = (value) => value.replace('https://openalex.org/', '');
  const lookup = (tableName, id) => tables[tableName].rows.find((row) => row.id === id);
  const related = (tableName, id) => tables[tableName].rows.filter((row) => row.work_id === id);

  function valueNode(value, column = '') {
    if (value === null || value === undefined) {
      const missing = el('span', 'NULL', 'preview-null');
      missing.title = 'Missing value in the database';
      return missing;
    }
    if (typeof value === 'boolean') return el('span', String(value), 'preview-boolean');
    if (typeof value === 'number') return el('span', column === 'publication_year' ? String(value) : format.format(value), 'preview-number');
    if (/^https:\/\/(openalex\.org|doi\.org|ror\.org|orcid\.org)\//.test(value)) {
      const link = el('a', value.startsWith('https://openalex.org/') ? shortID(value) : value.replace(/^https:\/\//, ''), 'preview-id');
      link.href = value;
      link.title = value;
      return link;
    }
    return el('span', String(value));
  }

  function filteredRows() {
    const query = search.value.trim().toLocaleLowerCase();
    const result = tables[name].rows.filter((row) => !query || Object.values(row).some((value) =>
      value !== null && String(value).toLocaleLowerCase().includes(query)));
    if (sort) result.sort((a, b) => {
      const av = a[sort], bv = b[sort];
      if (av === null && bv === null) return 0;
      if (av === null) return 1;
      if (bv === null) return -1;
      if (typeof av === 'number') return (av - bv) * direction;
      return String(av).localeCompare(String(bv), 'en', {numeric: true}) * direction;
    });
    return result;
  }

  function render() {
    const data = tables[name];
    const rows = filteredRows();
    page = Math.max(0, Math.min(page, Math.ceil(rows.length / pageSize) - 1));
    document.getElementById('preview-table-title').textContent = name;
    document.getElementById('preview-table-description').textContent = data.description;
    csv.href = `${csvBase}${name}.csv`;
    csv.title = 'Download all exported rows for this table, including rows hidden by the current search';
    const caption = el('caption', `Exported rows from openalex.${name}. Activate a column heading to sort.`, 'sr-only');
    const thead = el('thead');
    const headings = el('tr');
    for (const column of data.columns) {
      const th = el('th');
      th.scope = 'col';
      if (sort === column) th.setAttribute('aria-sort', direction === 1 ? 'ascending' : 'descending');
      const button = el('button', column + (sort === column ? (direction === 1 ? ' ↑' : ' ↓') : ' ↕'));
      button.type = 'button';
      button.addEventListener('click', () => {
        direction = sort === column ? -direction : 1;
        sort = column;
        page = 0;
        render();
        table.querySelectorAll('thead button')[data.columns.indexOf(column)].focus({preventScroll: true});
      });
      th.append(button);
      headings.append(th);
    }
    if (name === 'works') {
      const th = el('th', 'Record');
      th.scope = 'col';
      headings.prepend(th);
    }
    thead.append(headings);
    const tbody = el('tbody');
    for (const row of rows.slice(page * pageSize, (page + 1) * pageSize)) {
      const tr = el('tr');
      if (row.id === selectedWork) tr.classList.add('preview-selected');
      if (name === 'works') {
        const td = el('td');
        const button = el('button', 'Inspect →', 'preview-inspect');
        button.type = 'button';
        button.setAttribute('aria-label', `Inspect ${row.title || shortID(row.id)}`);
        button.setAttribute('aria-controls', 'preview-detail');
        button.addEventListener('click', () => showWork(row.id, true));
        td.append(button);
        tr.append(td);
      }
      for (const column of data.columns) {
        const td = el('td');
        if (column === 'title' || column === 'display_name') td.className = 'preview-title-cell';
        td.append(valueNode(row[column], column));
        tr.append(td);
      }
      tbody.append(tr);
    }
    if (!rows.length) {
      const tr = el('tr');
      const td = el('td', 'No matching records in this exported sample. Try a different search or reset the filters.', 'preview-empty');
      td.colSpan = data.columns.length + (name === 'works' ? 1 : 0);
      tr.append(td);
      tbody.append(tr);
    }
    table.replaceChildren(caption, thead, tbody);
    const start = rows.length ? page * pageSize + 1 : 0;
    const end = Math.min((page + 1) * pageSize, rows.length);
    document.getElementById('preview-count').textContent = `${start}–${end} of ${format.format(rows.length)} matching rows · ${format.format(data.rows.length)} rows exported`;
    document.getElementById('preview-prev').disabled = page === 0;
    document.getElementById('preview-next').disabled = (page + 1) * pageSize >= rows.length;
  }

  function detailGroup(title, records, renderRecord) {
    const section = el('section', undefined, 'preview-detail-group');
    section.append(el('h3', `${title} (${records.length})`));
    if (!records.length) section.append(el('p', 'No rows available in this export.', 'preview-muted'));
    else {
      const list = el('ul');
      records.forEach((record) => { const item = el('li'); renderRecord(item, record); list.append(item); });
      section.append(list);
    }
    return section;
  }

  function showWork(id, focus = false) {
    const work = lookup('works', id);
    if (!work) return;
    selectedWork = id;
    detail.replaceChildren();
    const top = el('div', undefined, 'preview-detail-top');
    top.append(el('p', `Selected work / ${shortID(id)}`, 'eyebrow'));
    const close = el('button', 'Close ×', 'preview-secondary');
    close.type = 'button';
    close.addEventListener('click', () => {
      detail.hidden = true;
      selectedWork = null;
      history.replaceState(null, '', `#table=${encodeURIComponent(name)}`);
      render();
      document.querySelector('.preview-inspect')?.focus({preventScroll: true});
    });
    top.append(close);
    detail.append(top);
    const title = el('h2', work.title || 'Untitled work');
    title.id = 'preview-detail-title';
    title.tabIndex = -1;
    detail.append(title);
    const metadata = el('dl', undefined, 'preview-work-metadata');
    for (const [label, value] of [['Year', work.publication_year], ['Type', work.type], ['Language', work.language], ['Citations', work.cited_by_count], ['DOI', work.doi], ['OpenAlex ID', work.id]]) {
      const item = el('div');
      const dd = el('dd');
      dd.append(valueNode(value, label === 'Year' ? 'publication_year' : ''));
      item.append(el('dt', label), dd);
      metadata.append(item);
    }
    detail.append(metadata);
    const context = el('p', undefined, 'preview-work-context');
    const venue = lookup('sources', work.primary_location_source_id);
    const primary = lookup('topics', work.primary_topic_id);
    context.textContent = `Source: ${venue?.display_name || 'Not resolved in this export'} · Primary topic: ${primary?.display_name || 'Not resolved in this export'}`;
    detail.append(context);
    const groups = el('div', undefined, 'preview-detail-grid');
    const authorships = related('works_authorships', id);
    const affiliationLinks = related('works_authorship_institutions', id);
    groups.append(detailGroup('Authorships', authorships, (item, row) => {
      const author = lookup('authors', row.author_id);
      item.append(el('strong', author?.display_name || 'Unresolved author'), document.createTextNode(' '), valueNode(row.author_id));
      item.append(el('small', `${row.author_position || 'Position unknown'}${row.is_corresponding ? ' · corresponding author' : ''}`));
    }));
    const institutionIDs = [...new Set(affiliationLinks.map((row) => row.institution_id))];
    groups.append(detailGroup('Institutions', institutionIDs, (item, institutionID) => {
      const institution = lookup('institutions', institutionID);
      item.append(el('strong', institution?.display_name || 'Unresolved institution'), document.createTextNode(' '), valueNode(institutionID));
      item.append(el('small', institution ? `${institution.country_code || 'Country unknown'} · ${institution.type || 'Type unknown'}` : 'Linked ID has no matching entity in this export'));
    }));
    groups.append(detailGroup('Topic assignments', related('works_topics', id), (item, row) => {
      const topic = lookup('topics', row.topic_id);
      item.append(el('strong', topic?.display_name || 'Unresolved topic'), document.createTextNode(' '), valueNode(row.topic_id));
      item.append(el('small', `${row.is_primary ? 'Primary · ' : ''}Score: ${row.score ?? 'unknown'}${topic ? ' · ' + topic.field_display_name : ''}`));
    }));
    groups.append(detailGroup('Exported references · up to 12', related('works_referenced_works', id), (item, row) => {
      item.append(valueNode(row.referenced_work_id));
      const target = lookup('works', row.referenced_work_id);
      item.append(el('small', target?.title || 'Target metadata not included in this export'));
    }));
    detail.append(groups);
    const oa = related('works_open_access', id)[0];
    detail.append(el('p', `Open-access status: ${oa?.oa_status || 'unknown'} · Retraction flag: ${work.is_retracted === null ? 'unknown' : work.is_retracted}. Statuses are observed in the loaded dataset.`, 'preview-muted'));
    detail.hidden = false;
    history.replaceState(null, '', `#table=${encodeURIComponent(name)}&work=${encodeURIComponent(shortID(id))}`);
    render();
    if (focus) {
      detail.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start'});
      title.focus({preventScroll: true});
    }
  }

  function changeTable(value) {
    if (!Object.hasOwn(tables, value)) return;
    name = value;
    select.value = name;
    search.value = '';
    page = 0;
    sort = null;
    direction = 1;
    selectedWork = null;
    detail.hidden = true;
    render();
  }
  select.addEventListener('change', () => {
    changeTable(select.value);
    history.replaceState(null, '', `#table=${encodeURIComponent(name)}`);
  });
  search.addEventListener('input', () => { page = 0; render(); });
  document.getElementById('preview-reset').addEventListener('click', () => {
    changeTable('works');
    history.replaceState(null, '', '#sample');
    search.focus();
  });
  document.getElementById('preview-prev').addEventListener('click', () => { page--; render(); });
  document.getElementById('preview-next').addEventListener('click', () => { page++; render(); });

  const catalogSearch = document.getElementById('catalog-search');
  const catalogItems = [...document.querySelectorAll('.catalog-item')];
  catalogSearch.addEventListener('input', () => {
    const query = catalogSearch.value.trim().toLocaleLowerCase();
    catalogItems.forEach((item) => { item.hidden = !item.textContent.toLocaleLowerCase().includes(query); });
    document.getElementById('catalog-count').textContent = `${catalogItems.filter((item) => !item.hidden).length} of ${catalogItems.length} tables match`;
  });

  function restoreHash() {
    const params = new URLSearchParams(location.hash.slice(1));
    if (params.has('table')) changeTable(params.get('table'));
    if (params.has('work')) showWork('https://openalex.org/' + params.get('work'));
  }
  document.querySelector('.preview-controls').hidden = false;
  document.querySelector('.preview-pagination').hidden = false;
  document.querySelector('.catalog-search-label').hidden = false;
  render();
  restoreHash();
  window.addEventListener('hashchange', restoreHash);
})();
