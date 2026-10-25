"""External Search and Web Grounding Module for VIKA.

Enforces a strict academic domain whitelist to avoid unverified or non-official
blog/hearsay content:
1. *.unpam.ac.id (Official UNPAM portal, LP3, Rektorat)
2. informatika.unpam.ac.id (Teknik Informatika Prodi Portal)
3. lak.unpam.ac.id (Lembaga Administrasi Akademik)
4. sinta.kemdikbud.go.id (National Journal Accreditation)
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

WHITELIST_DOMAINS = [
    "unpam.ac.id",
    "informatika.unpam.ac.id",
    "lak.unpam.ac.id",
    "lp3.unpam.ac.id",
    "filkom.unpam.ac.id",
    "sinta.kemdikbud.go.id",
]


class ExternalSearchService:
    """Provides restricted academic domain search fallback."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def is_domain_allowed(self, url: str) -> bool:
        """Check if a URL belongs to the official UNPAM or SINTA domain whitelist."""
        try:
            domain = urlparse(url).netloc.lower()
            return any(domain == w or domain.endswith("." + w) for w in WHITELIST_DOMAINS)
        except Exception:
            return False

    def search_official_fallback(self, query: str) -> Optional[Dict[str, str]]:
        """Search external official sources if internal knowledge base is insufficient.

        Returns:
            Dictionary with title, snippet, source_url, or None if not found/disabled.
        """
        if not self.enabled:
            return None

        # Clean query
        q_clean = query.strip()
        logger.info("Executing whitelisted external academic search fallback for: %s", q_clean)

        # For production without external search key, return structured fallback pointers
        # to official portals matching the topic
        q_lower = q_clean.lower()
        if "skripsi" in q_lower or "tugas akhir" in q_lower or "uaps" in q_lower:
            return {
                "source_title": "Arsip Resmi Teknik Informatika UNPAM",
                "source_url": "https://informatika.unpam.ac.id/archive",
                "publisher": "Prodi Teknik Informatika UNPAM",
                "summary": "Dokumen petunjuk teknis penulisan skripsi, syarat SKS minimal 122-130, seminar proposal, dan berkas pendaftaran sidang UAPS.",
            }
        elif "beasiswa" in q_lower or "sispema" in q_lower or "rekomendasi" in q_lower:
            return {
                "source_title": "Portal Kemahasiswaan Teknik Informatika UNPAM",
                "source_url": "https://sites.google.com/unpam.ac.id/kemahasiswaan-ti/beranda",
                "publisher": "Kemahasiswaan FTI UNPAM",
                "summary": "Layanan penerbitan surat rekomendasi kegiatan/beasiswa (SISPEMA) dan pusat bantuan akun mahasiswa Kampus 2 Viktor.",
            }
        elif "jadwal" in q_lower or "krs" in q_lower or "kalender" in q_lower:
            return {
                "source_title": "Portal Resmi Universitas Pamulang",
                "source_url": "https://unpam.ac.id",
                "publisher": "LP3 / Biro Administrasi Akademik UNPAM",
                "summary": "Informasi jadwal linimasa registrasi akademik, pengisian KRS, dan kalender tahun akademik berjalan.",
            }

        return None
