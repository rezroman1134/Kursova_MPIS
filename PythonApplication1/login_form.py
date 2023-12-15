import tkinter as tk
from tkinter import messagebox
import sqlite3
from app_utils import show_main_form

class LoginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизація та реєстрація")

        self.label_username = tk.Label(master, text="Логін:")
        self.label_password = tk.Label(master, text="Пароль:")

        self.entry_username = tk.Entry(master)
        self.entry_password = tk.Entry(master, show="*")

        self.button_login = tk.Button(master, text="Увійти", command=self.login)
        self.button_register = tk.Button(master, text="Зареєструватися", command=self.register)

        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        self.button_login.grid(row=2, column=1, pady=10)
        self.button_register.grid(row=3, column=1, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if validate_login(username, password):
            messagebox.showinfo("Успіх", "Авторизація пройшла успішно!")
            self.master.destroy()  # Закрити форму авторизації
            show_main_form(username)
        else:
            messagebox.showerror("Помилка", "Неправильний логін або пароль")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            add_user(username, password)
            messagebox.showinfo("Успіх", "Реєстрація пройшла успішно!")
        else:
            messagebox.showerror("Помилка", "Будь ласка, введіть логін та пароль")

def validate_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()