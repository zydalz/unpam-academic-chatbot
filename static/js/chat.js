/**
 * VIKA Chat Streaming & Markdown Renderer
 * Implements smooth typewriter cadence streaming, markdown table formatting,
 * inner sub-cards, real local session history, and action recommendation chips.
 * Author: Abu Ziyad Al Katani (zydalz)
 */

document.addEventListener('DOMContentLoaded', () => {
  initChatEngine();
  renderRealSessionHistory();
});

function initChatEngine() {
  const chatInput = document.getElementById('chat-input-field');
  const chatSendBtn = document.getElementById('btn-chat-send');
  const landingInput = document.getElementById('landing-input-field');
  const landingSendBtn = document.getElementById('btn-landing-send');
  const newChatBtn = document.getElementById('btn-new-chat');
  const clearHistoryBtn = document.getElementById('btn-clear-history');

  // Send from Chat view
  if (chatSendBtn && chatInput) {
    chatSendBtn.addEventListener('click', () => {
      const text = chatInput.value.trim();
      if (text) {
        chatInput.value = '';
        submitUserPrompt(text);
      }
    });

    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatSendBtn.click();
      }
    });
  }

  // Send from Landing view
  if (landingSendBtn && landingInput) {
    landingSendBtn.addEventListener('click', () => {
      const text = landingInput.value.trim();
      if (text) {
        landingInput.value = '';
        window.switchView('chat');
        submitUserPrompt(text);
      }
    });

    landingInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        landingSendBtn.click();
      }
    });
  }

  // Shortcut Cards on Landing Page
  document.querySelectorAll('.shortcut-box').forEach(card => {
    card.addEventListener('click', () => {
      const prompt = card.dataset.prompt;
      if (prompt) {
        window.switchView('chat');
        submitUserPrompt(prompt);
      }
    });
  });

  // "+ Chat Baru" Button
  if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
      resetToDefaultWelcome();
    });
  }

  // Clear History Button
  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', () => {
      localStorage.removeItem('vika_chat_sessions');
      renderRealSessionHistory();
    });
  }
}

function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
}

// -------------------------------------------------------------
// CHAT SUBMISSION & SMOOTH TYPEWRITER STREAMING
// -------------------------------------------------------------
async function submitUserPrompt(promptText) {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  const timeStr = getCurrentTime();

  // Update Chat Header Topic Label
  const topicLabel = document.getElementById('chat-topic-label');
  if (topicLabel) {
    topicLabel.textContent = promptText.length > 35 ? promptText.slice(0, 32) + '...' : promptText;
  }

  // 1. Render User Message Bubble
  const userRow = document.createElement('div');
  userRow.className = 'message-row-user';
  userRow.innerHTML = `
    <div class="user-bubble">
      ${escapeHtml(promptText)}
      <span class="message-time">${timeStr}</span>
    </div>
  `;
  chatMessages.appendChild(userRow);
  scrollToBottom();

  // 2. Render Assistant Card Placeholder with Blinking Cursor
  const assistantRow = document.createElement('div');
  assistantRow.className = 'message-row-assistant';
  
  const logoSrc = AppState.theme === 'dark' 
    ? '/static/images/VIKA Logo Dark Mode.png' 
    : '/static/images/Logo VIKA Light mode.png';

  assistantRow.innerHTML = `
    <div class="bot-avatar-circle">
      <img src="${logoSrc}" alt="VIKA" class="bot-avatar-img">
    </div>
    <div class="assistant-response-card">
      <div class="assistant-text-content">
        <span class="stream-text"></span><span class="cursor-blinker">|</span>
      </div>
      <div class="card-footer-meta" style="display: none;"></div>
    </div>
  `;
  chatMessages.appendChild(assistantRow);
  scrollToBottom();

  const streamTextSpan = assistantRow.querySelector('.stream-text');
  const cursorSpan = assistantRow.querySelector('.cursor-blinker');
  const cardFooterDiv = assistantRow.querySelector('.card-footer-meta');

  // Save to Real Session History
  saveSessionToHistory(promptText);

  // 3. Connect to SSE Stream with Smooth Typewriter Queue
  try {
    const payload = {
      query: promptText,
      style: AppState.style,
      scope: AppState.scope,
      provider: AppState.modelProvider,
    };

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errText = await response.text();
      streamTextSpan.innerHTML = `❌ Gagal menghubungi server: ${errText}`;
      if (cursorSpan) cursorSpan.remove();
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    let rawAccumulated = '';
    let citations = [];
    let recommendations = [];
    let externalSource = null;

    // Typewriter Queue Mechanism
    const tokenQueue = [];
    let isQueueRunning = false;

    function processQueue() {
      if (tokenQueue.length === 0) {
        isQueueRunning = false;
        return;
      }
      isQueueRunning = true;
      const token = tokenQueue.shift();
      rawAccumulated += token;
      
      // Update formatted content in DOM
      streamTextSpan.innerHTML = formatMarkdownText(rawAccumulated);
      scrollToBottom();

      setTimeout(processQueue, 16); // 16ms typing delay per token
    }

    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const dataStr = line.replace('data: ', '').trim();
        if (dataStr === '[DONE]') break;

        try {
          const parsed = JSON.parse(dataStr);
          if (parsed.type === 'token') {
            tokenQueue.push(parsed.content);
            if (!isQueueRunning) processQueue();
          } else if (parsed.type === 'meta') {
            if (parsed.citations) citations = parsed.citations;
            if (parsed.recommendations && parsed.recommendations.length > 0) recommendations = parsed.recommendations;
            if (parsed.external_source) externalSource = parsed.external_source;
          }
        } catch (e) {
          tokenQueue.push(dataStr);
          if (!isQueueRunning) processQueue();
        }
      }
    }

    // Wait until queue is completely drained
    const checkDrain = setInterval(() => {
      if (tokenQueue.length === 0) {
        clearInterval(checkDrain);
        if (cursorSpan) cursorSpan.remove();
        // Final render with tables and subcards
        streamTextSpan.innerHTML = formatMarkdownText(rawAccumulated, true);
        finalizeResponseCard(assistantRow, cardFooterDiv, citations, externalSource, recommendations, timeStr);
      }
    }, 50);

  } catch (err) {
    if (cursorSpan) cursorSpan.remove();
    streamTextSpan.innerHTML = `❌ Terjadi kesalahan jaringan: ${err.message}`;
  }
}

// -------------------------------------------------------------
// MARKDOWN & SUB-CARD PARSER (MATCHING MOCKUP 2 & 4)
// -------------------------------------------------------------
function formatMarkdownText(text, isFinal = false) {
  if (!text) return '';

  let clean = text.replace(/<!--\s*RECS:.*?-->/gs, '');

  // 1. Convert Markdown Tables into Styled Subcards
  clean = clean.replace(/(\|.+?\|\n\|[-:| ]+?\|\n(?:\|.+?\|\n?)+)/g, (match) => {
    const lines = match.trim().split('\n');
    if (lines.length < 3) return match;

    const rows = lines.slice(2);
    let tableHtml = '<div class="inner-subcard"><div class="subcard-header"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> <span>Linimasa Penting / Ketentuan Kunci</span></div><table class="subcard-table">';

    rows.forEach(r => {
      const cols = r.split('|').map(c => c.trim()).filter(c => c.length > 0);
      if (cols.length >= 2) {
        tableHtml += `<tr><td class="col-event">• ${escapeHtml(cols[0])}</td><td class="col-date">${escapeHtml(cols[1])}</td></tr>`;
      } else if (cols.length === 1) {
        tableHtml += `<tr><td class="col-event">• ${escapeHtml(cols[0])}</td><td></td></tr>`;
      }
    });

    tableHtml += '</table></div>';
    return tableHtml;
  });

  // 2. Format Headings
  clean = clean.replace(/^###\s+(.*$)/gm, '<h4 style="margin: 12px 0 6px 0; color: var(--accent-blue); font-weight: 700;">$1</h4>');
  clean = clean.replace(/^##\s+(.*$)/gm, '<h3 style="margin: 14px 0 8px 0; color: var(--text-primary); font-weight: 800;">$1</h3>');

  // 3. Format Bold & Italic
  clean = clean.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  clean = clean.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // 4. Format Bullet lists
  clean = clean.replace(/^\s*[-•]\s+(.*)$/gm, '<li style="margin-left: 20px; line-height: 1.6;">$1</li>');

  // 5. Paragraph linebreaks
  clean = clean.replace(/\n\n/g, '<br><br>');
  clean = clean.replace(/\n/g, '<br>');

  return clean;
}

function finalizeResponseCard(row, footerDiv, citations, externalSource, recs, timeStr) {
  let citationsHtml = '';
  if (citations && citations.length > 0) {
    const primary = citations[0];
    citationsHtml = `
      <div class="sources-block">
        <span class="sources-label">Sumber Resmi:</span>
        <a href="${primary.url || 'https://unpam.ac.id'}" target="_blank" class="source-citation-badge">
          📌 ${escapeHtml(primary.title)} (${escapeHtml(primary.decree)}) ↗
        </a>
      </div>
    `;
  } else if (externalSource) {
    citationsHtml = `
      <div class="sources-block">
        <span class="sources-label">Sumber Eksternal Resmi:</span>
        <a href="${externalSource.source_url}" target="_blank" class="source-citation-badge">
          🌐 ${escapeHtml(externalSource.source_title)} ↗
        </a>
      </div>
    `;
  }

  footerDiv.style.display = 'block';
  footerDiv.innerHTML = `
    ${citationsHtml}
    <span class="message-time">${timeStr}</span>
  `;

  // Render 3 Action Recommendation Chips beneath the card
  if (recs && recs.length > 0) {
    const recsWrap = document.createElement('div');
    recsWrap.className = 'recommendation-chips-wrap';
    recs.slice(0, 3).forEach(recText => {
      const chip = document.createElement('button');
      chip.className = 'rec-chip-btn';
      chip.textContent = recText;
      chip.addEventListener('click', () => {
        submitUserPrompt(recText);
      });
      recsWrap.appendChild(chip);
    });

    row.parentNode.insertBefore(recsWrap, row.nextSibling);
  }

  scrollToBottom();
}

function scrollToBottom() {
  const container = document.getElementById('chat-messages');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

function resetToDefaultWelcome() {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  const topicLabel = document.getElementById('chat-topic-label');
  if (topicLabel) topicLabel.textContent = 'Konsultasi Akademik';

  const logoSrc = AppState.theme === 'dark' 
    ? '/static/images/VIKA Logo Dark Mode.png' 
    : '/static/images/Logo VIKA Light mode.png';

  chatMessages.innerHTML = `
    <div class="message-row-assistant">
      <div class="bot-avatar-circle">
        <img src="${logoSrc}" alt="VIKA" class="bot-avatar-img">
      </div>
      <div class="assistant-response-card">
        <div class="assistant-text-content">
          <strong>Halo! Saya VIKA, Asisten Akademik Resmi Universitas Pamulang.</strong><br><br>
          Silakan tanyakan apa saja seputar jadwal perkuliahan, SK kalender akademik 2026/2027, aturan presensi UAS ≥ 75%, prosedur cuti, atau panduan Tugas Akhir/Skripsi Teknik Informatika.
        </div>
        <div class="card-footer-meta" style="display: block;">
          <span class="message-time">${getCurrentTime()}</span>
        </div>
      </div>
    </div>
    <div class="recommendation-chips-wrap">
      <button class="rec-chip-btn" onclick="submitUserPrompt('Kapan saja linimasa SK Kalender Akademik 2026/2027 UNPAM?')">Linimasa Kalender 2026/2027</button>
      <button class="rec-chip-btn" onclick="submitUserPrompt('Berapa batas minimal presensi kehadiran UAS?')">Syarat Kehadiran UAS (≥ 75%)</button>
      <button class="rec-chip-btn" onclick="submitUserPrompt('Apa saja syarat ujian sidang skripsi Teknik Informatika?')">Syarat Sidang Skripsi TI</button>
    </div>
  `;
}

// -------------------------------------------------------------
// REAL SESSION HISTORY STORAGE
// -------------------------------------------------------------
function saveSessionToHistory(promptText) {
  let sessions = [];
  try {
    sessions = JSON.parse(localStorage.getItem('vika_chat_sessions') || '[]');
  } catch (e) {
    sessions = [];
  }

  const shortTitle = promptText.length > 28 ? promptText.slice(0, 26) + '...' : promptText;
  
  // Avoid duplicate consecutively
  if (sessions.length > 0 && sessions[0].query === promptText) return;

  sessions.unshift({
    id: Date.now(),
    title: shortTitle,
    query: promptText,
    timestamp: 'Baru saja',
  });

  // Limit to 10 sessions
  if (sessions.length > 10) sessions = sessions.slice(0, 10);
  localStorage.setItem('vika_chat_sessions', JSON.stringify(sessions));

  renderRealSessionHistory();
}

function renderRealSessionHistory() {
  const container = document.getElementById('sidebar-history-list');
  if (!container) return;

  let sessions = [];
  try {
    sessions = JSON.parse(localStorage.getItem('vika_chat_sessions') || '[]');
  } catch (e) {
    sessions = [];
  }

  if (sessions.length === 0) {
    container.innerHTML = `<div class="history-empty-note">Belum ada riwayat percakapan.</div>`;
    return;
  }

  container.innerHTML = '';
  sessions.forEach(sess => {
    const item = document.createElement('div');
    item.className = 'history-item';
    item.dataset.query = sess.query;
    item.innerHTML = `
      <div class="history-item-content">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        <span>${escapeHtml(sess.title)}</span>
      </div>
      <span class="history-time">${sess.timestamp}</span>
    `;

    item.addEventListener('click', () => {
      window.switchView('chat');
      submitUserPrompt(sess.query);
    });

    container.appendChild(item);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
