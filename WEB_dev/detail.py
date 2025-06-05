# detail.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import engine
import json

def detail_page(region):
    # 1) 로그인/게스트 체크
    if not (st.session_state.get("is_login", False) or st.session_state.get("is_guest", False)):
        st.session_state["page"] = "login"
        st.stop()

    # 2) region parameter check
    if not region:
        st.warning("지도에서 보고 싶은 지역 마커를 먼저 클릭하세요.")
        return

    st.title(f"‘{region}’ 지역 사고 상세 정보")

    # 3) 사고 상세 테이블(accident_detail)에서 해당 지역 정보 조회
    with engine.connect() as conn:
        query_detail = text("""
            SELECT *
            FROM accident_detail
            WHERE region_name = :r
        """)
        detail_rows = conn.execute(query_detail, {"r": region}).fetchall()

    if not detail_rows:
        st.info("해당 지역의 상세 정보가 없습니다.")
        return

    data = [dict(row._mapping) for row in detail_rows]
    df_detail = pd.DataFrame(data)

    # --- 상단 요약 ---
    lat = df_detail.loc[0, "latitude"]
    lon = df_detail.loc[0, "longitude"]
    st.markdown(f"<b>좌표:</b> {lat:.5f}, {lon:.5f}", unsafe_allow_html=True)

    # --- 위험등급 컬러/아이콘 ---
    risk_level = df_detail.loc[0, "risk_level"]
    color = {"고":"#ff4d4d","중":"#ffb94d","저":"#3498db"}.get(risk_level,"gray")
    st.markdown(f"<span style='color:{color}; font-size:1.2em;'>●</span> <b style='color:{color};'>{risk_level} 위험</b>", unsafe_allow_html=True)

    st.subheader("사고 상세 레코드")
    st.dataframe(df_detail)  # 전체 raw 데이터를 표로 보여줌

    # --- 최근 1~3년 사고건수 ---
    if "year" in df_detail.columns and "accident_count" in df_detail.columns:
        year_group = df_detail.groupby("year")["accident_count"].sum().sort_index(ascending=False)
        st.subheader("최근 1~3년 사고 건수")
        st.bar_chart(year_group)

    # --- 사고 유형별 분포1 (보행자/운전자 등) ---
    if "accident_type_stats" in df_detail.columns:
        acc_types = df_detail.loc[0, "accident_type_stats"]
        if isinstance(acc_types, str):
            acc_types = json.loads(acc_types)
        df_types = pd.DataFrame(list(acc_types.items()), columns=["사고유형", "건수"]).set_index("사고유형")
        st.subheader("사고 유형별 분포(보행자/운전자 등)")
        st.bar_chart(df_types)

    # --- 사고 유형별 분포2 (교차로/횡단보도 등 도로 환경) ---
    if "road_env" in df_detail.columns:
        envs = df_detail["road_env"].value_counts()
        st.subheader("도로 환경별 분포(교차로/횡단보도 등)")
        st.bar_chart(envs)

    # --- 시간대별 사고 그래프 ---
    if "hourly_stats" in df_detail.columns:
        hourly = df_detail.loc[0, "hourly_stats"]
        if isinstance(hourly, str):
            hourly = json.loads(hourly)
        hours = list(hourly.keys())
        counts = list(hourly.values())
        st.subheader("시간대별 사고 건수")
        st.bar_chart(pd.DataFrame({"건수": counts}, index=hours))

    # --- 도로 환경(텍스트/사진/거리뷰 등) ---
    if "road_env" in df_detail.columns:
        env_str = df_detail.loc[0, "road_env"]
        st.markdown(f"**도로 환경:** {env_str}")

        # 구글 거리뷰(예시)
        # if "streetview_url" in df_detail.columns and pd.notnull(df_detail.loc[0, "streetview_url"]):
        #     url = df_detail.loc[0, "streetview_url"]
        #     st.markdown(f"[거리뷰로 보기]({url})")

    # --- 리포트 다운로드 ---
    st.download_button(
        label="리포트 엑셀 다운로드",
        data=df_detail.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{region}_사고상세.csv",
        mime="text/csv"
    )

    # 7) ‘뒤로 가기’ 등 버튼
    if st.button("뒤로 가기"):
        st.session_state["page"] = "main"
        st.experimental_rerun()