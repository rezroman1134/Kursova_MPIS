import tkinter as tk
from login_form import LoginForm

if __name__ == "__main__":
    root = tk.Tk()
    LoginForm(root)
    root.mainloop()
    import sqlite3

# Підключення до бази даних або створення нової, якщо не існує
conn = sqlite3.connect('images.db')

# Створення курсора для виконання SQL-запитів
cursor = conn.cursor()

# SQL-запит для створення таблиці images
create_table_query = '''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    image_data TEXT NOT NULL
);
'''

# Виконання SQL-запиту
cursor.execute(create_table_query)

# Збереження змін та закриття підключення
conn.commit()
conn.close()