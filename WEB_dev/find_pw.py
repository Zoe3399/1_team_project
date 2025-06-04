import streamlit as st
import random
import bcrypt
from sqlalchemy import create_engine, text

# DB 연결 설정
DB_URI = "postgresql://username:password@localhost:5432/dbname"
engine = create_engine(DB_URI)

def send_verification_code(email):
    code = "1234"
    st.session_state['verification_code'] = code
    st.session_state['email_for_verification'] = email
    # 실제 메일 발송은 생략
    st.success("인증번호가 이메일로 발송되었습니다. (실제 메일 발송은 생략)")

def verify_code(input_code):
    if 'verification_code' not in st.session_state:
        st.error("먼저 이메일 인증을 진행해 주세요.")
        return False
    if input_code == st.session_state['verification_code']:
        st.session_state['verified'] = True
        st.session_state["page"] = "reset_pw"
        st.success("이메일 인증이 완료되었습니다.")
        #st.experimental_rerun()
        st.rerun()
        return True
    else:
        st.error("인증번호가 일치하지 않습니다.")
        return False

st.title("비밀번호 찾기")

if 'verified' not in st.session_state:
    st.session_state['verified'] = False

if not st.session_state['verified']:
    email = st.text_input("이메일 입력")
    if st.button("이메일 인증"):
        if email.strip() == "":
            st.error("이메일을 입력해 주세요.")
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
