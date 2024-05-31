import mysql.connector
from aiogram import Dispatcher
from mysql.connector import Error

from aiogram import Bot, Dispatcher, executor, types
from config import db_host, db_user, db_pass, db_data, db_port
from config import TOKEN


# Настройка бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


#Подключение к MySql к базе данных 
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_data,
            port=db_port
        )
        if connection.is_connected():
            print("[OK] Подключена database US_ID")
        return connection
    except mysql.connector.Error as err:
        print(f"[Ошибка] {err}")
        return None


#Обработка user_id
def insert_user(user_id):
    connection = create_connection()
    if connection is None:
        return "[Ошибка] Не удалось подключиться к базе данных"
    
    # Добавление пользывателя в табилцу 
    try:
        cursor = connection.cursor()
        query = "INSERT INFO users (user_id) VALUES (%S)"
        cursor.execute(query, (user_id))
        connection.commit()
        return "[OK] Добавлен новый лох"
    except Error as err:
        print(f"[Ошибка] {err}")
        return f"[Ошибка] {err}" 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    response = insert_user(user_id)
    await message.reply(response)

#Пока добей ту часть которая связанна с ботом тут просто запуск остался, я курить 

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
