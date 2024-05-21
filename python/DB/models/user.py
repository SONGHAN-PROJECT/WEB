from datetime import datetime
from python.DB.database import get_connection
from hashlib import sha256
import logging
import traceback

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str, created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = sha256(password.encode()).hexdigest()
        self.created_at = created_at.strftime("%Y.%m.%d")
        self.updated_at = updated_at.strftime("%Y.%m.%d")

    @property
    def convert_json(result):
        return {
            "user_id": result.user_id,
            "username": result.username,
            "email": result.email,
            "password": result.password,
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    @staticmethod
    def load_all_user():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM users;
            """)

            results = cursor.fetchall()
            return list(map(lambda x: User(*x).convert_json, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def load_username_from_user_id(user_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT username FROM users WHERE user_id={user_id};
            """)

            results = cursor.fetchall()
            return results[0][0]
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_user(username: str, email: str, password: str):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            hash_password = sha256(password.encode()).hexdigest()
            cursor.execute(f"""
                INSERT INTO users(username, email, password_hash) VALUES ('{username}', '{email}', '{hash_password}');
            """)
            results = cursor.fetchall()
            conn.commit()
            return len(results) is not None

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()