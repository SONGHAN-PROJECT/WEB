from __future__ import annotations

import time
from datetime import datetime
from python.DB.database import get_connection
from python.DB.models.user import User
import logging
import traceback

class Article:
    def __init__(self, post_id: int, title: str, start_time: time, description:str):
        self.id = post_id
        self.title = title
        self.start_time = start_time
        self.description = description
        # self.image_url = image
        # self.user_id = user_id

    @property
    def convert_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time,
            "description": self.description
            # "image_url": self.image,
            # "user_id": self.user_id
        }

    @staticmethod
    def get_all_article(page: int = 1, count: int = 15):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                SELECT * FROM border
                ORDER BY start_time DESC;
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return list(map(lambda x: {
                "id": x[0],
                "title": x[1],
                "time": x[2]
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
                SELECT * FROM border
                WHERE title LIKE '%{search_value}%'
                AND  id BETWEEN {(page - 1) * count + 1} AND {page * count + 1}
                ORDER BY id ASC;
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return list(map(lambda x: {
                "id": x[0],
                "title": x[1]
            }, results))

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def get_max_page(search_value: str | None = None, count: int = 15):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "SELECT COUNT(*) FROM border"
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
                SELECT * FROM border WHERE id={post_id};
            """)

            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return Article(*results[0]).convert_json

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

    @staticmethod
    def insert_article(title: str, description: str):
        try:
            print(title+" "+description)
            conn = get_connection()
            cursor = conn.cursor()
            print('db업로드')
            cursor.execute(f"""
                INSERT INTO border(title, description) VALUES ('{title}','{description}');
             """)
            results = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            return 200

        except Exception as e:
            print("MySQL에서 에러가 발생했습니다:", e)