import streamlit as st
import os

def read_md(file_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, file_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

st.markdown(
    "<h1 style='text-align:center;'>회원가입 - 약관동의</h1>"
    "<p style='text-align:center;color:gray;'>서비스 이용을 위해 약관에 동의해 주세요.</p>",
    unsafe_allow_html=True
)

terms = [
    ("이용약관 동의 (필수)", "약관동의/service_terms.md", True),
    ("개인정보처리방침 동의 (필수)", "약관동의/privacy_policy.md", True),
    ("위치정보 동의 (선택)", "약관동의/location_info_consent.md", False),
    ("고유식별정보 동의 (선택)", "약관동의/unique_id_consent.md", False),
    ("마케팅 정보 수신 동의 (선택)", "약관동의/marketing_consent.md", False),
]

# --- 상태 초기화 ---
for label, _, _ in terms:
    if label not in st.session_state:
        st.session_state[label] = False
if "all_agree" not in st.session_state:
    st.session_state["all_agree"] = False

# --- 전체동의 체크 UX ---
all_required_checked = all(st.session_state[label] for label, _, _ in terms)
all_agree_clicked = st.checkbox(
    "전체 약관에 모두 동의합니다", 
    value=st.session_state["all_agree"],
    key="all_agree_cb", 
    help="모든 약관에 한번에 동의할 수 있습니다."
)

# 전체동의 버튼을 눌렀을 때만 전체 값 변경
if all_agree_clicked != st.session_state["all_agree"]:
    st.session_state["all_agree"] = all_agree_clicked
    for label, _, _ in terms:
        st.session_state[label] = all_agree_clicked

# 개별 약관 체크박스
for label, file, required in terms:
    prev = st.session_state[label]
    st.session_state[label] = st.checkbox(label, value=st.session_state[label], key=f"agree_{label}")
    # 개별 체크가 하나라도 해제되면 전체동의도 해제
    if prev and not st.session_state[label]:
        st.session_state["all_agree"] = False

    with st.expander("자세히 보기"):
        st.markdown(read_md(file))

# 필수 동의만 확인
all_required = all(st.session_state[label] for label, _, required in terms if required)

if all_required:
    if st.button("동의하고 회원가입 계속", type="primary", use_container_width=True):
        st.session_state["page"] = "sign_up"
else:
    st.button("동의하고 회원가입 계속", disabled=True, use_container_width=True)

if st.button("로그인으로 돌아가기"):
    st.session_state["page"] = "login"