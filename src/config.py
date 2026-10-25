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
STATIC_DIR = ROOT_DIR / "static"

# Load environment variables
load_dotenv(ROOT_DIR / ".env")

# Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Google Gemini API Configuration (Default / Recommended)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Fallback Gemini models in order of preference
MODEL_CANDIDATES = [
    GEMINI_MODEL,
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

# Groq API Configuration (Llama 3.3 Engine)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_MODEL_CANDIDATES = [
    GROQ_MODEL,
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

# Application Branding Constants
APP_NAME = "VIKA"
APP_FULL_NAME = "Virtual Interactive Knowledge Assistant"
APP_TAGLINE = "Asisten Akademik UNPAM"
APP_SUBTITLE = "Tanya apa saja tentang perkuliahan, dapatkan jawaban akurat dari sumber resmi kampus — cepat, mudah, dan terpercaya."
APP_INSTITUTION = "Universitas Pamulang"

# Default Preferences
DEFAULT_STYLE = "Kasual"
DEFAULT_SCOPE = "universitas"
DEFAULT_MODEL_PROVIDER = "gemini"

# Persona / Tone Profiles
STYLE_OPTIONS = {
    "Formal": {
        "label": "Formal",
        "description": "Bahasa resmi kelembagaan kampus, terstruktur, berbasis SK dan pasal hukum yang presisi.",
    },
    "Kasual": {
        "label": "Kasual",
        "description": "Bahasa santun, komunikatif, luwes, dan bersahabat layaknya rekan diskusi kampus tanpa sebutan kakak.",
    },
    "Ringkas": {
        "label": "Ringkas",
        "description": "To-the-point, berpoin padat, dan cepat dipahami. Cocok untuk mahasiswa kelas karyawan (Reguler C).",
    },
}

# Scope Options
SCOPE_OPTIONS = {
    "universitas": "Universitas (Kalender & Pedoman Umum)",
    "filkom": "Fakultas (FILKOM / Teknik Informatika)",
    "all": "Semua Cakupan (Universitas & FILKOM)",
}

# 4 Shortcut Topic Cards on Landing Page (Matching Mockup 1:1)
SHORTCUT_CARDS = [
    {
        "id": "kalender",
        "title": "Kalender Akademik",
        "subtitle": "2026/2027",
        "icon": "calendar",
        "prompt": "Kapan saja linimasa SK Kalender Akademik 2026/2027 UNPAM?",
        "scope": "universitas",
    },
    {
        "id": "kehadiran",
        "title": "Kehadiran & UAS",
        "subtitle": "(≥ 75%)",
        "icon": "check-circle",
        "prompt": "Berapa batas minimal presensi kehadiran agar mahasiswa boleh mengikuti UAS UNPAM?",
        "scope": "universitas",
    },
    {
        "id": "cuti",
        "title": "Cuti & Remedial",
        "subtitle": "(SOP LAK)",
        "icon": "file-text",
        "prompt": "Bagaimana prosedur pengajuan cuti kuliah dan ketentuan pelaksanaan remedial di UNPAM?",
        "scope": "universitas",
    },
    {
        "id": "kurikulum",
        "title": "Kurikulum OBE &",
        "subtitle": "Magang MBKM",
        "icon": "award",
        "prompt": "Bagaimana ketentuan kurikulum OBE S1 Informatika, syarat Tugas Akhir, dan program magang MBKM?",
        "scope": "filkom",
    },
]
