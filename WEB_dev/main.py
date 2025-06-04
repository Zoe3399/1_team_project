import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import duckdb

from map import show_map  # 팀에서 만든 지도 함수 import

DB_URI = "postgresql://postgres:1234@localhost:5432/traffic_db"
engine = create_engine(DB_URI, echo=False)

def get_risk_data():
    query = """
    SELECT 
        latitude,
        longitude,
        region_name AS location_name,
        risk_level,
        accident_count
    FROM accident_detail
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    LIMIT 300
    """
    df = duckdb.sql(query).df()
    return df

def show():
    st.markdown(
        '''
        <style>
        .big-title { font-size:2.2rem; font-weight:600; margin-bottom:1em; color:#fff; }
        .desc { font-size:1.1rem; color:#bbb; margin-bottom:2em; }
        .detail-panel { background: #181e22; padding: 2em 1em 2em 1.5em; border-radius: 12px; margin-top: 2em; min-height: 350px; }
        </style>
        ''', unsafe_allow_html=True
    )
    st.markdown('<div class="big-title">🗺️ 교통사고 위험 지도</div>', unsafe_allow_html=True)
    st.markdown('<div class="desc">실시간 교통사고 위험지역을 한눈에! 마커에 마우스를 올리면 주요 정보, 클릭하면 상세정보가 화면에 나와요.</div>', unsafe_allow_html=True)

    search = st.text_input("🔎 지역 검색", placeholder="예: 강남역, 서초구, 서울시청")
    st.markdown("#### 🔍 위험도 색상 안내")
    st.markdown("🟥 고위험 | 🟧 중위험 | 🟩 저위험")
    risk_filter = st.radio("위험도 선택", ["전체", "고", "중", "저"], horizontal=True)

    df = get_risk_data()

    # --- 2열 레이아웃: 왼쪽(상세), 오른쪽(지도) ---
    col1, col2 = st.columns([1.1, 2])

    with col2:
        # 지도 및 마커 출력
        # show_map에서 클릭된 마커 index를 st.session_state["selected_marker"]에 저장하도록 map.py에서 구현 필요
        show_map(df, search=search, risk_filter=risk_filter)

    with col1:
        # 클릭된 마커 정보 (없으면 안내)
        selected = st.session_state.get("selected_marker", None)
        if selected is not None and isinstance(selected, int) and 0 <= selected < len(df):
            row = df.iloc[selected]
            st.markdown('<div class="detail-panel">', unsafe_allow_html=True)
            st.markdown(f"### 📍 {row['location_name']}  \n"
                        f"**위험등급**: {row['risk_level']}  \n"
                        f"**사고건수**: {row['accident_count']}건  \n"
                        f"**좌표**: ({row['latitude']:.4f}, {row['longitude']:.4f})", unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            st.button("상세창 닫기", on_click=lambda: st.session_state.pop("selected_marker", None))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="detail-panel" style="color:#666;">지도에서 지역을 클릭하면 상세 정보가 여기에 표시됩니다.</div>', unsafe_allow_html=True)