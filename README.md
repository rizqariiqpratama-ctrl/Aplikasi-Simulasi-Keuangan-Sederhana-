# Aplikasi-Simulasi-Keuangan-Sederhana-

---

## 🔗 Konsep Signal dan Slot (Event Handling)

PySide6 menggunakan konsep **Signal dan Slot** untuk menghubungkan aksi pengguna
dengan fungsi (logika program).

Contoh penerapan pada aplikasi ini:
- Saat tombol **Simpan** ditekan, maka fungsi `simpan_data()` akan dijalankan
- Saat teks nominal berubah, format rupiah otomatis diperbarui

Hal ini membuat aplikasi menjadi **interaktif dan responsif** terhadap input pengguna.

---

## 🗂️ Pengaturan Layout (Tata Letak)

Aplikasi ini menggunakan sistem layout dari Qt agar tampilan rapi dan fleksibel.

Layout yang digunakan:
- **QVBoxLayout** → Mengatur widget secara vertikal
- **QGridLayout** → Mengatur widget dalam bentuk baris dan kolom (form input)
- **QGroupBox** → Mengelompokkan widget agar tampilan lebih terstruktur

Dengan layout ini, aplikasi tetap terlihat rapi meskipun ukuran window berubah.

---

## 🖼️ Banner dan Tampilan GUI

Aplikasi menggunakan **banner gambar (.jpg)** sebagai header untuk memperindah tampilan.
Banner ditampilkan menggunakan:
- `QLabel` untuk menampilkan gambar
- `QPixmap` untuk memuat file gambar
- Teks judul ditampilkan di tengah banner menggunakan overlay label

Tujuan penggunaan banner:
- Membuat tampilan lebih profesional
- Memberikan identitas visual pada aplikasi

---

## 🧮 Format Mata Uang Rupiah

Aplikasi ini memiliki fitur otomatis untuk:
- Mengubah input angka menjadi format Rupiah (Rp)
- Menghapus karakter non-angka sebelum disimpan ke database

Hal ini bertujuan untuk:
- Menghindari kesalahan input
- Menyeragamkan format data keuangan

---

## 🗄️ Database SQLite

Aplikasi ini menggunakan **SQLite** sebagai database lokal.
Database dipisahkan ke file `database.py` agar:
- Kode lebih rapi dan terstruktur
- Mudah dikembangkan di masa depan
- Logika database tidak tercampur dengan GUI

Fungsi database meliputi:
- Menyimpan transaksi
- Mengambil data transaksi
- Menghapus transaksi
- Menghitung saldo

---

## 📊 Simulasi Keuangan

Selain transaksi nyata, aplikasi menyediakan fitur **simulasi keuangan**.
Fitur ini memungkinkan pengguna:
- Memprediksi saldo di masa depan
- Menambahkan pemasukan atau pengeluaran simulasi
- Menghapus data simulasi tanpa memengaruhi data asli

Fitur simulasi membantu pengguna dalam **pengambilan keputusan finansial**.

---

## 🧑‍🎓 Tujuan Pembuatan Aplikasi

Aplikasi ini dibuat sebagai:
- Final Project mata kuliah Pemrograman Visual
- Media pembelajaran GUI dengan PySide6
- Simulasi sederhana pengelolaan keuangan pribadi

---

Link Video :
https://www.youtube.com/watch?v=WWzKSvExGyE
