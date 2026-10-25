# 🎓 VIKA — UNPAM Academic Chatbot
> **Virtual Interactive Knowledge Assistant — Asisten Akademik Universitas Pamulang**  
> *Tagline: "Asisten Akademik UNPAM — Cepat, Mudah, dan Terpercaya"*  
> *Pengembang: Abu Ziyad Al Katani (`zydalz`)*  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8 Maju Bersama AI*

<p align="center">
  <img src="assets/images/VIKA Logo Dark Mode.png" alt="VIKA Brand Logo" width="105" style="border-radius: 50%; vertical-align: middle; margin-right: 16px; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);" />
  <img src="assets/images/maskot landing page.png" alt="Maskot VIKA" width="115" style="vertical-align: middle;" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Frontend-Modern%20SPA%20(HTML5%2FCSS3%2FJS)-E34F26?logo=html5" alt="Frontend" />
  <img src="https://img.shields.io/badge/LLM-Gemini%203.8%20Flash%20%7C%20Llama%203.3-4285F4?logo=google" alt="Gemini & Llama" />
  <img src="https://img.shields.io/badge/RAG-Hybrid%20Vector%20Retrieval-8B5CF6" alt="Hybrid Vector RAG" />
  <img src="https://img.shields.io/badge/Knowledge%20Base-7%20Official%20Decrees-10B981" alt="Knowledge Base" />
  <img src="https://img.shields.io/badge/Security-Admin%20PIN%20%2B%20Rate%20Limiter-EF4444" alt="Security Suite" />
  <img src="https://img.shields.io/badge/License-Academic%20Restricted-red" alt="License" />
</p>

---

## 📌 Tentang Proyek

**VIKA (Virtual Interactive Knowledge Assistant)** adalah asisten akademik virtual cerdas yang dirancang khusus untuk sivitas akademika Universitas Pamulang (UNPAM), khususnya mahasiswa Program Studi S1 Teknik Informatika (FILKOM/FTIK).

VIKA dibangun untuk memenuhi tugas akhir program **Hacktiv8: LLM-Based Tools and Gemini API Integration for Data Scientists (Maju Bersama AI)** dengan mengadopsi arsitektur **Hybrid Vector RAG (Retrieval-Augmented Generation)**:
1. **Pencarian Semantik Terstruktur & Vektor Hibrida:** Menggabungkan Dense Vector Embedding (`text-embedding-004`) dan Cosine Similarity dengan pencocokan kata kunci leksikal berbobot (BM25) untuk akurasi maksimal.
2. **Grounding & Anti-Halusinasi:** Memberikan jawaban akurat berbasis tanggal kalender, rincian biaya proposal skripsi, SOP project work, dan persyaratan SKS dengan sitasi transparan.
3. **Antarmuka Modern (Single Page Application):** Frontend responsif dengan Server-Sent Events (SSE) streaming, animasi typewriter, horizontal top fade, floating controls, mini-rail sidebar, dan tombol geser tema Terang/Gelap.
4. **Keamanan Berlapis:** Dilengkapi *Developer Admin PIN Gate* dan middleware pembatas laju permintaan (*Rate Limiting* `slowapi`).

---

## 📸 Tampilan Antarmuka Pengguna (UI Showcase)

### 1. Papan Antarmuka Lengkap (*Showcase Board*)
<p align="center">
  <img src="assets/images/UNPAM AI Interface Showcase Board.png" alt="VIKA Interface Showcase Board" width="850" style="border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.1);" />
</p>

### 2. Mode Tampilan: Terang (*Light Mode*) & Gelap (*Dark Mode*)
<p align="center">
  <img src="assets/images/UI Light Mode.png" alt="VIKA UI Mode Terang" width="430" style="border-radius: 10px; margin-right: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); vertical-align: top;" />
  <img src="assets/images/UI Dark Mode.png" alt="VIKA UI Mode Gelap" width="430" style="border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); vertical-align: top;" />
</p>

---

## 🧠 Arsitektur Hybrid Vector Retrieval & RAG Engine

VIKA mengimplementasikan modul mesin penelusuran hibrida (`src/vector_engine.py`) yang menggabungkan kekuatan **Dense Vector Semantic Search** dengan **Lexical BM25 Scoring**:

```
[ Pertanyaan Mahasiswa ]
          │
          ├───► 1. Dense Semantic Embedding (Google text-embedding-004 / Local Vectorizer)
          │            │
          │            ▼
          │     Cosine Similarity Math:  sim(u, v) = (u · v) / (||u|| * ||v||)
          │            │
          ├───► 2. Lexical Domain-Boosted Scoring (BM25 Keywords, Title Match, SKS/UAS terms)
          │            │
          ▼            ▼
[ Formula Hybrid Scoring ]:  Score_hybrid = α · Score_dense + (1 - α) · Score_lexical
          │
          ▼
[ Top-K Dokumen Rujukan Terpilih + Sitasi Resmi SK Kampus ]
```

### Formula Matematis
1. **Cosine Similarity ($L_2$-Normalized):**
   $$\text{CosineSimilarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2} = \mathbf{u} \cdot \mathbf{v} \quad (\in [0.0, 1.0])$$
2. **Weighted Hybrid Score:**
   $$\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Score}_{\text{dense}} + (1 - \alpha) \cdot \text{Score}_{\text{lexical\_norm}}$$
   *Default:* $\alpha = 0.55$ (55% bobot kemiripan semantik dense + 45% presisi kata kunci leksikal). Dapat diatur bebas melalui variabel lingkungan `HYBRID_ALPHA`.
3. **Persistent On-Disk Vector Cache:**
   Seluruh 38 chunk dokumen telah di-embedding dan disimpan permanen di berkas `data/processed/vector_embeddings.json` (1.2 MB), menjamin waktu mulai server instan (< 1 milidetik) dan ketahanan saat offline.

---

## 📚 Basis Dokumen Rujukan Resmi (7 Pilar Pengetahuan)

VIKA mengindeks 7 dokumen kebijakan resmi Universitas Pamulang (38 chunk terkurasi):

| No | Dokumen Target | Dasar Hukum / Nomor SK | Unit Penerbit | Fokus Rujukan Utama |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **SK Kalender Akademik TA 2026/2027** | `SK Rektor No. 1694/A/UNPAM/KP/VII/2026` | LP3 / Rektorat UNPAM | Linimasa KRS, awal perkuliahan Reguler A/B/C, rentang UTS/UAS, libur semester, dan wisuda. |
| **2** | **Buku Pedoman Akademik UNPAM** | `SK Rektor No. 240/A/O/UNPAM/I/2020` | Rektorat / Unpam Press | Batas masa studi S1 (maks 14 semester), beban SKS, hak & kewajiban, serta ketentuan Drop Out (DO). |
| **3** | **SOP Layanan Administrasi Akademik (LAK)** | `SK Rektor No. 240/A/O/UNPAM/I/2020` | Biro LAK / Rektorat UNPAM | Ketentuan batas presensi 75% UAS, bobot penilaian (10:20:30:40), kuota remedial, dan cuti kuliah (maks 2x). |
| **4** | **Buku Pedoman FILKOM** | `SK Rektor No. 0269/A/UNPAM/KP/II/2026` | Dekanat FILKOM / S1 TI | Kurikulum OBE, profil lulusan S1 Teknik Informatika (144–146 SKS), syarat KP/Skripsi, dan konversi MBKM. |
| **5** | **Pedoman Tugas Akhir, Skripsi & Jalur TI** | `SK Dekan & Arsip Resmi Prodi TI UNPAM` | Prodi S1 Teknik Informatika | Ketentuan skripsi 6 SKS ($\ge$ 122–130 SKS, bebas nilai E), jalur jurnal SINTA/Scopus, dan rekognisi MBKM. |
| **6** | **Info Pendaftaran Proposal Skripsi TA 2026-1** | `Pengumuman Resmi No. 2026-1/TI/UNPAM` | Prodi S1 Teknik Informatika | Jadwal sidang proposal 24–25 September 2026, 2 eksemplar naskah offline, biaya Smt 8 Rp 1.000.000 & denda Smt 9–14. |
| **7** | **SOP Ujian Akhir Jalur Project Work** | `SK & Keputusan Kaprodi S1 TI UNPAM` | Prodi S1 Teknik Informatika | Syarat mitra berbadan hukum, semester 7, tim 1–3 orang, alur 16 langkah KAK, MoA, sistem ftiunpam.com & MyUnpam. |

---

## 🛡️ Analisis Risiko & Mitigasi Keamanan Teknis

VIKA menerapkan mitigasi berlapis terhadap celah keamanan sistem berbasis AI:

| Jenis Celah | Risiko Utama | Solusi yang Diterapkan di VIKA | Status |
| :--- | :--- | :--- | :---: |
| **1. API Route Terbuka** | Kunci API bocor ke publik atau di-*scrape* bot crawler. | **Server-side Orchestration & Admin PIN Gate:** Pemanggilan AI murni di server Python. Kunci disamarkan (`AQ.A••••••••38Fg`), file `.env` diabaikan git, dan menu pengaturan dilindungi verifikasi Admin PIN (`ADMIN_PIN=2026`). | ✅ Terproteksi Penuh |
| **2. Spam / DoS Attack** | Kuota API habis (*rate limit*) dan server overload. | **Middleware `slowapi`:** Membatasi 20 request/menit untuk chat streaming dan 10 request/menit untuk verifikasi PIN admin. Mengembalikan respons HTTP 429 jika melebihi batas. | ✅ Termitigasi |
| **3. Prompt Injection** | Pembajakan peran (*jailbreak*), instruksi bocor, atau SARA. | **Strict Grounding & Prompt Leak Resistance:** Aturan Pasal 6 melarang model membocorkan instruksi internal atau bertindak di luar peran asisten akademik kampus. Query diisolasi di dalam blok `[PERTANYAAN MAHASISWA]`. | ✅ Teruji 100% Lulus |
| **4. Salah Informasi (*Hallucination*)** | Tanggal atau nominal biaya fiktif menyesatkan mahasiswa. | **Sampling Hyperparameters & Mandatory Citation:** Temperatur rendah (`0.2`), Top-P (`0.90`), wajib sitasi dokumen resmi, dan penolakan transparan jika informasi tidak tercantum di dokumen. | ✅ Teruji 100% Lulus |

---

## 💻 Panduan Instalasi & Menjalankan Lokal

### 1. Kloning Repositori & Masuk ke Direktori
```bash
git clone https://github.com/zydalz/unpam-academic-chatbot.git
cd unpam-academic-chatbot
```

### 2. Pasang Dependensi Python
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Variabel Lingkungan (`.env`)
Salin berkas template `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Isi konfigurasi Anda pada berkas `.env`:
```env
# Kunci API Model (Dapatkan gratis di https://aistudio.google.com/ & https://console.groq.com/)
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Security: Developer Admin PIN Gate (Pengaman menu ubah kunci API)
ADMIN_PIN=2026

# Data Science & AI Generation Hyperparameters (Anti-Hallucination)
LLM_TEMPERATURE=0.2
LLM_TOP_P=0.90
LLM_TOP_K=40
LLM_MAX_OUTPUT_TOKENS=2048

# Hybrid Vector Retrieval Hyperparameters
EMBEDDING_MODEL=text-embedding-004
HYBRID_ALPHA=0.55

# Server Port
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### 4. Jalankan Server Aplikasi
```bash
python app.py
```
Buka peramban Anda di: **`http://localhost:8000`**

---

## 🧪 Rangkaian Pengujian Otomatis (*Automated Test Suite*)

Untuk memverifikasi keandalan sistem secara independen, jalankan skrip pengujian berikut di terminal:

```bash
# 1. Uji Modul Hybrid Vector Embedding, Cosine Similarity, & Cache Disk
python scripts/test_hybrid_vector_engine.py

# 2. Uji Audit Keamanan Black-Box (Inspect Element, Prompt Injection, & Tamper Gate)
python scripts/test_security_audit.py

# 3. Uji Tiga Fitur Tambahan (Hyperparameters, Memory, & Rate Limiter slowapi)
python scripts/test_three_enhancements.py
```
*(Seluruh pengujian dirancang untuk berjalan otomatis dengan status `100% PASS`).*

---

## 📜 Riwayat Rilis (*Changelog*)

* **`v2.0.0` (Full-Stack Hybrid Vector RAG Release - Current):**
  - Transformasi arsitektur menjadi FastAPI Full-Stack Engine + Modern SPA (Vanilla CSS/JS) dengan SSE Streaming.
  - Integrasi modul Hybrid Vector Retrieval (`src/vector_engine.py`) dengan Cosine Similarity dan persistent cache JSON.
  - Perluasan basis pengetahuan menjadi 7 dokumen resmi (38 chunk terkurasi).
  - Pemasangan Developer Admin PIN Gate dan middleware pembatas frekuensi `slowapi`.
  - Penambahan multi-turn conversational memory dan parameter anti-halusinasi.
  - Penghalusan antarmuka: horizontal top fade gradient, floating input capsule, dan tema terang/gelap.
* **`v1.0.0` (MVP Foundation Prototype):**
  - Prototipe awal berbasis Streamlit dengan ekstraksi 4 dokumen umum UNPAM dan integrasi dasar Gemini API.

---

## ⚖️ Lisensi, Hak Cipta & Pernyataan Hukum (Disclaimer)

### 1. Hak Cipta Kode Sumber (*Source Code Copyright*)
Aplikasi ini dilindungi di bawah **Custom Academic & Non-Commercial Restrictive License**.  
Hak Cipta © 2026 **Abu Ziyad Al Katani (`zydalz`)**. Seluruh Hak Dilindungi Undang-Undang (*All Rights Reserved*).

* **Izin Evaluasi:** Diberikan secara cuma-cuma kepada instruktur, mentor, dan penguji program **Hacktiv8 Maju Bersama AI** serta penilai akademik untuk mengunduh, menguji, dan mengevaluasi sistem ini secara lokal untuk kepentingan penilaian studi.
* **Larangan Tegas (Anti-Plagiarisme & Anti-Rebranding):** DILARANG KERAS memodifikasi, me-*rebrand*, memperjualbelikan, atau menawarkan konsep/arsitektur sistem ini kepada pihak Universitas Pamulang, Yayasan Sasmita Jaya, atau institusi lain manapun tanpa izin tertulis dari pembuat asli (**Abu Ziyad Al Katani**).

### 2. Pernyataan Merek & Non-Afiliasi (*Trademark & Fair Use Notice*)
* Nama *"Universitas Pamulang"*, singkatan *"UNPAM"*, *"Fakultas Ilmu Komputer (FILKOM)"*, logo kampus, serta dokumen regulasi internal (SK Rektor, SK Dekan, SOP LAK) adalah hak kekayaan intelektual milik **Universitas Pamulang / Yayasan Sasmita Jaya**.
* Penggunaan nama, logo, dan rujukan dokumen dalam aplikasi ini dilakukan semata-mata untuk tujuan penelitian ilmiah, demonstrasi studi, dan pemanfaatan wajar akademik (*fair use* sesuai UU Hak Cipta No. 28 Tahun 2014 Pasal 44).
* **VIKA adalah proyek inovasi akademik independen** yang dikembangkan oleh mahasiswa dan **TIDAK berafiliasi secara komersial maupun mewakili pernyataan resmi pimpinan Universitas Pamulang**.

### 3. Batasan Tanggung Jawab (*Disclaimer of Liability*)
Jawaban yang dihasilkan AI bersumber dari dokumen yang tersedia saat sistem ini dikembangkan. Untuk urusan administrasi final perkuliahan, wisuda, atau yudisium, mahasiswa diwajibkan untuk selalu merujuk pada pengumuman resmi di portal MyUnpam atau loket sekretariat program studi terkait.
