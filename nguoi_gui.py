import socket
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from datetime import datetime, timedelta
import base64
import json
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import zlib
import threading
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os

class NguoiGui:
    def __init__(self):
        self.window = ttk.Window(themename="superhero")
        self.window.title("Người Gửi - Chuyển File An Toàn")
        self.window.geometry("700x500")
        self.SERVER_HOST = "192.168.1.9"
        self.SERVER_PORT = 12345
        self.rsa_key = RSA.generate(2048)
        self.session_key = None
        self.deployment_mode = None
        self.khoa_nguoi_nhan = None
        logging.basicConfig(filename='log_gui.txt', level=logging.INFO, format='%(asctime)s: %(message)s')
        self.thiet_lap_gui()

    def thiet_lap_gui(self):
        try:
            img = Image.open("background.png")
            img = img.resize((700, 500), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.window, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except:
            pass

        khung_gui = ttk.Frame(self.window, padding=20, bootstyle="dark")
        khung_gui.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ttk.Label(khung_gui, text="Chuyển File An Toàn", font=("Arial", 20, "bold"), bootstyle="light").pack(pady=10)

        ttk.Label(khung_gui, text="Chọn phương thức triển khai:", font=("Arial", 12)).pack(pady=5)
        self.mode_var = tk.StringVar(value="1")
        ttk.Radiobutton(khung_gui, text="1. Local", variable=self.mode_var, value="1", bootstyle="primary").pack()
        ttk.Radiobutton(khung_gui, text="2. Internet (Google Drive)", variable=self.mode_var, value="2", bootstyle="primary").pack()

        ttk.Button(khung_gui, text="Chọn File", command=self.chon_file, bootstyle="success-outline", style="TButton").pack(pady=10)
        self.nhan_file = ttk.Label(khung_gui, text="Chưa chọn file", font=("Arial", 10), bootstyle="light")
        self.nhan_file.pack(pady=5)

        ttk.Button(khung_gui, text="Nhập Khóa Công Khai", command=self.nhap_khoa_cong_khai, bootstyle="info-outline").pack(pady=10)
        ttk.Button(khung_gui, text="Gửi File An Toàn", command=self.gui_file, bootstyle="danger", style="TButton").pack(pady=10)

        self.nhat_ky_text = tk.Text(khung_gui, height=8, font=("Arial", 10), bg="#2b2b2b", fg="white", insertbackground="white")
        self.nhat_ky_text.pack(padx=10, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        # Hiệu ứng hover cho nút
        for widget in khung_gui.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.bind("<Enter>", lambda e: e.widget.configure(bootstyle="primary"))
                widget.bind("<Leave>", lambda e: e.widget.configure(bootstyle=e.widget["bootstyle"].replace("primary", e.widget["bootstyle"].split("-")[0])))

    def nhat_ky(self, thong_bao):
        self.nhat_ky_text.insert(tk.END, f"{datetime.now()}: {thong_bao}\n")
        self.nhat_ky_text.see(tk.END)
        logging.info(thong_bao)

    def chon_file(self):
        duong_dan_file = filedialog.askopenfilename(filetypes=[("File", "*.*")])
        if duong_dan_file:
            self.duong_dan_file = duong_dan_file
            self.nhan_file.config(text=f"Đã chọn: {duong_dan_file.split('/')[-1]}")
            self.nhat_ky(f"Đã chọn file: {duong_dan_file}")

    def nhap_khoa_cong_khai(self):
        khoa_text = simpledialog.askstring("Nhập Khóa Công Khai", "Dán khóa công khai RSA của người nhận (định dạng PEM):")
        if khoa_text:
            try:
                self.khoa_nguoi_nhan = RSA.import_key(khoa_text)
                self.nhat_ky("Đã nhập khóa công khai của người nhận")
                messagebox.showinfo("Thành công", "Đã nhập khóa công khai!")
            except Exception as e:
                self.nhat_ky(f"Lỗi khi nhập khóa công khai: {str(e)}")
                messagebox.showerror("Lỗi", f"Khóa công khai không hợp lệ: {str(e)}")

    def gui_file(self):
        if not hasattr(self, 'duong_dan_file'):
            messagebox.showerror("Lỗi", "Vui lòng chọn file trước!")
            return

        self.deployment_mode = self.mode_var.get()
        if self.deployment_mode == "2" and not self.khoa_nguoi_nhan:
            messagebox.showerror("Lỗi", "Vui lòng nhập khóa công khai của người nhận trước!")
            return

        if self.deployment_mode == "1":
            threading.Thread(target=self._gui_file_local, daemon=True).start()
        elif self.deployment_mode == "2":
            threading.Thread(target=self._gui_file_internet, daemon=True).start()
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn phương thức triển khai!")

    def _gui_file_local(self):
        try:
            with open(self.duong_dan_file, 'rb') as f:
                du_lieu = f.read()
            du_lieu_nen = zlib.compress(du_lieu)

            self.session_key = get_random_bytes(32)
            iv = get_random_bytes(16)

            cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
            du_lieu_dinh_dang = self._dinh_dang(du_lieu_nen)
            ban_ma = cipher.encrypt(du_lieu_dinh_dang)

            thoi_han = (datetime.utcnow() + timedelta(hours=24)).isoformat() + 'Z'
            metadata = f"{self.duong_dan_file.split('/')[-1]}{thoi_han}".encode()
            doi_tuong_hash = SHA512.new(iv + ban_ma + thoi_han.encode())
            chu_ky = pkcs1_15.new(self.rsa_key).sign(doi_tuong_hash)

            goi_tin = {
                "iv": base64.b64encode(iv).decode(),
                "cipher": base64.b64encode(ban_ma).decode(),
                "hash": doi_tuong_hash.hexdigest(),
                "sig": base64.b64encode(chu_ky).decode(),
                "exp": thoi_han,
                "original_file": self.duong_dan_file.split('/')[-1]
            }

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.SERVER_HOST, self.SERVER_PORT))
                self.nhat_ky(f"Kết nối tới người nhận tại {self.SERVER_HOST}:{self.SERVER_PORT}")
                s.sendall("Xin chào!")
                phan_hoi = s.recv(1024).decode()
                if phan_hoi != "Sẵn sàng!":
                    self.nhat_ky("Bắt tay thất bại")
                    return

                s.sendall(self.rsa_key.publickey().export_key())
                self.khoa_nguoi_nhan = RSA.import_key(s.recv(4096))
                cipher_rsa = PKCS1_OAEP.new(self.khoa_nguoi_nhan)
                khoa_phien_ma_hoa = cipher_rsa.encrypt(self.session_key)
                s.sendall(base64.b64encode(khoa_phien_ma_hoa))

                s.sendall(json.dumps(goi_tin).encode())
                phan_hoi = s.recv(1024).decode()
                self.nhat_ky(f"Phản hồi từ người nhận ({self.SERVER_HOST}:{self.SERVER_PORT}): {phan_hoi}")
                if phan_hoi == "ACK":
                    messagebox.showinfo("Thành công", f"Gửi file {goi_tin['original_file']} thành công qua local tới {self.SERVER_HOST}:{self.SERVER_PORT}!")
                else:
                    messagebox.showerror("Lỗi", f"Gửi file thất bại: {phan_hoi}")

        except Exception as e:
            self.nhat_ky(f"Lỗi khi gửi qua local: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể gửi file qua local: {str(e)}")

    def _gui_file_internet(self):
        try:
            with open(self.duong_dan_file, 'rb') as f:
                du_lieu = f.read()
            du_lieu_nen = zlib.compress(du_lieu)

            self.session_key = get_random_bytes(32)
            iv = get_random_bytes(16)

            cipher = AES.new(self.session_key, AES.MODE_CBC, iv)
            du_lieu_dinh_dang = self._dinh_dang(du_lieu_nen)
            ban_ma = cipher.encrypt(du_lieu_dinh_dang)

            thoi_han = (datetime.utcnow() + timedelta(hours=24)).isoformat() + 'Z'
            metadata = f"{self.duong_dan_file.split('/')[-1]}{thoi_han}".encode()
            doi_tuong_hash = SHA512.new(iv + ban_ma + thoi_han.encode())
            chu_ky = pkcs1_15.new(self.rsa_key).sign(doi_tuong_hash)

            # Sử dụng pycryptodome để mã hóa khóa phiên với padding OAEP
            from Crypto.Cipher import PKCS1_OAEP
            cipher_rsa = PKCS1_OAEP.new(self.khoa_nguoi_nhan)
            khoa_phien_ma_hoa = cipher_rsa.encrypt(self.session_key)

            goi_tin = {
                "iv": base64.b64encode(iv).decode(),
                "cipher": base64.b64encode(ban_ma).decode(),
                "hash": doi_tuong_hash.hexdigest(),
                "sig": base64.b64encode(chu_ky).decode(),
                "exp": thoi_han,
                "public_key": self.rsa_key.publickey().export_key().decode(),
                "session_key": base64.b64encode(khoa_phien_ma_hoa).decode(),
                "original_file": self.duong_dan_file.split('/')[-1]
            }

            ten_file_tam = "encrypted_package.json"
            with open(ten_file_tam, 'w') as f:
                json.dump(goi_tin, f)

            file_size = os.path.getsize(ten_file_tam)
            credentials = None
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    ['https://www.googleapis.com/auth/drive.file']
                )
                credentials = flow.run_local_server(port=0)
            except FileNotFoundError:
                self.nhat_ky("Lỗi: Không tìm thấy file credentials.json")
                messagebox.showerror("Lỗi", "Vui lòng cung cấp file credentials.json!")
                return
            except Exception as e:
                self.nhat_ky(f"Lỗi xác thực Google Drive: {str(e)}")
                messagebox.showerror("Lỗi", f"Không thể xác thực với Google Drive: {str(e)}")
                return

            service = build('drive', 'v3', credentials=credentials)
            file_metadata = {
                'name': 'encrypted_email_package.json',
                'mimeType': 'application/json'
            }
            media = MediaFileUpload(ten_file_tam)
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink, createdTime'
            ).execute()

            file_id = file.get('id')
            web_link = file.get('webViewLink')
            created_time = file.get('createdTime')
            self.nhat_ky(f"Đã tải file lên Google Drive cá nhân. File ID: {file_id}, Link: {web_link}, Tên: {file_metadata['name']}, Thời gian tạo: {created_time}, Dung lượng: {file_size} bytes")
            messagebox.showinfo("Thành công", f"File đã được tải lên Google Drive cá nhân!\nLink: {web_link}\nFile ID: {file_id}\nDung lượng: {file_size} bytes\nHãy gửi link này cho người nhận.")

        except Exception as e:
            self.nhat_ky(f"Lỗi khi gửi qua Internet: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể gửi file qua Internet: {str(e)}")

    def _dinh_dang(self, du_lieu):
        do_dai_dinh_dang = 16 - (len(du_lieu) % 16)
        return du_lieu + bytes([do_dai_dinh_dang] * do_dai_dinh_dang)

    def chay(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = NguoiGui()
    app.chay()
