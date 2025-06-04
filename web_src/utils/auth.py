def login_check(username, password):
    USERS = {
        "admin": "1234",
        "user1": "abcd"
    }
    return USERS.get(username) == password