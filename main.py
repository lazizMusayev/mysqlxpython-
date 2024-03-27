import mysql.connector
import hashlib

# Подключение к базе данных MySQL
conn = mysql.connector.connect(
    host="127.0.0.1 ",
    user="root",
    password="",
    database="projectx"
)
cursor = conn.cursor()

# Создание таблицы users
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20) UNIQUE, password VARCHAR(8))''')

def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if user:
        print("Пользователь с таким именем уже существует")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        print("Пользователь зарегистрирован")

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
    user = cursor.fetchone()
    if user:
        print(f"Добро пожаловать, {username}!")
    else:
        print("Неправильное имя пользователя или пароль")

def view_all_users():
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    for user in all_users:
        print(user)

while True:
    print("\nМеню:")
    print("1. Регистрация")
    print("2. Логин")
    print("3. Просмотр всех зарегистрированных пользователей")
    print("4. Выход")

    choice = input("Выберите действие: ")

    if choice == '1':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        register_user(username, password)

    elif choice == '2':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        login_user(username, password)

    elif choice == '3':
        view_all_users()

    elif choice == '4':
        conn.close()
        break

    else:
        print("Неверный выбор. Попробуйте снова.")
