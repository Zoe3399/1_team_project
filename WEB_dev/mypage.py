import streamlit as st
from sqlalchemy import create_engine, text
from db import engine


def mypage_page():
    # 로그인 또는 비회원 상태 확인
    if not (st.session_state.get("is_login", False) or st.session_state.get("is_guest", False)):
        st.session_state["page"] = "login"
        st.stop()

    # 로그인된 사용자 정보 조회 (비회원일 경우 제한된 정보만)
    st.title("마이 페이지")

    if st.session_state.get("is_guest", False):
        st.error("로그인이 필요합니다.")
        st.stop()
    else:
        user_email = st.session_state.get("user_id")
        with engine.connect() as conn:
            user_query = text("""
                SELECT id, username, email, user_type, created_at, is_active 
                FROM users 
                WHERE email = :e
            """)
            user_data = conn.execute(user_query, {"e": user_email}).fetchone()

        if not user_data:
            st.error("사용자 정보를 불러오지 못했습니다.")
            return

        user_id, username, email, user_type, created_at, is_active = user_data

        st.subheader("회원 정보")
        st.write(f"- ID: {user_id}")
        st.write(f"- 아이디(사용자명): {username}")
        st.write(f"- 이메일: {email}")
        st.write(f"- 사용자 유형: {user_type}")
        st.write(f"- 가입 일시: {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"- 계정 활성화 여부: {'활성' if is_active else '비활성'}")

        # 회원탈퇴 섹션
        st.markdown("---")
        st.subheader("회원 탈퇴")
        agree_withdraw = st.checkbox("정말로 회원 탈퇴를 진행하시겠습니까?", key="agree_withdraw")
        if agree_withdraw:
            if st.button("회원 탈퇴", use_container_width=True):
                try:
                    with engine.connect() as conn:
                        delete_stmt = text("UPDATE users SET is_active = FALSE WHERE email = :e")
                        with conn.begin():
                            conn.execute(delete_stmt, {"e": user_email})
                    st.success("회원 탈퇴가 완료되었습니다. 로그아웃 후 더 이상 로그인할 수 없습니다.")
                    # 세션 초기화 후 로그인 페이지로 이동
                    st.session_state["is_login"] = False
                    st.session_state["user_id"] = None
                    st.session_state["is_guest"] = False
                    st.session_state["page"] = "login"
                    st.rerun()
                except Exception:
                    st.error("회원 탈퇴 중 오류가 발생했습니다. 다시 시도해주세요.")

    # 로그아웃 버튼 (비회원도 로그아웃)
    st.markdown("---")
    if st.button("로그아웃", use_container_width=True):
        st.session_state["is_login"] = False
        st.session_state["is_guest"] = False
        st.session_state["user_id"] = None
        st.success("로그아웃 되었습니다.")
        st.session_state["page"] = "login"
        st.rerun()
