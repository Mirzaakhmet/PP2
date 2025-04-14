import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="lab10",        # Имя базы в pgAdmin
    user="postgres",       # Пользователь
    password="AkhmetMK07",  # Пароль
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Создание таблицы phonebook
cur.execute('''
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        phone VARCHAR(20)
    );
''')

conn.commit()
print("Таблица phonebook создана!")


def insert_from_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("Данные из CSV добавлены!")


insert_from_csv("contacts.csv")


def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите номер: ")
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Контакт добавлен!")


def update_user(old_name, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, new_name or old_name))
    conn.commit()
    print("Контакт обновлён!")


def search(filter_text):
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s OR phone ILIKE %s", (f"%{filter_text}%", f"%{filter_text}%"))
    for row in cur.fetchall():
        print(row)


def delete_user(value):
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (value, value))
    conn.commit()
    print("Контакт удалён!")
