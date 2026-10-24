# 🎓 UNPAM Academic Chatbot
> **Chatbot Asisten Akademik & Layanan Mahasiswa Cerdas Universitas Pamulang**  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8*

---

## 📌 Tentang Proyek

**UNPAM Academic Chatbot** adalah aplikasi chatbot interaktif berbasis web yang dibangun untuk mempermudah puluhan ribu mahasiswa Universitas Pamulang (UNPAM) dalam memperoleh rujukan informasi akademik yang akurat, cepat, dan transparan.

Aplikasi ini menggunakan model **Google Gemini 3.8 Flash** yang dihubungkan langsung dengan basis pengetahuan resmi kampus (Kalender Akademik 2026/2027, Buku Pedoman Akademik, SOP LAK, dan Pedoman FILKOM) tanpa biaya sama sekali (**100% Zero-Cost**).

---

## 🚀 Fitur Utama

- 💬 **Streaming Real-time Chat:** Respon Gemini mengalir halus kata-per-kata layaknya ChatGPT/Claude.
- 🎭 **Parameter Gaya Bahasa (Persona Selector):**
  - **Kating Ramah:** Bahasa santai, akrab, dan suportif khas obrolan sesama mahasiswa.
  - **Formal Birokrat:** Bahasa resmi, baku, dan lugas mengedepankan pasal SK Rektor.
  - **Ringkas:** Ringkasan to-the-point dan checklist esensial.
- 🎯 **Filter Domain Cakupan:** Pilihan fokus regulasi Universitas (Umum) vs Fakultas Ilmu Komputer (FILKOM / Teknik Informatika).
- ⚡ **Quick Action Starter Chips:** Tombol pertanyaan cepat satu klik seputar KRS, batas absen 75% UAS, prosedur cuti, dan MBKM.
- 📚 **Anti-Halusinasi & Sitasi Dokumen:** Setiap respon faktual menyertakan rujukan dokumen resmi.
- 💾 **Multi-Turn Memory & Export:** Menjaga konteks percakapan berkelanjutan dan opsi unduh riwayat chat ke format Markdown/TXT.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/) (dengan Custom CSS Theming modern)
- **LLM Engine:** [Google Gemini 3.8 Flash](https://aistudio.google.com/) via Google GenAI SDK
- **Language:** Python 3.10+
- **Version Control & Branching:** Git Flow (`main`, `develop`, `feature/*`)
- **Deployment:** Streamlit Community Cloud (Gratis & terintegrasi dengan GitHub)

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
git clone https://github.com/USERNAME_KAMU/unpam-academic-chatbot.git
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
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-3.8-flash
```

### 5. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser pada alamat `http://localhost:8501`.

---

## 🌿 Alur Git Flow

Proyek ini menerapkan standar percabangan Git Flow yang rapi:
- **`main`**: Branch produksi bersih (hanya commit awal dan rilis versi final).
- **`develop`**: Branch utama integrasi seluruh fitur.
- **`feature/*`**: Branch pengerjaan fitur individual (misal: `feature/ui-theming`, `feature/gemini-api`, `feature/knowledge-base`).

---

## 📄 Lisensi
Dikembangkan untuk keperluan Final Project Hacktiv8 — *LLM-Based Tools and Gemini API Integration for Data Scientists*.
