"""Configuration module for VIKA (Virtual Interactive Knowledge Assistant).

Handles environment variables, default model settings, and app-wide constants.
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
ASSETS_DIR = ROOT_DIR / "assets"
ASSETS_IMAGES_DIR = ASSETS_DIR / "images"
ASSETS_CSS_DIR = ASSETS_DIR / "css"

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Fallback models in order of preference
MODEL_CANDIDATES = [
    GEMINI_MODEL,
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

# Application Branding Constants
APP_NAME = "VIKA"
APP_FULL_NAME = "Virtual Interactive Knowledge Assistant"
APP_TAGLINE = "Selalu Ada untuk Jawaban Akademikmu"
APP_INSTITUTION = "Universitas Pamulang"

# Persona / Tone Profiles
STYLE_OPTIONS = {
    "Kating Ramah": {
        "label": "Kating Ramah",
        "description": "Komunikatif, suportif, santun, dan mudah dicerna seperti berdiskusi dengan kakak tingkat.",
        "icon": "sparkles",
    },
    "Formal Birokrat": {
        "label": "Formal Birokrat",
        "description": "Bahasa resmi kelembagaan kampus, terstruktur, berbasis SK dan pasal hukum yang presisi.",
        "icon": "shield-check",
    },
    "Ringkas": {
        "label": "Ringkas",
        "description": "To-the-point, berpoin padat, dan cepat dipahami. Cocok untuk mahasiswa kelas karyawan (Reguler C).",
        "icon": "zap",
    },
}

# Scope Options
SCOPE_OPTIONS = {
    "all": "Semua Cakupan (Universitas & FILKOM)",
    "universitas": "Universitas (Kalender & Pedoman Umum)",
    "filkom": "FILKOM (Informatika & Kurikulum OBE)",
}

# Starter Action Chips for Quick Exploration
STARTER_CHIPS = [
    {
        "id": "krs_jadwal",
        "category": "Jadwal",
        "icon": "calendar",
        "label": "Jadwal KRS & Perkuliahan",
        "prompt": "Kapan jadwal awal perkuliahan dan periode revisi KRS untuk Semester Gasal TA 2026/2027?",
        "scope": "universitas",
    },
    {
        "id": "presensi_uas",
        "category": "Akademik",
        "icon": "check-circle",
        "label": "Syarat Presensi UAS",
        "prompt": "Berapa persen minimal kehadiran kuliah agar saya diizinkan mengikuti ujian akhir semester (UAS)?",
        "scope": "universitas",
    },
    {
        "id": "cuti_kuliah",
        "category": "Layanan LAK",
        "icon": "clock",
        "label": "Ketentuan Cuti Kuliah",
        "prompt": "Berapa kali maksimal saya bisa mengambil cuti akademik dan apa saja syarat pengajuannya?",
        "scope": "universitas",
    },
    {
        "id": "skripsi_obe",
        "category": "FILKOM",
        "icon": "book-open",
        "label": "Syarat Skripsi Informatika",
        "prompt": "Apa saja syarat untuk mengambil skripsi di S1 Teknik Informatika dan bagaimana prinsip kurikulum OBE?",
        "scope": "filkom",
    },
]
