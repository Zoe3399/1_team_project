import streamlit as st

def login_page():
    st.markdown("<h1 style='text-align: center;'>🚦 로그인</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>서비스 이용을 위해 로그인하세요</p>", unsafe_allow_html=True)
    st.write("")
    user_id = st.text_input("ID", placeholder="아이디를 입력하세요")
    user_pw = st.text_input("PW", type="password", placeholder="비밀번호를 입력하세요")

    if st.button("로그인", use_container_width=True):
        st.success(f"{user_id}님 환영합니다!")
        st.session_state["is_login"] = True
        st.session_state["user_id"] = user_id
        st.session_state["page"] = "main"

    if st.button("비회원으로 이용하기", use_container_width=True):
        st.session_state["is_login"] = False
        st.session_state["user_id"] = "guest"
        st.session_state["page"] = "main"

    # 회원가입/비밀번호 찾기 버튼 아래 배치 (2열)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("회원가입", use_container_width=True):
            st.session_state["page"] = "sign_up"
    with col2:
        if st.button("비밀번호 찾기", use_container_width=True):
            st.session_state["page"] = "find_pw"
if __name__ == "__main__":
    login_page()