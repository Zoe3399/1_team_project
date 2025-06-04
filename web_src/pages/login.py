# pages/login.py
import streamlit as st

def show():
    st.title("🔐 로그인")

    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", key="login_submit_button"):  # key 추가
        if 'users' in st.session_state and username in st.session_state.users:
            if st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "home"
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
        else:
            st.error("존재하지 않는 아이디입니다.")
