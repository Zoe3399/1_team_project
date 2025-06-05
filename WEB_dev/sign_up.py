import streamlit as st
from sqlalchemy import text
import bcrypt
import time
from db import engine  # DB 연결 엔진

def sign_up_page():
    # ── (A) 회원가입 직후 "just_signed_up=True"가 세팅되어 있다면, 성공 메시지를 보여준 뒤 곧 바로 로그인 페이지로 리다이렉트 ──
    if st.session_state.get("just_signed_up", False):
        st.success("회원가입이 완료되었습니다! 3초 후 로그인 페이지로 이동합니다.")
        time.sleep(3)
        # 로그인 페이지로 이동하기 위해 page 키를 변경
        st.session_state["page"] = "login"
        # 플래그는 꺼줍니다(다시 반복하지 않도록)
        st.session_state["just_signed_up"] = False
        st.rerun()
        return

    # ── (B) 페이지 타이틀 및 안내 문구 ────────────────────────────────────────────
    st.markdown("<h1 style='margin-bottom:32px;'>회원가입</h1>", unsafe_allow_html=True)
    st.markdown("※ 이메일 인증은 필수입니다. 이메일을 입력하고 인증번호를 확인해 주세요.")

    # ── (1) 이메일 입력 + 인증 버튼 ───────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input("이메일", placeholder="이메일 주소를 입력하세요", key="email_input")
    with col2:
        st.write("")  # 빈 칸
        email_auth_btn = st.button("이메일 인증", key="email_auth_btn")

    # ── (2) 인증번호 입력 + 확인 버튼 ─────────────────────────────────────────────
    col3, col4 = st.columns([3, 1])
    with col3:
        email_code_input = st.text_input("인증번호 입력", placeholder="6자리 숫자", key="email_code_input")
    with col4:
        st.write("")
        email_verify_btn = st.button("인증번호 확인", key="email_verify_btn")

    # 세션 초기화 (한번도 세팅된 적 없을 때만)
    if "email_code" not in st.session_state:
        st.session_state["email_code"] = None
    if "email_verified" not in st.session_state:
        st.session_state["email_verified"] = False

    # ── (3) 비밀번호/추가정보 입력 ────────────────────────────────────────────────
    col_pw1, col_pw2 = st.columns(2)
    with col_pw1:
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
    with col_pw2:
        password2 = st.text_input("비밀번호 확인", type="password", placeholder="비밀번호를 다시 입력하세요")

    user_type = st.selectbox("사용자 유형", ["학생", "공공기관", "회사", "기타"], key="user_type")
    purpose = st.text_input("사용 목적", placeholder="앱 이용 목적을 입력해 주세요", key="purpose_input")
    signup_btn = st.button("회원가입", key="signup_btn", use_container_width=True)

    # ── (1) 이메일 인증 버튼 클릭 로직 ─────────────────────────────────────────────
    if email_auth_btn:
        # 1-1) 이메일 입력 여부 확인
        if not email:
            st.warning("이메일을 입력해 주세요.")
        elif "@" not in email or "." not in email:
            st.warning("유효한 이메일 형식으로 입력해 주세요.")
        else:
            # 1-2) DB에서 중복 여부 검사
            with engine.begin() as conn:
                duplicate_count = conn.execute(
                    text("SELECT COUNT(*) FROM users WHERE email = :e"),
                    {"e": email}
                ).scalar()
            if duplicate_count > 0:
                st.error("이미 가입된 이메일입니다.")
            else:
                # 1-3) (테스트용) 고정 코드 "123456" 발송
                st.session_state["email_code"] = "123456"
                st.session_state["email_verified"] = False
                st.success("인증번호가 이메일로 발송되었습니다. (테스트용 코드: 123456)")

    # ── (2) 인증번호 확인 버튼 클릭 로직 ───────────────────────────────────────────
    if email_verify_btn:
        if not email_code_input:
            st.warning("인증번호를 입력해 주세요.")
        elif email_code_input == st.session_state["email_code"]:
            st.session_state["email_verified"] = True
            st.success("이메일 인증이 완료되었습니다.")
        else:
            st.error("인증번호가 일치하지 않습니다.")

    # ── (3) 회원가입 버튼 클릭 로직 ──────────────────────────────────────────────
    if signup_btn:
        # 3-1) 필수 입력 체크
        if not email or not password or not password2 or not purpose:
            st.error("이메일, 비밀번호, 비밀번호 확인, 사용 목적은 모두 필수 입력입니다.")
            return
        if not st.session_state["email_verified"]:
            st.error("이메일 인증을 완료해 주세요.")
            return
        if password != password2:
            st.error("비밀번호가 일치하지 않습니다.")
            return

        # 3-2) DB 중복 검사 후 INSERT (컬럼명을 명시해서 안전하게)
        with engine.begin() as conn:
            existing_count = conn.execute(
                text("SELECT COUNT(*) FROM users WHERE email = :e"),
                {"e": email}
            ).scalar()
            if existing_count > 0:
                st.error("이미 등록된 이메일입니다.")
                return

            # 3-3) 비밀번호 해시화 (bcrypt)
            password_bytes = password.encode("utf-8")
            hashed_pw = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")
            try:
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
            except Exception as e:
                st.error(f"회원가입 중 오류가 발생했습니다: {e}")
                return

        # ── (C) 회원가입 성공 후 "just_signed_up" 플래그 세팅 & 페이지 갱신 ──
        st.session_state["just_signed_up"] = True     
        # ※ 여기서는 바로 page 를 바꾸지 않고, 
        #    다음 리로드 시 (A) 블록이 동작하도록 just_signed_up=True만 설정합니다.
        st.rerun()