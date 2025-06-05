# download.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import engine  # db.py에 정의된 engine 사용

def download_page():
    # 로그인 여부 체크(필요 시)
    if not (st.session_state.get("is_login", False) or st.session_state.get("is_guest", False)):
        st.session_state["page"] = "login"
        st.stop()

    st.title("데이터 다운로드")

    # 1) 사용자에게 다운로드 옵션 받기
    year = st.selectbox("연도 선택", [2021, 2022, 2023, 2024, 2025])
    region = st.text_input("지역명 입력 (예: 종로구)", placeholder="원하는 지역을 입력하세요")
    file_type = st.selectbox("파일 형식", ["CSV", "Excel"])

    # 2) “다운로드 생성” 버튼
    if st.button("다운로드 생성"):
        if not region:
            st.error("지역명을 입력하세요.")
            return

        # 3) DB에서 데이터 조회
        query = text("""
            SELECT region, year, month, hour, accident_count, elderly_ratio
            FROM accident_summary
            WHERE year = :y AND region ILIKE :r
            ORDER BY month, hour
        """)
        df = pd.read_sql(query, engine, params={"y": year, "r": f"%{region}%"})

        if df.empty:
            st.warning("해당 조건에 맞는 데이터가 없습니다.")
            return

        # 4) 데이터 표시
        st.subheader(f"{year}년 {region} 예측결과")
        st.dataframe(df)

        # 5) 파일로 변환 후 다운로드 버튼 제공
        if file_type == "CSV":
            csv_bytes = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="CSV 파일 다운로드",
                data=csv_bytes,
                file_name=f"{region}_{year}_예측결과csv",
                mime="text/csv",
            )
        else:  # Excel
            # 메모리에 Excel 파일 생성
            towrite = pd.ExcelWriter("temp.xlsx", engine="xlsxwriter")
            df.to_excel(towrite, index=False, sheet_name="Sheet1")
            towrite.save()
            with open("temp.xlsx", "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="Excel 파일 다운로드",
                data=excel_bytes,
                file_name=f"{region}_{year}_예측결과.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )