# PRODUCT REQUIREMENTS DOCUMENT (PRD)
## Proyek: VIKA — Virtual Interactive Knowledge Assistant (UNPAM Academic Chatbot)

---

| Dokumen | Versi | Status | Tanggal Pembuatan | Author / Role |
| :--- | :---: | :---: | :---: | :--- |
| **PRD - Final Project Hacktiv8** | `1.1.0` | **Approved** | 24 Oktober 2026 | Mentee & AI Mentor |

---

## 1. Executive Summary & Visi Produk

### 1.1 Latar Belakang & Identitas Produk
Universitas Pamulang (UNPAM) merupakan salah satu perguruan tinggi swasta terbesar di Indonesia dengan puluhan ribu mahasiswa aktif yang tersebar di berbagai program kelas (Reguler A, Reguler B, Reguler C/Sabtu). Setiap awal dan akhir semester, bagian Layanan Administrasi Akademik (LAK) dan fakultas menerima ribuan pertanyaan berulang mengenai linimasa pengisian KRS, ambang batas kehadiran 75% untuk UAS, prosedur pengajuan cuti, remedial, serta konversi magang MBKM.

Untuk menyelesaikan permasalahan tersebut secara nyata, dikembangkanlah **VIKA** (*Virtual Interactive Knowledge Assistant*).
- **Nama Produk:** VIKA (Virtual Interactive Knowledge Assistant)
- **Tagline:** *"Selalu Ada untuk Jawaban Akademikmu"*
- **Repositori:** `unpam-academic-chatbot`
- **Platform:** Standalone Web Portal (Streamlit Modern dengan Custom CSS)

### 1.2 Visi Produk
Membangun web portal mandiri berbasis AI (*Standalone Web Assistant*) yang bertindak sebagai pusat konsultasi informasi akademik UNPAM yang cepat, ramah, akurat, dan memiliki sitasi dokumen resmi (*evidence-based*). Aplikasi dibangun secara efisien dengan **biaya Rp 0,- (Zero Cost)** menggunakan **Google Gemini 3.8 Flash** dan **Streamlit Modern**.

---

## 2. Ruang Lingkup Proyek (Scope of Work)

### 2.1 In-Scope (Cakupan Fitur yang Dikerjakan)
1. **Pusat Informasi Kalender Akademik TA 2026/2027:**
   - Jadwal pembayaran registrasi, pengisian dan revisi KRS Gasal & Genap.
   - Linimasa perkuliahan aktif, pelaksanaan UTS, UAS, dan yudisium/wisuda.
2. **Konsultasi Aturan Presensi & Kelayakan Ujian:**
   - Kalkulasi dan aturan kehadiran minimal 75% untuk syarat mengikuti UAS.
   - Tata cara permohonan izin/sakit dan batas waktu penyerahan surat keterangan.
   - Alur, jadwal, dan kriteria pendaftaran Ujian Remedial / Susulan.
3. **Layanan Prosedural Administrasi Mahasiswa (SOP LAK):**
   - Panduan alur permohonan cuti akademik (maksimal 2 semester kumulatif).
   - Prosedur pengaktifan kembali status mahasiswa pasca-cuti.
   - Syarat permohonan Surat Keterangan Mahasiswa Aktif dan legalisir.
   - Tata cara mutasi kelas (Reguler A/B/C) dan perpindahan prodi.
4. **Regulasi Akademik & Kurikulum (Pedoman Akademik & FILKOM):**
   - Batas masa studi jenjang S1 (maksimal 14 semester).
   - Perhitungan bobot 1 SKS (50 menit tatap muka, 60 menit tugas, 60 menit mandiri).
   - Penjelasan standar Kurikulum Berbasis Capaian (OBE - *Outcome-Based Education*).
   - Syarat SKS untuk mengambil Kerja Praktik (KP), Seminar Proposal, Skripsi, dan magang MBKM (Studi Independen / MSIB).
5. **Parameter Kreatif (Sesuai Syarat Hacktiv8):**
   - **Gaya Bahasa (Tone):** 
     - *Kating Ramah:* Bahasa santai, komunikatif, suportif layaknya kakak tingkat.
     - *Formal Birokrat:* Bahasa baku, lugas, mengedepankan pasal dan bahasa hukum SK Rektor.
     - *Ringkas (To-the-Point):* Hanya menyajikan tanggal/poin checklist esensial.
   - **Filter Domain:** Tingkat Universitas (Umum) vs Khusus FILKOM (Teknik Informatika).
   - **Multi-turn Memory:** Mempertahankan konteks obrolan dalam 1 sesi aktif.
   - **Quick Action Starter Chips:** Pertanyaan rekomendasi 1-klik di awal obrolan.
   - **Fitur Export & Reset:** Unduh ringkasan percakapan (Markdown/TXT) dan hapus sesi chat.

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
     > *"Mohon maaf, informasi data privat tersebut berada di luar wewenang saya. Silakan cek langsung melalui portal MyUnpam (my.unpam.ac.id) atau hubungi loket Bagian Keuangan UNPAM."*

---

## 3. Data & Knowledge Base (Sumber Kebenaran Primer)

Sistem chatbot mengonsumsi dan mengekstrak pengetahuan dari 4 dokumen resmi:

| No | Dokumen Sumber | Penerbit Resmi | Topik Kunci |
| :-: | :--- | :--- | :--- |
| **1** | **SK Kalender Akademik TA 2026/2027** | LP3 / Rektorat UNPAM | Linimasa KRS, tanggal aktif kuliah, rentang UTS/UAS, libur semester, pendaftaran wisuda. |
| **2** | **Buku Pedoman Akademik Universitas Pamulang** | Rektorat / Unpam Press | Batas masa studi 14 semester, hak & kewajiban mahasiswa, definisi 1 SKS, sanksi akademik. |
| **3** | **SOP Layanan Administrasi Akademik (LAK)** | Biro LAK UNPAM | Aturan absen 75%, remedial, syarat permohonan cuti maksimal 2 kali, mutasi kelas. |
| **4** | **Buku Pedoman Fakultas Ilmu Komputer (FILKOM)** | Dekanat FILKOM / Informatika | Kurikulum OBE, peminatan Informatika, syarat KP/Skripsi, aturan konversi SKS MBKM. |

---

## 4. User Personas & User Stories

### 4.1 User Personas
* **Persona 1: Rian (Mahasiswa Baru S1 Informatika)**
  - *Karakteristik:* Masih bingung membedakan SKS, takut salah jadwal KRS, dan belum paham aturan absen 75%.
  - *Kebutuhan:* Penjelasan yang ramah, santai (*kating style*), dan tidak intimidatif.
* **Persona 2: Siti (Mahasiswa Kelas Reguler C / Karyawan)**
  - *Karakteristik:* Kuliah sambil bekerja, waktu sangat terbatas, butuh jawaban cepat dan langsung ke intinya.
  - *Kebutuhan:* Informasi to-the-point mengenai jadwal UAS susulan atau mekanisme cuti.
* **Persona 3: Dika (Mahasiswa Semester 6 Menjelang Skripsi & MBKM)**
  - *Karakteristik:* Ingin memastikan apakah SKS-nya sudah cukup untuk mengambil magang MSIB atau KP.
  - *Kebutuhan:* Penjelasan terstruktur mengenai aturan OBE dan syarat administrasi FILKOM.

### 4.2 User Stories & Acceptance Criteria (Gherkin Style)

#### US-01: Memilih Gaya Bahasa (Tone)
* **Sebagai** mahasiswa UNPAM,
* **Saya ingin** dapat memilih gaya bahasa interaksi (Formal, Kating Santai, atau Ringkas),
* **Agar** penjelasan yang diberikan AI terasa nyaman dan sesuai situasi saya.
  - **Given** pengguna berada di halaman aplikasi,
  - **When** pengguna memilih radio button gaya bahasa di sidebar menjadi *"Kating Santai"*,
  - **Then** respon chat berikutnya menggunakan sapaan akrab, nada suportif, dan bahasa kasual yang sopan.

#### US-02: Menanyakan Regulasi Kehadiran & UAS
* **Sebagai** mahasiswa,
* **Saya ingin** mengetahui syarat persentase absensi untuk bisa mengikuti UAS,
* **Agar** saya tidak terkena pencekalan ujian.
  - **Given** sesi obrolan aktif,
  - **When** pengguna bertanya *"Berapa persen minimal kehadiran buat ikut UAS?"*,
  - **Then** chatbot menjawab **75%** secara tegas dan menyertakan sitasi rujukan *(Sumber: SOP Akademik LAK UNPAM)*.

#### US-03: Quick Action Starter Chips
* **Sebagai** pengguna baru yang belum tahu harus bertanya apa,
* **Saya ingin** melihat tombol rekomendasi pertanyaan populer di awal layar,
* **Agar** saya bisa langsung mencoba fitur bot dengan satu kali klik.
  - **Given** riwayat chat masih kosong (*initial state*),
  - **When** pengguna mengklik kartu chip *"Kapan batas akhir pengisian KRS?"*,
  - **Then** pertanyaan tersebut otomatis terkirim dan bot menjawab linimasa KRS dari Kalender Akademik 2026/2027.

#### US-04: Chat Memory & Konteks Berkelanjutan
* **Sebagai** mahasiswa,
* **Saya ingin** mengajukan pertanyaan lanjutan tanpa mengulang subjek dari awal,
* **Agar** alur percakapan terasa natural.
  - **Given** pengguna baru saja bertanya tentang syarat cuti kuliah,
  - **When** pengguna bertanya pertanyaan lanjutan *"Lalu maksimal boleh berapa kali?"*,
  - **Then** bot memahami bahwa konteksnya adalah cuti kuliah dan menjawab maksimal 2 semester/kali.

---

## 5. Technical Requirements & Architecture

### 5.1 Tech Stack (Zero Cost / Full Gratis)
* **Frontend & Web Framework:** Streamlit (Python) dengan Custom CSS Injection.
* **LLM Engine:** Google Gemini API (`gemini-3.8-flash` dengan Google GenAI Client).
* **Knowledge Retrieval:** Chunk-based Structured Knowledge Base (Clean Markdown/JSON index) yang di-grounding ke prompt.
* **State Management:** `st.session_state` untuk chat history, pengaturan parameter, dan session caching.
* **Hosting / Cloud Deployment:** Streamlit Community Cloud (Gratis & terintegrasi dengan GitHub).

### 5.2 Alur Arsitektur Sistem
```
[User Input via Streamlit UI]
              │
              ├── Mengambil Pengaturan Sidebar (Tone, Domain Filter, Model)
              ├── Mengambil Riwayat Percakapan (Multi-turn Memory)
              ▼
[Knowledge Grounding Engine]
              │ (Mencocokkan keyword/topik dengan 4 Dokumen UNPAM)
              ▼
[Prompt Assembler]
  ├── System Instruction (Guardrail, Anti-Halusinasi, Persona)
  ├── Relevant Context Chunks (Pasal/Jadwal terkait)
  └── Chat History + Pesan Terakhir
              │
              ▼
[Google Gemini 3.8 Flash API]
              │ (Streaming Response Token)
              ▼
[Streamlit Output Container]
  ├── Streamed Markdown Response
  └── Official Citation Badge
```

---

## 6. Git Flow & Workflow Repositori

Agar repositori memenuhi standar industri dan rapi saat dinilai instruktur Hacktiv8:

1. **`main` Branch:**
   - Bersih dari *wip commit*.
   - Commit pertama: `Initial commit: Project structure and PRD`.
   - Hanya menerima merge dari `develop` saat versi rilis v1.0.0 selesai diuji.
2. **`develop` Branch:**
   - Branch integrasi utama.
3. **`feature/*` Branches:**
   - `feature/setup-knowledge-base`: Ekstraksi dan penataan data 4 dokumen UNPAM.
   - `feature/gemini-service`: Modul client Gemini 3.8 Flash, prompt templates, dan memory.
   - `feature/ui-interface`: Layout Streamlit, CSS styling, chat container, dan chips.
   - `feature/export-and-polish`: Fitur unduh log percakapan, error handling, dan dokumentasi README.
