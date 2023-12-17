import tkinter as tk
from tkinter import filedialog, messagebox
from app_utils import show_login_form, show_admin_panel
import sqlite3
import base64
import hashlib
from PIL import Image, ImageTk
import io

class MainForm:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Головна форма")
        self.username = username  # Збереження імені користувача
        self.image_path = None
        self.selected_image_username = None
        self.photo_images = {}
        self.label_welcome = tk.Label(master, text=f"Ласкаво просимо, {username}!", font=("Helvetica", 16))
        self.label_welcome.pack(pady=20)

        self.label_image = tk.Label(master)
        self.label_image.pack(pady=10)

        self.button_add_image = tk.Button(master, text="Додати зображення", command=self.choose_image)
        self.button_add_image.pack(pady=10)

        self.button_save_image = tk.Button(master, text="Зберегти зображення", command=self.save_image)
        self.button_save_image.pack(pady=10)

        self.button_view_images = tk.Button(master, text="Переглянути зображення", command=self.view_images)
        self.button_view_images.pack(pady=10)

        self.button_logout = tk.Button(master, text="Вийти", command=self.logout)
        self.button_logout.pack(pady=10)

        # Додайте кнопку "Адміністраторська панель"
        if username == "admin":
            self.button_admin_panel = tk.Button(master, text="Адміністраторська панель", command=self.open_admin_panel)
            self.button_admin_panel.pack(pady=10)

        # Відображення зображення при старті форми
        self.update_image()

    def logout(self):
        self.master.destroy()  # Закрити головну форму
        show_login_form()      # Показати форму авторизації

    def open_admin_panel(self):
        show_admin_panel()

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path
            self.update_image()

    def update_image(self):
        if self.image_path:
            try:
                image = tk.PhotoImage(file=self.image_path)
                self.label_image.configure(image=image)
                self.label_image.image = image  # Зберегіть посилання на зображення
            except tk.TclError:
                messagebox.showerror("Помилка", "Не вдалося завантажити зображення. Будь ласка, виберіть інше зображення.")

    def save_image(self):
        if self.image_path:
            username = self.username  # Вам потрібно визначити користувача, для якого зберігається зображення
            if not self.check_duplicate_images(username, self.image_path):
                if self.save_image_to_database(username, self.image_path):
                    messagebox.showinfo("Успіх", "Зображення успішно збережено.")
                else:
                    messagebox.showerror("Помилка", "Не вдалося зберегти зображення.")
            else:
                messagebox.showinfo("Повідомлення", "Це зображення вже збережено.")
        else:
            messagebox.showinfo("Помилка", "Будь ласка, виберіть зображення для збереження.")

    def save_image_to_database(self, username, image_path):
        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            conn = sqlite3.connect('images.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO images (username, image_data) VALUES (?, ?)', (username, encoded_image))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def check_duplicate_images(self, username, new_image_path):
        new_image_hash = self.calculate_image_hash(new_image_path)

        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        cursor.execute('SELECT image_data FROM images WHERE username=?', (username,))
        stored_images = cursor.fetchall()
        conn.close()

        for stored_image in stored_images:
            stored_image_data = stored_image[0]
            stored_image_hash = hashlib.md5(base64.b64decode(stored_image_data)).hexdigest()

            if new_image_hash == stored_image_hash:
                return True  # Знайдено однакове зображення

        return False  # Однакових зображень не знайдено

    def calculate_image_hash(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                return hashlib.md5(image_data).hexdigest()
        except Exception as e:
            print(f"Error calculating image hash: {e}")
            return None

    def view_images(self):
        image_viewer = tk.Toplevel(self.master)
        image_viewer.title("Перегляд зображень")

        listbox_images = tk.Listbox(image_viewer)
        listbox_images.pack(pady=20)

        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, image_data FROM images')
        images = cursor.fetchall()
        conn.close()

        for image in images:
            username = image[0]
            listbox_images.insert(tk.END, f"Користувач: {username}")

        view_button = tk.Button(image_viewer, text="Переглянути вибране зображення", command=lambda: self.view_image(listbox_images.get(listbox_images.curselection())))
        view_button.pack(pady=5)

    def view_image(self, selected_item):
     if selected_item:
        username = selected_item.split(": ")[1]
        image_viewer = tk.Toplevel(self.master)
        image_viewer.title("Перегляд зображення")

        conn = sqlite3.connect('images.db')
        cursor = conn.cursor()
        cursor.execute('SELECT image_data FROM images WHERE username=?', (username,))
        image_data_list = cursor.fetchall()
        conn.close()

        for i, image_data in enumerate(image_data_list):
            # Декодуємо base64 та створюємо об'єкт ImageTk.PhotoImage
            image = ImageTk.PhotoImage(Image.open(io.BytesIO(base64.b64decode(image_data[0]))))
            self.photo_images[f"{username}_{i}"] = image  # Зберегти PhotoImage для даного користувача

            label = tk.Label(image_viewer, image=image)
            label.image = image
            label.pack(pady=20)

    def select_image(self, selected_item):
        if selected_item:
            self.selected_image_username = selected_item.split(": ")[1]

    def find_duplicates(self):
        if hasattr(self, 'selected_image_username') and self.selected_image_username:
            conn = sqlite3.connect('images.db')
            cursor = conn.cursor()
            cursor.execute('SELECT username, image_data FROM images WHERE username!=?', (self.selected_image_username,))
            images = cursor.fetchall()
            conn.close()

            selected_image_data = None
            for image in images:
                username, image_data = image
                if not selected_image_data:
                    # Декодуємо та зберігаємо дані для вибраного зображення
                    selected_image_data = (username, Image.open(io.BytesIO(base64.b64decode(image_data))))
                    continue

                # Декодуємо та порівнюємо дані
                current_image_data = Image.open(io.BytesIO(base64.b64decode(image_data)))
                if self.compare_images(selected_image_data[1], current_image_data):
                    messagebox.showinfo("Однакові зображення", f"Зображення користувачів {selected_image_data[0]} та {username} ідентичні.")
                else:
                    messagebox.showinfo("Різні зображення", f"Зображення користувачів {selected_image_data[0]} та {username} різні.")

    def compare_images(self, image1, image2):
        # Додайте ваш алгоритм порівняння зображень тут
        # Наприклад, можна порівнювати хеші зображень, як у попередньому прикладі
        hash1 = hashlib.md5(image1.tobytes()).hexdigest()
        hash2 = hashlib.md5(image2.tobytes()).hexdigest()
        return hash1 == hash2
    

if __name__ == "__main__":
    root = tk.Tk()
    MainForm(root, "example_user")
    root.mainloop()