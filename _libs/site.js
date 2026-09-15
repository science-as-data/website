document.documentElement.classList.add('js');

const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
menu?.addEventListener('click', () => {
  const expanded = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(expanded));
  nav.classList.toggle('is-open', expanded);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    menu.focus();
  }
});

// Ordinary Franklin Markdown fences gain the same copy control as the homepage.
document.querySelectorAll('.article pre > code').forEach((code, index) => {
  code.id ||= `code-${index}`;
  const wrapper = document.createElement('div');
  wrapper.className = 'code-wrap';
  const pre = code.parentElement;
  pre.before(wrapper);
  wrapper.append(pre);
  const button = document.createElement('button');
  button.className = 'copy-button';
  button.dataset.copy = code.id;
  button.textContent = 'Copy';
  button.setAttribute('aria-label', 'Copy code example');
  wrapper.prepend(button);
});

document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copy);
    const original = button.textContent;
    const status = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(target.textContent.trimEnd());
      button.textContent = 'Copied ✓';
      status.textContent = 'Code copied to clipboard.';
    } catch {
      // Selection remains useful when clipboard access is denied or over HTTP.
      const range = document.createRange();
      range.selectNodeContents(target);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Selected';
      status.textContent = 'Automatic copying is unavailable. Code selected; use your browser’s copy command.';
    }
    button.disabled = true;
    setTimeout(() => { button.textContent = original; button.disabled = false; }, 2200);
  });
});

// Progressive enhancement: every query stays readable without JavaScript.
const tabs = [...document.querySelectorAll('.query-tab')];
const panels = [...document.querySelectorAll('.query-panel')];
function selectQuery(tab, updateHash = true) {
  tabs.forEach((item) => {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
  });
  panels.forEach((panel) => { panel.hidden = panel.id !== tab.getAttribute('aria-controls'); });
  if (updateHash) history.replaceState(null, '', `#${tab.getAttribute('aria-controls')}`);
}
if (tabs.length) {
  document.querySelector('.query-tabs').setAttribute('role', 'tablist');
  tabs.forEach((tab, index) => {
    tab.setAttribute('role', 'tab');
    tab.addEventListener('click', () => selectQuery(tab));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectQuery(tabs[next]); tabs[next].focus(); }
    });
  });
  panels.forEach((panel) => { panel.setAttribute('role', 'tabpanel'); panel.tabIndex = 0; });
  const tabFromHash = () => tabs.find((tab) => `#${tab.getAttribute('aria-controls')}` === location.hash);
  selectQuery(tabFromHash() || tabs[0], false);
  window.addEventListener('hashchange', () => { if (tabFromHash()) selectQuery(tabFromHash(), false); });
}

document.querySelectorAll('.article table').forEach((table) => {
  const wrapper = document.createElement('div');
  wrapper.className = 'table-scroll';
  wrapper.tabIndex = 0;
  wrapper.setAttribute('role', 'region');
  wrapper.setAttribute('aria-label', 'Scrollable reference table');
  table.before(wrapper);
  wrapper.append(table);
});
