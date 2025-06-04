import streamlit as st
from pages import home, login, sign_in, dashboard, stats, map

# 세션 초기화
def init_session():
    defaults = {
        'logged_in': False,
        'username': None,
        'page': 'home',
        'users': {
            'admin': '1234',
            'guest': 'guestpass'
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# 페이지 목록 정의 (selectbox에 보일 것만)
pages = {
    "Home": "home",
    "Dashboard": "dashboard",
    "Map": "map",
    "Stats": "stats"
}

page_keys = list(pages.keys())
page_values = list(pages.values())

# 상단 메뉴 구성
col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    # 로그인/회원가입 페이지일 땐 selectbox 숨기기
    if st.session_state.page in page_values:
        selected_key = st.selectbox("페이지 이동", page_keys, index=page_values.index(st.session_state.page))
        st.session_state.page = pages[selected_key]

with col2:
    if not st.session_state.logged_in:
        if st.button("login", key="nav_login"):
            st.session_state.page = "login"
            st.rerun()
    else:
        if st.button("log out", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.page = "home"
            st.rerun()

with col3:
    if not st.session_state.logged_in:
        if st.button("sign in", key="nav_signin"):
            st.session_state.page = "sign_in"
            st.rerun()

# 페이지 라우팅
if st.session_state.page == 'home':
    home.show()
elif st.session_state.page == 'login':
    login.show()
elif st.session_state.page == 'sign_in':
    sign_in.show()
elif st.session_state.page == 'dashboard':
    if st.session_state.logged_in:
        dashboard.show()
    else:
        st.warning("🚫 로그인 후 이용 가능합니다.")
elif st.session_state.page == 'map':
    if st.session_state.logged_in:
        map.show()
    else:
        st.warning("🚫 로그인 후 이용 가능합니다.")
elif st.session_state.page == 'stats':
    if st.session_state.logged_in:
        stats.show()
    else:
        st.warning("🚫 로그인 후 이용 가능합니다.")
        

# cd 1_team_project/web_src && streamlit run app.py
# http://localhost:8501