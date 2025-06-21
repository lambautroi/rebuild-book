# rebuild-book

# 📚 RebuildBook – AI tái xuất bản sách Public Domain

**RebuildBook** là hệ thống sử dụng AI để tự động tái xuất bản sách Public Domain. Dự án cho phép tạo ra các phiên bản mới của sách cũ (viết lại, tóm tắt, thay đổi phong cách, v.v.), đồng thời hỗ trợ xuất bản sách dưới dạng EPUB có bìa đẹp và dashboard quản lý thân thiện.

---

## 🎯 Mục tiêu

-   Tự động tái cấu trúc nội dung sách Public Domain
-   Tạo nhiều phiên bản khác nhau cho một sách gốc (nhiều phong cách viết)
-   Xuất bản sách dưới dạng EPUB có bìa đẹp sinh bằng AI
-   Quản lý nội dung, phiên bản và xuất bản qua React Dashboard
-   Lưu trữ và đồng bộ với Firestore + Firebase Storage

---

## 🧱 Kiến trúc hệ thống

Nhập sách (.pdf / .epub / .txt / URL)
└── Làm sạch nội dung
└── Tách chương

🤖 Viết lại theo phong cách AI (5+ style)
└── GPT-4 / Claude API
└── Prompt tùy chỉnh theo style

🖼️ Sinh ảnh bìa AI (Stable Diffusion via Colab)
└── Upload lên Firebase Storage

📘 Tạo EPUB từ nội dung style
└── Metadata + ảnh bìa

📤 Dashboard quản lý sách
└── React + Firebase

---

## 📌 Các tính năng chính

-   [x] Tải sách từ URL hoặc upload file
-   [x] Làm sạch và chia chương tự động
-   [x] Viết lại sách theo nhiều phong cách:
    -   Hiện đại
    -   Tóm tắt
    -   Hài hước
    -   Truyện ngắn
    -   Giữ nguyên văn phong cổ
-   [x] Sinh ảnh bìa bằng AI (Stable Diffusion)
-   [x] Tạo file EPUB có metadata và ảnh bìa
-   [x] Dashboard React để quản lý, xem trước và xuất bản
-   [x] Lưu trữ nội dung & EPUB trên Firebase Firestore & Storage

---

## 🛠 Công nghệ sử dụng

| Thành phần        | Công nghệ               |
| ----------------- | ----------------------- |
| Backend xử lý     | Python, OpenAI API      |
| Tạo ảnh bìa       | Stable Diffusion, Colab |
| Tạo file EPUB     | `ebooklib` (Python)     |
| Frontend          | React.js                |
| Cơ sở dữ liệu     | Firebase Firestore      |
| Lưu trữ           | Firebase Storage        |
| Hosting Dashboard | Firebase Hosting        |

---

## 🚀 Cài đặt và chạy local

```bash
# 1. Clone repo
git clone https://github.com/yourusername/rebuildbook.git
cd rebuildbook

# 2. Cài đặt backend (Python)
cd backend
pip install -r requirements.txt

# 3. Cài đặt frontend (React)
cd ../frontend
npm install
npm run dev

```
