import streamlit as st
import pandas as pd
from map import show_map
from db import engine
from detail import get_detail_info

def get_risk_data():
    query = """
    SELECT 
        latitude,
        longitude,
        region_code,
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
    st.markdown('''
    <div style="background:#212a3e; padding:1.7em 2em 1.3em 2em; border-radius:16px; margin-bottom:2em; box-shadow:0 2px 14px 0 rgba(0,0,0,0.13);">
      <div style="font-size:2.2rem; font-weight:700; color:#fff;">🗺️ 교통사고 발생 예측 지도</div>
      <div style="font-size:1.08rem; color:#f5f5f5; margin-top:0.6em;">지도에서 지역을 클릭하면 상세 정보가 좌측에 표시됩니다.</div>
      <div style="margin-top:1.1em;">
        <span style="font-size:1.15em; color:#ff4d4d; font-weight:600;">🟥 고위험</span> &nbsp;
        <span style="font-size:1.15em; color:#ffb94d; font-weight:600;">🟧 중위험</span> &nbsp;
        <span style="font-size:1.15em; color:#22bb33; font-weight:600;">🟩 저위험</span>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    df = get_risk_data()

    colA, colB = st.columns([3, 5])
    with colA:
        search = st.text_input("지역 검색", placeholder="예: 강남역, 서울역")
    with colB:
        risk_filter = st.radio("위험도", ["전체", "고", "중", "저"], horizontal=True)

    df_filtered = df.copy()
    if risk_filter != "전체":
        df_filtered = df_filtered[df_filtered["risk_level"] == risk_filter]
    if search:
        df_filtered = df_filtered[df_filtered["location_name"].str.contains(search, case=False, na=False)]

    if "selected_region_code" not in st.session_state:
        st.session_state.selected_region_code = None

    col_left, col_right = st.columns([2, 4], gap="large")
    with col_right:
        st.markdown("### 🗺️ 사고 위험 지도")
        selected_code = show_map(df_filtered, height=420, width=600)
        if selected_code:
            st.session_state.selected_region_code = selected_code
    with col_left:
        st.markdown("#### 🗂️ 지역 상세 정보")
        region_code = st.session_state.selected_region_code
        if region_code:
            detail = get_detail_info(region_code)
            if detail:
                st.markdown(f"""
                    <div style="font-size:1.1rem;">
                    <b>지역명:</b> {detail['region_name']}<br>
                    <b>위험도:</b> {detail['risk_level']}<br>
                    <b>사고건수:</b> {detail['accident_count']}<br>
                    <b>고령자 비율:</b> {detail['elderly_ratio']*100:.1f}%<br>
                    <b>도로환경:</b> {detail['road_env']}<br>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("상세 정보가 없습니다.")
        else:
            st.info("지도의 지역을 클릭하세요.")

if __name__ == "__main__":
    main_page()