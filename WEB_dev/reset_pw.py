import streamlit as st
from sqlalchemy import text
import bcrypt

if "reset_email" not in st.session_state:
    st.error("비밀번호 찾기 페이지에서 이메일 인증을 먼저 해주세요.")
    st.stop()

st.title("비밀번호 재설정")

new_password = st.text_input("새 비밀번호", type="password")
confirm_password = st.text_input("새 비밀번호 확인", type="password")

if st.button("비밀번호 재설정"):
    if not new_password or not confirm_password:
        st.error("비밀번호와 비밀번호 확인을 모두 입력해주세요.")
    elif new_password != confirm_password:
        st.error("비밀번호가 일치하지 않습니다.")
    else:
        hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        try:
            with engine.connect() as conn:
                update_stmt = text("UPDATE users SET password = :password WHERE email = :email")
                conn.execute(update_stmt, {"password": hashed_pw.decode('utf-8'), "email": st.session_state["reset_email"]})
                conn.commit()
            st.success("비밀번호가 성공적으로 재설정되었습니다. 로그인 페이지로 이동합니다.")
            del st.session_state["reset_email"]
        except Exception:
            st.error("비밀번호 재설정 중 오류가 발생했습니다. 다시 시도해주세요.")
