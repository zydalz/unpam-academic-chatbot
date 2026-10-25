"""Knowledge Base Management and Document Retrieval Module for VIKA.

Loads, indexes, and retrieves structured academic reference documents from
UNPAM official decrees:
1. SK Kalender Akademik TA 2026/2027 (SK No. 1694/A/UNPAM/KP/VII/2026)
2. Buku Pedoman Akademik UNPAM (SK No. 240/A/O/UNPAM/I/2020)
3. SOP Layanan Administrasi Akademik (LAK) & Evaluasi
4. Pedoman Akademik FILKOM & S1 Informatika (SK No. 0269/A/UNPAM/KP/II/2026)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Metadata describing an official UNPAM reference document."""

    doc_id: str
    title: str
    decree_number: str
    publisher: str
    focus: str
    scope: str  # "universitas" or "filkom"
    file_path: str
    official_source_url: Optional[str] = None


class KnowledgeChunk(BaseModel):
    """A granular chunk from a section of an academic document."""

    chunk_id: str
    doc_id: str
    doc_title: str
    decree_number: str
    publisher: str
    scope: str
    section_title: str
    content: str
    keywords: List[str] = Field(default_factory=list)


class SearchResult(BaseModel):
    """Search retrieval item with relevance score and citation metadata."""

    chunk_id: str
    doc_title: str
    decree_number: str
    publisher: str
    scope: str
    section_title: str
    content: str
    relevance_score: float
    citation: Dict[str, str]


class KnowledgeBase:
    """In-memory indexing and structured retrieval engine for VIKA."""

    def __init__(self, data_dir: Optional[str | Path] = None) -> None:
        if data_dir is None:
            # Default to <project_root>/data/processed
            self.data_dir = (
                Path(__file__).resolve().parent.parent / "data" / "processed"
            )
        else:
            self.data_dir = Path(data_dir)

        self.documents: Dict[str, DocumentMetadata] = {}
        self.chunks: List[KnowledgeChunk] = []
        self._init_documents_registry()
        self._load_and_index()

    def _init_documents_registry(self) -> None:
        """Register the 4 official UNPAM benchmark documents."""
        self.documents = {
            "kalender_akademik_2026_2027": DocumentMetadata(
                doc_id="kalender_akademik_2026_2027",
                title="SK Kalender Akademik TA 2026/2027",
                decree_number="SK Rektor No. 1694/A/UNPAM/KP/VII/2026",
                publisher="LP3 / Rektorat UNPAM",
                focus="Linimasa KRS, tanggal perkuliahan, rentang UTS/UAS, libur semester, dan wisuda",
                scope="universitas",
                file_path="kalender_akademik_2026_2027.md",
                official_source_url="https://unpam.ac.id",
            ),
            "pedoman_akademik_unpam": DocumentMetadata(
                doc_id="pedoman_akademik_unpam",
                title="Buku Pedoman Akademik Universitas Pamulang",
                decree_number="SK Rektor No. 240/A/O/UNPAM/I/2020",
                publisher="Rektorat / Lembaga Penjaminan Mutu UNPAM",
                focus="Batas masa studi S1, hak & kewajiban mahasiswa, definisi SKS, dan etika akademik",
                scope="universitas",
                file_path="pedoman_akademik_unpam.md",
                official_source_url="https://unpam.ac.id",
            ),
            "sop_administrasi_akademik": DocumentMetadata(
                doc_id="sop_administrasi_akademik",
                title="SOP Layanan Administrasi Akademik (LAK)",
                decree_number="SK Rektor No. 240/A/O/UNPAM/I/2020 (Bab Evaluasi & Administrasi)",
                publisher="Biro LAK / Rektorat UNPAM",
                focus="Ketentuan batas presensi 75% UAS, remedial teaching, pengajuan cuti kuliah, dan pindah kelas",
                scope="universitas",
                file_path="sop_administrasi_akademik.md",
                official_source_url="https://lak.unpam.ac.id",
            ),
            "pedoman_filkom_informatika": DocumentMetadata(
                doc_id="pedoman_filkom_informatika",
                title="Buku Pedoman Fakultas Ilmu Komputer (FILKOM)",
                decree_number="SK Rektor No. 0269/A/UNPAM/KP/II/2026 (Kurikulum OBE)",
                publisher="Dekanat FILKOM / Prodi S1 Teknik Informatika",
                focus="Prinsip kurikulum OBE, penjurusan Informatika, syarat KP/Skripsi, dan magang MBKM",
                scope="filkom",
                file_path="pedoman_filkom_informatika.md",
                official_source_url="https://filkom.unpam.ac.id",
            ),
            "pedoman_tugas_akhir_skripsi": DocumentMetadata(
                doc_id="pedoman_tugas_akhir_skripsi",
                title="Pedoman Tugas Akhir, Skripsi & Jalur Kelulusan TI",
                decree_number="SK Dekan & Arsip Resmi Prodi S1 Teknik Informatika UNPAM",
                publisher="Prodi Teknik Informatika / Dekanat FTIK UNPAM",
                focus="Jalur skripsi reguler 6 SKS, syarat SKS minimal 122-130, seminar proposal, sidang UAPS, dan rekognisi publikasi jurnal ilmiah SINTA",
                scope="filkom",
                file_path="pedoman_tugas_akhir_skripsi.md",
                official_source_url="https://informatika.unpam.ac.id/archive",
            ),
        }

    def _load_and_index(self) -> None:
        """Parse markdown files into structured sections/chunks."""
        self.chunks.clear()

        for doc_id, meta in self.documents.items():
            full_path = self.data_dir / meta.file_path
            if not full_path.exists():
                continue

            content = full_path.read_text(encoding="utf-8")
            # Split content by markdown major sections (## )
            sections = re.split(r"\n(?=##\s+)", content)

            for idx, sec in enumerate(sections):
                sec_text = sec.strip()
                if not sec_text:
                    continue

                # Extract section header title
                match = re.match(r"^##\s+(.+)$", sec_text, re.MULTILINE)
                sec_title = match.group(1).strip() if match else f"Bagian {idx + 1}"

                # Extract keywords from title and content
                tokens = re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", sec_text.lower())
                unique_tokens = list(set(tokens))

                chunk = KnowledgeChunk(
                    chunk_id=f"{doc_id}_{idx+1}",
                    doc_id=doc_id,
                    doc_title=meta.title,
                    decree_number=meta.decree_number,
                    publisher=meta.publisher,
                    scope=meta.scope,
                    section_title=sec_title,
                    content=sec_text,
                    keywords=unique_tokens,
                )
                self.chunks.append(chunk)

    def search(
        self,
        query: str,
        scope: str = "all",
        top_k: int = 3,
    ) -> List[SearchResult]:
        """Perform semantic keyword-weighted retrieval against indexed chunks.

        Args:
            query: The user prompt or question in Indonesian.
            scope: Filtering scope ('all', 'universitas', or 'filkom').
            top_k: Maximum number of relevant chunks to return.

        Returns:
            List of SearchResult items ranked by relevance score.
        """
        clean_query = query.lower()
        query_words = set(re.findall(r"\b[a-zA-Z0-9_\-]{3,}\b", clean_query))

        # Specialized domain booster mappings
        domain_boosters = {
            "uts": ["uts", "ujian tengah semester", "19", "24", "oktober", "susulan"],
            "uas": ["uas", "ujian akhir semester", "14", "19", "desember", "susulan"],
            "krs": ["krs", "heregistrasi", "revisi krs", "registrasi", "februari"],
            "presensi": ["presensi", "kehadiran", "75%", "10%", "evaluasi"],
            "absen": ["presensi", "kehadiran", "75%", "10%"],
            "remedial": ["remedial", "remedial teaching", "nilai d", "15 orang", "perbaikan nilai", "susulan"],
            "susulan": ["ujian susulan", "remedial", "uts susulan", "uas susulan"],
            "cuti": ["cuti", "cuti akademik", "2 kali", "dua semester"],
            "drop out": ["drop out", "d.o.", "ips", "14 semester"],
            "do": ["drop out", "d.o.", "ips", "14 semester"],
            "sks": ["sks", "170 menit", "50 menit", "beban studi"],
            "skripsi": ["skripsi", "tugas akhir", "uaps", "130 sks", "122 sks", "6 sks", "sempro", "proposal", "bimbingan", "jurnal", "sinta"],
            "tugas akhir": ["tugas akhir", "skripsi", "uaps", "6 sks", "sempro", "jurnal", "sinta", "capstone"],
            "sidang": ["sidang", "uaps", "ujian akhir program", "lsp", "toefl", "ipk", "2.40"],
            "sempro": ["seminar proposal", "sempro", "proposal skripsi", "judul"],
            "jurnal": ["jurnal", "sinta", "scopus", "non-skripsi", "rekognisi", "publikasi"],
            "kp": ["kerja praktik", "kp", "100 sks", "magang"],
            "obe": ["obe", "outcome-based education", "cpl", "0269"],
            "mbkm": ["mbkm", "magang bersertifikat", "studi independen", "20 sks", "capstone"],
            "bayar": ["biaya", "pelunasan", "angsuran", "pembayaran"],
            "biaya": ["biaya", "pelunasan", "angsuran", "pembayaran"],
            "sispema": ["sispema", "surat rekomendasi", "kemahasiswaan"],
            "viktor": ["viktor", "kampus 2", "helpdesk", "fti"],
        }

        scored_results: List[SearchResult] = []

        for chunk in self.chunks:
            content_lower = chunk.content.lower()
            title_lower = chunk.section_title.lower()

            score = 0.0

            # 0. Scope priority boost (boost matching scope by +12.0, but never exclude shared university regulations)
            if scope and scope.lower() != "all":
                if chunk.scope.lower() == scope.lower():
                    score += 12.0

            # 1. Exact phrase match in title
            for qw in query_words:
                if qw in title_lower:
                    score += 18.0
                if qw in chunk.keywords:
                    score += 3.5

            # 2. Check domain boosters
            for key, boost_terms in domain_boosters.items():
                if key in clean_query:
                    for bt in boost_terms:
                        if bt in content_lower:
                            score += 6.0
                        if bt in title_lower:
                            score += 15.0

            # 3. Query string substring density
            for qw in query_words:
                count = content_lower.count(qw)
                score += min(count * 2.0, 10.0)

            if score > 0.0:
                citation_dict = {
                    "doc_title": chunk.doc_title,
                    "decree_number": chunk.decree_number,
                    "publisher": chunk.publisher,
                    "section": chunk.section_title,
                }
                scored_results.append(
                    SearchResult(
                        chunk_id=chunk.chunk_id,
                        doc_title=chunk.doc_title,
                        decree_number=chunk.decree_number,
                        publisher=chunk.publisher,
                        scope=chunk.scope,
                        section_title=chunk.section_title,
                        content=chunk.content,
                        relevance_score=score,
                        citation=citation_dict,
                    )
                )

        # Sort descending by relevance score
        scored_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return scored_results[:top_k]

    def get_document_catalog(self) -> List[DocumentMetadata]:
        """Return the official registered catalog of documents."""
        return list(self.documents.values())

    def format_context_for_prompt(
        self,
        results: List[SearchResult],
        include_citations: bool = True,
    ) -> str:
        """Format retrieved search results into a clean prompt context block."""
        if not results:
            return "TIDAK ADA DOKUMEN RELEVAN YANG DITEMUKAN PADA BASIS PENGETAHUAN."

        context_lines: List[str] = [
            "=== BASIS PENGETAHUAN RESMI UNIVERSITAS PAMULANG ==="
        ]

        for i, item in enumerate(results, 1):
            context_lines.append(f"\n[RUJUKAN RESMI #{i}]")
            context_lines.append(f"Dokumen: {item.doc_title}")
            context_lines.append(f"Nomor SK / Dasar Hukum: {item.decree_number}")
            context_lines.append(f"Penerbit: {item.publisher}")
            context_lines.append(f"Bagian: {item.section_title}")
            context_lines.append("Isi Kebijakan Terverifikasi:")
            context_lines.append(item.content)
            context_lines.append("-" * 40)

        return "\n".join(context_lines)
