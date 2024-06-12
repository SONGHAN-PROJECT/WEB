import mysql
from datetime import datetime
from mysql.connector import pooling

# Connection pool 생성
dbconfig = {
    "host": 'localhost',
    "user": "root",
    "password": "Abc1301!",
    "database": "sh",
    "port": 3306
}

pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=10,
    **dbconfig
)

# Connection pool에서 연결 가져오기
def get_connection():
    return pool.get_connection()

def execute_query(operation, params=None):
    try:
        # 연결을 가져옴
        connection = get_connection()

        # 쿼리 수행
        cursor = connection.cursor(dictionary=True)

        if params:
            cursor.execute(operation, params)
        else:
            cursor.execute(operation)

        if str(operation).upper().startswith("SELECT"):
            results = cursor.fetchall()

        connection.commit()
        # 결과 출력


    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals():
            # 연결을 풀에 반환
            connection.close()

        if 'results' not in locals():
            results = None

        return results