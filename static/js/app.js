/**
 * VIKA App Core Manager
 * Handles SPA navigation, theme switching (Light/Dark), and user preferences.
 * Author: Abu Ziyad Al Katani (zydalz)
 */

const AppState = {
  currentView: 'landing', // 'landing' | 'chat' | 'settings'
  theme: localStorage.getItem('vika_theme') || 'light',
  style: localStorage.getItem('vika_style') || 'Kasual',
  scope: localStorage.getItem('vika_scope') || 'universitas',
  modelProvider: localStorage.getItem('vika_model') || 'gemini',
};

// Initialize App on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initSettingsControls();
  initSidebarControls();
});

// -------------------------------------------------------------
// THEME MANAGEMENT (Light / Dark)
// -------------------------------------------------------------
function initTheme() {
  applyTheme(AppState.theme);

  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const nextTheme = AppState.theme === 'dark' ? 'light' : 'dark';
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

  // Update logo images based on theme
  const brandLogos = document.querySelectorAll('.nav-logo, .bot-avatar-img');
  brandLogos.forEach(logo => {
    logo.src = theme === 'dark' ? '/static/images/VIKA Logo Dark Mode.png' : '/static/images/Logo VIKA Light mode.png';
  });

  // Update toggle button icon
  const toggleIcon = document.getElementById('theme-toggle-icon');
  if (toggleIcon) {
    toggleIcon.innerHTML = theme === 'dark' 
      ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }

  // Update settings segmented theme buttons if present
  document.querySelectorAll('[data-theme-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === theme);
  });
}

// -------------------------------------------------------------
// SPA NAVIGATION (Landing, Chat, Settings)
// -------------------------------------------------------------
function initNavigation() {
  const landingView = document.getElementById('landing-view');
  const chatView = document.getElementById('chat-view');
  const settingsView = document.getElementById('settings-view');

  window.switchView = function(viewName) {
    AppState.currentView = viewName;

    // View visibility
    if (landingView) landingView.style.display = viewName === 'landing' ? 'block' : 'none';
    if (chatView) chatView.style.display = viewName === 'chat' ? 'flex' : 'none';
    if (settingsView) settingsView.style.display = viewName === 'settings' ? 'block' : 'none';

    // Navbar active class
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.toggle('active', link.dataset.targetView === viewName);
    });

    // Sidebar active class
    document.querySelectorAll('.sidebar-nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.targetView === viewName);
    });

    // Auto-focus chat input when switching to chat
    if (viewName === 'chat') {
      const chatInput = document.getElementById('chat-input-field');
      if (chatInput) chatInput.focus();
    }
  };

  // Nav brand click -> go to landing
  document.getElementById('nav-brand')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchView('landing');
  });

  // "Mulai Sekarang" button -> go to chat
  document.getElementById('btn-start-chat')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchView('chat');
  });

  // Nav links
  document.querySelectorAll('[data-target-view]').forEach(elem => {
    elem.addEventListener('click', (e) => {
      e.preventDefault();
      switchView(elem.dataset.targetView);
    });
  });
}

// -------------------------------------------------------------
// SETTINGS PREFERENCES
// -------------------------------------------------------------
function initSettingsControls() {
  // 1. Style Segmented Buttons
  document.querySelectorAll('[data-style-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.styleChoice.toLowerCase() === AppState.style.toLowerCase());
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-style-choice]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.style = btn.dataset.styleChoice;
      localStorage.setItem('vika_style', AppState.style);

      // Sync with Chat Header Dropdown
      const chatStyleSelect = document.getElementById('chat-style-select');
      if (chatStyleSelect) chatStyleSelect.value = AppState.style;
    });
  });

  // 2. Scope Segmented Buttons
  document.querySelectorAll('[data-scope-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.scopeChoice === AppState.scope);
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-scope-choice]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      AppState.scope = btn.dataset.scopeChoice;
      localStorage.setItem('vika_scope', AppState.scope);

      // Sync with Chat Header Dropdown
      const chatScopeSelect = document.getElementById('chat-scope-select');
      if (chatScopeSelect) chatScopeSelect.value = AppState.scope;
    });
  });

  // 3. Theme Segmented Buttons on Settings Page
  document.querySelectorAll('[data-theme-choice]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeChoice === AppState.theme);
    btn.addEventListener('click', () => {
      applyTheme(btn.dataset.themeChoice);
    });
  });

  // 4. Model Selector Toggle
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

// -------------------------------------------------------------
// SIDEBAR TOGGLE
// -------------------------------------------------------------
function initSidebarControls() {
  const sidebar = document.getElementById('chat-sidebar');
  const toggleBtn = document.getElementById('btn-toggle-sidebar');
  
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      toggleBtn.innerHTML = sidebar.classList.contains('collapsed')
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg> <span>Tampilkan</span>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg> <span>Sembunyikan sidebar</span>';
    });
  }
}
