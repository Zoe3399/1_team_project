from db import engine
from sqlalchemy import text  # ← 추가!

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database(), current_schema()"))  # ← text()로 감싸기
    print("현재 연결 DB, 스키마:", result.fetchone())