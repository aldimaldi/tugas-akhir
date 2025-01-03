import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from datetime import datetime
from subprocess import call

# Validasi login
if '--logged_in' not in sys.argv:
    call(['python', 'login.py'])
    sys.exit()

class User:
    def __init__(self, username, password, level):
        self.username = username
        self.password = password
        self.level = level

class AplikasiInventaris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Barang Admin")

        # Koneksi ke database
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="aldima15",  # Sesuaikan dengan password MySQL Anda
            database="inventaris"
        )
        self.cursor = self.conn.cursor()

        self.label_info = tk.Label(self, text="Informasi User", font=("Helvetica", 16, "bold"))
        self.label_info.grid(row=0, column=0, columnspan=2, pady=10)

        self.treeview_user = ttk.Treeview(self, columns=("username", "Level"), show="headings")
        self.treeview_user.heading("username", text="Username")
        self.treeview_user.heading("Level", text="Level")
        self.treeview_user.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.update_treeview()

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.btn_tambah = tk.Button(button_frame, text="Tambah User", command=self.tambah_user)
        self.btn_tambah.pack(side=tk.LEFT, padx=5)

        self.btn_edit = tk.Button(button_frame, text="Edit User", command=self.edit_user)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

        self.btn_hapus = tk.Button(button_frame, text="Hapus User", command=self.hapus_user)
        self.btn_hapus.pack(side=tk.LEFT, padx=5)

        self.btn_beli = tk.Button(self, text="Tampilkan data barang", command=self.tampilkan_barang)
        self.btn_beli.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.btn_jual = tk.Button(self, text="Tampilkan data transaksi", command=self.tampilkan_transaksi)
        self.btn_jual.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        self.label_cari = tk.Label(self, text="Cari username User:")
        self.label_cari.grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.entry_cari = tk.Entry(self)
        self.entry_cari.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
        self.btn_cari = tk.Button(self, text="Cari", command=self.cari_user)
        self.btn_cari.grid(row=5, column=2, pady=5, padx=5, sticky="w")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_treeview(self):
        self.treeview_user.delete(*self.treeview_user.get_children())

        query = "SELECT id, password, username, level FROM user"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        for row in data:
            # row[0] = id, row[1] = password, row[2] = username, row[3] = level
            self.treeview_user.insert("", tk.END, iid=row[0], values=(row[2], row[3]))

    # def tambah_user(self):
    #     nama = simpledialog.askstring("Tambah User", "Masukkan nama user:")
    #     password = float(simpledialog.askstring("Tambah user", "Masukkan password:"))
    #     level = float(simpledialog.askstring("Tambah user", "Masukkan harga jual user:"))

    #     query = "INSERT INTO user (nama, password, level) VALUES (%s, %s, %s)"
    #     self.cursor.execute(query, (nama, password, level))
    #     self.conn.commit()

    #     self.update_treeview()

    def tambah_user(self):
        def submit_user():
            username = entry_username.get().strip()
            password = entry_password.get().strip()
            level = combo_level.get().strip()

            if not username or not password or level == "Pilih level":
                messagebox.showerror("Error", "Semua kolom harus diisi!")
                return

            # Masukkan data ke database
            query = "INSERT INTO user (username, password, level) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password, level))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"User '{username}' berhasil ditambahkan!")
            window.destroy()

        # Window input
        window = tk.Toplevel(self)
        window.title("Tambah User")
        window.geometry("400x300")

        tk.Label(window, text="Username:").pack(pady=5)
        entry_username = tk.Entry(window)
        entry_username.pack(pady=5)

        tk.Label(window, text="Password:").pack(pady=5)
        entry_password = tk.Entry(window, show="*")
        entry_password.pack(pady=5)

        tk.Label(window, text="Level:").pack(pady=5)
        combo_level = ttk.Combobox(window, values=["Admin", "User"], state="readonly")
        combo_level.set("Pilih level")
        combo_level.pack(pady=5)

        tk.Button(window, text="Submit", command=submit_user).pack(pady=10)


    def edit_user(self):
        selected_item = self.treeview_user.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih user yang ingin diedit!")
            return

        id_user = selected_item[0]  # Ambil ID dari selection
        query = "SELECT password, username, level FROM user WHERE id=%s"
        self.cursor.execute(query, (id_user,))
        row = self.cursor.fetchone()

        if not row:
            messagebox.showerror("Error", "Data user tidak ditemukan!")
            return

        old_password, old_username, old_level = row

        def submit_edit():
            new_username = entry_username.get().strip()
            new_password = entry_password.get().strip()
            new_level = combo_level.get().strip()

            if new_password == '*' * len(old_password):
                new_password = old_password  # Password tidak diubah
            if not new_username or not new_password or new_level == "Pilih level":
                messagebox.showerror("Error", "Semua kolom harus diisi!")
                return

            # Update data di database
            query = "UPDATE user SET username=%s, password=%s, level=%s WHERE id=%s"
            self.cursor.execute(query, (new_username, new_password, new_level, id_user))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"User '{old_username}' berhasil diperbarui!")
            window.destroy()

        # Window input
        window = tk.Toplevel(self)
        window.title("Edit User")
        window.geometry("400x300")

        tk.Label(window, text="Username:").pack(pady=5)
        entry_username = tk.Entry(window)
        entry_username.insert(0, old_username)
        entry_username.pack(pady=5)

        tk.Label(window, text="Password:").pack(pady=5)
        entry_password = tk.Entry(window, show="*")
        entry_password.insert(0, '*' * len(old_password))
        entry_password.pack(pady=5)

        tk.Label(window, text="Level:").pack(pady=5)
        combo_level = ttk.Combobox(window, values=["Admin", "User"], state="readonly")
        combo_level.set(old_level)
        combo_level.pack(pady=5)

        tk.Button(window, text="Submit", command=submit_edit).pack(pady=10)

    def hapus_user(self):
        selected_item = self.treeview_user.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih user yang ingin dihapus!")
            return

        id_user = selected_item[0]
        item = self.treeview_user.item(selected_item)
        username = item['values'][0]

        confirm = messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus user '{username}'?")
        if confirm:
            query = "DELETE FROM user WHERE id=%s"
            self.cursor.execute(query, (id_user,))
            self.conn.commit()

            self.update_treeview()
            messagebox.showinfo("Success", f"User '{username}' berhasil dihapus!")

    def tampilkan_barang(self):
        barang_window = tk.Toplevel(self)
        barang_window.title("Daftar barang")

        treeview_barang = ttk.Treeview(barang_window, columns=("Nama", "Harga Beli", "Harga Jual", "Stok", "Vendor", "Total Harga"), show="headings")
        treeview_barang.heading("Nama", text="Nama Barang")
        treeview_barang.heading("Harga Beli", text="Harga Beli")
        treeview_barang.heading("Harga Jual", text="Harga Jual")
        treeview_barang.heading("Stok", text="Stok")
        treeview_barang.heading("Vendor", text="Vendor")
        treeview_barang.heading("Total Harga", text="Total Harga")
        treeview_barang.pack(padx=10, pady=10, fill="both", expand=True)

        query = "SELECT nama, harga_beli, harga_jual, stok, vendor FROM data_barang"
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        for row in data:
            total_harga = row[1] * row[3]
            treeview_barang.insert("", tk.END, values=[row[0], row[1], row[2], row[3], row[4], total_harga])

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

    def cari_user(self):
        query = self.entry_cari.get().strip()
        if not query:
            self.update_treeview()
            return

        sql = "SELECT username, level FROM user WHERE username LIKE %s"
        self.cursor.execute(sql, (f"%{query}%",))
        results = self.cursor.fetchall()

        if results:
            self.treeview_user.delete(*self.treeview_user.get_children())
            for row in results:
                self.treeview_user.insert("", tk.END, values=[row[0], row[1]])
        else:
            messagebox.showinfo("Info", "User tidak ditemukan.")


if __name__ == "__main__":
    app = AplikasiInventaris()
    app.mainloop()
