from shapely.geometry import shape, Point
from detail import detail_page
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
from db import engine

def show_map(data=None,height=400):
    # st.subheader("📍 사고 위험 지도")

    # 1. 지도의 기본 중심(서울) 설정
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    # 2. 사고 데이터 불러오기 (구/군 단위)
    #   region_code: 구/군 코드, region_name: 지역명, risk_level: 위험도
    if data is None:
        query = """
            SELECT ad.region_code, ri.region_name AS region_name, ad.risk_level
            FROM accident_detail ad
            JOIN region_info ri ON ad.region_code = ri.region_code
            WHERE ad.region_code IS NOT NULL
            GROUP BY ad.region_code, ri.region_name, ad.risk_level
            LIMIT 100
        """
        data = pd.read_sql(query, engine)
        # 실제 컬럼명 출력(디버그)
        st.write("데이터프레임 컬럼:", data.columns.tolist())
        # region_name 컬럼이 없을 경우 컬럼명을 소문자로 강제 변환
        if "region_name" not in data.columns:
            data.columns = [col.lower() for col in data.columns]
            st.write("컬럼 소문자 변환 후:", data.columns.tolist())

    # region_name 컬럼명 정합성 체크 및 변환
    if "region_name" not in data.columns:
        if "location_name" in data.columns:
            data.rename(columns={"location_name": "region_name"}, inplace=True)
            # st.info("location_name 컬럼명을 region_name으로 변경하였습니다.")
        else:
            st.warning(f"데이터프레임에 'region_name' 컬럼이 없습니다. 실제 컬럼명: {data.columns.tolist()}")

    # 3. GeoJSON (행정구역 경계 데이터) 파일 불러오기
    geojson_path = "./data/법정구역_시군구_simplified.geojson"
    with open(geojson_path, encoding="utf-8") as f:
        geojson = json.load(f)

    def find_region_by_coordinate(lat, lon, geojson):
        """좌표(lat, lon)가 포함된 GeoJSON feature의 SIG_KOR_NM 반환"""
        point = Point(lon, lat)
        for feature in geojson.get("features", []):
            polygon = shape(feature.get("geometry"))
            if polygon.contains(point):
                return feature.get("properties", {}).get("SIG_KOR_NM")
        return None

    # 4. 위험도별 색상 지정 (고:빨강, 중:주황, 저:파랑)
    risk_color_map = {
        "고": "#FF4D4D",     # 빨강
        "중": "#FFB94D",     # 주황
        "저": "#3498DB"      # 파랑
    }

    # 5. 각 구/군 경계(폴리곤)에 위험도별로 색 입히는 함수
    def style_function(feature):
        try:
            region_name = feature["properties"].get("SIG_KOR_NM", "")
            # 간단한 이름 매핑 예시
            region_alias = {
                "강남구": "강남구",
                "서초구": "서초구",
                "용산구": "용산구",
                "관악구": "관악구"
            }
            mapped_name = region_alias.get(region_name, region_name)
            # 데이터에서 현재 폴리곤(region_name)에 해당하는 위험도 가져오기
            row = data[data["region_name"] == mapped_name]
            if not row.empty:
                risk_level = row["risk_level"].values[0]
                color = risk_color_map.get(risk_level, "#888888")  # 없으면 회색
                return {
                    "fillColor": color,
                    "color": "#333",
                    "weight": 1,
                    "fillOpacity": 0.5
                }
            else:
                # 데이터가 없으면 연회색
                return {
                    "fillColor": "#dddddd",
                    "color": "#cccccc",
                    "weight": 0.3,
                    "fillOpacity": 0.1
                }
        except KeyError as e:
            st.warning(f"데이터프레임에 'region_name' 컬럼이 없습니다. 실제 컬럼명: {data.columns.tolist()}")
            return {
                "fillColor": "#ff00ff",
                "color": "#000",
                "weight": 0.1,
                "fillOpacity": 0.1
            }

    # 6. GeoJson 레이어 지도에 추가
    gj = folium.GeoJson(
        geojson,
        name="지역 위험도",
        style_function=style_function,
        highlight_function=lambda feat: {"weight": 3, "color": "#111"},
        tooltip=folium.GeoJsonTooltip(fields=["SIG_KOR_NM"], aliases=["지역:"]),
    )
    gj.add_to(m)

    # 각 영역에 popup 텍스트 추가
    for feature in geojson["features"]:
        region_name = feature["properties"].get("SIG_KOR_NM", "")
        risk_row = data[data["region_name"] == region_name]
        if not risk_row.empty:
            risk_level = risk_row["risk_level"].values[0]
            popup_text = f"{region_name} 위험도: {risk_level}"
            folium.Popup(popup_text).add_to(folium.GeoJson(feature))

    # 전체 지도 먼저 표시
    map_ret = st_folium(m, height=750, use_container_width=True, key="main_map")

    # 클릭 처리: 좌표에 해당하는 행정구역명을 찾아 세션에 저장
    if map_ret and map_ret.get("last_clicked"):
        lat = map_ret["last_clicked"]["lat"]
        lon = map_ret["last_clicked"]["lng"]
        region_name = find_region_by_coordinate(lat, lon, geojson)
        if region_name:
            st.session_state["selected_region"] = region_name

    # 선택된 지역이 있는 경우 상세 페이지 표시
    if "selected_region" in st.session_state:
        detail_page(st.session_state["selected_region"])