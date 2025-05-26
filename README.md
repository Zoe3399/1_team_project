# 1_team_project
[이스트캠프 AI모델 개발자과정] 1차 1조 팀 프로젝트 깃허브 입니다.

<details> <summary><strong>📁 파일 구조 보기</strong></summary>

📁 1_team_project/ <br>
│ <br>
├── data/                       # 데이터 저장 폴더 <br>
│   ├── raw/                   # 원본 데이터 (CSV, XLS 등)  <br>
│   ├── processed/             # 전처리된 데이터 <br>
│   └── external/              # 캐글 등 외부 참조 데이터 <br>
│ <br>
├── notebooks/                 # 분석 및 실험용 Jupyter 노트북 <br>
│   ├── 01_eda.ipynb           # EDA 및 시각화 <br>
│   ├── 02_preprocessing.ipynb # 데이터 전처리 <br>
│   ├── 03_modeling.ipynb      # 모델링 및 성능 평가 <br>
│   └── 04_visualization.ipynb # 지도 시각화 등 <br>
│ <br>
├── src/                       # 실제 코드 모듈 (함수 단위로 분리) <br>
│   ├── __init__.py <br>
│   ├── preprocess.py          # 전처리 함수 모듈 <br>
│   ├── model.py               # 모델 학습 및 예측 코드 <br>
│   ├── evaluate.py            # 성능 평가 함수 <br>
│   └── map_visualizer.py      # 지도 시각화 함수 <br>
│ <br>
├── outputs/                   # 결과물 저장 <br>
│   ├── figures/               # 시각화 이미지 (heatmap 등) <br>
│   └── reports/               # 결과 보고서, 발표자료 <br>
│ <br>
├── docs/                      # 문서 및 보고서 관련 파일 <br>
│   ├── proposal.md            # 프로젝트 기획안 <br>
│   └── report_final.md        # 최종 결과 리포트 <br>
│ <br>
├── README.md                  # 프로젝트 개요 및 실행 방법 안내 <br>
├── requirements.txt           # 필요한 패키지 목록 <br>
└── .gitignore                 # Git에서 제외할 파일 설정 <br>

</details>
