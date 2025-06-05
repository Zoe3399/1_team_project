# test_insert_fetch.py
from sqlalchemy import text
from db import engine
import random
import string

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_insert_and_fetch():
    test_username = "test_user_" + random_string()
    test_email = test_username + "@example.com"
    test_password = "password123"
    test_user_type = "테스트유저"
    
    print(f"Inserting user: {test_username}, email: {test_email}")
    
    with engine.begin() as conn:
        insert_stmt = text("""
            INSERT INTO users (username, password, email, user_type)
            VALUES (:u, :p, :e, :t)
            RETURNING id
        """)
        inserted_id = conn.execute(
            insert_stmt, 
            {"u": test_username, "p": test_password, "e": test_email, "t": test_user_type}
        ).scalar()
    
    print(f"Inserted with ID: {inserted_id}")
        
    with engine.connect() as conn:
        fetch_stmt = text("""
            SELECT id, username, email, user_type, created_at, is_active
            FROM users
            WHERE id = :id
        """)
        result = conn.execute(fetch_stmt, {"id": inserted_id}).fetchone()
        
    print("Fetched row:", result)
        
    with engine.begin() as conn:
        delete_stmt = text("""
            DELETE FROM users WHERE id = :id
        """)
        conn.execute(delete_stmt, {"id": inserted_id})
        
    print(f"Deleted test user ID: {inserted_id}")