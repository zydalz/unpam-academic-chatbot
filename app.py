"""VIKA (Virtual Interactive Knowledge Assistant) - Universitas Pamulang.

Official Academic Virtual Assistant Web Portal.
Built with Streamlit, Google GenAI SDK (gemini-3.8-flash), and Semantic Knowledge Base.
"""

from __future__ import annotations

import base64
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import streamlit as st

from src.config import (
    APP_FULL_NAME,
    APP_INSTITUTION,
    APP_NAME,
    APP_TAGLINE,
    ASSETS_CSS_DIR,
    ASSETS_IMAGES_DIR,
    MODEL_CANDIDATES,
    SCOPE_OPTIONS,
    STARTER_CHIPS,
    STYLE_OPTIONS,
)
from src.gemini_service import GeminiService
from src.knowledge_base import KnowledgeBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Page Configuration ---
st.set_page_config(
    page_title=f"{APP_NAME} - Asisten Akademik {APP_INSTITUTION}",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Helper: Load CSS & Images ---
def load_custom_css() -> None:
    """Inject custom CSS stylesheet."""
    css_file = ASSETS_CSS_DIR / "style.css"
    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def get_image_base64(image_path: Path) -> str:
    """Encode image to base64 for reliable in-line HTML embedding."""
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    ext = image_path.suffix.lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{encoded}"


# --- Session State Management ---
def init_session_state() -> None:
    """Initialize all application session state variables."""
    if "view" not in st.session_state:
        st.session_state["view"] = "landing"  # 'landing', 'chat', 'settings'

    if "kb" not in st.session_state:
        st.session_state["kb"] = KnowledgeBase()

    if "gemini_service" not in st.session_state:
        st.session_state["gemini_service"] = GeminiService(
            knowledge_base=st.session_state["kb"]
        )

    if "tone" not in st.session_state:
        st.session_state["tone"] = "Kating Ramah"

    if "scope" not in st.session_state:
        st.session_state["scope"] = "all"

    if "conversations" not in st.session_state:
        # Default starter conversation
        st.session_state["conversations"] = {
            "session_default": {
                "id": "session_default",
                "title": "Percakapan Baru",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": [],
            }
        }
        st.session_state["active_session_id"] = "session_default"

    if "active_session_id" not in st.session_state:
        st.session_state["active_session_id"] = "session_default"

    if "pending_query" not in st.session_state:
        st.session_state["pending_query"] = None


# --- Navigation Bar Component ---
def render_navbar() -> None:
    """Render consistent header navbar across views."""
    logo_path = ASSETS_IMAGES_DIR / "VIKA Logo Brand.png"
    logo_base64 = get_image_base64(logo_path)

    col_brand, col_nav = st.columns([3, 2], vertical_alignment="center")

    with col_brand:
        html = f"""
        <div style="display: flex; align-items: center; gap: 14px;">
            <img src="{logo_base64}" style="width: 44px; height: 44px; border-radius: 10px; object-fit: contain; box-shadow: 0 2px 6px rgba(0,0,0,0.08);" />
            <div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0F2742; letter-spacing: -0.02em;">{APP_NAME} <span style="font-size: 0.85rem; font-weight: 600; color: #38BDF8; background: #E0F2FE; padding: 2px 8px; border-radius: 99px;">v1.0 • TA 2026/2027</span></div>
                <div style="font-size: 0.8rem; color: #64748B;">{APP_FULL_NAME} • {APP_INSTITUTION}</div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    with col_nav:
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🏠 Beranda", key="nav_home", use_container_width=True):
                st.session_state["view"] = "landing"
                st.rerun()
        with c2:
            if st.button("💬 Konsultasi", key="nav_chat", use_container_width=True):
                st.session_state["view"] = "chat"
                st.rerun()
        with c3:
            if st.button("⚙️ Pengaturan", key="nav_settings", use_container_width=True):
                st.session_state["view"] = "settings"
                st.rerun()

    st.markdown("<hr style='margin: 12px 0 20px 0; border-color: #DCE7F1;' />", unsafe_allow_html=True)


# --- View 1: Landing Page ---
def render_landing_view() -> None:
    """Render the modern editorial landing page with hero banner and topic cards."""
    # Hero Section
    banner_path = ASSETS_IMAGES_DIR / "kampus viktor.jpg"
    banner_base64 = get_image_base64(banner_path)

    hero_html = f"""
    <div style="
        position: relative;
        background: linear-gradient(135deg, rgba(15, 39, 66, 0.92) 0%, rgba(30, 58, 95, 0.88) 100%), url('{banner_base64}');
        background-size: cover;
        background-position: center;
        border-radius: 20px;
        padding: 48px 36px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(15, 39, 66, 0.15);
        text-align: center;
    ">
        <div style="display: inline-block; background: rgba(56, 189, 248, 0.2); border: 1px solid rgba(56, 189, 248, 0.4); color: #38BDF8; font-size: 0.8rem; font-weight: 700; padding: 4px 14px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px;">
            ✦ Portal Asisten Akademik Resmi Sivitas UNPAM
        </div>
        <h1 style="font-size: 2.5rem; font-weight: 800; color: #FFFFFF; margin-bottom: 12px; letter-spacing: -0.02em;">
            {APP_TAGLINE}
        </h1>
        <p style="font-size: 1.05rem; color: #E2E8F0; max-width: 680px; margin: 0 auto 24px auto; line-height: 1.6;">
            Temukan jawaban presisi seputar linimasa kalender akademik, syarat batas presensi 75% UAS, prosedur pengajuan cuti kuliah, hingga kurikulum OBE S1 Teknik Informatika berbasis SK Rektor resmi.
        </p>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # Quick Starter Input Bar
    st.markdown("### 🔍 Mulai Konsultasi Cepat")
    col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
    with col_input:
        quick_query = st.text_input(
            label="Ketik pertanyaan akademik Anda:",
            placeholder="Contoh: Kapan jadwal pendaftaran ujian susulan UTS Gasal 2026?",
            key="landing_search_input",
            label_visibility="collapsed",
        )
    with col_btn:
        if st.button("Tanya VIKA 🚀", key="btn_landing_submit", use_container_width=True):
            if quick_query.strip():
                st.session_state["pending_query"] = quick_query.strip()
                st.session_state["view"] = "chat"
                st.rerun()

    # Topic Cards (Quick Action Chips)
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📌 Topik Populer Mahasiswa")
    st.caption("Klik topik di bawah ini untuk konsultasi otomatis dengan data terverifikasi:")

    cols = st.columns(4)
    for idx, chip in enumerate(STARTER_CHIPS):
        with cols[idx]:
            card_html = f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #DCE7F1;
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 12px;
                height: 140px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 4px 12px rgba(15, 39, 66, 0.03);
            ">
                <div>
                    <div style="font-size: 0.72rem; font-weight: 700; color: #2563EB; text-transform: uppercase;">{chip['category']}</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #0F2742; margin-top: 4px;">{chip['label']}</div>
                </div>
                <div style="font-size: 0.78rem; color: #64748B; line-height: 1.3;">
                    {chip['prompt'][:65]}...
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            if st.button(
                f"Tanyakan Topik Ini ↗",
                key=f"chip_btn_{chip['id']}",
                use_container_width=True,
            ):
                st.session_state["pending_query"] = chip["prompt"]
                st.session_state["scope"] = chip.get("scope", "all")
                st.session_state["view"] = "chat"
                st.rerun()

    # Verified Knowledge Catalog Section
    st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📚 4 Basis Dokumen Rujukan Resmi Terintegrasi")
    docs = st.session_state["kb"].get_document_catalog()

    doc_cols = st.columns(2)
    for i, doc in enumerate(docs):
        with doc_cols[i % 2]:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #DCE7F1; border-left: 4px solid #38BDF8; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;">
                    <div style="font-weight: 700; font-size: 0.95rem; color: #0F2742;">{doc.title}</div>
                    <div style="font-size: 0.78rem; font-weight: 600; color: #2563EB; margin: 2px 0 6px 0;">{doc.decree_number} • {doc.publisher}</div>
                    <div style="font-size: 0.82rem; color: #64748B;">{doc.focus}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# --- View 2: Chat Interface ---
def render_chat_view() -> None:
    """Render the interactive multi-turn chat consultation interface."""
    active_session_id = st.session_state["active_session_id"]
    current_session = st.session_state["conversations"][active_session_id]

    # --- Top Bar Controls in Workspace ---
    col_scope, col_tone, col_export = st.columns([2, 2, 2], vertical_alignment="center")

    with col_scope:
        scope_choice = st.selectbox(
            "Cakupan Kebijakan:",
            options=list(SCOPE_OPTIONS.keys()),
            format_func=lambda x: SCOPE_OPTIONS[x],
            index=list(SCOPE_OPTIONS.keys()).index(st.session_state.get("scope", "all")),
            key="chat_scope_selector",
        )
        st.session_state["scope"] = scope_choice

    with col_tone:
        tone_choice = st.selectbox(
            "Gaya Bahasa (Persona):",
            options=list(STYLE_OPTIONS.keys()),
            index=list(STYLE_OPTIONS.keys()).index(st.session_state.get("tone", "Kating Ramah")),
            key="chat_tone_selector",
        )
        st.session_state["tone"] = tone_choice

    with col_export:
        # Export conversation as markdown file
        if current_session["messages"]:
            chat_export_text = f"# Riwayat Konsultasi Akademik UNPAM - {APP_NAME}\n"
            chat_export_text += f"Tanggal: {datetime.now().strftime('%d %B %Y %H:%M')}\n"
            chat_export_text += f"Persona: {tone_choice} | Cakupan: {SCOPE_OPTIONS[scope_choice]}\n\n---\n\n"
            for m in current_session["messages"]:
                role_label = "MAHASISWA" if m["role"] == "user" else "VIKA (ASISTEN AKADEMIK)"
                chat_export_text += f"### {role_label}\n{m['content']}\n\n"

            st.download_button(
                label="📥 Unduh Riwayat Chat (.md)",
                data=chat_export_text,
                file_name=f"konsultasi_vika_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.button("📥 Unduh Riwayat Chat", disabled=True, use_container_width=True)

    st.markdown("<hr style='margin: 10px 0 20px 0; border-color: #DCE7F1;' />", unsafe_allow_html=True)

    # --- Message History Rendering ---
    logo_path = ASSETS_IMAGES_DIR / "VIKA Logo Brand.png"
    logo_base64 = get_image_base64(logo_path)

    for msg in current_session["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                    <div class="vika-user-bubble">
                        {msg["content"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                    <img src="{logo_base64}" style="width: 36px; height: 36px; border-radius: 8px; object-fit: contain; flex-shrink: 0; margin-top: 4px;" />
                    <div class="vika-assistant-bubble">
                """,
                unsafe_allow_html=True,
            )
            st.markdown(msg["content"])

            # Render official citations if attached
            if "citations" in msg and msg["citations"]:
                with st.expander("📌 Rujukan Resmi Terverifikasi", expanded=False):
                    for cit in msg["citations"]:
                        st.markdown(
                            f"""
                            - **Dokumen:** {cit.get('doc_title', '-')}  
                              **Dasar Hukum:** `{cit.get('decree_number', '-')}`  
                              **Penerbit:** {cit.get('publisher', '-')}  
                              **Bagian:** *{cit.get('section', '-')}*
                            """
                        )

            st.markdown("</div></div>", unsafe_allow_html=True)

    # --- Handle Incoming Queries (Streamed) ---
    incoming_query = None

    # Check if we got a query passed from the landing page
    if st.session_state.get("pending_query"):
        incoming_query = st.session_state["pending_query"]
        st.session_state["pending_query"] = None
    else:
        user_input = st.chat_input("Ketik pertanyaan akademik seputar jadwal, presensi, cuti, atau kurikulum...")
        if user_input and user_input.strip():
            incoming_query = user_input.strip()

    if incoming_query:
        # Append user message
        current_session["messages"].append({"role": "user", "content": incoming_query})

        # Update conversation title if still default
        if current_session["title"] == "Percakapan Baru":
            snippet = incoming_query[:35] + ("..." if len(incoming_query) > 35 else "")
            current_session["title"] = snippet

        # Display user message immediately
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 16px;">
                <div class="vika-user-bubble">
                    {incoming_query}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Build context summary from prior turns
        history_summary_parts = []
        for past_msg in current_session["messages"][-6:-1]:
            role = "Mahasiswa" if past_msg["role"] == "user" else "VIKA"
            history_summary_parts.append(f"{role}: {past_msg['content'][:120]}")
        history_summary = "\n".join(history_summary_parts) if history_summary_parts else None

        # Call Gemini Service stream
        svc: GeminiService = st.session_state["gemini_service"]
        stream_gen, retrieved_results = svc.answer_query_stream(
            query=incoming_query,
            style=st.session_state["tone"],
            scope=st.session_state["scope"],
            chat_history_summary=history_summary,
        )

        st.markdown(
            f"""
            <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                <img src="{logo_base64}" style="width: 36px; height: 36px; border-radius: 8px; object-fit: contain; flex-shrink: 0; margin-top: 4px;" />
                <div class="vika-assistant-bubble">
            """,
            unsafe_allow_html=True,
        )

        # Stream response chunks live
        full_assistant_reply = st.write_stream(stream_gen)

        # Prepare structured citations
        citations_data = [res.citation for res in retrieved_results]
        if citations_data:
            with st.expander("📌 Rujukan Resmi Terverifikasi", expanded=True):
                for cit in citations_data:
                    st.markdown(
                        f"""
                        - **Dokumen:** {cit.get('doc_title', '-')}  
                          **Dasar Hukum:** `{cit.get('decree_number', '-')}`  
                          **Penerbit:** {cit.get('publisher', '-')}  
                          **Bagian:** *{cit.get('section', '-')}*
                        """
                    )

        st.markdown("</div></div>", unsafe_allow_html=True)

        # Save assistant message to session
        current_session["messages"].append({
            "role": "assistant",
            "content": full_assistant_reply,
            "citations": citations_data,
        })
        st.rerun()

    # Sticky Footer Disclaimer
    st.markdown(
        f"""
        <div class="vika-footer-disclaimer">
            💡 <strong>Ketentuan Integritas Data:</strong> Jawaban VIKA dirujuk langsung dari SK Rektor UNPAM No. 1694/2026, 240/2020, dan 0269/2026. Bot tidak melayani cek tagihan finansial personal atau manipulasi nilai KRS.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --- View 3: Settings Page ---
def render_settings_view() -> None:
    """Render application settings, API key management, and system information."""
    st.markdown("### ⚙️ Pengaturan & Konfigurasi Sistem")
    st.caption("Kelola kredensial API Gemini dan periksa status basis pengetahuan akademik.")

    svc: GeminiService = st.session_state["gemini_service"]

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### 🔑 Kredensial Gemini API Key")
        st.markdown(
            """
            VIKA menggunakan model **Google Gemini Flash** yang dapat digunakan secara **gratis** 
            melalui Google AI Studio tanpa biaya tambahan.
            """
        )

        current_key_display = svc.api_key if svc.api_key else ""
        masked_placeholder = ("••••••••" + current_key_display[-4:]) if len(current_key_display) > 8 else "Masukkan API Key Gemini..."

        api_input = st.text_input(
            "Masukkan Gemini API Key:",
            type="password",
            placeholder=masked_placeholder,
            help="Dapatkan API Key di https://aistudio.google.com/",
        )

        col_save, col_status = st.columns([1, 2], vertical_alignment="center")
        with col_save:
            if st.button("Simpan Kunci", key="btn_save_key"):
                if api_input.strip():
                    success = svc.update_api_key(api_input.strip())
                    if success:
                        st.success("✅ Kunci API berhasil disimpan dan siap digunakan!")
                    else:
                        st.warning("⚠️ Kunci API diperbarui, pastikan kunci memiliki izin akses yang valid.")
                    st.rerun()

        with col_status:
            if svc.is_configured():
                st.markdown("<span style='color: #15803D; font-weight: 700;'>● Kunci API Terhubung</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: #B45309; font-weight: 700;'>○ Belum Terhubung (Mode Pratinjau Rujukan)</span>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 20px 0; border-color: #DCE7F1;' />", unsafe_allow_html=True)

        st.markdown("#### 🤖 Konfigurasi Model AI")
        selected_model = st.selectbox(
            "Model Gemini Utama:",
            options=MODEL_CANDIDATES,
            index=0,
            help="Sistem secara cerdas akan beralih ke model fallback jika kuota atau latensi terjadi.",
        )
        svc.model_name = selected_model
        st.info(f"Model aktif saat ini: **{selected_model}**")

    with col_right:
        st.markdown("#### 📋 Status Basis Pengetahuan Resmi")
        docs = st.session_state["kb"].get_document_catalog()
        for doc in docs:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #DCE7F1; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #0F2742;">{doc.title}</div>
                    <div style="font-size: 0.75rem; color: #2563EB;">{doc.decree_number}</div>
                    <div style="font-size: 0.75rem; color: #15803D; margin-top: 4px;">✔ Terindeks ke dalam {len([c for c in st.session_state['kb'].chunks if c.doc_id == doc.doc_id])} bagian kebijakan</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# --- Sidebar Navigation & Conversation Manager ---
def render_sidebar() -> None:
    """Render sidebar for chat session switching and quick links."""
    with st.sidebar:
        logo_path = ASSETS_IMAGES_DIR / "Logo UNPAM.png"
        logo_base64 = get_image_base64(logo_path)

        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px 0 16px 0;">
                <img src="{logo_base64}" style="width: 70px; height: 70px; object-fit: contain; margin-bottom: 8px;" />
                <div style="font-size: 1.1rem; font-weight: 800; color: #0F2742;">{APP_NAME}</div>
                <div style="font-size: 0.76rem; color: #64748B;">{APP_INSTITUTION}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Primary Action: Start New Conversation
        if st.button("➕ Percakapan Baru", key="btn_new_chat", use_container_width=True):
            new_id = f"session_{len(st.session_state['conversations']) + 1}_{int(datetime.now().timestamp())}"
            st.session_state["conversations"][new_id] = {
                "id": new_id,
                "title": "Percakapan Baru",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": [],
            }
            st.session_state["active_session_id"] = new_id
            st.session_state["view"] = "chat"
            st.rerun()

        st.markdown("<hr style='margin: 12px 0; border-color: #DCE7F1;' />", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;'>Riwayat Percakapan</div>", unsafe_allow_html=True)

        # List existing sessions
        sessions = list(st.session_state["conversations"].values())
        sessions.reverse()  # Latest first

        for s in sessions:
            is_active = s["id"] == st.session_state["active_session_id"]
            btn_label = f"{'👉 ' if is_active else '💬 '}{s['title']}"
            if st.button(btn_label, key=f"session_btn_{s['id']}", use_container_width=True):
                st.session_state["active_session_id"] = s["id"]
                st.session_state["view"] = "chat"
                st.rerun()

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        st.caption(f"{APP_NAME} v1.0 • Hacktiv8 Final Project")


# --- Main Application Router ---
def main() -> None:
    """Main application entry point."""
    init_session_state()
    load_custom_css()
    render_sidebar()
    render_navbar()

    current_view = st.session_state.get("view", "landing")

    if current_view == "landing":
        render_landing_view()
    elif current_view == "chat":
        render_chat_view()
    elif current_view == "settings":
        render_settings_view()


if __name__ == "__main__":
    main()
