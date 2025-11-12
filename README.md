<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology – DaiNam University
    </a>
</h2>

<h2 align="center">
   🤖 DỰ ÁN: AI AGENT BÍ THƯ ĐOÀN LỚP
</h2>

<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/FIT-DaiNam%20University-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/LICENSE-MIT-orange?style=for-the-badge)](./LICENSE)
</div>

---

## 📘 1. Giới thiệu

**AI Agent Bí thư Đoàn lớp** là một trợ lý thông minh giúp tự động hóa công việc hành chính trong lớp học:  
📅 Nhắc lịch học – 💬 Giao tiếp qua Telegram – 🧠 Trả lời tự nhiên bằng AI.

Hệ thống được xây dựng bằng **Python**, hoạt động dựa trên tệp dữ liệu **Excel (lich_hoc.xlsx)** và mô hình ngôn ngữ lớn **Ollama (llama3)** chạy nội bộ.  
Dự án hướng tới mục tiêu **chuyển đổi số công tác Đoàn – Hội – Lớp**, giúp giảm tải thủ tục, tăng hiệu quả thông tin.

---

## ⚙️ 2. Chức năng chính

| Nhóm tính năng | Mô tả |
|-----------------|--------|
| 🕒 **Nhắc lịch học tự động** | Gửi thông báo lịch học từ file Excel vào nhóm Telegram đúng giờ cấu hình. |
| 💬 **Giao tiếp tự nhiên** | AI (mô hình Ollama) có thể hiểu câu hỏi và phản hồi thân thiện. |
| 📑 **Ghi log hội thoại** | Lưu lại toàn bộ trao đổi giữa người dùng và bot. |
| 📂 **Không cần cơ sở dữ liệu** | Tất cả thông tin được lưu trong file Excel, dễ chỉnh sửa. |

---

## 🧩 3. Kiến trúc hệ thống

<p align="center">
  <img src="https://github.com/user-attachments/assets/fa2965ab-7eda-4e44-aa45-7538dff6e6de" alt="System Architecture" width="450"/>
</p>


> Hệ thống gồm 4 thành phần:  
> **Sinh viên (Telegram)** ↔ **Bot trung tâm Python** ↔ **Tệp Excel (lich_hoc.xlsx)** ↔ **AI Ollama LLM**.

---

## 💻 4. Công nghệ sử dụng

| Công nghệ | Vai trò |
|------------|----------|
| 🐍 **Python 3.10+** | Ngôn ngữ chính |
| 📊 **pandas** | Đọc & xử lý dữ liệu Excel |
| 🌐 **requests** | Gọi Telegram Bot API |
| ⏰ **schedule** | Đặt lịch nhắc học định kỳ |
| 🌍 **pytz** | Quản lý múi giờ Việt Nam |
| 🧠 **Ollama (llama3)** | Xử lý truy vấn ngôn ngữ tự nhiên |

---

## ⚡ 5. Cấu hình hệ thống

Tạo file `config.json` trong thư mục chính:

```json
{
    "TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
    "CHAT_ID": "-1001234567890",
    "REMIND_TIME": ["06:00", "12:00"],
    "TIMEZONE": "Asia/Ho_Chi_Minh"
}
