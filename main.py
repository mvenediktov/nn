import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATABASE = 'school_schedule.db'  # Имя файла базы данных
TOKEN = '6814221477:AAFXzt2ewSqXueRuNswmnYA2p6Ya6Sc2iY8'  # Замените своем токеном бота

class DB_Manager:
    def __init__(self, database):
        self.database = database
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            teacher TEXT NOT NULL,
            classroom TEXT NOT NULL,
            day_of_week TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()
        print("База данных успешно создана.")

    def add_lesson(self, subject, teacher, classroom, day_of_week, start_time, end_time):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO lessons (subject, teacher, classroom, day_of_week, start_time, end_time) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (subject, teacher, classroom, day_of_week, start_time, end_time))
        conn.commit()
        conn.close()

    def fetch_lessons(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons")
        rows = cursor.fetchall()
        conn.close()
        return rows

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для управления расписанием уроков.\n" 
                                      "Используйте /add_lesson для добавления урока и /lessons для просмотра расписания.")

async def add_lesson_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 6:
        await update.message.reply_text("Используйте: /add_lesson <предмет> <учитель> <кабинет> <день> <начало> <конец>")
    else:
        subject, teacher, classroom, day_of_week, start_time, end_time = context.args
        manager.add_lesson(subject, teacher, classroom, day_of_week, start_time, end_time)
        await update.message.reply_text("Урок успешно добавлен!")

async def lessons_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lessons_data = manager.fetch_lessons()

    if not lessons_data:
        await update.message.reply_text("Расписание пустое.")
        return

    message = "Расписание уроков:\n"
    for row in lessons_data:
        message += f"{row[4]}: {row[1]} - {row[0]} в аудитории {row[3]} " \
                   f"({row[5]} - {row[6]})\n"
    await update.message.reply_text(message)

def main():
    global manager  # Объявляем глобальную переменную для доступа в других функциях
    manager = DB_Manager(DATABASE)

    # Инициализация бота
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("add_lesson", add_lesson_command))
    app.add_handler(CommandHandler("lessons", lessons_command))

    app.run_polling()

if __name__ == '__main__':
    main()
