import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class AdminPanel:
    def __init__(self, master):
        self.master = master
        self.master.title("Адміністраторська панель")

        # Вхід у адміністраторську панель
        self.setup_admin_panel()

    def setup_admin_panel(self):
        self.listbox_users = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.listbox_users.pack(pady=20)

        self.button_view_users = tk.Button(self.master, text="Переглянути користувачів", command=self.view_users)
        self.button_view_users.pack(pady=5)

        self.button_delete_user = tk.Button(self.master, text="Видалити користувача", command=self.delete_user)
        self.button_delete_user.pack(pady=5)

        self.load_users()

    def load_users(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()

        for user in users:
            self.listbox_users.insert(tk.END, f"Логін: {user[1]}, Пароль: {user[2]}")

    def view_users(self):
        selected_index = self.listbox_users.curselection()
        if selected_index:
            selected_user = self.listbox_users.get(selected_index)
            messagebox.showinfo("Користувач", selected_user)
        else:
            messagebox.showinfo("Помилка", "Виберіть користувача зі списку")

    def delete_user(self):
        selected_index = self.listbox_users.curselection()
        if selected_index:
            response = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цього користувача?")
            if response == tk.YES:
                user_to_delete = self.listbox_users.get(selected_index)
                login_to_delete = user_to_delete.split(",")[0].split(":")[1].strip()
                self.remove_user_from_database(login_to_delete)
                self.listbox_users.delete(selected_index)
                messagebox.showinfo("Успіх", "Користувача видалено")
        else:
            messagebox.showinfo("Помилка", "Виберіть користувача зі списку")

    def remove_user_from_database(self, login):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username=?', (login,))
        conn.commit()
        conn.close()