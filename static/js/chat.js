/**
 * VIKA Chat Streaming & Message Renderer
 * Implements Real-time Server-Sent Events (SSE), response cards, inner sub-cards,
 * official citation badges, and action recommendation chips.
 * Author: Abu Ziyad Al Katani (zydalz)
 */

document.addEventListener('DOMContentLoaded', () => {
  initChatEngine();
});

function initChatEngine() {
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input-field');
  const chatSendBtn = document.getElementById('btn-chat-send');
  const landingInput = document.getElementById('landing-input-field');
  const landingSendBtn = document.getElementById('btn-landing-send');
  const newChatBtn = document.getElementById('btn-new-chat');

  // Send from Chat view input
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

  // Send from Landing view input
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
  document.querySelectorAll('.topic-card').forEach(card => {
    card.addEventListener('click', () => {
      const prompt = card.dataset.prompt;
      if (prompt) {
        window.switchView('chat');
        submitUserPrompt(prompt);
      }
    });
  });

  // New Chat Button
  if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
      resetChatMessages();
    });
  }

  // Sidebar History Item Click
  document.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const query = item.dataset.query;
      if (query) {
        window.switchView('chat');
        submitUserPrompt(query);
      }
    });
  });
}

function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
}

// -------------------------------------------------------------
// CHAT SUBMISSION & STREAMING
// -------------------------------------------------------------
async function submitUserPrompt(promptText) {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  const timeStr = getCurrentTime();

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

  // 2. Create Placeholder for Assistant Response Card
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
      <div class="assistant-text-content"><span class="typing-cursor">Sedang mencari rujukan resmi...</span></div>
      <div class="card-footer-meta" style="display: none;"></div>
    </div>
  `;
  chatMessages.appendChild(assistantRow);
  scrollToBottom();

  const textContentDiv = assistantRow.querySelector('.assistant-text-content');
  const cardFooterDiv = assistantRow.querySelector('.card-footer-meta');

  // 3. Call Streaming API
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
      textContentDiv.innerHTML = `❌ Gagal menghubungi server: ${errText}`;
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let accumulatedText = '';
    let citations = [];
    let recommendations = [];
    let externalSource = null;

    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // keep unfinished line

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const dataStr = line.replace('data: ', '').trim();
        if (dataStr === '[DONE]') break;

        try {
          const parsed = JSON.parse(dataStr);
          if (parsed.type === 'token') {
            accumulatedText += parsed.content;
            textContentDiv.innerHTML = formatMarkdownContent(accumulatedText);
            scrollToBottom();
          } else if (parsed.type === 'meta') {
            citations = parsed.citations || [];
            recommendations = parsed.recommendations || [];
            externalSource = parsed.external_source;
          }
        } catch (e) {
          // Plain text fallback
          accumulatedText += dataStr;
          textContentDiv.innerHTML = formatMarkdownContent(accumulatedText);
        }
      }
    }

    // Finalize card with citations and recommendations
    finalizeResponseCard(assistantRow, textContentDiv, cardFooterDiv, citations, externalSource, recommendations, timeStr);

  } catch (err) {
    textContentDiv.innerHTML = `❌ Terjadi kesalahan jaringan: ${err.message}`;
  }
}

// -------------------------------------------------------------
// RESPONSE FORMATTING & SUB-CARDS
// -------------------------------------------------------------
function finalizeResponseCard(row, textDiv, footerDiv, citations, externalSource, recs, timeStr) {
  // Format narrative with smart sub-card detection
  let rawHtml = formatMarkdownContent(textDiv.textContent || textDiv.innerText);

  // If there's a list with dates or key points, enhance into styled table
  textDiv.innerHTML = rawHtml;

  // Build Citations block
  let citationsHtml = '';
  if (citations && citations.length > 0) {
    const primary = citations[0];
    citationsHtml = `
      <div class="sources-block">
        <span class="sources-label">Sumber:</span>
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

  // Render 3 Action Recommendation Chips beneath card
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

function formatMarkdownContent(text) {
  if (!text) return '';

  // Clean raw recs tags
  let clean = text.replace(/<!--\s*RECS:.*?-->/gs, '').trim();

  // Highlight Linimasa Penting if detected
  if (clean.includes('Linimasa Penting') || clean.includes('Ketentuan Utama')) {
    clean = clean.replace(
      /(Linimasa Penting|Ketentuan Utama|Jadwal Penting)/gi,
      `<div class="subcard-header"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 8v4l3 3M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg> $1</div>`
    );
  }

  // Basic markdown bold, list, paragraphs
  clean = clean.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  clean = clean.replace(/\*(.*?)\*/g, '<em>$1</em>');
  clean = clean.replace(/^\s*[-•]\s+(.*)$/gm, '<li>$1</li>');
  clean = clean.replace(/(<li>.*<\/li>)/s, '<ul style="margin-left: 20px; margin-top: 6px;">$1</ul>');
  clean = clean.replace(/\n\n/g, '<br><br>');

  return clean;
}

function scrollToBottom() {
  const container = document.getElementById('chat-messages');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

function resetChatMessages() {
  const chatMessages = document.getElementById('chat-messages');
  if (!chatMessages) return;

  chatMessages.innerHTML = `
    <div class="message-row-assistant">
      <div class="bot-avatar-circle">
        <img src="${AppState.theme === 'dark' ? '/static/images/VIKA Logo Dark Mode.png' : '/static/images/Logo VIKA Light mode.png'}" alt="VIKA" class="bot-avatar-img">
      </div>
      <div class="assistant-response-card">
        <div class="assistant-text-content">
          <strong>Halo! Saya VIKA, Asisten Akademik Resmi Universitas Pamulang.</strong><br><br>
          Ada yang bisa saya bantu terkait jadwal perkuliahan, SK kalender akademik 2026/2027, aturan presensi UAS ≥ 75%, prosedur cuti, atau panduan Tugas Akhir/Skripsi Teknik Informatika?
        </div>
        <div class="card-footer-meta" style="display: block;">
          <span class="message-time">${getCurrentTime()}</span>
        </div>
      </div>
    </div>
    <div class="recommendation-chips-wrap">
      <button class="rec-chip-btn" onclick="submitUserPrompt('Kapan jadwal UAS semester ganjil?')">Jadwal UAS Ganjil</button>
      <button class="rec-chip-btn" onclick="submitUserPrompt('Berapa syarat SKS untuk memprogram skripsi?')">Syarat SKS Skripsi</button>
      <button class="rec-chip-btn" onclick="submitUserPrompt('Bagaimana prosedur pengajuan cuti kuliah?')">Prosedur Cuti Kuliah</button>
    </div>
  `;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
