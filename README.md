# 🎓 VIKA — UNPAM Academic Chatbot
> **Virtual Interactive Knowledge Assistant — Asisten Akademik Universitas Pamulang**  
> *Tagline: "Selalu Ada untuk Jawaban Akademikmu"*  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8*

<p align="center">
  <img src="assets/images/VIKA Logo Brand.png" alt="VIKA Brand Logo" width="160" style="border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit" alt="Streamlit" />
  <img src="https://img.shields.io/badge/LLM-Gemini%203.8%20Flash-4285F4?logo=google" alt="Gemini 3.8 Flash" />
  <img src="https://img.shields.io/badge/Knowledge%20Base-4%20Official%20Decrees-10B981" alt="Knowledge Base" />
  <img src="https://img.shields.io/badge/Git%20Flow-Strict-orange?logo=git" alt="Git Flow" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 📌 Tentang Proyek

**VIKA (Virtual Interactive Knowledge Assistant)** adalah portal web asisten akademik cerdas yang dirancang khusus untuk sivitas akademika Universitas Pamulang (UNPAM). 

Berbeda dari chatbot tanya-jawab umum, VIKA menerapkan prinsip **Strict Grounding & Anti-Halusinasi** yang mengacu langsung pada dokumen hukum dan pedoman resmi universitas (SK Rektor) yang masih berlaku untuk Tahun Akademik 2026/2027.

<p align="center">
  <img src="assets/images/UNPAM AI Interface Showcase Board.png" alt="VIKA Interface Showcase Board" width="850" style="border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08);" />
</p>

---

## 📚 Basis Dokumen Rujukan Resmi (4 Pilar Pengetahuan)

VIKA mengindeks 4 dokumen kebijakan resmi Universitas Pamulang secara komprehensif:

| No | Dokumen Target | Nomor SK / Dasar Hukum | Unit Penerbit | Fokus Rujukan Utama | Status Integrasi |
| :-: | :--- | :--- | :--- | :--- | :---: |
| **1** | **SK Kalender Akademik TA 2026/2027** | `SK Rektor No. 1694/A/UNPAM/KP/VII/2026` | LP3 / Rektorat UNPAM | Linimasa KRS, awal perkuliahan Reguler A/B/C, rentang UTS/UAS, pendaftaran susulan, libur semester, dan wisuda. | **100% Terverifikasi** |
| **2** | **Buku Pedoman Akademik Universitas Pamulang** | `SK Rektor No. 240/A/O/UNPAM/I/2020` | Rektorat / Unpam Press | Batas masa studi S1 (maksimal 14 semester), beban SKS (170 menit), hak & kewajiban mahasiswa, dan ketentuan Drop Out (DO). | **100% Terverifikasi** |
| **3** | **SOP Layanan Administrasi Akademik (LAK)** | `SK Rektor No. 240/A/O/UNPAM/I/2020` (Bab Evaluasi & Administrasi) | Biro LAK / Rektorat UNPAM | Ketentuan batas presensi 75% UAS, bobot penilaian (10:20:30:40), kuota remedial teaching (min 15 mhs), cuti kuliah (maks 2x), dan pindah kelas. | **100% Terverifikasi** |
| **4** | **Buku Pedoman Fakultas Ilmu Komputer (FILKOM)** | `SK Rektor No. 0269/A/UNPAM/KP/II/2026` | Dekanat FILKOM / S1 Informatika | Prinsip kurikulum OBE (Outcome-Based Education), profil lulusan S1 Teknik Informatika (144-146 SKS), syarat KP/Skripsi, dan konversi MBKM. | **100% Terverifikasi**<br>*(Dengan honest fallback)* |

> **Catatan Keterbukaan & Integritas Data:**  
> Untuk berkas teknis internal operasional yang berstatus privat (*restricted HTTP 401 pada cloud internal dekanat*), VIKA secara transparan menginfokan status dokumen dan mengarahkan mahasiswa ke Sekretariat S1 Teknik Informatika (Gedung Viktor Lantai 6, Tangerang Selatan).

---

## 🚀 Fitur Utama

- 💬 **Streaming Percakapan Real-Time:** Respon asisten dialirkan secara langsung (*word-by-word streaming*) untuk kenyamanan membaca layaknya mengetik langsung.
- 🎭 **3 Pilihan Gaya Bahasa (Persona):**
  - **Kating Ramah (Default):** Komunikatif, hangat (*"Halo Sobat UNPAM!"*), suportif, dan mudah dipahami oleh mahasiswa baru.
  - **Formal Birokrat:** Nada institusional, baku, merujuk langsung pada pasal dan nomor SK resmi kampus.
  - **Ringkas:** Berpoin padat (*to-the-point*) dan cepat dipahami, cocok untuk mahasiswa kelas karyawan (Reguler C).
- 🎯 **Filter Cakupan Domain:** Beralih antara fokus informasi umum Universitas vs Fakultas Ilmu Komputer (FILKOM).
- ⚡ **Starter Action Chips:** 4 kartu topik populer mahasiswa di beranda untuk memulai tanya jawab instan hanya dengan 1 klik:
  1. *Jadwal KRS & Perkuliahan*
  2. *Syarat Presensi UAS*
  3. *Ketentuan Cuti Kuliah*
  4. *Syarat Skripsi Informatika*
- 📌 **Kotak Sitasi Rujukan Resmi:** Setiap jawaban substantif menyertakan metadata dokumen rujukan (Nama SK, Nomor Keputusan, Unit Penerbit, dan Bagian Regulasi).
- 💾 **Riwayat Percakapan Multi-Turn & Ekspor:** Mengelola sesi percakapan independen dan opsi unduh riwayat konsultasi dalam format Markdown (`.md`).
- ⚙️ **Pengaturan Fleksibel & BYOK:** Mendukung konfigurasi model Gemini Flash (`gemini-3.8-flash` dengan fallback otomatis ke `gemini-2.5-flash` / `gemini-1.5-flash`) dan input API Key mandiri di menu Pengaturan.

---

## 🛠️ Arsitektur & Teknologi

```text
┌─────────────────────────────────────────────────────────────┐
│                    VIKA Web Application                     │
│                (Streamlit + Custom Modern CSS)              │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────┐┌──────────────────────────────┐
│     KnowledgeBase Engine    ││      GeminiService SDK       │
│  (Semantic Keyword Matcher  ││   (Google GenAI Streaming    │
│  & Official Document Index) ││    + Multi-Model Fallback)   │
└──────────────┬──────────────┘└──────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────┐┌──────────────────────────────┐
│  data/processed/*.md        ││   gemini-3.8-flash           │
│  - kalender_akademik_2026   ││   (Temperature: 0.3          │
│  - pedoman_akademik_unpam   ││    Grounding System Prompt)  │
│  - sop_administrasi_lak     │└──────────────────────────────┘
│  - pedoman_filkom_obe       │
└─────────────────────────────┘
```

- **Frontend:** Streamlit 1.66+ dengan Custom CSS tokens (Deep Navy `#0F2742`, Sky Blue `#38BDF8`, Light Blue `#E0F2FE`).
- **LLM Engine:** Google Gemini Flash (`gemini-3.8-flash` / `gemini-2.5-flash`) via `google-genai` SDK.
- **Data Ingestion:** `pypdf`, Markdown structured transcripts, Pydantic schemas.
- **Version Control:** Git Flow (`main`, `develop`, `feature/*`).

---

## 🗺️ Roadmap Pembangunan Proyek (5 Fase)

- [x] **Fase 1: Perencanaan & Inisialisasi Repositori**  
  Perumusan PRD, UI/UX Style Guide, Brand Identity VIKA, inisialisasi Git Flow di GitHub.
- [x] **Fase 2: Akuisisi & Kurasi Knowledge Base Dokumen**  
  Ekstraksi teks 116 halaman Buku Pedoman Akademik dan 8 halaman SK Kalender Akademik 2026/2027 ke format Markdown terstruktur pada `data/processed/` dan modul `src/knowledge_base.py`.
- [x] **Fase 3: Integrasi Gemini Service & Rekayasa Prompt VIKA**  
  Implementasi `src/config.py`, `src/prompts.py` (3 gaya persona & strict anti-hallucination guardrails), dan `src/gemini_service.py` (streaming + model fallback).
- [x] **Fase 4: Perancangan UI & Styling CSS Streamlit**  
  Pembuatan `assets/css/style.css`, halaman Landing Hero, Chat Workspace dengan bubble avatar, dan Settings View.
- [x] **Fase 5: Pengujian Terpadu & Rilis Final**  
  Verifikasi integrasi end-to-end, dokumentasi komprehensif, dan penggabungan release ke branch `main`.

---

## 📂 Struktur Direktori Proyek

```text
unpam-academic-chatbot/
├── .env.example             # Contoh format API Key
├── .gitignore               # Pengecualian file sensitif / cache
├── .streamlit/
│   └── config.toml          # Konfigurasi server Streamlit
├── PRD.md                   # Product Requirements Document
├── README.md                # Dokumentasi utama proyek
├── requirements.txt         # Dependensi Python
├── app.py                   # Aplikasi utama Streamlit
├── assets/
│   ├── css/
│   │   └── style.css        # Custom CSS styling modern academic AI
│   └── images/
│       ├── Logo UNPAM.png
│       ├── VIKA Logo Brand.png
│       ├── kampus viktor.jpg
│       └── UNPAM AI Interface Showcase Board.png
├── data/
│   ├── raw/                 # PDF asli resmi UNPAM (SK Rektor)
│   │   ├── buku_pedoman_akademik.pdf
│   │   └── kalender_akademik.pdf
│   └── processed/           # Transkrip markdown terstruktur & terverifikasi
│       ├── kalender_akademik_2026_2027.md
│       ├── pedoman_akademik_unpam.md
│       ├── sop_administrasi_akademik.md
│       └── pedoman_filkom_informatika.md
├── docs/
│   └── style-guide.md       # Panduan UI/UX dan token desain
└── src/
    ├── __init__.py
    ├── config.py            # Konfigurasi app, konstanta, starter chips
    ├── prompts.py           # Persona VIKA & strict grounding prompts
    ├── knowledge_base.py    # Modul retriever & metadata rujukan
    └── gemini_service.py    # Klien Google GenAI & streaming generator
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
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-3.8-flash
```
*(Catatan: Anda juga dapat memasukkan API Key secara langsung melalui menu **Pengaturan** di dalam aplikasi web).*

### 5. Jalankan Aplikasi Streamlit
```bash
streamlit run app.py
```
Buka peramban pada alamat: `http://localhost:8501`.

---

## 🌿 Standar Percabangan Git Flow

Proyek ini menerapkan standar percabangan Git Flow:
- **`main`**: Branch produksi bersih (hanya commit awal dan rilis versi final).
- **`develop`**: Branch utama integrasi seluruh tahapan fitur.
- **`feature/*`**: Branch pengerjaan fitur terisolasi:
  - `feature/knowledge-base`: Kurasi 4 dokumen & modul retriever.
  - `feature/gemini-service`: Rekayasa prompt, persona, dan Google GenAI SDK.
  - `feature/ui-interface`: Multi-view Streamlit UI & custom CSS.
  - `feature/integration-testing`: Pengujian menyeluruh & dokumentasi final.

---

## 📄 Lisensi
Dikembangkan untuk keperluan Final Project Hacktiv8 — *LLM-Based Tools and Gemini API Integration for Data Scientists*.
Seluruh data kebijakan mengacu pada dokumen resmi Universitas Pamulang.
