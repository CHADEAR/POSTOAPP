import streamlit as st
import pandas as pd
from streamlit_chat import message
import os

def check_login():
    if "login_status" not in st.session_state or not st.session_state.login_status:
        st.warning("กรุณา Login ก่อนเข้าหน้าอื่น")
        st.session_state.current_page = "Login"
        st.switch_page("pages/1_Login.py")

# กำหนดค่าเริ่มต้นสำหรับ messages
st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

def logout():
    if "login_status" in st.session_state:
        st.session_state.login_status = False
    if "email" in st.session_state:
        st.session_state.email = None  # ลบอีเมลออกจาก session
    st.success("Logout สำเร็จ!")
    st.session_state.current_page = "login"  # เปลี่ยนไปที่หน้า Login
    st.switch_page("pages/1_Login.py")  # สลับไปยังหน้า Home
    st.experimental_rerun()  # รีเฟรชหน้า

# สร้างโฟลเดอร์สำหรับอัปโหลดถ้าไม่มี
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_FILE = 'backend/names.csv'

# ฟังก์ชันสำหรับการตรวจสอบคำถามใน CSV และดึงค่า count
def get_count_from_csv(question):
    try:
        df = pd.read_csv(CSV_FILE)
        # ตรวจสอบว่า name มีอยู่ใน CSV หรือไม่
        if question in df['name'].values:
            count = df[df['name'] == question]['count'].values[0]
            return count
        else:
            return 0  # ถ้าไม่พบชื่อ ให้ส่งค่า count = 0
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์ CSV: {e}")
        return 0

# ฟังก์ชันที่จัดการคำถาม
def handle_chat(question):
    if question:
        count = get_count_from_csv(question)
        if count > 0:
            return f"✅ พัสดุของ {question} มาถึงแล้วครับ (จำนวนพัสดุ: {count} ชิ้น)"
        else:
            return f"❌ พัสดุของ {question} ยังไม่มาถึงครับ"
    return "🚫 กรุณาใส่ชื่อผู้รับพัสดุ"

# ฟังก์ชันสำหรับการส่งข้อความ
def on_input_change():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state.past.append(user_input)
        answer = handle_chat(user_input)
        st.session_state.generated.append(answer)
        st.session_state.user_input = ""

# ตรวจสอบการตั้งค่า session_state
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

# ฟังก์ชันหลักสำหรับการแสดง chatbot
def chat():
    check_login()

    # ใช้ CSS สำหรับ fix text input ให้ติดอยู่ที่ด้านล่างของหน้าจอ
    st.markdown(
        """
        <style>
        .body{
            padding:0;
            margin:0;
            box-sizing: border-box;
            width:100%;
            height:100%;
        }

        .st-emotion-cache-1igbibe {
            position: fixed;
            top: 15px;
            right: 10px;
            z-index: 1000; /* ให้องค์ประกอบอยู่ด้านบนสุด */
    }
        
        .st-emotion-cache-1vt4y43{
            position: fixed;
            left: 90%;
        }
        .stTextInput {
            position: fixed;
            bottom: 0;
            width: 85%;
            margin-bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
        }
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #FF5F5F;
            height: 10vh;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
        }
        .navbar span {
            color: white;
            font-size: 24px;
        }
        .st-emotion-cache-12fmjuu{
            background-color: #FF5F5F;
            z-index: 1;
        }
        .st-emotion-cache-1vt4y43 {
            background-color: #F4EBA4;
            position: fixed;
            top: 0;
            left:90%;
            margin-top:13px;
            z-index: 999; /* ให้องค์ประกอบอยู่ด้านบนสุด */
        }
        @media only screen and (max-width: 768px) {
        .st-emotion-cache-1vt4y43 {
            position: fixed;
            top: 0;
            left:75%;
            margin-top:7px;
            width: 75px; /* ขนาดที่เล็กลง */
            height: 50px; /* ขนาดที่เล็กลง */
            z-index: 999; /* ให้องค์ประกอบอยู่ด้านบนสุด */
        }
}

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="navbar">
            <span>POSTO</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # แสดงข้อความใน container
    chat_placeholder = st.empty()

    # ส่วนที่แสดงข้อความ
    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
            message(st.session_state['generated'][i], key=f"bot_{i}")

    # ช่องป้อนข้อความ
    st.text_input("ใส่ชื่อผู้รับพัสดุ :", on_change=on_input_change, key="user_input")

if st.button("Logout"):
        logout()  # เรียกฟังก์ชัน logout

if __name__ == "__main__":
    chat()
