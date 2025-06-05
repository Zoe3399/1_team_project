import streamlit as st
# 페이지 설정
st.set_page_config(layout="wide")
import login
import sign_up
import terms
import find_pw
import reset_pw
import main
import detail
import download
import mypage
import logout




# --- 세션 상태 기본값 ---
if "page" not in st.session_state:
    st.session_state["page"] = "login"
if "is_login" not in st.session_state:
    st.session_state["is_login"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

# --- 로그인 체크 함수 ---
def require_login():
    if not (st.session_state.get("is_login", False) or st.session_state.get("is_guest", False)):
        st.session_state["page"] = "login"
        st.stop()

# --- 사이드바 메뉴 구성 ---
def sidebar_menu():
    with st.sidebar:
        st.markdown("### 메뉴")
        pages = {
            "메인페이지": "main",
            "데이터 다운로드": "download",
            "마이페이지": "mypage",
            "로그아웃": "logout",
        }
        for name, page in pages.items():
            if st.button(name):
                st.session_state["page"] = page

# --- 상단 네비게이션(간단하게) ---
def top_nav():
    st.markdown("---")
    st.markdown(f"**현재 페이지:** {st.session_state.get('page', '')}")

# --- 라우팅 ---
def main_router():
    page = st.session_state.get("page", "login")
    if page == "login":
        login.login_page()         
    elif page == "sign_up":
        # 약관 동의가 안된 상태면 terms 페이지로, 동의하면 sign_up 페이지로
        if not st.session_state.get("terms_agreed", False):
            st.session_state["page"] = "terms"
            st.rerun()
        else:
            sign_up.sign_up_page()
    elif page == "terms":
        terms.terms_page()          
    elif page == "find_pw":
        find_pw.find_pw_page()      
    elif page == "reset_pw":
        reset_pw.reset_pw_page()   
    elif page == "main":
        require_login()
        sidebar_menu()
        top_nav()
        main.main_page()            
    elif page == "download":
        require_login()
        sidebar_menu()
        top_nav()
        download.download_page()   
    elif page == "mypage":
        require_login()
        sidebar_menu()
        top_nav()
        mypage.mypage_page()        
    elif page == "detail":
        require_login()
        sidebar_menu()
        top_nav()
        detail.detail_page()        
    elif page == "logout":
        logout.logout_page()
    else:
        st.error("페이지를 찾을 수 없습니다.")

# --- 실행 ---
if __name__ == "__main__":
    main_router()