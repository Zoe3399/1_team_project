# 1_team_project
[이스트캠프 AI모델 개발자과정] 1차 1조 팀 프로젝트 깃허브 입니다.

[ 파일 구조 ]
├── 📁 data/ # 데이터 저장 폴더
│ ├── raw/ # 원본 데이터 (CSV, XLS 등)
│ ├── processed/ # 전처리된 데이터
│ └── external/ # 캐글 등 외부 참조 데이터
│
├── 📁 notebooks/ # 분석 및 실험용 Jupyter 노트북
│ ├── 01_eda.ipynb # EDA 및 시각화
│ ├── 02_preprocessing.ipynb # 데이터 전처리
│ ├── 03_modeling.ipynb # 모델링 및 성능 평가
│ └── 04_visualization.ipynb # 지도 시각화 등
│
├── 📁 src/ # 실제 코드 모듈
│ ├── init.py
│ ├── preprocess.py # 전처리 함수 모듈
│ ├── model.py # 모델 학습 및 예측 코드
│ ├── evaluate.py # 성능 평가 함수
│ └── map_visualizer.py # 지도 시각화 함수
│
├── 📁 outputs/ # 결과물 저장
│ ├── figures/ # 시각화 이미지
│ └── reports/ # 결과 보고서, 발표자료
│
├── 📁 docs/ # 문서 및 보고서 관련 파일
│ ├── proposal.md # 프로젝트 기획안
│ └── report_final.md # 최종 결과 리포트
│
├── README.md # 프로젝트 개요
├── requirements.txt # 필요한 패키지 목록
├── .gitignore # Git에서 제외할 파일 설정
