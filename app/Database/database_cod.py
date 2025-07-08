import psycopg
import os

from contextlib import contextmanager

# Настройки подключения к PostgreSQL (замените на свои)
DB_CONFIG = {
    "host": "192.168.0.101",
    "port": 5432,
    "user": os.getenv("DB_USER").strip(),
    "password": os.getenv("DB_PASSWORD").strip(),
    "dbname": os.getenv("DB_USER").strip()
}

@contextmanager
def get_db_connection():
    """Контекстный менеджер для автоматического закрытия соединения"""
    conn = None
    try:
        conn = psycopg.connect(**DB_CONFIG)
        yield conn
    except:
        print(f"Database connection error")
        raise
    finally:
        if conn is not None:
            conn.close()

@contextmanager
def get_db_cursor(conn):
    """Контекстный менеджер для курсора"""
    cursor = None
    try:
        cursor = conn.cursor()
        yield cursor
    finally:
        if cursor is not None:
            cursor.close()

def input_all_lines_db(id_user: int, tag: str, topic: str, text: str):
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "INSERT INTO db_memory (id_user, tag, topic, text) VALUES (%s, %s, %s, %s)",
                (id_user, tag, topic, text)
            )
            conn.commit()

def tag_output_db(id_user: int):
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cursor:
            cursor.execute(
                "SELECT DISTINCT tag FROM db_memory WHERE id_user = %s",
                (id_user,)
            )
            return [tag[0] for tag in cursor.fetchall()]

def topic_output_db(id_user: int, tag: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT topic FROM db_memory WHERE id_user = %s AND tag = %s",
                (id_user, tag)
            )
            return [item[0] for item in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
        
def text_topic_output_db(id_user: int, topic: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT text FROM db_memory WHERE id_user = %s AND topic = %s",
                (id_user, topic)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
            conn.close()

def checking_the_availability_db(id_user: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM db_memory WHERE id_user = %s",
                (id_user,)
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

def del_last_commit_db(id_user: int, topic: str):
    with get_db_connection() as conn:  
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM db_memory WHERE id_user = %s AND topic = %s",
                (id_user, topic)
            )
            conn.commit()
        finally:
            cursor.close()