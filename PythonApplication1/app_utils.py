
import tkinter as tk

def show_login_form():
    from login_form import LoginForm
    root = tk.Tk()
    LoginForm(root)

def show_main_form(username):
    from main_form import MainForm
    main_form = tk.Tk()
    MainForm(main_form, username)

def show_admin_panel():
    from admin_panel import AdminPanel
    admin_panel = tk.Tk()
    AdminPanel(admin_panel)