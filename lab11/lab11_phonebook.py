import psycopg2

conn = psycopg2.connect(
    dbname="lab10", 
    user="postgres", 
    password="AkhmetMK07", 
    host="localhost", 
    port="5432", 
    client_encoding="UTF8"
)

cur = conn.cursor()

pattern = input("Введите шаблон для поиска: ")
cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
print(cur.fetchall())

name = input("Введите имя пользователя: ")
phone = input("Введите номер телефона: ")
cur.execute("CALL add_or_update_user(%s, %s)", (name, phone))

names = ['John', 'Alice']
phones = ['+1234567890', '+0987654321']
cur.execute("CALL add_multiple_users(%s, %s)", (names, phones))

limit = 5
offset = 0
cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
print(cur.fetchall())

delete_value = input("Введите имя или номер для удаления: ")
cur.execute("CALL delete_user_or_phonebook_entry(%s)", (delete_value,))

conn.commit()
cur.close()
conn.close()