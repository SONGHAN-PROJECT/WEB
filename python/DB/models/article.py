from __future__ import annotations

from datetime import datetime
from python.DB.database import get_connection
from python.DB.models.user import User
import logging
import traceback

class Article:
    def __init__(self, post_id: int, title: str, content: str, user_id: int, created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at.strftime("%Y.%m.%d")
        self.updated_at = updated_at.strftime("%Y.%m.%d")

    @property
    def convert_json(result):
        return {
            "post_id": result.post_id,
            "title": result.title,
            "content": result.content,
            "user_id": User.load_username_from_user_id(result.user_id),
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    @staticmethod
    def get_all_article(page: int = 1, count: int = 15):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM posts
                WHERE post_id BETWEEN {(page - 1) * count + 1} AND {page * count + 1}
                ORDER BY post_id ASC;
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return list(map(lambda x: {
                "post_id": x[0],
                "title": x[1],
                "username": User.load_username_from_user_id(x[3]),
                "created_at": x[4]
            }, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def search_article(search_value: str, page: int = 1, count: int = 15):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM posts
                WHERE title LIKE '%{search_value}%'
                AND  post_id BETWEEN {(page - 1) * count + 1} AND {page * count + 1}
                ORDER BY post_id ASC;
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return list(map(lambda x: {
                "post_id": x[0],
                "title": x[1],
                "username": User.load_username_from_user_id(x[3]),
                "created_at": x[4]
            }, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def get_max_page(search_value: str | None = None, count: int = 15):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM posts"
            if search_value:
                sql += f" WHERE title LIKE '%{search_value}%'"
            cursor.execute(sql + ";")

            cnt = cursor.fetchone()
            cursor.close()
            conn.close()
            return cnt[0] // count + 1

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def load_article_with_post_id(post_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM posts WHERE post_id={post_id};
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return Article(*results[0]).convert_json
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def insert_article(title: str, content: str, user_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO posts(title, content, user_id) VALUES ('{title}', '{content}', {user_id});
            """)
            results = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return len(results) is not None

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)