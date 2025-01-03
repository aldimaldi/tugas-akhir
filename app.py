import sys
import tkinter as tk
from tkinter import *
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
            password="aldima15",
            database="inventaris"
        )
        self.cursor = self.conn.cursor()

        # Frame untuk Title dan Pencarian
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Label Informasi Barang (Title)
        self.label_info = tk.Label(title_frame, text="Informasi Barang", font=("Helvetica", 16, "bold"))
        self.label_info.grid(row=0, column=0, sticky="w", padx=5)

        # Label Cari
        self.label_cari = tk.Label(title_frame, text="Cari Nama Barang:")
        self.label_cari.grid(row=0, column=1, padx=5, sticky="e")

        # Entry Cari
        self.entry_cari = tk.Entry(title_frame)
        self.entry_cari.grid(row=0, column=2, padx=5, sticky="ew")

        # Tombol Cari
        self.btn_cari = tk.Button(title_frame, text="Cari", command=self.cari_barang)
        self.btn_cari.grid(row=0, column=3, padx=5, sticky="e")

        # Konfigurasi kolom untuk title_frame agar responsif
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(2, weight=1)

        # Treeview untuk daftar barang
        self.treeview_barang = ttk.Treeview(self, columns=("Nama", "Harga Beli", "Harga Jual", "Stok", "Vendor", "Total Harga"), show="headings")
        self.treeview_barang.heading("Nama", text="Nama Barang")
        self.treeview_barang.heading("Harga Beli", text="Harga Beli")
        self.treeview_barang.heading("Harga Jual", text="Harga Jual")
        self.treeview_barang.heading("Stok", text="Stok")
        self.treeview_barang.heading("Vendor", text="Vendor")
        self.treeview_barang.heading("Total Harga", text="Total Harga")
        self.treeview_barang.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.update_treeview()

        # Tambahkan scroll jika diperlukan
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview_barang.yview)
        self.treeview_barang.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")

        # Frame untuk tombol-tombol utama
        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.btn_tambah = tk.Button(button_frame, text="Tambah Barang", command=self.tambah_barang)
        self.btn_tambah.pack(side=tk.LEFT, padx=5)

        self.btn_edit = tk.Button(button_frame, text="Edit Barang", command=self.edit_barang)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

        self.btn_hapus = tk.Button(button_frame, text="Hapus Barang", command=self.hapus_barang)
        self.btn_hapus.pack(side=tk.LEFT, padx=5)

        # Tombol Beli Barang
        self.btn_beli = tk.Button(self, text="Beli Barang", command=self.beli_barang)
        self.btn_beli.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        # Tombol Jual Barang
        self.btn_jual = tk.Button(self, text="Jual Barang", command=self.jual_barang)
        self.btn_jual.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        # Tombol Tampilkan Transaksi
        self.btn_trans = tk.Button(self, text="Tampilkan Transaksi", command=self.tampilkan_transaksi)
        self.btn_trans.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Tombol Logout
        self.btn_logout = tk.Button(self, text="Logout", command=self.logout)
        self.btn_logout.grid(row=5, column=0, pady=5, padx=5, sticky="w")

        # Konfigurasi grid untuk responsivitas
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

    def update_treeview(self, results=None):
        self.treeview_barang.delete(*self.treeview_barang.get_children())

        query = "SELECT id, nama, harga_beli, harga_jual, stok, vendor FROM data_barang"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        for row in data:
            total_harga = row[2] * row[4]
            self.treeview_barang.insert("", tk.END, iid=row[0], values=[row[1], row[2], row[3], row[4], row[5], total_harga])

    def tambah_barang(self):
        def submit_barang():
            nama = entry_nama.get().strip()
            harga_beli = entry_harga_beli.get().strip()
            harga_jual = entry_harga_jual.get().strip()
            stok = entry_stok.get().strip()
            vendor = entry_vendor.get().strip()

            query = "INSERT INTO data_barang (nama, harga_beli, harga_jual, stok, vendor) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (nama, harga_beli, harga_jual, stok, vendor))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"Barang '{nama}' berhasil ditambahkan!")
            window.destroy()

        # Window input data barang
        window = tk.Toplevel(self)
        window.title("Tambah Barang")
        window.geometry("500x400")

        tk.Label(window, text="Nama Barang:").pack(pady=5)
        entry_nama = tk.Entry(window)
        entry_nama.pack(pady=5)

        tk.Label(window, text="Harga Beli:").pack(pady=5)
        entry_harga_beli = tk.Entry(window)
        entry_harga_beli.pack(pady=5)

        tk.Label(window, text="Harga Jual:").pack(pady=5)
        entry_harga_jual = tk.Entry(window)
        entry_harga_jual.pack(pady=5) 

        tk.Label(window, text="Stock:").pack(pady=5)
        entry_stok = tk.Entry(window)
        entry_stok.pack(pady=5)  

        tk.Label(window, text="Vendor:").pack(pady=5)
        entry_vendor = tk.Entry(window)
        entry_vendor.pack(pady=5)

        tk.Button(window, text="Submit", command=submit_barang).pack(pady=10)    

    def edit_barang(self):
        selected_item = self.treeview_barang.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih barang yang ingin diedit!")
            return
        
        id_barang = selected_item[0]
        item = self.treeview_barang.item(selected_item)
        nama_lama = item['values'][0]
        
        def submit_edit():
            new_nama = entry_nama.get().strip()
            new_harga_beli = entry_harga_beli.get().strip()
            new_harga_jual = entry_harga_jual.get().strip()
            new_stok = entry_stok.get().strip()
            new_vendor = entry_vendor.get().strip()

            if not new_nama or not new_harga_beli or not new_harga_jual or not new_stok or not new_vendor:
                messagebox.showerror("Error", "Semua kolom harus diisi!")
                return

            query = "UPDATE data_barang SET nama=%s, harga_beli=%s, harga_jual=%s, stok=%s, vendor=%s WHERE id=%s"
            self.cursor.execute(query, (new_nama, new_harga_beli, new_harga_jual, new_stok, new_vendor, id_barang))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"User '{nama_lama}' berhasil diperbarui!")
            window.destroy()
        
        # Window input
        window = tk.Toplevel(self)
        window.title("Edit Barang")
        window.geometry("500x400")

        tk.Label(window, text="Nama Barang:").pack(pady=5)
        entry_nama = tk.Entry(window)
        entry_nama.insert(0, nama_lama)
        entry_nama.pack(pady=5)

        tk.Label(window, text="Harga Beli:").pack(pady=5)
        entry_harga_beli = tk.Entry(window)
        entry_harga_beli.insert(0, item['values'][1])
        entry_harga_beli.pack(pady=5)

        tk.Label(window, text="Harga Jual:").pack(pady=5)
        entry_harga_jual = tk.Entry(window)
        entry_harga_jual.insert(0, item['values'][2])
        entry_harga_jual.pack(pady=5) 

        tk.Label(window, text="Stock:").pack(pady=5)
        entry_stok = tk.Entry(window)
        entry_stok.insert(0, item['values'][3])
        entry_stok.pack(pady=5)  

        tk.Label(window, text="Vendor:").pack(pady=5)
        entry_vendor = tk.Entry(window)
        entry_vendor.insert(0, item['values'][4])
        entry_vendor.pack(pady=5)

        tk.Button(window, text="Submit", command=submit_edit).pack(pady=10)

    def hapus_barang(self):
        selected_item = self.treeview_barang.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih barang yang ingin dihapus!")
            return
        
        id_barang = selected_item[0]
        item = self.treeview_barang.item(selected_item)
        nama = item['values'][0]

        confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus barang '{nama}'?")
        if confirm:
            query = "DELETE FROM data_barang WHERE id=%s"
            self.cursor.execute(query, (id_barang,))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"Barang '{nama}' berhasil dihapus!")

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
        keyword = self.entry_cari.get().strip().lower()

        if not keyword:
            self.update_treeview()
            return
        
        sql = "SELECT nama, harga_beli, harga_jual, stok, vendor FROM data_barang WHERE nama LIKE %s"
        self.cursor.execute(sql, (f"%{keyword}%",))
        results = self.cursor.fetchall()

        if results:
            self.treeview_barang.delete(*self.treeview_barang.get_children())
            for row in results:
                self.treeview_barang.insert("", tk.END, values=[row[0], row[1], row[2], row[3], row[4]])
        else:
            messagebox.showinfo("Info", "barang tidak ditemukan.")

    def logout(self):
        confirm = messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?")
        if confirm:
            messagebox.showinfo("Logout", "Anda berhasil logout.")
            self.destroy()
            call(['python', 'login.py'])

if __name__ == "__main__":
    app = AplikasiInventaris()
    app.mainloop()
