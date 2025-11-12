import pandas as pd
import requests
import pytz
import json
import os
from datetime import datetime, timedelta
import time

# ===========================================
# 🔹 Đọc cấu hình
CONFIG_PATH = "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
CHAT_ID = config["CHAT_ID"]
REMIND_TIME = config["REMIND_TIME"]
TIMEZONE = pytz.timezone(config["TIMEZONE"])
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
LOG_FILE = "logs/chat_log.txt"

os.makedirs("logs", exist_ok=True)

# ===========================================
# 🔹 Gửi tin nhắn Telegram
def send_message(text, markdown=False):
    payload = {"chat_id": CHAT_ID, "text": text}
    if markdown:
        payload["parse_mode"] = "Markdown"
    try:
        requests.post(BASE_URL + "sendMessage", data=payload)
    except Exception as e:
        print(f"❌ Lỗi gửi tin nhắn: {e}")

# ===========================================
# 🔹 Ghi log hội thoại
def log_chat(role, message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}] {role}: {message}\n")

# ===========================================
# 🔹 Đọc lịch học
def doc_lich_hoc():
    try:
        df = pd.read_excel("lich_hoc.xlsx")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"❌ Lỗi đọc file Excel: {e}")
        return None

# ===========================================
# 🔹 Xử lý lệnh
def get_schedule_for(day_offset=0):
    df = doc_lich_hoc()
    if df is None:
        return "Không đọc được file lịch học 😢."

    date = datetime.now(TIMEZONE) + timedelta(days=day_offset)
    weekday = date.strftime("%A")
    days = {
        "Monday": "Thứ Hai", "Tuesday": "Thứ Ba", "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm", "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy", "Sunday": "Chủ Nhật"
    }
    ngay = days.get(weekday, weekday)
    lich = df[df["Ngày"].str.lower() == ngay.lower()]

    if lich.empty:
        return f"📅 {ngay} ({date.strftime('%d/%m')}) không có tiết học nào."
    else:
        msg = f"📚 Lịch học {ngay} ({date.strftime('%d/%m')}):\n"
        for _, row in lich.iterrows():
            msg += f"🕗 {row['Giờ bắt đầu']} — *{row['Môn học']}*\n📍 {row.get('Ghi chú', '')}\n\n"
        return msg.strip()

# ===========================================
# 🔹 AI trả lời
def ai_tra_loi(question):
    df = doc_lich_hoc()
    prompt = f"""
    Đây là lịch học của lớp:
    {df.to_string(index=False) if df is not None else 'Không có dữ liệu.'}

    Câu hỏi: {question}
    Trả lời thân thiện, ngắn gọn, tự nhiên.
    """
    try:
        r = requests.post("http://localhost:11434/api/generate",
                          json={"model": "llama3", "prompt": prompt, "stream": False},
                          timeout=60)
        if r.status_code == 200:
            return r.json().get("response", "").strip()
        else:
            return "❌ AI không phản hồi được."
    except Exception as e:
        return f"❌ Lỗi kết nối AI: {e}"

# ===========================================
# 🔹 Nhận cập nhật
def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    resp = requests.get(BASE_URL + "getUpdates", params=params)
    return resp.json().get("result", [])

# ===========================================
# 🔹 Main Loop
def main():
    print("🚀 Lớp Trưởng AI v2.0 đang chạy...")
    send_message("🤖 *Lớp Trưởng AI v2.0* đã sẵn sàng! Gõ /homnay, /mai hoặc hỏi mình nhé.", markdown=True)
    offset = None
    last_remind = {}

    while True:
        now = datetime.now(TIMEZONE)
        # Gửi nhắc học tự động
        for t in REMIND_TIME:
            if now.strftime("%H:%M") == t and last_remind.get(t) != now.date():
                send_message(get_schedule_for(0))
                last_remind[t] = now.date()

        # Nhận lệnh / tin nhắn
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"].strip()
                chat_id = update["message"]["chat"]["id"]
                log_chat("User", text)

                if text.lower() == "/homnay":
                    reply = get_schedule_for(0)
                elif text.lower() == "/mai":
                    reply = get_schedule_for(1)
                elif text.lower() == "/help":
                    reply = (
                        "📘 *Hướng dẫn sử dụng:*\n"
                        "/homnay – Xem lịch học hôm nay\n"
                        "/mai – Xem lịch học ngày mai\n"
                        "/help – Hướng dẫn lệnh\n"
                        "Hoặc hỏi tự nhiên: *Ngày mai có học không?*"
                    )
                else:
                    reply = ai_tra_loi(text)

                log_chat("Bot", reply)
                send_message(reply, markdown=True)

        time.sleep(2)

# ===========================================
if __name__ == "__main__":
    main()
