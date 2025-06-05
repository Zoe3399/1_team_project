import streamlit as st
import main

# 테스트용 이메일과 비밀번호
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "1234"

def mock_login(email, password):
    if email == VALID_EMAIL and password == VALID_PASSWORD:
        st.session_state["is_login"] = True
        st.session_state["user_id"] = email
        st.session_state["page"] = "main"
        return True
    return False