import streamlit as st
import folium
from streamlit_folium import st_folium

def show_map(data=None):
    st.subheader("📍 사고 위험 지도")
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 더미 또는 전달받은 데이터를 마커로 표시
    if data is None:
        # 예시 더미 마커
        folium.Marker(
            location=[37.5665, 126.9780],
            tooltip="서울시청\n위험도: 중",
            popup="서울시청 상세정보 보기"
        ).add_to(m)
    else:
        for _, row in data.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                tooltip=f"{row['location_name']} - 위험도: {row['risk_level']}",
                popup=f"{row['location_name']} 상세보기"
            ).add_to(m)

    st_folium(m, width=700, height=500)
