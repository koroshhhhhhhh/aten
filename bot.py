import asyncio
import threading
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest, UpdateStatusRequest

# ================== اطلاعات خودت ==================
api_id = 33166837
api_hash = "8ebc679a4936e2533cca8537971455f5"
phone = "+989036788104"
# ==================================================

# ================== تنظیمات ارسال پیام ==================
CHAT_ID = "Mimi ha"  # اسم گروه یا یوزرنیم
MESSAGE_TEXT = "میو"
INTERVAL = 301  # ۵ دقیقه و ۱ ثانیه = ۳۰۱ ثانیه
# ======================================================

client = TelegramClient("sessiona", api_id, api_hash)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

fancy_numbers = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
}

def to_fancy(text):
    return ''.join(fancy_numbers.get(c, c) for c in text)

async def update_name():
    while True:
        now = datetime.now(ZoneInfo("Asia/Tehran"))

        if now.second != 0:
            await asyncio.sleep(60 - now.second)
            now = datetime.now(ZoneInfo("Asia/Tehran"))

        fancy_time = to_fancy(now.strftime("%H:%M"))
        await client(UpdateProfileRequest(last_name=fancy_time))
        print(f"💙 تغییر کرد به {fancy_time}")

        await asyncio.sleep(60)

async def send_periodic_message():
    # پیدا کردن آی‌دی گروه با اسم
    group_id = None
    async for dialog in client.iter_dialogs():
        if dialog.is_group and dialog.name == CHAT_ID:
            group_id = dialog.id
            break

    if group_id is None:
        print(f"❌ گروه با اسم '{CHAT_ID}' پیدا نشد!")
        return

    print(f"✅ گروه پیدا شد: {CHAT_ID} (ID: {group_id})")

    while True:
        try:
            await client.send_message(group_id, MESSAGE_TEXT)
            print(f"✅ پیام به {CHAT_ID} ارسال شد: {MESSAGE_TEXT}")
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {e}")
        await asyncio.sleep(INTERVAL)

async def main():
    threading.Thread(target=run_web, daemon=True).start()
    await client.start(phone=phone)

    # ===== آفلاین کردن وضعیت =====
    await client(UpdateStatusRequest(offline=True))
    print("💙 Bot Started (وضعیت: آفلاین)")

    # اجرای همزمان دو کار
    await asyncio.gather(
        update_name(),
        send_periodic_message()
    )

asyncio.run(main())