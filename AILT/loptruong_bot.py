import requests
import schedule
import time
import pandas as pd
from datetime import datetime

# 🔹 Token bot Telegram của bạn
TOKEN = "8416142650:AAHlCKIFqPwII9BH7Ep0-AAPcw8lWWUwXpk"
CHAT_ID = -4948781872

# =====================================================
# Hàm gửi tin nhắn
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# =====================================================
# Đọc lịch học từ file Excel
def doc_lich_hoc():
    try:
        df = pd.read_excel("lich_hoc.xlsx")
        df.columns = df.columns.str.strip()  # loại bỏ khoảng trắng thừa
        return df
    except Exception as e:
        send_message(f"❌ Lỗi đọc file Excel: {e}")
        return None

# =====================================================
# Nhắc học theo lịch hôm nay
def nhac_hoc_theo_lich():
    df = doc_lich_hoc()
    if df is None:
        return

    # Lấy thứ hiện tại (VD: 'Thứ Hai', 'Thứ Ba', ...)
    today = datetime.now().strftime("%A")
    vietnamese_days = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba",
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật"
    }
    hom_nay = vietnamese_days.get(today, today)

    # Lọc các môn học hôm nay
    lich_hom_nay = df[df["Ngày"].str.lower() == hom_nay.lower()]

    if lich_hom_nay.empty:
        send_message(f"📅 Hôm nay ({hom_nay}) không có tiết học nào, nghỉ ngơi nhé!")
    else:
        send_message(f"📚 Lịch học hôm nay ({hom_nay}):")
        for _, row in lich_hom_nay.iterrows():
            gio = row["Giờ bắt đầu"]
            mon = row["Môn học"]
            ghi_chu = row.get("Ghi chú", "")
            send_message(f"🕗 {gio} — {mon}\n📍 {ghi_chu}")

# =====================================================
if __name__ == "__main__":
    # Kiểm tra hoạt động
    send_message("🤖 Bot Lớp Trưởng đã khởi động, sẽ nhắc học tự động mỗi sáng!")

    # Lên lịch nhắc học mỗi sáng 06:00
    schedule.every().day.at("06:00").do(nhac_hoc_theo_lich)
    schedule.every().day.at("12:00").do(nhac_hoc_theo_lich)
    
    print("🚀 Bot lớp trưởng đang chạy... (nhấn Ctrl+C để dừng)")
    while True:
        schedule.run_pending()
        time.sleep(1)
