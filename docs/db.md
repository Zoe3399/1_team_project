## DuckDB (분석/모델링 DB)
<details>
<summary>주요 테이블 및 기능</summary>
- 대용량 데이터 분석 및 모델 학습/예측 데이터 저장
- accident_summary : 지역별, 시간대별, 고령자 사고 집계
- elderly_ratio : 지역별 고령자 비율
- accident_type_summary : 사고 유형별 요약
- pedestrian_accident : 보행자 사고 상세
- 그 외 추가 분석용 테이블
</details>

----
## PostgreSQL (웹 서비스 DB)
<details>
<summary>주요 테이블 및 기능</summary>
- 웹 서비스 회원, 비회원, 관리자 정보 관리
- 로그인 및 인증 이력 관리
- region : 행정구역 및 위치(위경도) 정보
- accident_prediction : 예측 결과 저장
- download_log : 데이터 다운로드 이력
- 기타 서비스 운영 테이블
</details>
