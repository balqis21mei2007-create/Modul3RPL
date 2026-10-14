import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# --- KELAS DATABASE ---
class Database:
    def __init__(self):
        self.host = "localhost"
        self.db_name = "perpustakaan"
        self.username = "root"
        self.password = ""
        self.conn = None

    def get_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password
            )
            if self.conn.is_connected():
                return self.conn
        except Error as e:
            print(f"Koneksi Gagal: {e}")
            return None

# --- KELAS TAMPILAN & KONTROL ---
class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x450")
        
        # Inisialisasi Database
        self.db = Database()
        
        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1) # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2) # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)
        
        # ==========================================
        # FRAME KIRI: FORMULIR INPUT BUKU
        # ==========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kiri, text="Form Data Buku", font=("Arial", 16, "bold")).pack(pady=15)
        
        # Komponen Input
        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Judul Buku")
        self.entry_judul.pack(pady=10, padx=15, fill="x")
        
        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Penulis")
        self.entry_penulis.pack(pady=10, padx=15, fill="x")
        
        self.entry_tahun = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tahun Terbit (Misal: 2024)")
        self.entry_tahun.pack(pady=10, padx=15, fill="x")
        
        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green", command=self.simpan_data)
        self.btn_simpan.pack(pady=20, padx=15, fill="x")
        
        # ==========================================
        # FRAME KANAN: TABEL DAFTAR BUKU
        # ==========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")).pack(pady=15)
        
        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id_buku", "judul", "penulis", "tahun_terbit")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)
        
        # Konfigurasi Header Tabel
        self.tabel.heading("id_buku", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun_terbit", text="Tahun")
        
        # Konfigurasi Lebar Kolom
        self.tabel.column("id_buku", width=40, anchor="center")
        self.tabel.column("judul", width=150)
        self.tabel.column("penulis", width=120)
        self.tabel.column("tahun_terbit", width=80, anchor="center")
        
        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Muat data saat aplikasi pertama kali dibuka
        self.load_data()

    def simpan_data(self):
        judul = self.entry_judul.get()
        penulis = self.entry_penulis.get()
        tahun = self.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showerror("Peringatan", "Semua kolom harus diisi!")
            return

        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # DISESUAIKAN: Menggunakan kolom 'tahun_terbit'
                query = "INSERT INTO buku (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
                cursor.execute(query, (judul, penulis, tahun))
                conn.commit()
                messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
                
                # Bersihkan form setelah simpan
                self.entry_judul.delete(0, 'end')
                self.entry_penulis.delete(0, 'end')
                self.entry_tahun.delete(0, 'end')
                
                # Perbarui isi tabel
                self.load_data()
            except Error as e:
                messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
            finally:
                cursor.close()
                conn.close()

    def load_data(self):
        # Bersihkan data lama di tabel
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # DISESUAIKAN: Mengambil 'id_buku' dan 'tahun_terbit'
                cursor.execute("SELECT id_buku, judul, penulis, tahun_terbit FROM buku")
                rows = cursor.fetchall()
                for row in rows:
                    self.tabel.insert("", "end", values=row)
            except Error as e:
                print(f"Gagal memuat data: {e}")
            finally:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    app = BukuView()
    app.mainloop()