import sys
import os
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QDateEdit, QTabWidget, QGroupBox,
    QGridLayout
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont, QPixmap

import database
database.init_db()

# ================= RUPIAH =================
def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def rupiah_to_int(text):
    return int(re.sub(r"[^\d]", "", text)) if text else 0

# ================= MAIN WINDOW =================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Simulasi Keuangan")
        self.setGeometry(120, 70, 1000, 650)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab_input = QWidget()
        self.tab_riwayat = QWidget()
        self.tab_simulasi = QWidget()

        self.tabs.addTab(self.tab_input, "💰 Input Transaksi")
        self.tabs.addTab(self.tab_riwayat, "📊 Riwayat")
        self.tabs.addTab(self.tab_simulasi, "🧮 Simulasi")

        self.init_tab_input()
        self.init_tab_riwayat()
        self.init_tab_simulasi()

        self.simulasi_list = []

        self.load_data()
        self.update_ringkasan_by_date()

    # ================= TAB INPUT =================
    def init_tab_input(self):
        layout = QVBoxLayout()

        # --- Background Banner ---
        self.title_bg = QLabel()
        banner_path = os.path.join(os.path.dirname(__file__), "banner2.jpg")
        if os.path.exists(banner_path):
            pixmap = QPixmap(banner_path).scaled(600, 60, Qt.KeepAspectRatioByExpanding)
            self.title_bg.setPixmap(pixmap)
        else:
            print("⚠ Banner tidak ditemukan:", banner_path)
        self.title_bg.setFixedHeight(60)
        self.title_bg.setAlignment(Qt.AlignLeft)

        # Overlay teks
        self.title_text = QLabel("Input Transaksi Keuangan", self.title_bg)
        self.title_text.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_text.setStyleSheet("color: white; background-color: rgba(0,0,0,120);")
        self.title_text.setAlignment(Qt.AlignCenter)
        self.title_text.setGeometry(0, 0, 600, 60)

        # --- Form ---
        form_box = QGroupBox("Form Transaksi")
        grid = QGridLayout()

        self.tanggal = QDateEdit(QDate.currentDate())
        self.tanggal.setCalendarPopup(True)

        self.jenis = QComboBox()
        self.jenis.addItems(["Pemasukan", "Pengeluaran"])

        self.nominal = QLineEdit("Rp 0")
        self.nominal.setPlaceholderText("Rp 0")
        self.nominal.textChanged.connect(self.format_nominal_input)

        self.keterangan = QLineEdit()
        self.keterangan.setPlaceholderText("Contoh: Gaji, Makan, Beli Pulsa")
        self.keterangan.setMaxLength(50)

        self.btn_simpan = QPushButton("💾 Simpan")
        self.btn_simpan.clicked.connect(self.simpan_data)

        grid.addWidget(QLabel("Tanggal"), 0, 0)
        grid.addWidget(self.tanggal, 0, 1)
        grid.addWidget(QLabel("Jenis"), 1, 0)
        grid.addWidget(self.jenis, 1, 1)
        grid.addWidget(QLabel("Nominal"), 2, 0)
        grid.addWidget(self.nominal, 2, 1)
        grid.addWidget(QLabel("Keterangan"), 3, 0)
        grid.addWidget(self.keterangan, 3, 1)
        grid.addWidget(self.btn_simpan, 4, 0, 1, 2)

        form_box.setLayout(grid)

        # --- Ringkasan ---
        ring_box = QGroupBox("Ringkasan Hari Ini")
        ring_layout = QVBoxLayout()
        self.lbl_masuk = QLabel("Pemasukan: Rp 0")
        self.lbl_keluar = QLabel("Pengeluaran: Rp 0")
        self.lbl_saldo_hari = QLabel("Saldo Hari Ini: Rp 0")
        for lbl in (self.lbl_masuk, self.lbl_keluar, self.lbl_saldo_hari):
            lbl.setFont(QFont("Arial", 11, QFont.Bold))
        ring_layout.addWidget(self.lbl_masuk)
        ring_layout.addWidget(self.lbl_keluar)
        ring_layout.addWidget(self.lbl_saldo_hari)
        ring_box.setLayout(ring_layout)

        layout.addWidget(self.title_bg)
        layout.addWidget(form_box)
        layout.addWidget(ring_box)
        self.tab_input.setLayout(layout)

    # ================= TAB RIWAYAT =================
    def init_tab_riwayat(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tanggal", "Jenis", "Nominal", "Keterangan"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.label_saldo = QLabel("Saldo Total: Rp 0")
        self.label_saldo.setFont(QFont("Arial", 12, QFont.Bold))

        self.btn_hapus = QPushButton("🗑 Hapus Transaksi")
        self.btn_hapus.clicked.connect(self.hapus_transaksi)

        layout.addWidget(self.table)
        layout.addWidget(self.label_saldo)
        layout.addWidget(self.btn_hapus)
        self.tab_riwayat.setLayout(layout)

    # ================= TAB SIMULASI =================
    def init_tab_simulasi(self):
        layout = QVBoxLayout()

        form_box = QGroupBox("Form Simulasi")
        grid = QGridLayout()

        self.sim_tanggal = QDateEdit(QDate.currentDate())
        self.sim_tanggal.setCalendarPopup(True)

        self.sim_jenis = QComboBox()
        self.sim_jenis.addItems(["Pemasukan", "Pengeluaran"])

        self.sim_nominal = QLineEdit("Rp 0")
        self.sim_nominal.setPlaceholderText("Rp 0")
        self.sim_nominal.textChanged.connect(self.format_nominal_sim)

        self.sim_keterangan = QLineEdit()
        self.sim_keterangan.setPlaceholderText("Contoh: Gaji Tambahan, Belanja Bulanan")

        self.btn_tambah_sim = QPushButton("➕ Tambah Simulasi")
        self.btn_tambah_sim.clicked.connect(self.tambah_simulasi)

        grid.addWidget(QLabel("Tanggal"), 0, 0)
        grid.addWidget(self.sim_tanggal, 0, 1)
        grid.addWidget(QLabel("Jenis"), 1, 0)
        grid.addWidget(self.sim_jenis, 1, 1)
        grid.addWidget(QLabel("Nominal"), 2, 0)
        grid.addWidget(self.sim_nominal, 2, 1)
        grid.addWidget(QLabel("Keterangan"), 3, 0)
        grid.addWidget(self.sim_keterangan, 3, 1)
        grid.addWidget(self.btn_tambah_sim, 4, 0, 1, 2)

        form_box.setLayout(grid)

        self.table_sim = QTableWidget()
        self.table_sim.setColumnCount(5)
        self.table_sim.setHorizontalHeaderLabels(["Tanggal", "Jenis", "Nominal", "Keterangan", "Saldo Prediksi"])
        self.table_sim.horizontalHeader().setStretchLastSection(True)

        self.label_saldo_sim = QLabel("Saldo Simulasi: Rp 0")
        self.label_saldo_sim.setFont(QFont("Arial", 12, QFont.Bold))

        self.btn_hapus_sim = QPushButton("🗑 Hapus Simulasi")
        self.btn_hapus_sim.clicked.connect(self.hapus_simulasi)

        layout.addWidget(form_box)
        layout.addWidget(self.table_sim)
        layout.addWidget(self.label_saldo_sim)
        layout.addWidget(self.btn_hapus_sim)
        self.tab_simulasi.setLayout(layout)

    # ================= LOGIC =================
    def format_nominal_input(self):
        angka = rupiah_to_int(self.nominal.text())
        self.nominal.blockSignals(True)
        self.nominal.setText(format_rupiah(angka))
        self.nominal.blockSignals(False)

    def simpan_data(self):
        nominal = rupiah_to_int(self.nominal.text())
        keterangan = self.keterangan.text().strip()
        if nominal <= 0:
            QMessageBox.warning(self, "Error", "Nominal wajib diisi")
            return
        if keterangan == "":
            QMessageBox.warning(self, "Error", "Keterangan wajib diisi")
            return
        database.insert_transaksi(
            self.tanggal.date().toString("yyyy-MM-dd"),
            self.jenis.currentText(),
            nominal,
            keterangan
        )
        QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan")
        self.nominal.setText("Rp 0")
        self.keterangan.clear()
        self.load_data()
        self.update_ringkasan_by_date()

    def hapus_transaksi(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus")
            return
        id_trx = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus transaksi ini?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            database.delete_transaksi(id_trx)
            self.load_data()
            self.update_ringkasan_by_date()

    def load_data(self):
        data = database.get_all_transaksi()
        self.table.setRowCount(len(data))
        saldo = 0
        for row, (id_trx, tanggal, jenis, nominal, keterangan) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(id_trx)))
            self.table.setItem(row, 1, QTableWidgetItem(tanggal))
            self.table.setItem(row, 2, QTableWidgetItem(jenis))
            self.table.setItem(row, 3, QTableWidgetItem(format_rupiah(nominal)))
            self.table.setItem(row, 4, QTableWidgetItem(keterangan))
            saldo += nominal if jenis == "Pemasukan" else -nominal
        self.label_saldo.setText(f"Saldo Total: {format_rupiah(saldo)}")

    def update_ringkasan_by_date(self):
        selected_date = self.tanggal.date().toString("yyyy-MM-dd")
        data = database.get_all_transaksi()
        masuk = keluar = 0
        for _, tanggal, jenis, nominal, _ in data:
            if tanggal == selected_date:
                if jenis == "Pemasukan":
                    masuk += nominal
                else:
                    keluar += nominal
        self.lbl_masuk.setText(f"Pemasukan: {format_rupiah(masuk)}")
        self.lbl_keluar.setText(f"Pengeluaran: {format_rupiah(keluar)}")
        self.lbl_saldo_hari.setText(f"Saldo Hari Ini: {format_rupiah(masuk - keluar)}")

    # ================= LOGIC SIMULASI =================
    def format_nominal_sim(self):
        angka = rupiah_to_int(self.sim_nominal.text())
        self.sim_nominal.blockSignals(True)
        self.sim_nominal.setText(format_rupiah(angka))
        self.sim_nominal.blockSignals(False)

    def tambah_simulasi(self):
        nominal = rupiah_to_int(self.sim_nominal.text())
        keterangan = self.sim_keterangan.text().strip()
        if nominal <= 0:
            QMessageBox.warning(self, "Error", "Nominal wajib diisi")
            return
        if keterangan == "":
            QMessageBox.warning(self, "Error", "Keterangan wajib diisi")
            return
        tanggal = self.sim_tanggal.date().toString("yyyy-MM-dd")
        jenis = self.sim_jenis.currentText()
        self.simulasi_list.append((tanggal, jenis, nominal, keterangan))
        self.update_tabel_simulasi()
        self.sim_nominal.setText("Rp 0")
        self.sim_keterangan.clear()

    def hapus_simulasi(self):
        row = self.table_sim.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih simulasi yang ingin dihapus")
            return
        confirm = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus simulasi ini?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            del self.simulasi_list[row]
            self.update_tabel_simulasi()

    def update_tabel_simulasi(self):
        self.table_sim.setRowCount(len(self.simulasi_list))
        saldo = 0
        data = database.get_all_transaksi()
        for _, _, jenis, nominal, _ in data:
            saldo += nominal if jenis == "Pemasukan" else -nominal
        for row, (tgl, jenis, nominal, ket) in enumerate(sorted(self.simulasi_list)):
            saldo += nominal if jenis == "Pemasukan" else -nominal
            self.table_sim.setItem(row, 0, QTableWidgetItem(tgl))
            self.table_sim.setItem(row, 1, QTableWidgetItem(jenis))
            self.table_sim.setItem(row, 2, QTableWidgetItem(format_rupiah(nominal)))
            self.table_sim.setItem(row, 3, QTableWidgetItem(ket))
            self.table_sim.setItem(row, 4, QTableWidgetItem(format_rupiah(saldo)))
        self.label_saldo_sim.setText(f"Saldo Simulasi: {format_rupiah(saldo)}")

# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
