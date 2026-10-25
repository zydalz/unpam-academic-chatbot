# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Proyek: VIKA — Virtual Interactive Knowledge Assistant (UNPAM Academic Chatbot)

---

| Dokumen | Versi | Status | Tanggal Pembuatan | Author / Role |
| :--- | :---: | :---: | :---: | :--- |
| **PRD - VIKA Academic Assistant** | `2.0.0` | **Approved** | 24 Oktober 2026 | Abu Ziyad Al Katani (zydalz) |

---

## 1. Executive Summary & Visi Produk

### 1.1 Latar Belakang & Identitas Produk
Universitas Pamulang (UNPAM) memiliki basis mahasiswa yang besar dengan berbagai program perkuliahan (Reguler A, Reguler B, Reguler C/Kamis dan Sabtu). Dalam dinamika perkuliahan, mahasiswa kerap memerlukan rujukan cepat terkait jadwal akademik, ketentuan presensi ujian, prosedur administrasi cuti, serta pedoman kurikulum yang tercantum dalam dokumen resmi kampus.

Untuk memfasilitasi kebutuhan eksplorasi informasi tersebut, dirancanglah proyek **VIKA** (*Virtual Interactive Knowledge Assistant*).
- **Nama Produk:** VIKA (Virtual Interactive Knowledge Assistant)
- **Tagline:** *"Selalu Ada untuk Jawaban Akademikmu"*
- **Repositori:** `unpam-academic-chatbot`
- **Platform:** Standalone Web Portal (Streamlit dengan Custom CSS)

### 1.2 Visi Produk
Membangun portal web mandiri berbasis asisten percakapan AI yang membantu memetakan dan merujuk informasi perkuliahan dari dokumen panduan kampus. Sistem dirancang memanfaatkan *free-tier* Google AI Studio (Gemini 3.8 Flash) dan hosting komunitas Streamlit agar dapat diuji coba tanpa memerlukan biaya lisensi berbayar.

---

## 2. Ruang Lingkup Proyek (Scope of Work)

### 2.1 In-Scope (Cakupan Fitur yang Dikerjakan)
1. **Eksplorasi Informasi Linimasa Akademik:**
   - Jadwal pembayaran registrasi, pengisian dan revisi KRS Gasal & Genap (berdasarkan SK Kalender Akademik yang dihimpun).
   - Perkiraan linimasa perkuliahan aktif, pelaksanaan UTS, UAS, dan yudisium/wisuda.
2. **Rujukan Aturan Presensi & Kelayakan Ujian:**
   - Ketentuan batas kehadiran kuliah untuk syarat mengikuti UAS berdasarkan SOP LAK.
   - Prosedur umum permohonan izin/sakit dan batas waktu penyerahan surat keterangan.
   - Ketentuan umum dan alur pendaftaran Ujian Remedial / Susulan.
3. **Layanan Prosedural Administrasi Mahasiswa (SOP LAK):**
   - Rujukan alur permohonan cuti akademik dan batas maksimal semester yang diizinkan.
   - Prosedur pengaktifan kembali status mahasiswa setelah masa cuti.
   - Syarat umum permohonan Surat Keterangan Mahasiswa Aktif dan legalisir.
   - Prosedur pindah kelas (Reguler A/B/C) atau pindah program studi.
4. **Regulasi Akademik & Kurikulum (Pedoman Akademik & FILKOM):**
   - Ketentuan umum batas masa studi jenjang sarjana (S1).
   - Penjelasan bobot 1 SKS sesuai pedoman akademik yang berlaku.
   - Pengenalan prinsip Kurikulum Berbasis Capaian (OBE - *Outcome-Based Education*).
   - Ketentuan umum prasyarat akademik untuk Kerja Praktik (KP), Skripsi, dan magang MBKM.
5. **Parameter Kreatif & Kontrol Respons (Persona & Scope):**
   - **Gaya Bahasa (Tone):** 
     - *Kating Ramah:* Bahasa santai, komunikatif, suportif layaknya obrolan mahasiswa.
     - *Formal Birokrat:* Bahasa baku, lugas, mengedepankan kutipan ketentuan resmi.
     - *Ringkas (To-the-Point):* Hanya menyajikan poin inti/checklist esensial.
   - **Filter Domain:** Tingkat Universitas (Umum) vs Khusus FILKOM (Teknik Informatika).
   - **Multi-turn Memory:** Mempertahankan konteks obrolan dalam sesi aktif.
   - **Quick Action Starter Chips:** Rekomendasi pertanyaan cepat di awal interaksi.
   - **Fitur Export & Reset:** Unduh riwayat percakapan (Markdown/TXT) dan bersihkan sesi.

---

### 2.2 Out-of-Scope (Batasan Tegas di Luar Tanggung Jawab Chatbot)
Untuk menjaga keamanan data privat dan mencegah salah kaprah fungsi, fitur berikut **TIDAK** didukung oleh chatbot:
1. **Transaksi Finansial & Cek Tagihan Personal:**
   - Bot *tidak* melayani pengecekan saldo tagihan SPP, nomor virtual account perorangan, atau riwayat pembayaran mahasiswa (karena membutuhkan akses database privat MyUnpam/Keuangan).
2. **Modifikasi Data Akademik & Input Nilai:**
   - Bot *tidak* dapat mengubah nilai, mengisi KRS otomatis, atau memproses persetujuan Dosen Pembimbing Akademik (DPA).
3. **Konsultasi Kampus di Luar UNPAM:**
   - Bot menolak menjawab pertanyaan spesifik universitas lain di luar ekosistem UNPAM.
4. **Pertanyaan Umum Non-Akademik yang Tidak Relevan:**
   - Pertanyaan seputar politik, saran medis personal, atau hal umum di luar ranah pendidikan/kampus akan diarahkan kembali ke topik akademik.
5. **Mekanisme Fallback untuk Pertanyaan Out-of-Scope:**
   - Jika ditanya hal di luar ruang lingkup (misal tagihan SPP spesifik), bot wajib merespons:
     > *"Mohon maaf, informasi data privat tersebut berada di luar wewenang saya. Silakan periksa langsung melalui portal resmi MyUnpam (my.unpam.ac.id) atau hubungi loket Bagian Keuangan UNPAM."*

---

## 3. Target Referensi Data & Knowledge Base

Sistem chatbot dirancang untuk merujuk 4 dokumen panduan resmi kampus berikut:

| No | Dokumen Target | Unit Penerbit | Fokus Rujukan | Status Ketersediaan & Integrasi |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **SK Kalender Akademik TA 2026/2027** | LP3 / Rektorat UNPAM | Linimasa KRS, tanggal perkuliahan, rentang UTS/UAS, libur semester, dan wisuda. | **Tersedia Lengkap**<br>*(SK Rektor No. 1694/A/UNPAM/KP/VII/2026, diekstrak ke teks terstruktur)* |
| **2** | **Buku Pedoman Akademik Universitas Pamulang** | Rektorat / Unpam Press | Batas masa studi S1, hak & kewajiban mahasiswa, definisi SKS, dan etika akademik. | **Tersedia Lengkap**<br>*(SK Rektor No. 240/A/O/UNPAM/I/2020, 116 halaman)* |
| **3** | **SOP Layanan Administrasi Akademik (LAK)** | Biro LAK / Rektorat UNPAM | Ketentuan batas presensi UAS, remedial, pengajuan cuti kuliah, dan pindah kelas. | **Tersedia Lengkap**<br>*(Terintegrasi resmi pada Bab Ketentuan Perkuliahan & Evaluasi)* |
| **4** | **Buku Pedoman Fakultas Ilmu Komputer (FILKOM)** | Dekanat FILKOM / Informatika | Prinsip kurikulum OBE, penjurusan Informatika, syarat KP/Skripsi, dan magang MBKM. | **Akses Publik Terbatas**<br>*(Link portal resmi 401/izin akses; sistem menerapkan fallback aman)* |

> **Catatan Validitas & Pemrosesan Data:**  
> - Dokumen pindaian (*scanned image*) seperti Kalender Akademik diekstraksi ke format Markdown terstruktur pada `data/processed/` agar penelusuran kata kunci dan tanggal berlangsung instan dan tanpa kesalahan OCR saat runtime.
> - Jika informasi spesifik pada dokumen nomor 4 belum dapat diakses secara publik, chatbot wajib menyatakan batas pengetahuannya secara terbuka dan menyarankan mahasiswa mengonfirmasi langsung ke loket atau sekretariat terkait.

---

## 4. User Personas & User Stories

### 4.1 User Personas
* **Persona 1: Rian (Mahasiswa Baru S1 Informatika)**
  - *Karakteristik:* Baru memasuki dunia perkuliahan, membutuhkan adaptasi istilah akademik dan jadwal perkuliahan.
  - *Kebutuhan:* Penjelasan yang ramah, komunikatif (*kating style*), dan mudah dicerna.
* **Persona 2: Siti (Mahasiswa Kelas Reguler C / Karyawan)**
  - *Karakteristik:* Membagi waktu antara pekerjaan dan kuliah, membutuhkan informasi ringkas tanpa bertele-tele.
  - *Kebutuhan:* Informasi to-the-point mengenai linimasa ujian atau prosedur pengajuan cuti.
* **Persona 3: Dika (Mahasiswa Semester 6 Menjelang Skripsi & MBKM)**
  - *Karakteristik:* Sedang mempersiapkan rencana kelulusan dan kegiatan magang studi independen.
  - *Kebutuhan:* Penjelasan terstruktur mengenai aturan kurikulum OBE dan syarat administrasi fakultas.

### 4.2 User Stories & Acceptance Criteria (Gherkin Style)

#### US-01: Memilih Gaya Bahasa (Tone)
* **Sebagai** mahasiswa UNPAM,
* **Saya ingin** dapat memilih preferensi gaya bahasa interaksi (Formal, Kating Ramah, atau Ringkas),
* **Agar** penyampaian informasi terasa lebih nyaman sesuai konteks kebutuhan saya.
  - **Given** pengguna berada di antarmuka aplikasi,
  - **When** pengguna memilih preferensi gaya bahasa menjadi *"Kating Ramah"*,
  - **Then** respon jawaban berikutnya disesuaikan menggunakan sapaan akrab dan bahasa kasual yang sopan.

#### US-02: Menanyakan Ketentuan Presensi & UAS
* **Sebagai** mahasiswa,
* **Saya ingin** mengetahui ketentuan persentase absensi untuk mengikuti UAS,
* **Agar** saya dapat mengantisipasi kelayakan kepesertaan ujian.
  - **Given** sesi obrolan aktif dengan basis pengetahuan SOP LAK terhubung,
  - **When** pengguna menanyakan ketentuan minimal kehadiran untuk UAS,
  - **Then** chatbot menyajikan rujukan persentase kehadiran sesuai isi dokumen SOP LAK yang tersedia dan menyertakan nama dokumen sumber rujukan.

#### US-03: Quick Action Starter Chips
* **Sebagai** pengguna baru yang ingin mencoba fitur dengan cepat,
* **Saya ingin** melihat tombol rekomendasi topik populer di awal tampilan,
* **Agar** saya dapat memulai percakapan cukup dengan satu kali klik.
  - **Given** riwayat obrolan masih kosong (*initial state*),
  - **When** pengguna mengklik salah satu tombol topik (misal: *"Jadwal Pengisian KRS"*),
  - **Then** pertanyaan tersebut otomatis terkirim dan chatbot memproses respon berdasarkan data kalender akademik.

#### US-04: Chat Memory & Konteks Berkelanjutan
* **Sebagai** pengguna yang melakukan konsultasi bertahap,
* **Saya ingin** mengajukan pertanyaan lanjutan tanpa harus menulis ulang subjek utama,
* **Agar** percakapan terasa natural.
  - **Given** pengguna telah menanyakan prosedur pengajuan cuti kuliah,
  - **When** pengguna menanyakan pertanyaan lanjutan *"Lalu maksimal boleh berapa kali?"*,
  - **Then** chatbot memahami konteks pertanyaan sebelumnya dan merujuk ketentuan batas cuti dari dokumen yang tersedia.

---

## 5. Technical Requirements & Architecture

### 5.1 Tech Stack (Production-Grade Full-Stack Engine)
* **Backend Engine:** FastAPI (Python 3.10+) dengan Uvicorn ASGI Server & Server-Sent Events (SSE).
* **Frontend Interface:** Modern Single Page Application (HTML5, Vanilla CSS3 dengan CSS Design Tokens & Glassmorphism, Vanilla ES6 JavaScript).
* **AI & LLM Providers:** Dual-LLM Orchestration:
  - Google Gemini 3.8 Flash (via `google-genai` SDK) sebagai model primer.
  - Llama 3.3 (via Groq API) sebagai model alternatif berkecepatan tinggi.
* **Knowledge Retrieval Engine:** Hybrid Vector Retrieval (`src/vector_engine.py`) menggabungkan:
  - Dense Vector Semantic Search (`text-embedding-004` & Local Subword Vectorizer fallback).
  - Pure NumPy 2.x In-Memory Cosine Similarity.
  - Lexical Keyword BM25 Domain-Boosted Matching.
  - Formula Hybrid Weighted: $\text{Score}_{\text{hybrid}} = \alpha \cdot \text{Score}_{\text{dense}} + (1 - \alpha) \cdot \text{Score}_{\text{lexical}}$ ($\alpha = 0.55$).
  - Precomputed Persistent Cache: `data/processed/vector_embeddings.json`.
* **Security & Traffic Control:**
  - Developer Admin PIN Gate (`ADMIN_PIN=2026`) untuk memproteksi konfigurasi kunci API.
  - Middleware pembatas laju permintaan `slowapi` (20 req/menit untuk chat, 10 req/menit untuk PIN).
  - Isolasi prompt anti-jailbreak pada blok `[PERTANYAAN MAHASISWA]`.
* **State & Memory Management:** Client-side Session Rooms (`localStorage`) + Server-side Multi-turn Context Summary.

### 5.2 Alur Arsitektur Sistem
```
[User Input via Modern SPA (HTML/CSS/JS)]
              │
              ├── Mengambil Pengaturan (Persona Tone, Domain Scope, Provider)
              ├── Mengambil Ringkasan Percakapan (Multi-turn Memory)
              ▼
[FastAPI Backend Server (app.py)] ──[slowapi Rate Limiter]
              │
              ▼
[Hybrid Vector Retrieval Engine (src/vector_engine.py)]
              ├── Dense Embeddings & Cosine Similarity Math
              └── BM25 Lexical Keyword Domain Booster
              │ (Mencocokkan ke 7 Dokumen Resmi / 38 Chunk)
              ▼
[Prompt Assembler (src/prompts.py)]
  ├── System Instruction (Guardrail, Pasal 6 Anti-Leak, Persona VIKA)
  ├── Context Chunks Terverifikasi
  └── Ringkasan Riwayat Percakapan
              │
              ▼
[Dual LLM Engine: Gemini 3.8 / Llama 3.3]
              │ (Real-Time SSE Token Streaming)
              ▼
[FastAPI StreamingResponse (text/event-stream)]
              │
              ▼
[SPA Interface Rendering]
  ├── Typewriter Token Queue Animation
  ├── Inner Table Subcards & Markdown Formatter
  └── Official Citation Badge (📌 SK Dokumen Resmi ↗)
```

---

## 6. Git Flow & Workflow Repositori

1. **`main` Branch:**
   - Branch rilis produksi bersih.
   - Commit pertama: `initial commit` (scaffold, PRD, dan konfigurasi dasar).
   - Menerima merge dari `develop` saat pengujian menyeluruh telah selesai.
2. **`develop` Branch:**
   - Branch integrasi utama seluruh fitur.
3. **`feature/*` Branches:**
   - Dibuat dari `develop` untuk setiap pilar fungsionalitas, lalu di-merge kembali setelah teruji.

---

## 7. Rancangan Tahapan Sederhana Pembuatan Proyek (Project Roadmap)

Pelaksanaan proyek dibagi menjadi 5 tahapan kerja bertahap:

```text
[Tahap 1: Fondasi & Perencanaan]
       │
       ▼
[Tahap 2: Pengumpulan & Ekstraksi Data Dokumen]
       │
       ▼
[Tahap 3: Integrasi Service Gemini & Prompt Persona VIKA]
       │
       ▼
[Tahap 4: Desain Antarmuka Streamlit & Styling CSS]
       │
       ▼
[Tahap 5: Pengujian Terpadu, Dokumentasi & Rilis Final]
```

1. **Tahap 1: Fondasi, Perencanaan & Branding (Selesai)**
   - Penyusunan PRD, Style Guide, penetapan identitas VIKA (*Virtual Interactive Knowledge Assistant*).
   - Inisialisasi Git Flow (`main` bersih dan `develop` aktif di GitHub).
2. **Tahap 2: Pengumpulan & Ekstraksi Data Dokumen (Knowledge Base)**
   - Mengunduh dan menempatkan file PDF/teks resmi UNPAM ke `data/raw/`.
   - Melakukan ekstraksi teks, normalisasi, dan pembuatan struktur indeks pencarian di `src/knowledge_base.py`.
3. **Tahap 3: Integrasi Service Gemini & Prompt Persona VIKA**
   - Menghubungkan client Google GenAI dengan model `gemini-3.8-flash`.
   - Mengonfigurasi system instruction VIKA (mode tone: Kating Ramah, Formal, Ringkas; filter cakupan; serta pencegahan halusinasi).
4. **Tahap 4: Desain Antarmuka Streamlit & Styling CSS**
   - Menerapkan token warna (`#0F2742`, `#38BDF8`, `#E6F5FF`) dan tipografi dari panduan style ke `assets/css/style.css`.
   - Membangun 3 tampilan interaktif di `app.py`: Landing Page, Chat Interface, dan Halaman Pengaturan.
5. **Tahap 5: Pengujian Terpadu, Dokumentasi & Rilis Final**
   - Melakukan uji coba percakapan, multi-turn memory, kesesuaian sitasi, dan uji responsivitas tampilan.
   - Memperbarui dokumentasi akhir di `README.md`, merge dari `develop` ke `main`, dan persiapan deployment.
