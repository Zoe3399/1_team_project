import streamlit as st
from sqlalchemy import create_engine, text
import bcrypt
import random

DB_URI = "postgresql://postgres:1234@localhost:5432/traffic_db"
engine = create_engine(DB_URI, echo=False)

st.markdown("""
    <h1 style='margin-bottom:32px;'>회원가입</h1>
""", unsafe_allow_html=True)

# 이메일 인증 안내문 (가장 위)
st.markdown("※ 이메일 인증은 필수입니다. 이메일을 입력하고 인증번호를 확인해 주세요.")

# 이메일 + 인증 버튼 (같은 행, 버튼을 아래쪽에 위치)
col1, col2 = st.columns([3, 1])
with col1:
    email = st.text_input("이메일", placeholder="이메일 주소를 입력하세요", key="email_input")
with col2:
    st.write(" ")  # 빈 줄 추가로 버튼이 입력창 하단에 맞춰짐
    st.write(" ") 
    email_auth_btn = st.button("이메일 인증", key="email_auth_btn")

# 인증번호 입력 + 확인 버튼
col3, col4 = st.columns([3, 1])
with col3:
    email_code_input = st.text_input("인증번호 입력", key="email_code_input", placeholder="6자리 숫자")
with col4:
    st.write(" ")  # 빈 줄 추가
    st.write(" ") 
    email_verify_btn = st.button("인증번호 확인", key="email_verify_btn")

if 'email_code' not in st.session_state:
    st.session_state.email_code = None
if 'email_verified' not in st.session_state:
    st.session_state.email_verified = False

# 비밀번호, 비밀번호 확인 입력란
col_pw1, col_pw2 = st.columns(2)
with col_pw1:
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
with col_pw2:
    password2 = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")

user_type = st.selectbox("사용자 유형", ["학생", "공공기관", "회사", "기타"])
purpose = st.text_input("사용 목적", placeholder="앱 이용 목적을 입력해 주세요")

signup_btn = st.button("회원가입", key="signup_btn", use_container_width=True)

# -- 이메일 인증 버튼 처리 --
if email_auth_btn:
    if not email:
        st.warning("이메일을 입력해 주세요.")
    elif "@" not in email or "." not in email:
        st.warning("이메일 형식으로 입력해 주세요.")
    else:
        code = f"{random.randint(0, 999999):06d}"
        st.session_state.email_code = code
        st.session_state.email_verified = False
        st.success("인증번호가 이메일로 발송되었습니다. (테스트용: " + code + ")")

# -- 인증번호 확인 버튼 처리 --
if email_verify_btn:
    if not email_code_input:
        st.warning("인증번호를 입력해 주세요.")
    elif email_code_input == st.session_state.email_code:
        st.session_state.email_verified = True
        st.success("이메일 인증이 완료되었습니다.")
    else:
        st.error("인증번호가 일치하지 않습니다.")

# -- 회원가입 버튼 처리 --
if signup_btn:
    if not password or not password2 or not email:
        st.error("비밀번호, 비밀번호 확인, 이메일은 필수 입력입니다.")
    elif not st.session_state.email_verified:
        st.error("이메일 인증을 완료해 주세요.")
    elif password != password2:
        st.error("비밀번호가 일치하지 않습니다.")
    else:
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        hashed_pw = hashed.decode('utf-8')
        with engine.connect() as conn:
            check_email = conn.execute(
                text("SELECT COUNT(*) FROM users WHERE email = :e"),
                {"e": email}
            ).scalar()
            if check_email > 0:
                st.error("이미 등록된 이메일입니다.")
            else:
                conn.execute(
                    text(
                        """
                        INSERT INTO users (password, email, user_type, purpose)
                        VALUES (:p, :e, :t, :pu)
                        """
                    ),
                    {"p": hashed_pw, "e": email, "t": user_type, "pu": purpose}
                )
                st.success("회원가입이 완료되었습니다!")
                st.info("로그인 페이지로 이동하여 로그인해 주세요.")
                st.session_state.email_verified = False
                st.session_state.email_code = None