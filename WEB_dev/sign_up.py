# sign_up.py
import streamlit as st
from sqlalchemy import create_engine, text

# DB 연결 설정 (환경에 맞게 수정할 예정)
DB_URI = "postgresql://postgres:1234@localhost:5432/traffic_db"
engine = create_engine(DB_URI, echo=False)

st.title("회원가입")

# 입력 필드
username = st.text_input("아이디")
password = st.text_input("비밀번호", type="password")
email = st.text_input("이메일 (선택)")
user_type = st.selectbox("사용자 유형", ["학생", "공공기관", "회사", "기타"])
purpose = st.text_input("사용 목적")
signup_btn = st.button("회원가입")

if signup_btn:
    # 필수 입력 검사
    if not username or not password:
        st.error("아이디와 비밀번호는 필수 입력 항목입니다.")
    else:
        with engine.connect() as conn:
            # 중복 검사: 아이디
            check_user = conn.execute(
                text("SELECT COUNT(*) FROM users WHERE username = :u"),
                {"u": username}
            ).scalar()
            # 중복 검사: 이메일 (입력된 경우에만)
            check_email = 0
            if email:
                check_email = conn.execute(
                    text("SELECT COUNT(*) FROM users WHERE email = :e"),
                    {"e": email}
                ).scalar()

            if check_user > 0:
                st.error("이미 사용 중인 아이디입니다.")
            elif check_email > 0:
                st.error("이미 등록된 이메일입니다.")
            else:
                # 새 사용자 삽입
                conn.execute(
                    text(
                        """
                        INSERT INTO users (username, password, email, user_type, purpose)
                        VALUES (:u, :p, :e, :t, :pu)
                        """
                    ),
                    {"u": username, "p": password, "e": email or None, "t": user_type, "pu": purpose}
                )
                st.success("회원가입이 완료되었습니다!")
                st.info("로그인 페이지로 이동하여 로그인해 주세요.")