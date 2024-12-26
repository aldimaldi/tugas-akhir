import sys
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import pymysql
from datetime import datetime
from subprocess import call

# Validasi login
if '--logged_in' not in sys.argv:
    call(['python', 'login.py'])
    sys.exit()

class Barang:
    def __init__(self, nama, harga_beli, harga_jual, stok, vendor):
        self.nama = nama
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.stok = stok
        self.vendor = vendor

class AplikasiInventaris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Barang")

        # Koneksi ke database
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="aldima15",  # Sesuaikan dengan password MySQL Anda
            database="inventaris"
        )
        self.cursor = self.conn.cursor()

        self.label_info = tk.Label(self, text="Informasi Barang", font=("Helvetica", 16, "bold"))
        self.label_info.grid(row=0, column=0, columnspan=2, pady=10)

        self.treeview_barang = ttk.Treeview(self, columns=("Nama", "Harga Beli", "Harga Jual", "Stok", "Vendor", "Total Harga"), show="headings")
        self.treeview_barang.heading("Nama", text="Nama Barang")
        self.treeview_barang.heading("Harga Beli", text="Harga Beli")
        self.treeview_barang.heading("Harga Jual", text="Harga Jual")
        self.treeview_barang.heading("Stok", text="Stok")
        self.treeview_barang.heading("Vendor", text="Vendor")
        self.treeview_barang.heading("Total Harga", text="Total Harga")
        self.treeview_barang.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.update_treeview()

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.btn_tambah = tk.Button(button_frame, text="Tambah Barang", command=self.tambah_barang)
        self.btn_tambah.pack(side=tk.LEFT, padx=5)

        self.btn_edit = tk.Button(button_frame, text="Edit Barang", command=self.edit_barang)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

        self.btn_hapus = tk.Button(button_frame, text="Hapus Barang", command=self.hapus_barang)
        self.btn_hapus.pack(side=tk.LEFT, padx=5)

        self.btn_beli = tk.Button(self, text="Beli Barang", command=self.beli_barang)
        self.btn_beli.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.btn_jual = tk.Button(self, text="Jual Barang", command=self.jual_barang)
        self.btn_jual.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        self.btn_trans = tk.Button(self, text="Tampilkan Transaksi", command=self.tampilkan_transaksi)
        self.btn_trans.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        self.label_cari = tk.Label(self, text="Cari Nama Barang:")
        self.label_cari.grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.entry_cari = tk.Entry(self)
        self.entry_cari.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
        self.btn_cari = tk.Button(self, text="Cari", command=self.cari_barang)
        self.btn_cari.grid(row=5, column=2, pady=5, padx=5, sticky="w")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_treeview(self, results=None):
        self.treeview_barang.delete(*self.treeview_barang.get_children())
        query = "SELECT nama, harga_beli, harga_jual, stok, vendor FROM data_barang"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        for row in data:
            total_harga = row[1] * row[3]
            self.treeview_barang.insert("", tk.END, values=[row[0], row[1], row[2], row[3], row[4], total_harga])

    def tambah_barang(self):
        nama = simpledialog.askstring("Tambah Barang", "Masukkan nama barang:")
        harga_beli = float(simpledialog.askstring("Tambah Barang", "Masukkan harga beli barang:"))
        harga_jual = float(simpledialog.askstring("Tambah Barang", "Masukkan harga jual barang:"))
        stok = int(simpledialog.askstring("Tambah Barang", "Masukkan stok barang:"))
        vendor = simpledialog.askstring("Tambah Barang", "Masukkan vendor barang:")

        query = "INSERT INTO data_barang (nama, harga_beli, harga_jual, stok, vendor) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (nama, harga_beli, harga_jual, stok, vendor))
        self.conn.commit()

        self.update_treeview()

    def edit_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            item = self.treeview_barang.item(selected_item)
            nama_lama = item['values'][0]
            
            nama = simpledialog.askstring("Edit Barang", "Masukkan nama barang:", initialvalue=nama_lama)
            harga_beli = float(simpledialog.askstring("Edit Barang", "Masukkan harga beli barang:", initialvalue=item['values'][1]))
            harga_jual = float(simpledialog.askstring("Edit Barang", "Masukkan harga jual barang:", initialvalue=item['values'][2]))
            stok = int(simpledialog.askstring("Edit Barang", "Masukkan stok barang:", initialvalue=item['values'][3]))
            vendor = simpledialog.askstring("Edit Barang", "Masukkan vendor barang:", initialvalue=item['values'][4])

            query = "UPDATE data_barang SET nama=%s, harga_beli=%s, harga_jual=%s, stok=%s, vendor=%s WHERE nama=%s"
            self.cursor.execute(query, (nama, harga_beli, harga_jual, stok, vendor, nama_lama))
            self.conn.commit()

            self.update_treeview()

    def hapus_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            item = self.treeview_barang.item(selected_item)
            nama = item['values'][0]

            query = "DELETE FROM data_barang WHERE nama=%s"
            self.cursor.execute(query, (nama,))
            self.conn.commit()

            self.update_treeview()

    def beli_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            item = self.treeview_barang.item(selected_item)
            nama = item['values'][0]

            jumlah = int(simpledialog.askstring("Beli Barang", f"Masukkan jumlah pembelian {nama}:"))

            query = "UPDATE data_barang SET stok = stok + %s WHERE nama=%s"
            self.cursor.execute(query, (jumlah, nama))
            self.conn.commit()

            self.save_transaction(nama, "Beli", jumlah)
            self.update_treeview()

    def jual_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            item = self.treeview_barang.item(selected_item)
            nama = item['values'][0]

            jumlah = int(simpledialog.askstring("Jual Barang", f"Masukkan jumlah penjualan {nama}:"))

            query = "SELECT stok FROM data_barang WHERE nama=%s"
            self.cursor.execute(query, (nama,))
            stok = self.cursor.fetchone()[0]

            if stok >= jumlah:
                query = "UPDATE data_barang SET stok = stok - %s WHERE nama=%s"
                self.cursor.execute(query, (jumlah, nama))
                self.conn.commit()

                self.save_transaction(nama, "Jual", jumlah)
                self.update_treeview()
            else:
                messagebox.showerror("Error", "Stok tidak mencukupi.")

    def save_transaction(self, nama_barang, jenis_transaksi, jumlah):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO data_transaksi (waktu, nama_barang, jenis_transaksi, jumlah) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (waktu, nama_barang, jenis_transaksi, jumlah))
        self.conn.commit()

    def tampilkan_transaksi(self):
        transaksi_window = tk.Toplevel(self)
        transaksi_window.title("Daftar Transaksi")

        treeview_trans = ttk.Treeview(transaksi_window, columns=("Waktu", "Nama Barang", "Jenis Transaksi", "Jumlah"), show="headings")
        treeview_trans.heading("Waktu", text="Waktu")
        treeview_trans.heading("Nama Barang", text="Nama Barang")
        treeview_trans.heading("Jenis Transaksi", text="Jenis Transaksi")
        treeview_trans.heading("Jumlah", text="Jumlah")
        treeview_trans.pack(padx=10, pady=10, fill="both", expand=True)

        query = "SELECT waktu, nama_barang, jenis_transaksi, jumlah FROM data_transaksi"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        for row in data:
            treeview_trans.insert("", tk.END, values=row)

    def cari_barang(self):
        query = self.entry_cari.get().lower()
        results = []
        query_db = "SELECT * FROM data_barang WHERE LOWER(nama) LIKE %s"
        self.cursor.execute(query_db, (f"%{query}%",))
        results = self.cursor.fetchall()

        if results:
            self.update_treeview([Barang(row[0], row[1], row[2], row[3], row[4]) for row in results])
        else:
            messagebox.showinfo("Info", "Barang tidak ditemukan.")

if __name__ == "__main__":
    app = AplikasiInventaris()
    app.mainloop()
