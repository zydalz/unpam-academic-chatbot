# 🎓 VIKA — UNPAM Academic Chatbot
> **Virtual Interactive Knowledge Assistant — Asisten Akademik Universitas Pamulang**  
> *Tagline: "Asisten Akademik UNPAM — Cepat, Mudah, dan Terpercaya"*  
> *Pengembang: Abu Ziyad Al Katani (`zydalz`)*  
> *Final Project: LLM-Based Tools and Gemini API Integration for Data Scientists — Hacktiv8*

<p align="center">
  <img src="static/images/VIKA Logo Dark Mode.png" alt="VIKA Brand Logo" width="120" style="border-radius: 50%; box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Frontend-Modern%20SPA%20(HTML5%2FCSS3%2FJS)-E34F26?logo=html5" alt="Frontend" />
  <img src="https://img.shields.io/badge/LLM-Gemini%203.8%20Flash%20%7C%20Llama%203.3-4285F4?logo=google" alt="Gemini & Llama" />
  <img src="https://img.shields.io/badge/Knowledge%20Base-5%20Official%20Decrees-10B981" alt="Knowledge Base" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 📌 Tentang Proyek

**VIKA (Virtual Interactive Knowledge Assistant)** adalah asisten akademik virtual cerdas yang dirancang khusus untuk sivitas akademika Universitas Pamulang (UNPAM), khususnya mahasiswa Program Studi S1 Teknik Informatika (FILKOM/FTIK).

VIKA dibangun untuk memenuhi tugas akhir program **Hacktiv8: LLM-Based Tools and Gemini API Integration for Data Scientists** dengan mengadopsi arsitektur **RAG (Retrieval-Augmented Generation)** penuh:
1. **Pencarian Semantik & Skor Kedekatan (Similarity Scoring):** Mencocokkan pertanyaan mahasiswa dengan basis data regulasi resmi kampus.
2. **Grounding & Anti-Halusinasi:** Memberikan jawaban akurat berbasis tanggal kalender, bobot nilai, dan persyaratan SKS resmi dengan sitasi transparan.
3. **Antarmuka 100% Identik Mockup:** Disajikan menggunakan Single Page Application modern dengan Server-Sent Events (SSE) streaming, elevated response cards, sub-card Linimasa Penting, dan chip rekomendasi proaktif.

<p align="center">
  <img src="static/images/UNPAM AI Interface Showcase Board.png" alt="VIKA Interface Showcase Board" width="850" style="border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.08);" />
</p>

---

## 📚 Basis Dokumen Rujukan Resmi (5 Pilar Pengetahuan)

VIKA mengindeks 5 dokumen kebijakan resmi Universitas Pamulang secara komprehensif:

| No | Dokumen Target | Nomor SK / Dasar Hukum | Unit Penerbit | Fokus Rujukan Utama |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **SK Kalender Akademik TA 2026/2027** | `SK Rektor No. 1694/A/UNPAM/KP/VII/2026` | LP3 / Rektorat UNPAM | Linimasa KRS, awal perkuliahan Reguler A/B/C, rentang UTS/UAS, pendaftaran susulan, libur semester, dan wisuda. |
| **2** | **Buku Pedoman Akademik Universitas Pamulang** | `SK Rektor No. 240/A/O/UNPAM/I/2020` | Rektorat / Unpam Press | Batas masa studi S1 (maksimal 14 semester), beban SKS (170 menit), hak & kewajiban mahasiswa, dan ketentuan Drop Out (DO). |
| **3** | **SOP Layanan Administrasi Akademik (LAK)** | `SK Rektor No. 240/A/O/UNPAM/I/2020` (Bab Evaluasi & Administrasi) | Biro LAK / Rektorat UNPAM | Ketentuan batas presensi 75% UAS, bobot penilaian (10:20:30:40), kuota remedial teaching (min 15 mhs), cuti kuliah (maks 2x), dan pindah kelas. |
| **4** | **Buku Pedoman Fakultas Ilmu Komputer (FILKOM)** | `SK Rektor No. 0269/A/UNPAM/KP/II/2026` | Dekanat FILKOM / S1 Informatika | Prinsip kurikulum OBE (Outcome-Based Education), profil lulusan S1 Teknik Informatika (144-146 SKS), syarat KP/Skripsi, dan konversi MBKM. |
| **5** | **Pedoman Tugas Akhir, Skripsi & Jalur Kelulusan TI** | `SK Dekan & Arsip Resmi Prodi TI UNPAM` | Prodi S1 Teknik Informatika UNPAM | Jalur skripsi 6 SKS (syarat $\ge$ 122–130 SKS, IPK $\ge$ 2.40, sempro, sidang UAPS), jalur publikasi jurnal SINTA/Scopus, dan rekognisi MBKM. |

---

## 🚀 Fitur Unggulan

- 💬 **Streaming Percakapan Real-Time (SSE):** Respon asisten dialirkan secara langsung (*word-by-word streaming*) menggunakan Server-Sent Events standar modern.
- 🎭 **Persona "Kasual" Bebas 'Kakak':** Bahasa santun, luwes, dan bersahabat layaknya rekan diskusi kampus tanpa sebutan diri "kakak" atau birokrasi kaku.
- 🤖 **Dual-LLM Engine:**
  - **Google Gemini 3.8 Flash (Default / Rekomendasi):** Penalaran konteks panjang dan pemrosesan regulasi teruji.
  - **Llama 3.3 70B (Groq Engine):** Model open-weights super cepat dengan latensi inferensi < 1 detik.
- 🌐 **Whitelist Sumber Eksternal:** Fallback otomatis membaca dari portal resmi `informatika.unpam.ac.id`, `unpam.ac.id`, dan `sinta.kemdikbud.go.id` saat rujukan lokal belum tersedia.
- 💡 **Rekomendasi Proaktif (3 Action Recommendation Chips):** Menampilkan tombol saran topik tindak lanjut interaktif tepat di bawah setiap jawaban AI.
- 🌗 **Dukungan Tema Terang & Gelap (Light & Dark Mode):** Transisi instan dengan token warna presisi dan logo VIKA adaptif.
- 📱 **100% Identik dengan 5 Layar Mockup:** Menghadirkan Hero Banner Kampus Viktor, Elevated Response Card, Sub-Card Linimasa Penting, dan Floating Input Bar.

---

## 🛠️ Arsitektur Sistem

```text
┌─────────────────────────────────────────────────────────────┐
│                 Single-Unit Web Application                 │
│         (FastAPI Backend + Modern HTML5/CSS3/JS SPA)        │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────┐┌──────────────────────────────┐
│  Semantic Knowledge Engine  ││    Dual-Engine Orchestrator  │
│ (Similarity Scoring & Index)││  (Gemini Flash + Groq Llama) │
└──────────────┬──────────────┘└──────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────┐┌──────────────────────────────┐
│  5 Dokumen SK Resmi UNPAM   ││   Web Grounding Whitelist    │
│  data/processed/*.md        ││   *.unpam.ac.id / SINTA      │
└─────────────────────────────┘└──────────────────────────────┘
```

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

### 3. Konfigurasi Kunci API (Opsional / BYOK)
Salin berkas `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```
Isi kunci API Anda:
```env
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
```
*(Catatan: Anda juga bisa langsung memasukkan kunci API di halaman Pengaturan pada web).*

### 4. Jalankan Aplikasi Web
```bash
python main.py
```
atau:
```bash
python app.py
```

Buka peramban Anda di: **`http://localhost:8000`**

---

## 📄 Lisensi & Hak Cipta

Proyek ini dilisensikan di bawah lisensi **MIT License** — lihat berkas [LICENSE](LICENSE) untuk rincian lengkap.  
Hak Cipta (c) 2026 **Abu Ziyad Al Katani (`zydalz`)**.
