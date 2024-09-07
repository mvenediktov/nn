import sqlite3
from config import DATABASE
import pandas as pd
skills = [ (_,) for _ in (['Python', 'SQL', 'API', 'Telegram'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        with conn:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                teacher TEXT NOT NULL,
                classroom TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                grade_level INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            cursor.executescript('''
                INSERT INTO schedule (subject, teacher, classroom, day_of_week, start_time, end_time, grade_level) VALUES
                ('python', 'Иванов И.И.', '101', 'Понедельник', '08:30', '09:15', 5),
                ('java', 'Петрова А.А.', '102', 'Понедельник', '09:30', '10:15', 5),
                ('1C', 'Сидоров С.С.', '203', 'Понедельник', '10:30', '11:15', 6),
                ('java', 'Семенова К.К.', '204', 'Понедельник', '11:30', '12:15', 7),
                ('1C', 'Петров В.В.', '105', 'Понедельник', '12:30', '13:15', 8),
                ('python', 'Николаева Л.П.', '106', 'Вторник', '08:30', '09:15', 7),
                ('java', 'Александров А.А.', '107', 'Вторник', '09:30', '10:15', 8),
                ('1C', 'Кузнецов В.В.', '108', 'Вторник', '10:30', '11:15', 6),
                ('python', 'Рыбаков И.И.', 'Спортзал', 'Вторник', '11:30', '12:15', 5),
                ('java', 'Сурков Н.Н.', '202', 'Среда', '08:30', '09:15', 6),
                ('1C', 'Дворникова Е.Е.', '201', 'Среда', '09:30', '10:15', 7),
                ('python', 'Иванов И.И.', '101', 'Среда', '10:30', '11:15', 8),
                ('java', 'Петрова А.А.', '102', 'Среда', '11:30', '12:15', 5),
                ('1C', 'Сидорова О.О.', '103', 'Четверг', '08:30', '09:15', 6),
                ('python', 'Семенова К.К.', '203', 'Четверг', '09:30', '10:15', 7),
                ('java', 'Петров В.В.', '204', 'Четверг', '10:30', '11:15', 8),
                ('1C', 'Николаев Д.Д.', '105', 'Четверг', '11:30', '12:15', 5),
                ('python', 'Александрова Т.Т.', '106', 'Пятница', '08:30', '09:15', 6),
                ('java', 'Кузнецов И.И.', '107', 'Пятница', '09:30', '10:15', 7),
                ('1C', 'Сурков Н.Н.', '108', 'Пятница', '10:30', '11:15', 5),
                ('python', 'Рыбаков Н.Н.', 'Спортзал', 'Пятница', '11:30', '12:15', 8);
                ''')
            conn.commit()
           
        print("База данных успешно создана.")

        # Извлекаем данные из таблицы
        df = pd.read_sql_query('SELECT * FROM schedule', conn)

        # Закрываем соединение с базой данных
        conn.close()

        # Выводим данные в виде таблицы
        print(df)

    # Вызов функции

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.default_insert()
