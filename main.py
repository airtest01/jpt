# นำเข้าเครื่องมือที่จำเป็น
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# อ่านค่า "ความลับ" จากที่เก็บของระบบ (ในอนาคตคือ GitHub Secrets)
# เราจะไม่เขียน Token ลงไปในโค้ดโดยตรงแล้ว
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
user_id = os.environ.get('LINE_USER_ID', None)

# ข้อความที่ต้องการส่ง
message_to_send = "ทดสอบการส่งข้อความอัตโนมัติจาก GitHub!"

# ตรวจสอบว่ามีค่า Token และ ID ครบถ้วนหรือไม่
if channel_access_token is None or user_id is None:
    print("Error: ไม่พบค่า LINE_CHANNEL_ACCESS_TOKEN หรือ LINE_USER_ID")
    exit() # จบการทำงานทันทีถ้าไม่มีค่า

print("กำลังเตรียมส่งข้อความ...")

try:
    # สร้างการเชื่อมต่อกับ LINE API
    line_bot_api = LineBotApi(channel_access_token)

    # ทำการส่งข้อความ
    line_bot_api.push_message(user_id, TextSendMessage(text=message_to_send))

    print(f"ส่งข้อความ '{message_to_send}' สำเร็จ!")

except LineBotApiError as e:
    print(f"เกิดข้อผิดพลาดในการส่งข้อความ: {e.error.message}")
except Exception as e:
    print(f"เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ: {e}")