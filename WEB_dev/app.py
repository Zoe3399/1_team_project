import streamlit as st
import reset_pw

# 페이지별 함수 import (파일에 맞게 조정 필요)
import login
import terms
import sign_up
import find_pw
import main
import detail
import download
import mypage

# --- 세션 상태 기본값 ---
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "is_login" not in st.session_state:
    st.session_state["is_login"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# --- 로그인 체크 함수 ---
def require_login():
    if not st.session_state.get("is_login", False):
        st.session_state["page"] = "login"
        st.stop()

# --- 사이드바 메뉴 구성 ---
def sidebar_menu():
    with st.sidebar:
        st.markdown("### 🚦 서비스 메뉴")
        if st.session_state["is_login"]:
            st.write(f"**[{st.session_state['user_id']}]님 환영합니다!**")
            menu = st.radio(
                "이동할 페이지 선택",
                options=["메인", "데이터 다운로드", "마이페이지", "로그아웃"],
                key="sidebar_menu"
            )
            # 메뉴 선택시 페이지 전환
            if menu == "메인":
                st.session_state["page"] = "main"
            elif menu == "데이터 다운로드":
                st.session_state["page"] = "download"
            elif menu == "마이페이지":
                st.session_state["page"] = "mypage"
            elif menu == "로그아웃":
                st.session_state["is_login"] = False
                st.session_state["user_id"] = None
                st.session_state["page"] = "login"
                st.experimental_rerun()
        else:
            menu = st.radio(
                "이동할 페이지 선택",
                options=["로그인", "회원가입"],
                key="sidebar_menu_guest"
            )
            if menu == "로그인":
                st.session_state["page"] = "login"
            elif menu == "회원가입":
                st.session_state["page"] = "terms"

# --- 상단 네비게이션(간단하게) ---
def top_nav():
    st.markdown(
        f"<div style='background:#f6f6f6;padding:12px 0 6px 0;text-align:center;font-size:24px;'><b>🚦 안전 지도 서비스</b></div>",
        unsafe_allow_html=True
    )
    page_label = {
        "login": "로그인",
        "terms": "약관 동의",
        "sign_up": "회원가입",
        "find_pw": "비밀번호 찾기",
        "main": "메인(지도)",
        "detail": "상세정보",
        "download": "데이터 다운로드",
        "mypage": "마이페이지",
        "reset_pw": "비밀번호 재설정"
    }
    now = st.session_state["page"]
    st.markdown(
        f"<div style='text-align:center;color:#888;font-size:16px;margin-bottom:14px;'>[ {page_label.get(now, now)} ]</div>",
        unsafe_allow_html=True
    )

# --- 앱 메인 ---
def main_router():
    # 사이드바(로그인, 비로그인 모두)
    sidebar_menu()
    # 상단 네비
    top_nav()
    # 페이지 라우팅
    page = st.session_state["page"]

    if page == "login":
        login.login_page()
    elif page == "terms":
        terms.terms_page()
    elif page == "sign_up":
        sign_up.sign_up_page()
    elif page == "find_pw":
        find_pw.find_pw_page()
    elif page == "main":
        main.main_page()
    elif page == "detail":
        # 로그인 필요
        require_login()
        detail.detail_page()
    elif page == "download":
        require_login()
        download.download_page()
    elif page == "mypage":
        require_login()
        mypage.mypage_page()
    elif page == "reset_pw":
        reset_pw.reset_pw_page()
    else:
        st.error("존재하지 않는 페이지입니다.")

# --- 실행 ---
if __name__ == "__main__":
    main_router()