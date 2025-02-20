import streamlit as st
import os
import pandas as pd
from model import read_name_from_image, crop_and_read_names, save_to_csv, count_names_in_csv
import pyrebase
from streamlit_chat import message

# Firebase config
firebaseConfig = {
    'apiKey': "AIzaSyCt7JaHwmHCS9Lm_hiZQv1B2XM_1eR4zPM",
    'authDomain': "posto-ai-app.firebaseapp.com",
    'databaseURL': "https://YOUR_PROJECT_ID.firebaseio.com",
    'projectId': "posto-ai-app",
    'storageBucket': "posto-ai-app.appspot.com",
    'messagingSenderId': "408360408985",
    'appId': "1:408360408985:web:55ec7842c40203f28c6508",
    'measurementId': "G-HL46XMRBKM"
}

# Firebase initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def change_colors():
    style = """
        <style>
            #sign-up {
                color: #333366;  /* เปลี่ยนสีของคำว่า Login */
            }
            .st-emotion-cache-uef7qa {
                color: #333366;  /* สีข้อความในฟิลด์ input */
            }
           .stTextInput > div > div > input {
                background-color: #FCFAEE;  /* สีพื้นหลังของฟิลด์ input */
            }
            .st-emotion-cache-bm2z3a {
                background-color: #f0f0f0;  /* สีพื้นหลัง */
            }
            .st-emotion-cache-h4xjwg{
                background-color: #ff5f5f;  /* สีพื้นหลัง */
            }
            .st-emotion-cache-uef7qa{
                color: #333366;  /* สีข้อความในฟิลด์ input */
            }
            .st-emotion-cache-12fmjuu {
                background-color: #ff5f5f;  /* สีพื้นหลัง */
                color:#ffffff;
            }
            .stText {
                color: #333366;  /* สีของตัวอักษร */
            }
            .stButton>button {
                background-color: #f9e75e;  /*  */
                color: #333366;  /* สีของตัวอักษรในปุ่ม */
            }
            .stButton>button:hover {
                background-color: #f9e75e;  /* สีของปุ่มเมื่อชี้เมาส์ */
            }
            footer {
                visibility: hidden;  /* ซ่อนฟุตเตอร์ */
            }
            #MainMenu {
                visibility: hidden;  /* ซ่อนเมนูหลัก */
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def sign_up():
    change_colors()
    st.title("Sign Up")

    if "signup_status" not in st.session_state:
        st.session_state.signup_status = None  # ตั้งค่าเริ่มต้นเป็น None

    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.session_state.signup_status = "success"
        except:
            st.error("Sign Up ไม่สำเร็จ กรุณาตรวจสอบข้อมูลอีกครั้ง.")
            
    if st.session_state.signup_status == "success":
         st.success("Sign Up สำเร็จ! กรุณาเข้าสู่ระบบ.")
         st.session_state.current_page = "login"  # เปลี่ยนไปยังหน้า Home
         st.switch_page("pages/1_Login.py")  # สลับไปยังหน้า Login

if __name__ == "__main__":
    sign_up()
