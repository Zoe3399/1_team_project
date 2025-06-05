import streamlit as st
import random
import bcrypt
from sqlalchemy import text
from db import engine

def send_verification_code(email):
    code = "123456"
    st.session_state['verification_code'] = code
    st.session_state['email_for_verification'] = email
    st.success("테스트용 인증번호: 123456 (실제 메일 발송은 생략)")

def verify_code(input_code):
    if 'verification_code' not in st.session_state:
        st.error("먼저 이메일 인증을 진행해 주세요.")
        return False
    if input_code == "123456":
        st.session_state['verified'] = True
        st.session_state["reset_email"] = st.session_state.get("email_for_verification")
        st.session_state["page"] = "reset_pw"
        st.success("이메일 인증이 완료되었습니다.")
        st.rerun()
        return True
    else:
        st.error("인증번호가 일치하지 않습니다.")
        return False

def find_pw_page():
    st.title("비밀번호 찾기")
    st.markdown(
        "<style>div.block-container{max-width: 600px; margin: auto;}</style>",
        unsafe_allow_html=True
    )

    if 'verified' not in st.session_state:
        st.session_state['verified'] = False

    if not st.session_state['verified']:
        email = st.text_input("이메일 입력")
        if st.button("이메일 인증"):
            if email.strip() == "":
                st.error("이메일을 입력해 주세요.")
            else:
                with engine.connect() as conn:
                    exists = conn.execute(
                        text("SELECT COUNT(*) FROM users WHERE email = :e AND is_active = TRUE"),
                        {"e": email}
                    ).scalar()
                if exists == 0:
                    st.error("가입된 이메일이 아닙니다.")
                else:
                    send_verification_code(email)
        code_input = st.text_input("인증번호 입력")
        if st.button("인증번호 확인"):
            if code_input.strip() == "":
                st.error("인증번호를 입력해 주세요.")
            else:
                verify_code(code_input)
    else:
        st.success(f"{st.session_state.get('email_for_verification', '')} 이메일 인증 완료. 비밀번호 재설정을 위해 페이지를 이동합니다.")
