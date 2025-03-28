from datetime import datetime, timedelta
from logging import Logger
import sqlite3

from logger_config import get_logger

logger: Logger = get_logger(name='Data layer')


class SqlManager:

    def __init__(self, db_path='sqlite.db') -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(database=db_path)
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.db_path: str = db_path

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        logger.info('Close DB')
        self.conn.close()

    def add_issue(self, title: str,
                  description: str,
                  screenshot: int,
                  username: str,
                  jira: bool = False,
                  ) -> None:
        """Вставляет новую запись в таблицу issues"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_insert_issue = """
        INSERT INTO issues (title, description, screenshot, jira, date_created, username)
        VALUES (?, ?, ?, ?, ?, ?);
    """
        values = (title, description, screenshot, jira, current_date, username)
        try:
            self.cursor.execute(sql_insert_issue, values)
            self.conn.commit()
            print("Новая запись успешно добавлена.")
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении записи: {e}")

    def add_chat(self, chat_id) -> None:
        """Добавляет чат в базу данных с текущей датой."""
        current_date: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query: str = f"""
            INSERT OR IGNORE INTO chats (chat_id, date_added)
            VALUES ({chat_id}, '{current_date}')
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f'Запись с chat_id {chat_id} успешно добавлена.')
            else:
                print(f'Запись с chat_id {chat_id} уже существует.')
        except sqlite3.Error as e:
            print(f'Ошибка при добавлении записи: {e}')

    def check_table_exists(self, table_name: str) -> bool:
        """Проверяет существование таблицы в базе данных"""
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        result = self.cursor.fetchone()
        if result is None:
            return False
        else:
            return True

    def create_chats_table(self) -> None:
        """Создает таблицу chats, если она не существует"""
        sql_create_chats_table = """
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER UNIQUE NOT NULL,
                date_added TEXT NOT NULL
            );
        """
        try:
            self.cursor.execute(sql_create_chats_table)
            self.conn.commit()
            print("Таблица 'chats' успешно создана.")
        except sqlite3.Error as e:
            print(e)

    def create_issues_table(self) -> None:
        """Создает таблицу issues, если она не существует"""
        sql_create_issues_table = """
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                screenshot INTEGER,
                jira BOOLEAN DEFAULT FALSE,
                date_created TEXT NOT NULL,
                username TEXT NOT NULL,
                jira_issues_url TEXT DEFAULT NULL  -- Указываем тип данных (например, TEXT)
            );
        """
        try:
            self.cursor.execute(sql_create_issues_table)
            self.conn.commit()
            print("Таблица 'issues' успешно создана.")
        except sqlite3.Error as e:
            print(e)

    def get_all_chat_ids(self):
        """Извлекает все chat_id из таблицы chats."""
        query = "SELECT chat_id FROM chats;"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print(f'Ошибка при получении chat_id: {e}')
            return []

    def get_last_month_issues(self):
        """Извлекает столбцы title, username, date_created из таблицы issues за последний месяц."""
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        query = """
            SELECT title, username, date_created
            FROM issues
            WHERE date_created >= ?
            ORDER BY date_created DESC;
        """
        try:
            self.cursor.execute(query, (one_month_ago,))
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f'Ошибка при получении данных: {e}')
            return []


def main():
    db = SqlManager()
    # Проверяем, существует ли таблица
    if not db.check_table_exists(table_name='chats'):
        db.create_chats_table()
    else:
        print("Таблица 'chats' уже существует.")
    if not db.check_table_exists(table_name='issues'):
        db.create_issues_table()
    else:
        print("Таблица 'issues' уже существует.")
    db.close()


if __name__ == '__main__':
    main()
