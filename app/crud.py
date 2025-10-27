from app.db import get_connection

def add_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("User added successfully!")
    except Exception as e:
        print("Error adding user:", e)
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()
    return user
