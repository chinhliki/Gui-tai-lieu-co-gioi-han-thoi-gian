<h1 align="center">ỨNG DỤNG GỬI FILE AN TOÀN VÀ GIỚI HẠN THỜI GIAN</h1>

<div align="center">

<p align="center">
  <img src="logoDaiNam.png" alt="DaiNam University Logo" width="200"/>
  <img src="images/LogoAIoTLab.png" alt="AIoTLab Logo" width="170"/>
</p>

[![Made by AIoTLab](https://img.shields.io/badge/Made%20by%20AIoTLab-blue?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Fit DNU](https://img.shields.io/badge/Fit%20DNU-green?style=for-the-badge)](https://fitdnu.net/)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

</div>

<h2 align="center">Hệ thống gửi file an toàn với thời gian giới hạn</h2>

<p align="left">
  Hệ thống "Gửi File An Toàn và Giới Hạn Thời Gian" là một ứng dụng Python sử dụng các kỹ thuật mã hóa mạnh mẽ (AES, RSA), chữ ký số (SHA512, PKCS1_15) và nén dữ liệu (zlib) để đảm bảo tính bảo mật và toàn vẹn của file trong quá trình truyền tải. Ứng dụng hỗ trợ hai phương thức triển khai: truyền file cục bộ qua Socket hoặc qua Internet bằng Google Drive, đồng thời tích hợp cơ chế giới hạn thời gian nhận file. Giao diện người dùng được xây dựng bằng Tkinter, cung cấp trải nghiệm trực quan và thân thiện.
</p>

---

## 🌟 Giới thiệu

- **📌 Mã hóa mạnh mẽ:** Sử dụng kết hợp RSA để trao đổi khóa phiên (AES) và AES để mã hóa dữ liệu file, đảm bảo an toàn cho nội dung truyền tải.
- **🔐 Chữ ký số và Hash:** Tích hợp SHA512 và PKCS1_15 để tạo và xác minh chữ ký số, đảm bảo tính toàn vẹn của dữ liệu và xác thực nguồn gốc file.
- **⏱️ Giới hạn thời gian:** File được gửi đi kèm với thời gian hết hạn (expiration time). Người nhận chỉ có thể giải mã và truy cập file trước thời điểm này.
- **🌐 Đa phương thức triển khai:** Hỗ trợ gửi file qua mạng cục bộ (Socket) hoặc qua Internet sử dụng Google Drive làm trung gian.
- **🖥️ Giao diện thân thiện:** Sử dụng Tkinter (với `ttkbootstrap`) để cung cấp giao diện người dùng dễ sử dụng cho cả người gửi và người nhận.
- **📚 Ghi log chi tiết:** Toàn bộ quá trình gửi và nhận file, cũng như các lỗi phát sinh, đều được ghi lại trong file log để dễ dàng theo dõi và debug.

---

## 🏗️ CẤU TRÚC HỆ THỐNG

<p align="center">
  <img src="Sơ đồ trình tự.jpg" alt="System Architecture" width="800"/>
</p>


---

## 📂 Cấu trúc dự án

```

📦 Project
├── 📂 images/              \# Thư mục chứa hình ảnh sử dụng trong README (ví dụ: background.png)
│   ├── background.253a9926.png
│   └── ...
├── nguoi\_gui.py           \# Chương trình dành cho Người gửi: mã hóa, ký số, đóng gói và gửi file.
├── nguoi\_nhan.py          \# Chương trình dành cho Người nhận: lắng nghe/tải file, xác thực, giải mã và lưu file.
├── credentials.json       \# (Tùy chọn) File cấu hình xác thực Google Drive API (được tạo qua Google Cloud Console).
├── log\_gui.txt            \# File log của Người gửi.
└── log\_nhan.txt           \# File log của Người nhận.

````

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

<div align="center">

### 🖥️ Phần mềm
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)]()
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-yellow?style=for-the-badge)]()
[![Ttkbootstrap](https://img.shields.io/badge/Ttkbootstrap-Modern%20GUI-purple?style=for-the-badge)]()
[![PyCryptodome](https://img.shields.io/badge/PyCryptodome-Cryptography-orange?style=for-the-badge)]()
[![Google%20Drive%20API](https://img.shields.io/badge/Google%20Drive%20API-Cloud%20Storage-red?style=for-the-badge&logo=google-drive)]()
[![Socket](https://img.shields.io/badge/Socket-Networking-lightgray?style=for-the-badge)]()
[![Zlib](https://img.shields.io/badge/Zlib-Compression-brown?style=for-the-badge)]()

</div>

## 🛠️ Yêu cầu hệ thống

### 💻 Phần mềm
- **🐍 Python 3+**

### 📦 Các thư viện Python cần thiết
Cài đặt các thư viện bằng lệnh:

```bash
pip install pillow pycryptodome google-api-python-client google-auth-oauthlib ttkbootstrap
````

## 🚀 Hướng dẫn cài đặt và chạy

1️⃣ **Cấu hình Google Drive API (Chỉ cho chế độ Internet)**

  - Truy cập [Google Cloud Console](https://console.cloud.google.com/).
  - Tạo một dự án mới (hoặc chọn dự án hiện có).
  - Bật API "Google Drive API".
  - Tạo thông tin xác thực "OAuth client ID" cho ứng dụng desktop.
  - Tải xuống file `credentials.json` và đặt nó vào cùng thư mục với `nguoi_gui.py` và `nguoi_nhan.py`.

2️⃣ **Chạy ứng dụng Người gửi (`nguoi_gui.py`)**

```bash
python nguoi_gui.py
```

  - Giao diện "Người Gửi" sẽ hiển thị.

3️⃣ **Chạy ứng dụng Người nhận (`nguoi_nhan.py`)**

```bash
python nguoi_nhan.py
```

  - Giao diện "Người Nhận" sẽ hiển thị.

## 📖 Hướng dẫn sử dụng

### Cho Người nhận:

1.  **Hiển thị Khóa Công Khai:** Nhấn nút "Hiển Thị Khóa Công Khai". Một cửa sổ sẽ hiện lên chứa khóa công khai RSA của bạn. Sao chép khóa này và gửi cho Người gửi.
2.  **Chọn phương thức triển khai:**
      * **Local:** Để nhận file qua mạng cục bộ.
      * **Internet (Google Drive):** Để nhận file được tải lên Google Drive.
3.  **Bắt Đầu Nhận:**
      * **Local:** Ứng dụng sẽ bắt đầu lắng nghe kết nối từ Người gửi.
      * **Internet:** Một hộp thoại sẽ hiện ra yêu cầu bạn nhập link Google Drive của file JSON được gửi bởi Người gửi.

### Cho Người gửi:

1.  **Chọn File:** Nhấn nút "Chọn File" để chọn file bạn muốn gửi. Tên file sẽ hiển thị trên giao diện.
2.  **Nhập Khóa Công Khai:** Nhấn nút "Nhập Khóa Công Khai" và dán khóa công khai RSA của Người nhận (mà họ đã cung cấp cho bạn) vào hộp thoại.
3.  **Chọn phương thức triển khai:**
      * **Local:** Để gửi file trực tiếp qua mạng cục bộ đến Người nhận.
      * **Internet (Google Drive):** Để tải file mã hóa lên Google Drive và tạo link chia sẻ.
4.  **Gửi File An Toàn:**
      * **Local:** Ứng dụng sẽ kết nối với Người nhận và tiến hành gửi file.
      * **Internet:** File sẽ được mã hóa và tải lên Google Drive của bạn. Một thông báo sẽ hiển thị link Google Drive và File ID. Sao chép link này và gửi cho Người nhận.

## ⚙️ Cấu hình & Ghi chú

1.  **Địa chỉ IP và Cổng (Chế độ Local):**
      * Trong `nguoi_gui.py`, `SERVER_HOST` hiện đang là `"192.168.1.9"`. Bạn cần thay đổi nó thành địa chỉ IP của máy đang chạy `nguoi_nhan.py`.
      * Trong `nguoi_nhan.py`, `SERVER_HOST` hiện đang là `"192.168.1.11"`. Bạn cần đảm bảo địa chỉ IP này là địa chỉ IP của máy đang chạy `nguoi_nhan.py`.
      * `SERVER_PORT` mặc định là `12345` cho cả hai bên.
2.  **Thời gian hiệu lực file:** File có hiệu lực trong 24 giờ (`timedelta(hours=24)`) kể từ thời điểm tạo. Bạn có thể thay đổi giá trị này trong cả `nguoi_gui.py` và `nguoi_nhan.py`.
3.  **Xác thực Google Drive API:** Lần đầu tiên bạn chạy ứng dụng ở chế độ Internet, một cửa sổ trình duyệt sẽ mở ra yêu cầu bạn đăng nhập tài khoản Google và cấp quyền truy cập Google Drive.
4.  **Ký tự đặc biệt trong tên file:** Tên file gốc sẽ được giữ lại khi gửi qua Google Drive, nhưng cần đảm bảo không có ký tự lạ có thể gây lỗi.

## 🤝 Đóng góp

Dự án được phát triển bởi 3 thành viên:

| Họ và Tên         | Vai trò                                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------------------|
| Hà Tuấn Điệp      | Phát triển mã nguồn, thiết kế kiến trúc hệ thống.                                                           |
| Đinh Ngọc Chính   | Biên soạn tài liệu, Poster, Powerpoint, thuyết trình, đề xuất cải tiến, và hỗ trợ bài tập lớn.              |
| Trần Quang Lâm    | Hỗ trợ bài tập lớn, kiểm thử, triển khai dự án và thực hiện                                                 |

© 2025 NHÓM 12, CNTT17-11, TRƯỜNG ĐẠI HỌC ĐẠI NAM
