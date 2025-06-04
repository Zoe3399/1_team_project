import pandas as pd
import duckdb
import os

# 시간대 문자열 → 시간 숫자 매핑
time_map = {
    '0시~2시': 0, '2시~4시': 2, '4시~6시': 4, '6시~8시': 6,
    '8시~10시': 8, '10시~12시': 10, '12시~14시': 12,
    '14시~16시': 14, '16시~18시': 16, '18시~20시': 18,
    '20시~22시': 20, '22시~24시': 22
}

# 연도별 xls 파일을 정리하는 함수
def process_year_file(file_path: str, year: int) -> pd.DataFrame:
    df = pd.read_excel(file_path, engine="xlrd")

    # "사고(건)"이 포함된 행 필터링
    df = df[df['기준년도'].astype(str).str.contains("사고")]

    # 시간대 열만 추출
    time_cols = [col for col in df.columns if '시' in str(col)]

    df_long = df.melt(
        id_vars=['시도', '시군구'],
        value_vars=time_cols,
        var_name='time_range',
        value_name='accident_count'
    )

    # 시간대 변환
    df_long['hour'] = df_long['time_range'].map(time_map)

    # 기본 컬럼 추가
    df_long['year'] = year
    df_long['month'] = None
    df_long['elderly_ratio'] = None

    # 컬럼 정리
    df_long = df_long.rename(columns={'시군구': 'region'})
    df_final = df_long[['region', 'elderly_ratio', 'year', 'month', 'hour', 'accident_count']]

    return df_final

# DuckDB 연결 및 데이터 삽입 함수
def insert_to_duckdb(df_all: pd.DataFrame, db_path="elderly_accident.duckdb"):
    con = duckdb.connect(db_path)

    # 테이블 생성 (없으면)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS elderly_accident_summary (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        region VARCHAR,
        elderly_ratio DOUBLE,
        year INTEGER,
        month INTEGER,
        hour INTEGER,
        accident_count INTEGER
    );
    """
    con.execute(create_table_query)
    print("✅ 테이블 생성 완료 (DuckDB)")

    # 기존 데이터 삭제 (원한다면)
    con.execute("DELETE FROM elderly_accident_summary;")

    # 데이터 삽입
    con.execute("INSERT INTO elderly_accident_summary (region, elderly_ratio, year, month, hour, accident_count) SELECT * FROM df_all")
    print("✅ 데이터 삽입 완료 (DuckDB)")

    con.close()
    print("✅ DuckDB 연결 종료")

# 메인 실행 함수
def main():
    base_dir = "1_team_project/data"  # 엑셀 파일 위치
    year_files = {
        2020: "시도_시군구별_시간대별_노인_교통사고_2020.xls",
        2021: "시도_시군구별_시간대별_노인_교통사고_2021.xls",
        2022: "시도_시군구별_시간대별_노인_교통사고_2022.xls",
        2023: "시도_시군구별_시간대별_노인_교통사고_2023.xls",
        2024: "시도_시군구별_시간대별_노인_교통사고_2024.xls"
    }

    df_all_years = pd.DataFrame()

    for year, filename in year_files.items():
        file_path = os.path.join(base_dir, filename)
        df_year = process_year_file(file_path, year)
        df_all_years = pd.concat([df_all_years, df_year], ignore_index=True)

    print(f"📊 총 {len(df_all_years)}건 데이터 준비 완료")
    insert_to_duckdb(df_all_years)

if __name__ == "__main__":
    main()