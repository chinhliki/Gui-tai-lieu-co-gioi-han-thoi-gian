import socket
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import base64
import json
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
import zlib
import threading
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from Crypto.Cipher import PKCS1_OAEP

class NguoiNhan:
    def __init__(self):
        self.window = ttk.Window(themename="superhero")
        self.window.title("Người Nhận - Chuyển File An Toàn")
        self.window.geometry("700x500")
        self.SERVER_HOST = "192.168.1.11"
        self.SERVER_PORT = 12345
        self.rsa_key = RSA.generate(2048)
        self.deployment_mode = None
        self.is_processing = False  # Thêm biến kiểm soát trạng thái xử lý
        logging.basicConfig(filename='log_nhan.txt', level=logging.INFO, format='%(asctime)s: %(message)s')
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

        khung_nhan = ttk.Frame(self.window, padding=20, bootstyle="dark")
        khung_nhan.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.8)

        ttk.Label(khung_nhan, text="Nhận File An Toàn", font=("Arial", 20, "bold"), bootstyle="light").pack(pady=10)

        ttk.Label(khung_nhan, text="Chọn phương thức triển khai:", font=("Arial", 12)).pack(pady=5)
        self.mode_var = tk.StringVar(value="1")
        ttk.Radiobutton(khung_nhan, text="1. Local", variable=self.mode_var, value="1", bootstyle="primary").pack()
        ttk.Radiobutton(khung_nhan, text="2. Internet (Google Drive)", variable=self.mode_var, value="2", bootstyle="primary").pack()

        ttk.Button(khung_nhan, text="Hiển Thị Khóa Công Khai", command=self.hien_thi_khoa_cong_khai, bootstyle="info-outline").pack(pady=10)
        ttk.Button(khung_nhan, text="Bắt Đầu Nhận", command=self.bat_dau_nhan, bootstyle="danger", style="TButton").pack(pady=10)

        self.nhan_trang_thai = ttk.Label(khung_nhan, text="Trạng Thái: Đang chờ", font=("Arial", 10), bootstyle="light")
        self.nhan_trang_thai.pack(pady=5)

        self.nhat_ky_text = tk.Text(khung_nhan, height=8, font=("Arial", 10), bg="#2b2b2b", fg="white", insertbackground="white")
        self.nhat_ky_text.pack(padx=10, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        # Hiệu ứng hover cho nút
        for widget in khung_nhan.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.bind("<Enter>", lambda e: e.widget.configure(bootstyle="primary"))
                widget.bind("<Leave>", lambda e: e.widget.configure(bootstyle=e.widget["bootstyle"].replace("primary", e.widget["bootstyle"].split("-")[0])))

        # Xử lý khi cửa sổ đóng
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def nhat_ky(self, thong_bao):
        if self.window.winfo_exists():  # Chỉ ghi log nếu cửa sổ còn tồn tại
            self.nhat_ky_text.insert(tk.END, f"{datetime.now()}: {thong_bao}\n")
            self.nhat_ky_text.see(tk.END)
            logging.info(thong_bao)

    def hien_thi_khoa_cong_khai(self):
        if self.window.winfo_exists():
            khoa_cong_khai = self.rsa_key.publickey().export_key().decode()
            self.nhat_ky(f"Khóa công khai của bạn:\n{khoa_cong_khai}")
            messagebox.showinfo("Khóa Công Khai", f"Khóa công khai:\n{khoa_cong_khai}\nHãy gửi khóa này cho Người gửi.")

    def bat_dau_nhan(self):
        if self.is_processing:
            self.nhat_ky("Lỗi: Đang xử lý, vui lòng đợi!")
            messagebox.showerror("Lỗi", "Đang xử lý, vui lòng đợi!")
            return
        self.deployment_mode = self.mode_var.get()
        if self.deployment_mode == "1":
            threading.Thread(target=self._nhan_file_local, daemon=True).start()
        elif self.deployment_mode == "2":
            self._nhan_file_internet()
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn phương thức triển khai!")

    def _nhan_file_local(self):
        try:
            self.nhan_trang_thai.config(text="Trạng Thái: Đang lắng nghe")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.SERVER_HOST, self.SERVER_PORT))
                s.listen()
                
                conn, addr = s.accept()
                with conn:
                    self.nhat_ky(f"Nhận kết nối từ {addr[0]}:{addr[1]}")
                    du_lieu = conn.recv(1024).decode()
                    if du_lieu != "Xin chào!":
                        self.nhat_ky("Bắt tay không hợp lệ")
                        return
                    conn.sendall("Sẵn sàng!".encode())  # Đã mã hóa

                    khoa_gui = RSA.import_key(conn.recv(4096))
                    conn.sendall(self.rsa_key.publickey().export_key())

                    khoa_phien_ma_hoa = base64.b64decode(conn.recv(4096))
                    cipher_rsa = PKCS1_OAEP.new(self.rsa_key)
                    khoa_phien = cipher_rsa.decrypt(khoa_phien_ma_hoa)
                    if khoa_phien is None:
                        conn.sendall("NACK: Không thể giải mã khóa phiên".encode())
                        self.nhat_ky("Không thể giải mã khóa phiên")
                        return
                    self.nhat_ky("Đã giải mã khóa phiên thành công")

                    goi_tin = json.loads(conn.recv(4096).decode())
                    
                    thoi_han = datetime.fromisoformat(goi_tin['exp'][:-1])
                    if datetime.utcnow() > thoi_han:
                        conn.sendall("NACK: Hết hạn".encode())
                        self.nhat_ky("File bị từ chối: Hết hạn")
                        return
                    self.nhat_ky(f"Kiểm tra thời hạn: Hợp lệ, hết hạn vào {goi_tin['exp']}")

                    iv = base64.b64decode(goi_tin['iv'])
                    ban_ma = base64.b64decode(goi_tin['cipher'])
                    doi_tuong_hash = SHA512.new(iv + ban_ma + goi_tin['exp'].encode())
                    if doi_tuong_hash.hexdigest() != goi_tin['hash']:
                        conn.sendall("NACK: Hash không hợp lệ".encode())
                        self.nhat_ky("File bị từ chối: Hash không hợp lệ")
                        return
                    self.nhat_ky("Kiểm tra hash: Hợp lệ")

                    chu_ky = base64.b64decode(goi_tin['sig'])
                    try:
                        pkcs1_15.new(khoa_gui).verify(doi_tuong_hash, chu_ky)
                        self.nhat_ky("Kiểm tra chữ ký: Hợp lệ")
                    except:
                        conn.sendall("NACK: Chữ ký không hợp lệ".encode())
                        self.nhat_ky("File bị từ chối: Chữ ký không hợp lệ")
                        return

                    cipher = AES.new(khoa_phien, AES.MODE_CBC, iv)
                    du_lieu_giai_ma = cipher.decrypt(ban_ma)
                    du_lieu_giai_nen = zlib.decompress(self._giai_dinh_dang(du_lieu_giai_ma))

                    ten_file = goi_tin.get('original_file', 'email_nhan_duoc.txt')
                    with open(ten_file, 'wb') as f:
                        f.write(du_lieu_giai_nen)
                    
                    conn.sendall("ACK".encode())
                    self.nhat_ky(f"Đã nhận và lưu file {ten_file} thành công từ {addr[0]}:{addr[1]} qua local")
                    messagebox.showinfo("Thành công", f"Đã nhận file {ten_file} thành công từ {addr[0]}:{addr[1]} qua local!")
        except Exception as e:
            self.nhat_ky(f"Lỗi khi nhận qua local: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể nhận file qua local: {str(e)}")
        finally:
            self.is_processing = False

    def _nhan_file_internet(self):
        if self.is_processing:
            self.nhat_ky("Lỗi: Đang xử lý, vui lòng đợi!")
            messagebox.showerror("Lỗi", "Đang xử lý, vui lòng đợi!")
            return
        self.is_processing = True
        try:
            drive_link = simpledialog.askstring("Nhập Link", "Vui lòng nhập link Google Drive của file JSON:")
            if not drive_link:
                self.nhat_ky("Lỗi: Không nhập link Google Drive")
                messagebox.showerror("Lỗi", "Vui lòng nhập link Google Drive!")
                return

            file_id = None
            match = re.search(r'/d/([a-zA-Z0-9_-]+)(?:/|$)', drive_link)
            if not match:
                self.nhat_ky(f"Lỗi: Link Google Drive không hợp lệ. Định dạng phải là https://drive.google.com/file/d/<file_id>/view")
                messagebox.showerror("Lỗi", "Link Google Drive không hợp lệ! Vui lòng kiểm tra lại định dạng (https://drive.google.com/file/d/<file_id>/view).")
                return
            file_id = match.group(1)
            self.nhat_ky(f"Nhận file từ Google Drive, File ID: {file_id}, Link: {drive_link}")

            credentials = None
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    ['https://www.googleapis.com/auth/drive.readonly']
                )
                credentials = flow.run_local_server(port=0)
            except FileNotFoundError:
                self.nhat_ky("Lỗi: Không tìm thấy file credentials.json")
                messagebox.showerror("Lỗi", "Vui lòng cung cấp file credentials.json!")
                return
            except Exception as e:
                self.nhat_ky(f"Lỗi xác thực Google: {str(e)}")
                messagebox.showerror("Lỗi", f"Xác thực Google thất bại: {str(e)}. Vui lòng kiểm tra Test Users hoặc scope.")
                return

            # Chạy phần tải file trong luồng phụ để không chặn GUI
            def download_file():
                try:
                    service = build('drive', 'v3', credentials=credentials)
                    file_metadata = service.files().get(fileId=file_id, fields='id, name, createdTime, size').execute()
                    file_size = file_metadata.get('size', 'N/A')
                    self.nhat_ky(f"Metadata file: Tên={file_metadata['name']}, Thời gian tạo={file_metadata['createdTime']}, Dung lượng={file_size} bytes")

                    request = service.files().get_media(fileId=file_id)
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                    self.nhat_ky("Đã tải file JSON từ Google Drive cá nhân")

                    fh.seek(0)
                    goi_tin = json.loads(fh.read().decode())
                    khoa_gui = RSA.import_key(goi_tin['public_key'])
                    # Sửa lỗi giải mã khóa phiên
                    khoa_phien_ma_hoa = base64.b64decode(goi_tin['session_key'])
                    cipher_rsa = PKCS1_OAEP.new(self.rsa_key)
                    khoa_phien = cipher_rsa.decrypt(khoa_phien_ma_hoa)
                    if khoa_phien is None:
                        self.nhat_ky("Lỗi: Không thể giải mã khóa phiên")
                        messagebox.showerror("Lỗi", "Không thể giải mã khóa phiên! Vui lòng kiểm tra khóa công khai đã gửi cho người gửi.")
                        return
                    self.nhat_ky("Đã giải mã khóa phiên thành công")

                    thoi_han = datetime.fromisoformat(goi_tin['exp'][:-1])
                    if datetime.utcnow() > thoi_han:
                        self.nhat_ky("File bị từ chối: Hết hạn")
                        messagebox.showerror("Lỗi", "File đã hết hạn!")
                        return
                    self.nhat_ky(f"Kiểm tra thời hạn: Hợp lệ, hết hạn vào {goi_tin['exp']}")

                    iv = base64.b64decode(goi_tin['iv'])
                    ban_ma = base64.b64decode(goi_tin['cipher'])
                    doi_tuong_hash = SHA512.new(iv + ban_ma + goi_tin['exp'].encode())
                    if doi_tuong_hash.hexdigest() != goi_tin['hash']:
                        self.nhat_ky("File bị từ chối: Hash không hợp lệ")
                        messagebox.showerror("Lỗi", "Hash không hợp lệ!")
                        return
                    self.nhat_ky("Kiểm tra hash: Hợp lệ")

                    chu_ky = base64.b64decode(goi_tin['sig'])
                    try:
                        pkcs1_15.new(khoa_gui).verify(doi_tuong_hash, chu_ky)
                        self.nhat_ky("Kiểm tra chữ ký: Hợp lệ")
                    except:
                        self.nhat_ky("File bị từ chối: Chữ ký không hợp lệ")
                        messagebox.showerror("Lỗi", "Chữ ký không hợp lệ!")
                        return

                    cipher = AES.new(khoa_phien, AES.MODE_CBC, iv)
                    du_lieu_giai_ma = cipher.decrypt(ban_ma)
                    du_lieu_giai_nen = zlib.decompress(self._giai_dinh_dang(du_lieu_giai_ma))

                    ten_file = goi_tin.get('original_file', 'email_nhan_duoc.txt')
                    with open(ten_file, 'wb') as f:
                        f.write(du_lieu_giai_nen)
                    
                    self.nhat_ky(f"Đã nhận và lưu file {ten_file} thành công từ Google Drive (File ID: {file_id}, Link: {drive_link})")
                    messagebox.showinfo("Thành công", f"Đã nhận file {ten_file} thành công từ Google Drive!\nFile ID: {file_id}\nLink: {drive_link}")
                except Exception as e:
                    self.nhat_ky(f"Lỗi khi nhận qua Google Drive: {str(e)}")
                    messagebox.showerror("Lỗi", f"Không thể nhận file qua Google Drive: {str(e)}")
                finally:
                    self.is_processing = False

            threading.Thread(target=download_file, daemon=True).start()

        except Exception as e:
            self.nhat_ky(f"Lỗi khi nhận qua Google Drive: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể nhận file qua Google Drive: {str(e)}")
            self.is_processing = False

    def _giai_dinh_dang(self, du_lieu):
        do_dai_dinh_dang = du_lieu[-1]
        return du_lieu[:-do_dai_dinh_dang]

    def on_closing(self):
        self.is_processing = False
        self.window.destroy()

    def chay(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = NguoiNhan()
    app.chay()
