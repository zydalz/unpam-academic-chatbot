/**
 * VIKA App Core Manager (Unified Architecture)
 * Handles SPA views, sliding theme switcher, custom dropdowns, sidebar collapse/open,
 * and API Key settings persistence.
 * Author: Abu Ziyad Al Katani (zydalz)
 */

const AppState = {
  currentView: 'landing', // 'landing' | 'chat' | 'settings'
  theme: localStorage.getItem('vika_theme') || 'dark',
  style: localStorage.getItem('vika_style') || 'Kasual',
  scope: localStorage.getItem('vika_scope') || 'universitas',
  modelProvider: localStorage.getItem('vika_model') || 'gemini',
};

document.addEventListener('DOMContentLoaded', () => {
  initThemeSwitch();
  initNavigation();
  initCustomDropdowns();
  initSidebarControls();
  initApiKeyManagement();
  initSettingsPreferences();
});

// -------------------------------------------------------------
// 1. SLIDING THEME TOGGLE SWITCH
// -------------------------------------------------------------
function initThemeSwitch() {
  applyTheme(AppState.theme);

  const switchCheckbox = document.getElementById('theme-switch-checkbox');
  if (switchCheckbox) {
    switchCheckbox.checked = AppState.theme === 'dark';
    switchCheckbox.addEventListener('change', (e) => {
      const nextTheme = e.target.checked ? 'dark' : 'light';
      applyTheme(nextTheme);
    });
  }
}

function applyTheme(theme) {
  AppState.theme = theme;
  localStorage.setItem('vika_theme', theme);

  if (theme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  } else {
    document.documentElement.removeAttribute('data-theme');
  }

  // Update brand logos
  const brandLogos = document.querySelectorAll('.nav-logo, .sidebar-brand-img, .bot-avatar-img');
  brandLogos.forEach(logo => {
    logo.src = theme === 'dark' 
      ? '/static/images/VIKA Logo Dark Mode.png' 
      : '/static/images/Logo VIKA Light mode.png';
  });

  // Sync checkbox if called externally
  const switchCheckbox = document.getElementById('theme-switch-checkbox');
  if (switchCheckbox) switchCheckbox.checked = theme === 'dark';

  // Sync settings segmented buttons
  document.querySelectorAll('[data-theme-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === theme);
  });
}

// -------------------------------------------------------------
// 2. UNIFIED SPA NAVIGATION (Landing, Chat, Settings)
// -------------------------------------------------------------
function initNavigation() {
  const landingView = document.getElementById('landing-view');
  const chatView = document.getElementById('chat-view');
  const settingsView = document.getElementById('settings-view');
  const headerTitle = document.getElementById('header-active-title');

  window.switchView = function(viewName) {
    AppState.currentView = viewName;

    // View visibility
    if (landingView) landingView.style.display = viewName === 'landing' ? 'flex' : 'none';
    if (chatView) chatView.style.display = viewName === 'chat' ? 'flex' : 'none';
    if (settingsView) settingsView.style.display = viewName === 'settings' ? 'block' : 'none';

    // Sidebar active item highlight
    document.querySelectorAll('.sidebar-nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.targetView === viewName);
    });

    // Update Header Title Text
    if (headerTitle) {
      if (viewName === 'landing') {
        headerTitle.innerHTML = '<span>Asisten Akademik UNPAM</span>';
      } else if (viewName === 'chat') {
        headerTitle.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> <span id="chat-topic-label">Linimasa SK Kalender 2026/2027</span>';
      } else if (viewName === 'settings') {
        headerTitle.innerHTML = '<span>Pengaturan Sistem</span>';
      }
    }

    if (viewName === 'chat') {
      const chatInput = document.getElementById('chat-input-field');
      if (chatInput) chatInput.focus();
    }
  };

  // Sidebar Nav Items
  document.querySelectorAll('[data-target-view]').forEach(elem => {
    elem.addEventListener('click', (e) => {
      e.preventDefault();
      switchView(elem.dataset.targetView);
    });
  });

  // Sidebar Brand Click -> Landing
  document.getElementById('sidebar-brand')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchView('landing');
  });
}

// -------------------------------------------------------------
// 3. CUSTOM DROPDOWNS (Cakupan & Gaya)
// -------------------------------------------------------------
function initCustomDropdowns() {
  // Setup Dropdown Scope
  setupDropdown('dropdown-scope', AppState.scope, (value) => {
    AppState.scope = value;
    localStorage.setItem('vika_scope', value);
    // Sync Settings Scope
    document.querySelectorAll('[data-scope-choice]').forEach(b => {
      b.classList.toggle('active', b.dataset.scopeChoice === value);
    });
  });

  // Setup Dropdown Style
  setupDropdown('dropdown-style', AppState.style, (value) => {
    AppState.style = value;
    localStorage.setItem('vika_style', value);
    // Sync Settings Style
    document.querySelectorAll('[data-style-choice]').forEach(b => {
      b.classList.toggle('active', b.dataset.styleChoice.toLowerCase() === value.toLowerCase());
    });
  });

  // Close dropdowns on outside click
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.custom-dropdown')) {
      document.querySelectorAll('.custom-dropdown').forEach(d => d.classList.remove('open'));
    }
  });
}

function setupDropdown(dropdownId, initialValue, onSelectCallback) {
  const container = document.getElementById(dropdownId);
  if (!container) return;

  const btn = container.querySelector('.custom-dropdown-btn');
  const labelSpan = container.querySelector('.dropdown-label-text');
  const items = container.querySelectorAll('.dropdown-item');

  // Sync initial state if provided
  if (initialValue) {
    items.forEach(item => {
      const isMatch = item.dataset.value.toLowerCase() === initialValue.toLowerCase();
      item.classList.toggle('active', isMatch);
      if (isMatch) {
        const text = item.querySelector('span')?.textContent || item.textContent;
        if (labelSpan) labelSpan.textContent = text.trim();
      }
    });
  }

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    // Close other dropdowns
    document.querySelectorAll('.custom-dropdown').forEach(d => {
      if (d !== container) d.classList.remove('open');
    });
    container.classList.toggle('open');
  });

  items.forEach(item => {
    item.addEventListener('click', () => {
      items.forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      const val = item.dataset.value;
      const text = item.querySelector('span')?.textContent || item.textContent;
      if (labelSpan) labelSpan.textContent = text.trim();

      container.classList.remove('open');
      if (onSelectCallback) onSelectCallback(val);
    });
  });
}

// -------------------------------------------------------------
// 4. SIDEBAR TOGGLE & RESTORE
// -------------------------------------------------------------
function initSidebarControls() {
  const sidebar = document.getElementById('app-sidebar');
  const collapseBtn = document.getElementById('btn-sidebar-collapse');
  const openBtn = document.getElementById('sidebar-open-btn');

  if (collapseBtn && sidebar) {
    collapseBtn.addEventListener('click', () => {
      sidebar.classList.add('collapsed');
      if (openBtn) openBtn.style.display = 'flex';
    });
  }

  if (openBtn && sidebar) {
    openBtn.addEventListener('click', () => {
      sidebar.classList.remove('collapsed');
      openBtn.style.display = 'none';
    });
  }
}

// -------------------------------------------------------------
// 5. API KEY MANAGEMENT (Settings Form & Status)
// -------------------------------------------------------------
async function initApiKeyManagement() {
  const geminiInput = document.getElementById('input-gemini-key');
  const groqInput = document.getElementById('input-groq-key');
  const saveGeminiBtn = document.getElementById('btn-save-gemini-key');
  const saveGroqBtn = document.getElementById('btn-save-groq-key');
  const geminiBadge = document.getElementById('gemini-status-badge');
  const groqBadge = document.getElementById('groq-status-badge');

  // Fetch current status from backend
  try {
    const res = await fetch('/api/settings/keys');
    if (res.ok) {
      const data = await res.json();
      if (data.gemini_configured) {
        if (geminiBadge) {
          geminiBadge.className = 'api-status-badge active';
          geminiBadge.textContent = '✓ Aktif';
        }
        if (geminiInput && data.gemini_masked) {
          geminiInput.placeholder = data.gemini_masked;
        }
      }
      if (data.groq_configured) {
        if (groqBadge) {
          groqBadge.className = 'api-status-badge active';
          groqBadge.textContent = '✓ Aktif';
        }
        if (groqInput && data.groq_masked) {
          groqInput.placeholder = data.groq_masked;
        }
      }
    }
  } catch (e) {
    console.warn('Could not check keys status:', e);
  }

  // Save Gemini Key
  if (saveGeminiBtn && geminiInput) {
    saveGeminiBtn.addEventListener('click', async () => {
      const keyVal = geminiInput.value.trim();
      if (!keyVal) return;

      saveGeminiBtn.textContent = 'Menyimpan...';
      try {
        const res = await fetch('/api/settings/keys', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ gemini_key: keyVal }),
        });
        if (res.ok) {
          saveGeminiBtn.textContent = '✓ Tersimpan';
          geminiInput.value = '';
          geminiInput.placeholder = keyVal.slice(0, 4) + '••••••••' + keyVal.slice(-4);
          if (geminiBadge) {
            geminiBadge.className = 'api-status-badge active';
            geminiBadge.textContent = '✓ Aktif';
          }
          setTimeout(() => { saveGeminiBtn.textContent = 'Simpan'; }, 2000);
        }
      } catch (err) {
        saveGeminiBtn.textContent = 'Gagal';
        setTimeout(() => { saveGeminiBtn.textContent = 'Simpan'; }, 2000);
      }
    });
  }

  // Save Groq Key
  if (saveGroqBtn && groqInput) {
    saveGroqBtn.addEventListener('click', async () => {
      const keyVal = groqInput.value.trim();
      if (!keyVal) return;

      saveGroqBtn.textContent = 'Menyimpan...';
      try {
        const res = await fetch('/api/settings/keys', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ groq_key: keyVal }),
        });
        if (res.ok) {
          saveGroqBtn.textContent = '✓ Tersimpan';
          groqInput.value = '';
          groqInput.placeholder = keyVal.slice(0, 4) + '••••••••' + keyVal.slice(-4);
          if (groqBadge) {
            groqBadge.className = 'api-status-badge active';
            groqBadge.textContent = '✓ Aktif';
          }
          setTimeout(() => { saveGroqBtn.textContent = 'Simpan'; }, 2000);
        }
      } catch (err) {
        saveGroqBtn.textContent = 'Gagal';
        setTimeout(() => { saveGroqBtn.textContent = 'Simpan'; }, 2000);
      }
    });
  }
}

// -------------------------------------------------------------
// 6. SETTINGS PAGE SEGMENTED BUTTONS
// -------------------------------------------------------------
function initSettingsPreferences() {
  // Style Segmented Buttons
  document.querySelectorAll('[data-style-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.styleChoice.toLowerCase() === AppState.style.toLowerCase());
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-style-choice]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.style = btn.dataset.styleChoice;
      localStorage.setItem('vika_style', AppState.style);

      // Sync header dropdown label
      const styleDropdown = document.getElementById('dropdown-style');
      if (styleDropdown) {
        const label = styleDropdown.querySelector('.dropdown-label-text');
        if (label) label.textContent = AppState.style;
      }
    });
  });

  // Scope Segmented Buttons
  document.querySelectorAll('[data-scope-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.scopeChoice === AppState.scope);
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-scope-choice]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.scope = btn.dataset.scopeChoice;
      localStorage.setItem('vika_scope', AppState.scope);

      // Sync header dropdown label
      const scopeDropdown = document.getElementById('dropdown-scope');
      if (scopeDropdown) {
        const label = scopeDropdown.querySelector('.dropdown-label-text');
        if (label) label.textContent = btn.textContent.trim();
      }
    });
  });

  // Theme Segmented Buttons on Settings Page
  document.querySelectorAll('[data-theme-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === AppState.theme);
    btn.addEventListener('click', () => {
      applyTheme(btn.dataset.themeChoice);
    });
  });

  // Model Toggle Card
  const modelToggleCard = document.getElementById('model-toggle-card');
  if (modelToggleCard) {
    modelToggleCard.addEventListener('click', () => {
      const nextModel = AppState.modelProvider === 'gemini' ? 'llama' : 'gemini';
      AppState.modelProvider = nextModel;
      localStorage.setItem('vika_model', nextModel);
      updateModelCardDisplay();
    });
    updateModelCardDisplay();
  }
}

function updateModelCardDisplay() {
  const modelNameElem = document.getElementById('active-model-name');
  const modelDescElem = document.getElementById('active-model-desc');
  const modelBadgeElem = document.getElementById('active-model-badge');

  if (AppState.modelProvider === 'llama') {
    if (modelNameElem) modelNameElem.textContent = 'Llama 3.3 70B (Groq Engine)';
    if (modelDescElem) modelDescElem.textContent = 'Open-weights super cepat, latensi < 1 detik.';
    if (modelBadgeElem) {
      modelBadgeElem.textContent = 'Open Source';
      modelBadgeElem.style.background = '#FEF3C7';
      modelBadgeElem.style.color = '#B45309';
    }
  } else {
    if (modelNameElem) modelNameElem.textContent = 'Google Gemini 3.8 Flash';
    if (modelDescElem) modelDescElem.textContent = 'Cepat, akurat, dan penalaran regulasi teruji.';
    if (modelBadgeElem) {
      modelBadgeElem.textContent = 'Rekomendasi';
      modelBadgeElem.style.background = '';
      modelBadgeElem.style.color = '';
    }
  }
}
