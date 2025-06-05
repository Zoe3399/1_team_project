from sqlalchemy import text
import bcrypt
from db import engine

def insert_user():
    try:
        email = "test_insert@sample.com"
        plain_pw = "sample1234"
        user_type = "테스트"
        purpose = "테스트 삽입"

        # 비밀번호 bcrypt 해시
        hashed_pw = bcrypt.hashpw(plain_pw.encode("utf-8"), bcrypt.gensalt()).decode()

        # 이미 존재하면 삭제 (테스트 반복을 위해)
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM users WHERE email = :e"), {"e": email})

        # INSERT
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO users (password, email, user_type, purpose)
                    VALUES (:p, :e, :t, :pu)
                    RETURNING id
                """),
                {"p": hashed_pw, "e": email, "t": user_type, "pu": purpose}
            )
            new_id = result.scalar()
            print(f"삽입 완료! 새 user id: {new_id}")

        # SELECT로 바로 확인
        # SELECT로 바로 확인
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT id, email, user_type, purpose FROM users WHERE id = :id"),
                {"id": new_id}
            ).fetchone()
            if row:
                print("DB 저장 확인:", dict(row._mapping))
            else:
                print("저장된 데이터가 조회되지 않습니다!")
    except Exception as e:
        print(f"예외 발생: {e}")

if __name__ == "__main__":
    insert_user()