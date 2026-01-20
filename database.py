import sqlite3

DB_NAME = "keuangan.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Buat tabel dasar
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jenis TEXT,
            nominal INTEGER,
            keterangan TEXT
        )
    """)
    conn.commit()
    conn.close()

    # Pastikan kolom tanggal ada
    migrate_add_tanggal()


def migrate_add_tanggal():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(transaksi)")
    kolom = [row[1] for row in cursor.fetchall()]

    if "tanggal" not in kolom:
        cursor.execute("ALTER TABLE transaksi ADD COLUMN tanggal TEXT")
        conn.commit()

    conn.close()


def insert_transaksi(tanggal, jenis, nominal, keterangan):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transaksi (tanggal, jenis, nominal, keterangan)
        VALUES (?, ?, ?, ?)
    """, (tanggal, jenis, nominal, keterangan))

    conn.commit()
    conn.close()


def get_all_transaksi():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, tanggal, jenis, nominal, keterangan
        FROM transaksi
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def delete_transaksi(id_transaksi):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transaksi WHERE id = ?",
        (id_transaksi,)
    )

    conn.commit()
    conn.close()


def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(nominal) FROM transaksi WHERE jenis='Pemasukan'"
    )
    pemasukan = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(nominal) FROM transaksi WHERE jenis='Pengeluaran'"
    )
    pengeluaran = cursor.fetchone()[0] or 0

    conn.close()
    return pemasukan, pengeluaran
