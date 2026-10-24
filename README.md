# 🎓 VIKA — UNPAM Academic Chatbot
> **Virtual Interactive Knowledge Assistant — Asisten Akademik Universitas Pamulang**  
> *Tagline: "Selalu Ada untuk Jawaban Akademikmu"*  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8*

---

## 📌 Tentang Proyek

**VIKA (Virtual Interactive Knowledge Assistant)** adalah aplikasi asisten percakapan interaktif berbasis web yang dikembangkan untuk membantu mahasiswa Universitas Pamulang (UNPAM) mengeksplorasi dan memahami rujukan informasi perkuliahan.

Aplikasi ini dirancang untuk merujuk dokumen resmi kampus (seperti Kalender Akademik, Buku Pedoman Akademik, SOP LAK, dan Pedoman FILKOM) dengan memanfaatkan model **Google Gemini 3.8 Flash** via Google AI Studio (*free tier*) dan antarmuka **Streamlit**.

> **Catatan Validitas & Sumber:**  
> Jawaban yang disajikan sistem merujuk pada materi dokumen panduan yang dihimpun ke dalam basis pengetahuan aplikasi. Untuk keperluan administrasi resmi, mahasiswa tetap disarankan mengonfirmasi langsung ke pihak akademik atau portal resmi kampus terkait.

---

## 🚀 Fitur Utama

- 💬 **Streaming Percakapan Real-Time:** Respon asisten ditampilkan mengalir kata-per-kata untuk pengalaman membaca yang nyaman.
- 🎭 **Preferensi Gaya Bahasa (Tone Selector):**
  - **Kating Ramah:** Gaya bahasa santai dan komunikatif khas mahasiswa.
  - **Formal Birokrat:** Gaya bahasa baku dan formal merujuk klausul aturan resmi.
  - **Ringkas:** Penyajian poin-poin esensial secara to-the-point.
- 🎯 **Filter Cakupan Domain:** Pilihan fokus informasi tingkat Universitas (Umum) vs Fakultas Ilmu Komputer (FILKOM / Teknik Informatika).
- ⚡ **Starter Action Chips:** Rekomendasi topik umum di awal halaman untuk memudahkan pengguna memulai dialog.
- 📚 **Kutipan Dokumen Rujukan:** Menampilkan rujukan nama dokumen sumber yang mendasari jawaban asisten.
- 💾 **Memori Percakapan Multi-Turn & Ekspor:** Menjaga konteks dialog berkelanjutan dalam satu sesi dan opsi unduh riwayat percakapan.

---

## 🛠️ Tech Stack

- **Frontend & Web Framework:** [Streamlit](https://streamlit.io/) (dengan Custom CSS)
- **LLM Engine:** [Google Gemini 3.8 Flash](https://aistudio.google.com/) via Google GenAI SDK
- **Language:** Python 3.10+
- **Version Control & Branching:** Git Flow (`main`, `develop`, `feature/*`)
- **Hosting / Deployment:** Streamlit Community Cloud

---

## 🗺️ Tahapan Sederhana Pembangunan Proyek (Roadmap)

Proyek ini dibangun secara bertahap melalui 5 fase kerja yang terukur:

```text
[Fase 1: Perencanaan & Inisialisasi] (Selesai)
       │
       ▼
[Fase 2: Akuisisi & Kurasi Knowledge Base Dokumen]
       │
       ▼
[Fase 3: Integrasi Gemini Service & Rekayasa Prompt VIKA]
       │
       ▼
[Fase 4: Perancangan UI & Styling CSS Streamlit]
       │
       ▼
[Fase 5: Pengujian Terpadu & Rilis Final]
```

1. **Fase 1: Perencanaan & Inisialisasi (Selesai)**
   - Perumusan PRD, Style Guide, Brand Identity VIKA, dan setup Git Flow di GitHub.
2. **Fase 2: Akuisisi & Kurasi Knowledge Base Dokumen**
   - Menghimpun dokumen PDF/teks resmi UNPAM ke `data/raw/`.
   - Melakukan ekstraksi teks, normalisasi, dan pembuatan modul retriever di `src/knowledge_base.py`.
3. **Fase 3: Integrasi Gemini Service & Rekayasa Prompt VIKA**
   - Konfigurasi klien API Google GenAI menggunakan model `gemini-3.8-flash`.
   - Perancangan system prompt persona VIKA (tone formal/ramah/ringkas, filter cakupan, dan guardrails).
4. **Fase 4: Perancangan UI & Styling CSS Streamlit**
   - Implementasi stylesheet modern di `assets/css/style.css` sesuai brand identity VIKA.
   - Pembangunan tampilan multi-view: Landing Page, Chat Interface, dan Pengaturan.
5. **Fase 5: Pengujian Terpadu & Rilis Final**
   - Uji coba tanya-jawab berbagai skenario akademik, evaluasi konsistensi rujukan, final release merge ke branch `main`.

---

## 📂 Struktur Direktori

```text
unpam-academic-chatbot/
├── .env.example             # Template konfigurasi environment variables
├── .gitignore               # Daftar pengecualian file sensitif
├── PRD.md                   # Product Requirements Document
├── README.md                # Dokumentasi utama proyek
├── requirements.txt         # Daftar pustaka Python
├── assets/                  # File CSS dan gambar UI
│   ├── css/
│   └── images/
├── data/                    # Sumber pengetahuan resmi UNPAM
│   └── raw/
├── docs/                    # Panduan desain & dokumentasi pendukung
│   └── style-guide.md       # Panduan UI/UX dan Style Guide
└── src/                     # Source code modular
    ├── __init__.py
    ├── config.py            # Konfigurasi aplikasi & model
    ├── prompts.py           # System instruction & persona
    ├── gemini_service.py    # Integrasi API Gemini 3.8 Flash
    └── knowledge_base.py    # Modul pembaca & penelusuran regulasi
```

---

## ⚙️ Panduan Menjalankan Proyek Secara Lokal

### 1. Klon Repositori
```bash
git clone https://github.com/zydalz/unpam-academic-chatbot.git
cd unpam-academic-chatbot
```

### 2. Buat & Aktifkan Virtual Environment
```bash
python -m venv .venv
# Di Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Di macOS / Linux:
source .venv/bin/activate
```

### 3. Pasang Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key
Salin file `.env.example` menjadi `.env`, lalu masukkan API Key Google Gemini:
```bash
cp .env.example .env
```
Isi file `.env`:
```env
GEMINI_API_KEY=masukkan_api_key_disini
GEMINI_MODEL=gemini-3.8-flash
```

### 5. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Aplikasi akan terbuka pada peramban di alamat `http://localhost:8501`.

---

## 🌿 Alur Git Flow

Proyek ini menerapkan standar percabangan Git Flow yang rapi:
- **`main`**: Branch produksi bersih (hanya commit awal dan rilis versi final).
- **`develop`**: Branch utama integrasi seluruh fitur.
- **`feature/*`**: Branch pengerjaan fitur individual (misal: `feature/knowledge-base`, `feature/gemini-service`, `feature/ui-interface`).

---

## 📄 Lisensi
Dikembangkan untuk keperluan Final Project Hacktiv8 — *LLM-Based Tools and Gemini API Integration for Data Scientists*.
