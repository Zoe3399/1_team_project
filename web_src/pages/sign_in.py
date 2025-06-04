# pages/sign_in.py
import streamlit as st

def show():
    st.title("📝 회원가입")

    new_username = st.text_input("새 아이디")
    new_password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")

    if st.button("회원가입", key="signup_submit_button"):  # key 추가
        if new_username == "" or new_password == "":
            st.warning("모든 항목을 입력해주세요.")
        elif new_password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        elif 'users' in st.session_state and new_username in st.session_state.users:
            st.error("이미 존재하는 아이디입니다.")
        else:
            if 'users' not in st.session_state:
                st.session_state.users = {}
            st.session_state.users[new_username] = new_password
            st.success("회원가입 성공! 이제 로그인 해주세요.")
            st.session_state.page = "login"
            st.rerun()
