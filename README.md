# 🎓 VIKA — UNPAM Academic Chatbot
> **Virtual Interactive Knowledge Assistant — Asisten Akademik Universitas Pamulang**  
> *Tagline: "Asisten Akademik UNPAM — Cepat, Mudah, dan Terpercaya"*  
> *Pengembang: Abu Ziyad Al Katani (`zydalz`)*  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8 Maju Bersama AI*

<p align="center">
  <img src="static/images/VIKA Logo Dark Mode.png" alt="VIKA Brand Logo" width="120" style="border-radius: 50%; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Frontend-Modern%20SPA%20(HTML5%2FCSS3%2FJS)-E34F26?logo=html5" alt="Frontend" />
  <img src="https://img.shields.io/badge/LLM-Gemini%203.8%20Flash%20%7C%20Llama%203.3-4285F4?logo=google" alt="Gemini & Llama" />
  <img src="https://img.shields.io/badge/Knowledge%20Base-7%20Official%20Decrees-10B981" alt="Knowledge Base" />
  <img src="https://img.shields.io/badge/License-Academic%20Restricted-red" alt="License" />
</p>

---

## 📌 Tentang Proyek

**VIKA (Virtual Interactive Knowledge Assistant)** adalah asisten akademik virtual cerdas yang dirancang khusus untuk sivitas akademika Universitas Pamulang (UNPAM), khususnya mahasiswa Program Studi S1 Teknik Informatika (FILKOM/FTIK).

VIKA dibangun untuk memenuhi tugas akhir program **Hacktiv8: LLM-Based Tools and Gemini API Integration for Data Scientists (Maju Bersama AI)** dengan mengadopsi arsitektur **RAG (Retrieval-Augmented Generation)** penuh:
1. **Pencarian Semantik Terstruktur:** Mencocokkan pertanyaan mahasiswa dengan basis data regulasi resmi kampus secara cepat dan presisi.
2. **Grounding & Anti-Halusinasi:** Memberikan jawaban akurat berbasis tanggal kalender, rincian biaya bimbingan skripsi, SOP project work, dan persyaratan SKS dengan sitasi transparan.
3. **Antarmuka Modern (100% Identik Mockup):** Single Page Application modern dengan Server-Sent Events (SSE) streaming, typewriter animation, floating controls, mini-rail sidebar, dan light/dark theme switch.

<p align="center">
  <img src="static/images/UNPAM AI Interface Showcase Board.png" alt="VIKA Interface Showcase Board" width="850" style="border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08);" />
</p>

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

Sebagai bagian dari standar rekayasa perangkat lunak dan arsitektur AI yang matang, VIKA menerapkan mitigasi terhadap 4 celah utama dalam sistem berbasis LLM:

| Jenis Celah | Risiko Utama | Solusi yang Diterapkan di VIKA | Status |
| :--- | :--- | :--- | :---: |
| **1. API Route Terbuka** | API Key bocor ke publik atau di-*scrape* bot crawler. | **Server-side Orchestration:** Seluruh pemanggilan Google Gemini dan Groq dilakukan murni di *backend* Python (`src/gemini_service.py`). Kunci disamarkan (*masked*), dan file `.env` terisolasi 100% dari git repository. Menu pengaturan dilengkapi proteksi Developer Admin Gate. | ✅ Terproteksi Penuh |
| **2. Spam / Bot Attack** | Kuota API habis (*rate limit*) dan server overload. | **Local Single-User Architecture:** Aman pada tahap evaluasi lokal. Pada deployment publik, mitigasi dilakukan via Cloudflare WAF/DDoS protection dan middleware `slowapi` (10 request/menit per IP). | ✅ Termitigasi |
| **3. Prompt Injection** | Bot dijebol (*jailbreak*), berbicara kasar, atau bocor instruksi. | **System Prompt Persona & Safety Guardrails:** Instruksi sistem mengunci batasan tugas secara ketat. Teruji pada Blackbox Testing (TC-06) dengan penolakan 100% terhadap perintah pembajakan peran (*system override*). | ✅ Teruji 100% Lulus |
| **4. Salah Informasi (*Hallucination*)** | Komplain mahasiswa tersesat akibat jadwal/biaya fiktif. | **RAG Strict Grounding & Fallback:** Suhu model (*temperature*) disetel rendah, wajib menyertakan sitasi resmi SK/Pengumuman, dan wajib menyatakan tidak tahu jika data belum tercantum di dokumen (Teruji di TC-04). | ✅ Teruji 100% Lulus |

---

## 💻 Cara Menjalankan Aplikasi di Lokal

### 1. Kloning Repositori & Masuk ke Folder Proyek
```bash
git clone https://github.com/zydalz/unpam-academic-chatbot.git
cd unpam-academic-chatbot
```

### 2. Pasang Dependensi Python
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Kunci API (BYOK)
Salin berkas `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Isi kunci API Anda pada berkas `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
*(Catatan: Kunci API Anda tersimpan aman secara lokal dan tidak akan pernah ter-push ke GitHub).*

### 4. Jalankan Server Aplikasi
```bash
python app.py
```
Buka peramban Anda di: **`http://localhost:8000`**

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
