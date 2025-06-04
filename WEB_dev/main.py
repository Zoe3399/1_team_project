import streamlit as st
import folium
import json
from streamlit_folium import st_folium
from shapely.geometry import shape

def show():
    st.title("🗺️ 대한민국 교통사고 위험 지도")
    st.markdown("대한민국 지도를 기반으로 시각화가 준비될 예정입니다.")

    # 지역 선택 드롭다운
    region_coords = {
        "전국": [36.5, 127.9],
        "서울": [37.5665, 126.9780],
        "부산": [35.1796, 129.0756],
        "대구": [35.8722, 128.6025],
        "인천": [37.4563, 126.7052],
        "광주": [35.1595, 126.8526],
        "대전": [36.3504, 127.3845],
        "울산": [35.5384, 129.3114],
        "세종": [36.4801, 127.2890],
        "제주": [33.4996, 126.5312]
    }

    selected_region = st.selectbox("📍 지역 선택", list(region_coords.keys()))
    center = region_coords[selected_region]

    # 지도 생성
    m = folium.Map(location=center, zoom_start=10 if selected_region != "전국" else 7, control_scale=True)

    # 선택 지역에 마커 표시
    folium.Marker(
        location=center,
        popup=selected_region,
        tooltip=selected_region,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # 시도 GeoJSON
    with open("data/법정구역_시도_simplified.geojson", 'r', encoding='utf-8') as f:
        sido_geo = json.load(f)

    folium.GeoJson(
        sido_geo,
        name="시도 경계",
        style_function=lambda x: {
            'fillColor': '#f2f2f2',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.2
        },
        tooltip=folium.GeoJsonTooltip(fields=['CTP_KOR_NM'], aliases=['시도'])
    ).add_to(m)

    # 시군구 GeoJSON
    geojson_path = "data/법정구역_시군구_simplified.geojson"
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # 시군구 경계선 추가
    folium.GeoJson(
        geojson_data,
        name="시군구 경계",
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'blue',
            'weight': 1,
            'fillOpacity': 0.1
        },
        tooltip=folium.GeoJsonTooltip(fields=['SIG_KOR_NM'], aliases=['시군구'])
    ).add_to(m)

    # 시군구 중심에 이름 추가
    for feature in geojson_data['features']:
        name = feature['properties'].get('SIG_KOR_NM', '')
        geom = shape(feature['geometry'])
        centroid = geom.centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            icon=folium.DivIcon(html=f"""<div style="font-size: 13px; color: black; text-align: center;">{name}</div>""")
        ).add_to(m)

    # 지도 출력
    st_folium(m, width=800, height=600)