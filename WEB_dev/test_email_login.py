# sign_up.py

import streamlit as st
import bcrypt
from sqlalchemy import text
from db import engine  # engine: SQLAlchemy 엔진
import time

def sign_up_page():
    """
    회원가입 페이지를 그려주고,
    입력된 값을 받아 DB에 삽입한 뒤 3초 뒤 로그인 페이지로 이동합니다.
    """
    st.title("회원가입")

    # 이미 회원가입 직후 리디렉션이 예약되어 있으면, 메시지 띄우고 페이지 전환
    if st.session_state.get("just_signed_up", False):
        st.success("회원가입이 완료되었습니다! 3초 후 로그인 페이지로 이동합니다.")
        time.sleep(3)
        st.session_state["page"] = "login"
        st.session_state["just_signed_up"] = False
        st.experimental_rerun()
        return

    # 이메일 입력
    email = st.text_input("이메일 주소를 입력하세요", key="signup_email")
    # (여기서는 이메일 인증 기능을 생략하고, 미리 발급된 ‘123456’ 고정 코드로 처리합니다.)
    email_code_input = st.text_input("인증번호 입력 (테스트용: 123456)", max_chars=6, key="signup_email_code")

    # 비밀번호 입력
    password = st.text_input("비밀번호", type="password", key="signup_password")
    password_confirm = st.text_input("비밀번호 확인", type="password", key="signup_password_confirm")

    # 사용자 유형 및 목적
    user_type = st.selectbox("사용자 유형", ["학생", "사업자", "공공기관", "기타"], key="signup_user_type")
    purpose = st.text_input("사용 목적", "앱 이용 목적을 입력해 주세요", key="signup_purpose")

    # 이메일 인증 버튼 (여기서는 테스트용으로 “123456”만 입력되면 인증 통과)
    if st.button("인증번호 확인"):
        if email_code_input == "123456":
            st.success("이메일 인증이 완료되었습니다.")
            st.session_state["email_verified"] = True
        else:
            st.error("인증번호가 올바르지 않습니다.")

    # 회원가입 버튼
    if st.button("회원가입"):
        # 1) 이메일 인증 여부 확인
        if not st.session_state.get("email_verified", False):
            st.error("이메일 인증을 먼저 진행해주세요.")
            return

        # 2) 비밀번호 매칭 확인
        if password != password_confirm:
            st.error("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
            return

        # 3) 이메일 중복 체크
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT COUNT(*) FROM users WHERE email = :e"),
                {"e": email}
            ).scalar()
        if result > 0:
            st.error("이미 사용 중인 이메일입니다.")
            return

        # 4) 비밀번호 해싱
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # 5) DB 삽입 (컬럼명을 명시해서 필요한 컬럼만 넣는다)
        try:
            with engine.begin() as conn:
                inserted = conn.execute(
                    text("""
                        INSERT INTO users (password, email, user_type, purpose)
                        VALUES (:p, :e, :t, :pu)
                        RETURNING id
                    """),
                    {
                        "p": hashed_pw,
                        "e": email,
                        "t": user_type,
                        "pu": purpose
                    }
                )
                new_id = inserted.scalar()
        except Exception as ex:
            st.error(f"회원가입 중 오류가 발생했습니다: {ex}")
            return

        # 6) 성공 메시지 및 세션 상태 설정 → 3초 뒤 로그인으로 리디렉션
        st.success("회원가입이 완료되었습니다! 3초 뒤 로그인 페이지로 이동합니다.")
        st.session_state["email_verified"] = False
        st.session_state["email_code"] = None
        st.session_state["just_signed_up"] = True
        st.experimental_rerun()


# 해당 모듈을 독립 실행했을 때(예: 개발용으로 python sign_up.py 로 실행)도 에러 안 나게 처리
if __name__ == "__main__":
    st.set_page_config(page_title="회원가입", layout="centered")
    sign_up_page()