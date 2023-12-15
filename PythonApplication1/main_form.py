import tkinter as tk
from tkinter import filedialog, messagebox
from app_utils import show_login_form, show_admin_panel

class MainForm:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Головна форма")

        self.image_path = None

        self.label_welcome = tk.Label(master, text=f"Ласкаво просимо, {username}!", font=("Helvetica", 16))
        self.label_welcome.pack(pady=20)

        self.label_image = tk.Label(master)
        self.label_image.pack(pady=10)

        self.button_add_image = tk.Button(master, text="Додати зображення", command=self.choose_image)
        self.button_add_image.pack(pady=10)

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