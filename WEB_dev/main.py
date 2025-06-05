import streamlit as st
import pandas as pd
from map import show_map  # 팀에서 만든 지도 함수 import
from db import engine  # 데이터베이스 연결 엔진 import
from detail import detail_page

def get_risk_data():
    query = """
    SELECT 
        latitude,
        longitude,
        region_code,  -- region_code 추가
        region_name AS location_name,
        risk_level,
        accident_count
    FROM accident_detail
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    LIMIT 300
    """
    df = pd.read_sql(query, engine)
    return df

def main_page():
    # 제목 영역
    st.markdown('''
    <div style="background:#212a3e; padding:1.7em 2em 1.3em 2em; border-radius:16px; margin-bottom:2em; box-shadow:0 2px 14px 0 rgba(0,0,0,0.13);">
      <div style="font-size:2.2rem; font-weight:700; color:#fff;">🗺️ 교통사고 위험 지도</div>
      <div style="font-size:1.08rem; color:#f5f5f5; margin-top:0.6em;">지도에서 지역을 선택하면 왼쪽에 상세 정보가 표시됩니다.</div>
      <div style="margin-top:1.1em;">
        <span style="font-size:1.15em; color:#ff4d4d; font-weight:600;">🟥 고위험</span> &nbsp;
        <span style="font-size:1.15em; color:#ffb94d; font-weight:600;">🟧 중위험</span> &nbsp;
        <span style="font-size:1.15em; color:#3498db; font-weight:600;">🟦 저위험</span>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    # 검색 필터 영역
    with st.container():
        st.markdown('<div style="background:#f8f9fc;border-radius:13px;padding:1em 2em 0.7em 2em;margin-bottom:1.3em;">', unsafe_allow_html=True)
        colA, colB = st.columns([3, 5])
        with colA:
            search = st.text_input("지역 검색", placeholder="예: 강남역, 서울역")
        with colB:
            risk_filter = st.radio("위험도", ["전체", "고", "중", "저"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 데이터 가져오기 및 필터
    df = get_risk_data()
    if risk_filter != "전체":
        df = df[df["risk_level"] == risk_filter]
    if search:
        df = df[df["location_name"].str.contains(search, case=False, na=False)]

    # 와이어프레임 구조: 좌측 상세정보 + 우측 지도
    col_left, col_right = st.columns([1.5, 2], gap="large")

    with col_left:
        # 선택된 지역 코드를 세션 상태에서 확인하도록 변경
        if "selected_region_code" in st.session_state and st.session_state["selected_region_code"]:
            region_code = st.session_state["selected_region_code"]
            # detail_page에 region_code 전달
            detail_page(region_code)
        else:
            st.markdown("### 📋 상세 정보")
            st.info("지역을 클릭하면 여기에 상세 정보가 표시됩니다.")

    with col_right:
        st.markdown("### 📍 사고 위험 지도")
        # show_map 호출 시, 각 지역 클릭하면 st.session_state['selected_region_code']가 해당 region_code로 변경되도록 map.py에서 처리됨
        show_map(df)  # 지도 클릭 시 선택된 지역의 region_code가 st.session_state['selected_region_code']에 저장되도록 구현 필요 (map.py 참고)