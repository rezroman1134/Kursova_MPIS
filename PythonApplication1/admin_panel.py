import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk

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

        # Додайте кнопку для видалення зображень
        self.button_delete_image = tk.Button(self.master, text="Видалити зображення", command=self.delete_image)
        self.button_delete_image.pack(pady=5)

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

    def delete_image(self):
        # Відкрийте нове вікно для видалення зображень
        image_deletion_window = tk.Toplevel(self.master)
        image_deletion_window.title("Видалення зображень")

        listbox_images = tk.Listbox(image_deletion_window)
        listbox_images.pack(pady=20)

        self.load_images(listbox_images)

        delete_button = tk.Button(image_deletion_window, text="Видалити обране зображення", command=lambda: self.delete_selected_image(listbox_images))
        delete_button.pack(pady=5)

    def load_images(self, listbox):
        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, image_data FROM images')
        images = cursor.fetchall()
        conn.close()

        for image in images:
            username = image[0]
            listbox.insert(tk.END, f"Користувач: {username}")

    def delete_selected_image(self, listbox):
        selected_index = listbox.curselection()
        if selected_index:
            response = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити це зображення?")
            if response == tk.YES:
                selected_image = listbox.get(selected_index)
                username_to_delete = selected_image.split(": ")[1]
                self.remove_image_from_database(username_to_delete)
                listbox.delete(selected_index)
                messagebox.showinfo("Успіх", "Зображення видалено")
        else:
            messagebox.showinfo("Помилка", "Виберіть зображення зі списку")

    def remove_image_from_database(self, username):
        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM images WHERE username=?', (username,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    AdminPanel(root)
    root.mainloop()