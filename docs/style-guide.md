# 🎨 UNPAM Academic Chatbot - UI/UX & Style Guide


UNPAM AI --- UI/UX Style Guide
Produk: Asisten Akademik UNPAM (UNPAM Academic AI Assistant)
Platform: Standalone web portal
Versi: 1.0
Arah desain: Modern minimalis, editorial premium, academic
technology

1. Ringkasan Produk
UNPAM AI adalah portal web mandiri yang membantu mahasiswa dan civitas
akademika mendapatkan informasi perkuliahan melalui percakapan AI.
Portal ini bukan widget pop-up kecil dan bukan ekstensi yang disisipkan
ke website resmi kampus.

Antarmuka harus terasa bersih, tenang, mudah dipahami, dan dapat
dipercaya. Pengguna perlu bisa memulai percakapan dengan cepat,
melanjutkan pertanyaan, melihat riwayat chat, mengatur preferensi
jawaban, serta memeriksa sumber resmi yang menjadi dasar jawaban.

Prinsip desain
Clarity first: informasi utama mudah ditemukan dan dipahami.
Whitespace terukur: berikan ruang antarelemen agar halaman
terasa lapang, bukan kosong tanpa tujuan.
Trust through sources: sumber akademik harus terlihat jelas di
dalam jawaban.
Conversation first: area percakapan menjadi fokus utama setelah
pengguna mulai bertanya.
Consistent themes: light mode dan dark mode memiliki struktur
serta kontras yang konsisten.
Responsive by design: tampilan harus tetap nyaman di desktop,
tablet, dan ponsel.
Subtle interaction: animasi membantu memberi umpan balik, bukan
menjadi dekorasi yang mengganggu.
2. Arah Visual
Gunakan pendekatan clean academic AI dengan kualitas visual yang
terinspirasi dari produk AI modern dan website editorial premium.
Identitas kampus hadir melalui nama, logo yang sah digunakan, konten
akademik, dan aksen visual yang terkendali.

Karakter visual
Modern, minimalis, profesional, dan ramah.
Dominasi putih atau warna netral lembut dengan aksen biru langit.
Tipografi jelas dengan hierarki yang tegas.
Sudut komponen sedikit membulat, tidak berlebihan.
Border tipis dan bayangan lembut hanya jika membantu pemisahan
bidang.
Hindari dashboard yang padat, gradient berlebihan, efek kaca yang
terlalu kuat, serta ornamen yang tidak mendukung tugas pengguna.
Referensi nuansa
ChatGPT: fokus pada percakapan, komposisi sederhana, dan input
yang mudah dijangkau.
Gemini: penggunaan aksen warna yang ringan dan kesan AI modern.
Website editorial premium: headline kuat, ritme whitespace,
serta tata letak yang rapi.
Referensi tersebut menjadi inspirasi arah desain, bukan untuk menyalin
antarmuka atau identitas visual produk lain.

3. Sistem Warna
3.1 Light mode
Token Nilai Penggunaan

--color-bg #F8FAFC Latar utama aplikasi
--color-surface #FFFFFF Sidebar, kartu, panel, dan input
--color-surface-muted #F1F7FC Area sekunder dan hover lembut
--color-primary #38BDF8 Aksen biru langit
--color-primary-strong #2563EB Tombol utama dan aksi penting
--color-primary-soft #E0F2FE Chip, badge, dan latar ikon
--color-text #0F2742 Teks utama
--color-text-muted #64748B Teks sekunder
--color-border #DCE7F1 Border dan pemisah
--color-success #15803D Status berhasil
--color-warning #B45309 Peringatan
--color-danger #B91C1C Error dan tindakan berisiko

3.2 Dark mode
Token Nilai Penggunaan

--color-bg #0B1220 Latar utama
--color-surface #111C2E Sidebar dan panel
--color-surface-raised #17263B Kartu dan area input
--color-primary #38BDF8 Aksen biru langit
--color-primary-strong #60A5FA Aksi utama dan tautan
--color-primary-soft #153653 Latar aksen
--color-text #E8F1FA Teks utama
--color-text-muted #9CB0C7 Teks sekunder
--color-border #26374D Border dan pemisah
--color-success #4ADE80 Status berhasil
--color-warning #FBBF24 Peringatan
--color-danger #F87171 Error dan tindakan berisiko

Aturan penggunaan warna
Biru langit menjadi identitas visual, tetapi jangan gunakan sebagai
warna semua elemen.
Gunakan biru yang lebih kuat untuk tombol utama agar jelas sebagai
aksi.
Pastikan teks dan komponen memiliki kontras yang cukup pada kedua
tema.
Jangan mengandalkan warna saja untuk membedakan status; tambahkan
label atau ikon.
Status sumber resmi, sumber tidak tersedia, dan jawaban yang perlu
diverifikasi harus dibedakan secara jelas.
4. Tipografi
Font utama: Inter atau Geist. Gunakan satu keluarga font secara
konsisten jika memungkinkan.

Elemen Ukuran desktop Berat Catatan

Headline landing 44--56 px Bold / 700 Ringkas dan
dominan

Judul halaman 28--36 px Semibold / 600 Menandai konteks
halaman

Judul bagian 20--24 px Semibold / 600 Untuk kelompok
konten

Isi percakapan 15--16 px Regular / 400 Nyaman untuk
membaca jawaban
panjang

Label kontrol 13--14 px Medium / 500 Untuk input dan
pengaturan

Metadata 12--13 px Regular / 400 Waktu, status,
dan keterangan
sumber

Aturan tipografi
Gunakan headline yang kuat, tetapi hindari seluruh teks menggunakan
bold.
Batasi lebar baris untuk paragraf panjang agar mudah dipindai.
Beri jarak yang cukup antara judul, isi, daftar, dan blok sumber.
Gunakan line-height sekitar 1.5--1.7 untuk isi jawaban.
Pada layar ponsel, headline landing dapat turun menjadi sekitar
32--38 px.
5. Layout dan Spacing
Gunakan sistem spacing berbasis kelipatan 4 atau 8 px agar jarak
konsisten.

Token Nilai Penggunaan

space-1 4 px Jarak ikon dan label yang rapat
space-2 8 px Jarak kecil antarelemen
space-3 12 px Jarak kontrol dan metadata
space-4 16 px Padding komponen standar
space-6 24 px Jarak antarkelompok
space-8 32 px Jarak antarbagiannya
space-12 48 px Ruang section
space-16 64 px Ruang besar pada landing

Grid dan ukuran
Lebar konten landing: sekitar 1120--1240 px pada layar desktop
lebar.
Area baca percakapan: sekitar 720--820 px agar jawaban tidak terlalu
melebar.
Sidebar desktop: sekitar 250--290 px, dapat disembunyikan.
Tinggi input chat: sekitar 56--72 px, bertambah sesuai isi.
Gunakan padding halaman yang adaptif; jangan mempertahankan padding
desktop pada ponsel.
Hindari memenuhi setiap ruang kosong dengan kartu atau dekorasi.
6. Struktur Portal
Portal terdiri dari empat area utama:

Landing page.
Chat interface.
Riwayat percakapan.
Pengaturan.
Navigasi dan struktur visual harus konsisten di seluruh area.

6.1 Landing page
Tujuan: membantu pengguna memahami fungsi portal dan memulai pertanyaan
tanpa hambatan.

Struktur:

Header berisi identitas UNPAM AI, navigasi ringkas, kontrol tema,
dan tombol mulai.
Hero dengan label singkat tentang asisten akademik.
Headline utama: "Asisten Akademik UNPAM".
Deskripsi pendek yang menjelaskan bahwa pengguna dapat bertanya
tentang perkuliahan dan memperoleh jawaban berbasis sumber.
Kartu pintasan topik akademik.
Input pertanyaan utama dengan ikon lampiran opsional dan tombol
kirim.
Catatan singkat bahwa jawaban merujuk pada sumber yang tersedia.
Pintasan topik yang disarankan:

Kalender Akademik 2026/2027.
Kehadiran dan syarat UAS.
Cuti Kuliah dan Remedial.
Kurikulum OBE dan Magang MBKM.
Gunakan kartu sederhana dengan ikon, judul, dan deskripsi satu baris.
Kartu hanya menjadi jalan pintas; input pertanyaan tetap menjadi aksi
utama.

Visual: latar putih atau biru sangat pucat, headline gelap, aksen
biru langit, whitespace luas. Foto gedung kampus boleh dipakai sebagai
elemen pendukung yang lembut, tetapi jangan sampai mengurangi
keterbacaan atau menjadikan halaman seperti situs promosi.

6.2 Chat interface
Tujuan: menjadi ruang kerja utama untuk tanya jawab akademik.

Struktur desktop:

Sidebar kiri yang bisa disembunyikan.
Header percakapan dengan judul chat.
Kontrol cakupan informasi: Universitas atau Fakultas FILKOM.
Kontrol gaya jawaban: Formal, Ramah, atau Ringkas.
Kontrol tema dan akses profil/pengaturan.
Area pesan dengan lebar baca terkontrol.
Input pesan yang mudah dijangkau di bagian bawah.
Keterangan ringkas mengenai verifikasi informasi dan sumber.
Tampilan pesan:

Pesan pengguna rata kanan atau memakai bubble yang ringan.
Jawaban AI memiliki ruang lebih luas dan struktur yang jelas.
Gunakan heading, paragraf, daftar, dan tabel hanya jika memang
membantu.
Hindari membungkus setiap paragraf jawaban AI dalam kartu terpisah.
Tampilkan indikator proses saat AI sedang menyiapkan jawaban.
Sediakan tindakan salin atau beri umpan balik jika dibutuhkan.
Jawaban berbasis sumber:

Setiap jawaban yang merujuk dokumen perlu menyediakan bagian Sumber
yang mudah ditemukan. Tampilkan nama dokumen, jenis atau bagian dokumen
jika tersedia, serta tautan untuk membuka sumber apabila tersedia.

Contoh struktur visual:

Sumber

SK Kalender Akademik 2026/2027 --- Universitas Pamulang
Lihat dokumen sumber ↗

Jangan membuat judul dokumen, nomor halaman, kutipan, atau tautan yang
tidak benar-benar tersedia. Jika sumber tidak ditemukan, beri tahu
pengguna secara jelas dan jangan menampilkan sitasi palsu.

6.3 Sidebar dan riwayat chat
Sidebar menampung:

Logo dan nama UNPAM AI.
Tombol Chat Baru sebagai aksi utama.
Navigasi Beranda, Riwayat Chat, dan Pengaturan.
Daftar percakapan terbaru.
Tombol sembunyikan sidebar.
Perilaku:

Chat aktif ditandai dengan latar aksen lembut atau indikator yang
jelas.
Nama percakapan dipotong dengan ellipsis jika terlalu panjang.
Kelompokkan riwayat berdasarkan waktu bila jumlah percakapan
meningkat.
Berikan hover state yang halus.
Pada layar kecil, sidebar berubah menjadi drawer yang bisa dibuka
dan ditutup.
Tindakan menghapus percakapan harus memiliki konfirmasi jika
penghapusan bersifat permanen.
6.4 Halaman pengaturan
Kelompokkan pengaturan ke dalam bagian yang mudah dipindai.

Preferensi jawaban - Gaya bahasa: Formal, Ramah, Ringkas. - Cakupan
informasi: Universitas atau Fakultas FILKOM. - Model AI: tampilkan
informasi model yang benar-benar digunakan oleh aplikasi.

Tampilan - Tema: Terang, Gelap, Ikuti Sistem. - Bahasa antarmuka
jika didukung. - Preferensi visual lain hanya jika memiliki fungsi yang
jelas.

Privasi dan percakapan - Informasi tentang penyimpanan riwayat. -
Kontrol riwayat sesuai kemampuan aplikasi. - Penjelasan singkat mengenai
pemrosesan data.

Jangan menampilkan pengaturan yang belum benar-benar didukung oleh
sistem. Misalnya, jika riwayat hanya disimpan selama sesi, jangan
memberi kesan bahwa riwayat tersimpan permanen.

7. Komponen UI
Tombol
Primary: biru kuat, teks putih, digunakan untuk aksi utama
seperti mengirim pesan atau memulai chat.
Secondary: latar transparan atau netral dengan border tipis.
Ghost: tanpa latar permanen, digunakan untuk ikon atau aksi
pendukung.
Danger: digunakan khusus untuk tindakan destruktif.
Tombol harus memiliki state normal, hover, focus, active, disabled, dan
loading.

Input chat
Latar mengikuti surface tema.
Border tipis dengan focus ring biru.
Placeholder singkat dan jelas.
Tombol kirim memiliki ikon panah ke atas atau ikon kirim yang
konsisten.
Mendukung Enter untuk mengirim dan Shift+Enter untuk baris baru jika
perilaku tersebut sesuai dengan implementasi.
Berikan label aksesibel, bukan hanya placeholder.
Kartu topik
Ikon sederhana dalam bidang aksen lembut.
Judul singkat.
Deskripsi ringkas.
Border tipis, sudut membulat, dan hover state yang tidak mencolok.
Seluruh kartu dapat diklik jika memang berfungsi sebagai pintasan.
Chip dan selector
Gunakan chip untuk cakupan, gaya bahasa, atau saran pertanyaan. Pilihan
aktif harus memiliki pembeda visual yang jelas dan tetap terbaca pada
kedua tema.

Sumber dan sitasi
Pisahkan sumber dari isi jawaban menggunakan ruang, garis tipis,
atau surface lembut.
Tautan harus terlihat sebagai tautan.
Sumber yang tidak dapat dibuka tidak boleh diberi gaya seolah-olah
tautan aktif.
Jika ada beberapa sumber, tampilkan dalam daftar yang ringkas.
Ikon
Gunakan satu keluarga ikon outline secara konsisten. Ikon harus
mendukung makna dan memiliki ukuran yang seragam. Hindari mencampur ikon
outline, solid, emoji, dan ilustrasi dengan gaya yang berbeda-beda dalam
satu kelompok kontrol.

8. Dark Mode dan Light Mode
Kedua mode harus memakai struktur, ukuran, dan hierarki komponen yang
sama. Yang berubah terutama adalah token warna dan tingkat kontras.

Light mode menggunakan latar netral terang dan surface putih.
Dark mode menggunakan navy-charcoal, bukan hitam murni di semua
area.
Aksen biru tetap menjadi identitas produk.
Hover, focus, border, disabled, dan status harus disesuaikan per
tema.
Hindari membalik seluruh warna secara otomatis tanpa pemeriksaan
kontras.
Pilihan Ikuti Sistem harus mengikuti preferensi perangkat jika
implementasi mendukungnya.
Preferensi tema sebaiknya tetap konsisten saat berpindah halaman.
9. Responsive Design
Desktop
Sidebar riwayat terlihat secara default dan dapat disembunyikan.
Area percakapan berada di tengah dengan lebar baca terbatas.
Landing memiliki komposisi hero yang lapang dan kartu pintasan dalam
grid.
Tablet
Kurangi padding halaman dan jarak antarkomponen.
Sidebar dapat memakai mode ringkas atau drawer.
Kartu topik menggunakan dua kolom bila ruang memungkinkan.
Mobile
Gunakan header ringkas dengan tombol menu.
Sidebar tampil sebagai drawer, bukan kolom permanen.
Input chat tetap mudah dijangkau tanpa menutupi pesan.
Kartu topik dapat disusun satu kolom atau grid dua kolom jika masih
terbaca.
Kontrol cakupan dan gaya jawaban harus tetap mudah ditemukan,
misalnya melalui selector ringkas.
Hindari teks terlalu kecil, tombol berdekatan, dan area klik yang
sempit.
Pastikan keyboard virtual tidak menutupi input atau pesan terbaru.
10. Micro-interactions dan Motion
Animasi harus singkat, halus, dan memiliki tujuan.

Interaksi Perilaku yang disarankan

Hover tombol Perubahan warna atau elevasi yang sangat ringan
Membuka sidebar Transisi geser sekitar 180--240 ms
Berpindah tema Transisi warna sekitar 180--250 ms
Mengirim pesan Pesan muncul tanpa animasi berlebihan
AI sedang menjawab Indikator loading atau status yang jelas
Membuka sumber Tautan merespons dengan hover/focus state
Mengubah preferensi State aktif langsung terlihat

Gunakan easing yang lembut. Hormati preferensi prefers-reduced-motion
bila memungkinkan. Jangan menggunakan animasi panjang pada elemen yang
sering diakses.

11. Aksesibilitas dan Kepercayaan
Jaga kontras teks sesuai standar aksesibilitas yang relevan.
Semua kontrol dapat digunakan dengan keyboard.
Focus state harus terlihat jelas.
Gunakan label pada input dan tombol ikon.
Jangan mengandalkan warna saja untuk menyampaikan status.
Sediakan pesan error yang spesifik dan membantu.
Bedakan fakta dari sumber, ringkasan AI, dan informasi yang belum
terverifikasi.
Jangan menjanjikan jawaban selalu benar atau mengklaim sumber resmi
jika sumber tersebut tidak tersedia.
Sediakan cara yang jelas untuk membuka dokumen rujukan.
12. Konten dan Microcopy
Gunakan bahasa Indonesia yang alami, jelas, dan ramah. Hindari bahasa
terlalu birokratis, klaim berlebihan, atau istilah teknis yang tidak
diperlukan.

Contoh copy
Headline landing
Asisten Akademik UNPAM

Deskripsi
Tanyakan informasi perkuliahan dan temukan jawaban berdasarkan sumber
akademik yang tersedia.

Placeholder input
Tanyakan sesuatu tentang akademik...

Chat baru
Mulai percakapan baru

Sumber
Sumber rujukan

Sumber tidak ditemukan
Saya belum menemukan sumber yang cukup untuk memastikan informasi
tersebut. Silakan periksa dokumen resmi atau hubungi unit akademik
terkait.

Catatan kepercayaan
Periksa dokumen sumber untuk memastikan informasi akademik terbaru.

Pastikan nama model AI yang ditampilkan pada antarmuka sama dengan model
yang benar-benar digunakan oleh backend. Jangan menganggap nama model,
versi, atau status gratis selalu tetap; konfirmasikan melalui
konfigurasi dan dokumentasi penyedia saat implementasi.

13. Implementasi Visual
Style guide ini dapat diterapkan pada Streamlit dengan custom CSS.
Pisahkan token warna, tipografi, spacing, dan komponen agar mudah
dirawat.

Rekomendasi implementasi
Gunakan CSS variables untuk token tema.
Pisahkan gaya landing, sidebar, chat, sumber, input, dan pengaturan.
Gunakan state aplikasi untuk mengontrol tema, sidebar, cakupan, gaya
jawaban, dan percakapan.
Pastikan interaksi bukan sekadar dekorasi: setiap tombol dan
selector harus benar-benar menjalankan fungsi yang ditampilkan.
Uji tampilan pada lebar desktop, tablet, dan ponsel.
Periksa kembali perilaku komponen bawaan Streamlit agar konsisten
dengan desain kustom.
Jangan menampilkan fitur yang belum tersedia seolah-olah sudah
berfungsi.
Contoh token CSS
:root {
  --color-bg: #F8FAFC;
  --color-surface: #FFFFFF;
  --color-surface-muted: #F1F7FC;
  --color-primary: #38BDF8;
  --color-primary-strong: #2563EB;
  --color-primary-soft: #E0F2FE;
  --color-text: #0F2742;
  --color-text-muted: #64748B;
  --color-border: #DCE7F1;

  --font-sans: "Inter", "Geist", sans-serif;

  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;

  --shadow-soft: 0 8px 28px rgba(15, 39, 66, 0.06);
}

[data-theme="dark"] {
  --color-bg: #0B1220;
  --color-surface: #111C2E;
  --color-surface-muted: #17263B;
  --color-primary: #38BDF8;
  --color-primary-strong: #60A5FA;
  --color-primary-soft: #153653;
  --color-text: #E8F1FA;
  --color-text-muted: #9CB0C7;
  --color-border: #26374D;

  --shadow-soft: 0 8px 28px rgba(0, 0, 0, 0.18);
}
Contoh ini merupakan fondasi token, bukan implementasi tema yang
otomatis aktif. Atribut data-theme perlu diatur oleh aplikasi, atau
disesuaikan dengan mekanisme tema yang dipakai.

14. Checklist Evaluasi Desain
Sebelum mockup dianggap siap diimplementasikan, periksa hal berikut:

Portal terasa seperti aplikasi web mandiri, bukan widget pop-up.
Identitas UNPAM AI terlihat jelas dan tidak mendominasi konten.
Landing memiliki headline, deskripsi, pintasan topik, dan input
utama.
Chat menjadi fokus setelah percakapan dimulai.
Sidebar dapat disembunyikan dan riwayat mudah ditemukan.
Light mode dan dark mode sama-sama terbaca dengan baik.
Cakupan Universitas/FILKOM mudah ditemukan.
Gaya jawaban Formal/Ramah/Ringkas mudah diubah.
Sumber jawaban terlihat jelas dan tidak dibuat-buat.
Tampilan tetap nyaman di ponsel.
Focus state, loading state, error state, dan disabled state
dirancang.
Animasi halus, singkat, dan tidak mengganggu.
Tidak ada tombol atau kontrol yang hanya menjadi dekorasi.
Nama dan versi model AI sesuai dengan konfigurasi backend
sebenarnya.
15. Ringkasan Arah Desain
UNPAM AI harus terasa seperti asisten akademik digital yang modern,
terpercaya, dan mudah digunakan. Putih dan biru langit membentuk
identitas visual utama; tipografi tegas dan whitespace memberi kesan
premium; sidebar dan riwayat menjaga navigasi; sementara sitasi sumber
resmi memperkuat kepercayaan pengguna.

Prioritasnya bukan membuat antarmuka paling ramai atau paling
futuristik. Prioritasnya adalah membuat mahasiswa cepat menemukan tempat
bertanya, nyaman membaca jawaban, dan mudah memeriksa sumber informasi
akademik.

