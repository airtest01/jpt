import os
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# --- ส่วนของการตั้งค่า (เหมือนเดิม) ---
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
user_id = os.environ.get('LINE_USER_ID', None)

# --- ส่วนของการดึงข้อมูลน้ำ (ส่วนที่เพิ่มเข้ามาใหม่) ---
def get_dam_data():
    """
    ฟังก์ชันสำหรับดึงข้อมูลการระบายน้ำของเขื่อนเจ้าพระยาจาก API ของกรมชลประทาน
    """
    print("กำลังดึงข้อมูลน้ำจาก API กรมชลประทาน...")
    api_url = "https://water.rid.go.th/monitor/dam/data"
    # dam_id: 21 คือรหัสของเขื่อนเจ้าพระยา
    payload = {'dam_id': 21}
    
    try:
        response = requests.post(api_url, data=payload, timeout=10)
        # ตรวจสอบว่า API ตอบกลับมาสำเร็จ (status code 200)
        response.raise_for_status() 
        
        # แปลงข้อมูลจาก JSON เป็น Dictionary
        data = response.json()
        
        # ดึงข้อมูลการระบายน้ำล่าสุด (discharge)
        # โครงสร้างข้อมูลคือ data -> data[0] -> discharge
        discharge_value = data['data'][0]['discharge']
        dam_date = data['data'][0]['dam_date']
        
        print(f"ดึงข้อมูลสำเร็จ: ค่าการระบายน้ำ = {discharge_value} ลบ.ม./วินาที (ข้อมูล ณ วันที่ {dam_date})")
        return discharge_value, dam_date
        
    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ API: {e}")
        return None, None
    except (KeyError, IndexError) as e:
        print(f"เกิดข้อผิดพลาด: โครงสร้างข้อมูล JSON ที่ได้รับกลับมาไม่ถูกต้อง: {e}")
        return None, None

# --- ส่วนของการทำงานหลัก ---
if channel_access_token is None or user_id is None:
    print("Error: ไม่พบค่า LINE_CHANNEL_ACCESS_TOKEN หรือ LINE_USER_ID")
else:
    # 1. เรียกฟังก์ชันเพื่อดึงข้อมูลน้ำ
    discharge, data_time = get_dam_data()
    
    # 2. ตรวจสอบว่าดึงข้อมูลสำเร็จหรือไม่
    if discharge is not None:
        # 3. สร้างข้อความที่จะส่ง
        message_to_send = (
            f"แจ้งเตือนระดับน้ำท้ายเขื่อนเจ้าพระยา 🌊\n"
            f"----------------------------------\n"
            f"อัตราการระบายน้ำ: {discharge} ลบ.ม./วินาที\n"
            f"ข้อมูล ณ วันที่: {data_time}"
        )
        
        # 4. ส่งข้อความไปที่ LINE (เหมือนเดิม)
        try:
            line_bot_api = LineBotApi(channel_access_token)
            line_bot_api.push_message(user_id, TextSendMessage(text=message_to_send))
            print("ส่งข้อความแจ้งเตือนไปที่ LINE สำเร็จ!")
        except LineBotApiError as e:
            print(f"เกิดข้อผิดพลาดในการส่งข้อความ LINE: {e.error.message}")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ: {e}")
    else:
        print("ไม่สามารถดึงข้อมูลน้ำได้ จึงไม่ได้ส่งข้อความ")
