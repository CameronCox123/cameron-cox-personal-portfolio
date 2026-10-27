(function () {
  'use strict';
  const root = document.documentElement;
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const button = document.getElementById('themeToggle');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let explicitTheme = false;
  try { explicitTheme = !!localStorage.getItem('hf-theme'); } catch (e) { }
  function applyTheme(theme) {
    root.dataset.theme = theme;
    const dark = theme === 'dark';
    if (button) { button.querySelector('.theme-label').textContent = dark ? 'Light mode' : 'Dark mode'; button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode'); }
  }
  applyTheme(root.dataset.theme || (mq.matches ? 'dark' : 'light'));
  if (button) button.addEventListener('click', () => { const next = root.dataset.theme === 'dark' ? 'light' : 'dark'; explicitTheme = true; try { localStorage.setItem('hf-theme', next); } catch (e) { } applyTheme(next); });
  mq.addEventListener('change', e => { if (!explicitTheme) applyTheme(e.matches ? 'dark' : 'light'); });
  document.getElementById('year').textContent = new Date().getFullYear();
  const name = document.getElementById('heroNameText'), caret = document.getElementById('heroCaret');
  if (name && caret) {
    const full = name.textContent;
    if (reduced) caret.classList.add('hidden');
    else { let i = 0; name.textContent = ''; function type() { name.textContent = full.slice(0, ++i); if (i < full.length) setTimeout(type, 45); else setTimeout(() => caret.classList.add('hidden'), 700); } type(); }
  }
  const sequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA']; let progress = 0;
  document.addEventListener('keydown', e => {
    if (e.target.closest('input,textarea,select,[contenteditable="true"]')) return;
    if (e.ctrlKey || e.altKey || e.metaKey) return;
    if (progress > 0 && e.code === sequence[progress] && e.code.startsWith('Arrow')) e.preventDefault();
    progress = e.code === sequence[progress] ? progress + 1 : (e.code === sequence[0] ? 1 : 0);
    if (progress === sequence.length) {
      progress = 0; const photo = document.getElementById('headshot'); const toast = document.getElementById('toast');
      if (photo) { const fun = photo.classList.toggle('fun'); const pro = photo.querySelector('.photo-pro'), alt = photo.querySelector('.photo-fun'); pro.setAttribute('aria-hidden', String(fun)); alt.setAttribute('aria-hidden', String(!fun)); alt.alt = fun ? 'Harrison Floyd’s alternate fun photo' : ''; toast.textContent = fun ? 'Cheat code accepted. Secret photo unlocked!' : 'Back to business. Mostly.'; } else { toast.textContent = 'Cheat code accepted. Try it on the homepage for a surprise.'; }
      toast.hidden = false; clearTimeout(toast._timer); toast._timer = setTimeout(() => toast.hidden = true, 3200);
    }
  });
  const filters = [...document.querySelectorAll('[data-filter]')], cards = [...document.querySelectorAll('.project-card')];
  filters.forEach(filter => filter.addEventListener('click', () => { const value = filter.dataset.filter; filters.forEach(b => b.setAttribute('aria-pressed', String(b === filter))); cards.forEach(c => c.hidden = value !== 'all' && c.dataset.category !== value); const count = cards.filter(c => !c.hidden).length; document.querySelector('.filter-status').textContent = `Showing ${count} ${value === 'all' ? '' : filter.textContent + ' '}project${count === 1 ? '' : 's'}.`; }));
  document.querySelectorAll('.headshot img').forEach(img => { function hideMissing() { img.hidden = true; } img.addEventListener('error', hideMissing); if (img.complete && img.naturalWidth === 0) hideMissing(); });
  document.querySelectorAll('.project-media video').forEach(video => {
    const message = video.closest('.project-media').querySelector('.media-error'); if (!message) return;
    function showError() { const code = video.error ? video.error.code : 0; if (code === 1) return; message.textContent = code === 3 ? 'The browser could not decode this video. Try the direct video link above.' : code === 4 ? 'The video is unavailable or its format is unsupported. Try the direct video link above.' : 'The video could not load. Try the direct video link above.'; message.hidden = false; }
    video.addEventListener('error', showError); video.addEventListener('loadeddata', () => message.hidden = true); if (video.error) showError();
  });
})();
