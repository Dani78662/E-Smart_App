import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .base_gui import BaseGUI
from models.admin_model import Admin
from models.cashier_model import Cashier

class LoginGUI(BaseGUI):
    def __init__(self, on_admin_login: Optional[Callable[[str, str], None]] = None,
                 on_cashier_login: Optional[Callable[[str, str], None]] = None):
        super().__init__("Login")
        self.on_admin_login = on_admin_login
        self.on_cashier_login = on_cashier_login
        
        # Create centered login form
        main_frame = ttk.Frame(self.main_container)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Welcome section
        welcome_frame = ttk.Frame(main_frame)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(welcome_frame, 
                 text="Welcome to Smart Mart",
                 style='Header.TLabel',
                 font=('Segoe UI', 24, 'bold')).pack()
                 
        ttk.Label(welcome_frame,
                 text="Please login to continue",
                 font=('Segoe UI', 12)).pack()
        
        # Login form
        form_frame = ttk.Frame(main_frame, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style for radio buttons
        style = ttk.Style()
        style.configure('Login.TRadiobutton',
                       font=('Segoe UI', 10),
                       padding=5)
        
        # Login type selection with better spacing
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill=tk.X, pady=10)
        
        self.login_type = tk.StringVar(value="admin")
        ttk.Radiobutton(type_frame,
                       text="Administrator",
                       variable=self.login_type,
                       value="admin",
                       style='Login.TRadiobutton').pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame,
                       text="Cashier",
                       variable=self.login_type,
                       value="cashier",
                       style='Login.TRadiobutton').pack(side=tk.LEFT, padx=10)
        
        # Username and password fields with icons
        self.username_entry = self.create_entry_field(form_frame, "Username:")
        self.password_entry = self.create_entry_field(form_frame, "Password:", show="*")
        
        # Add some space before the login button
        ttk.Frame(form_frame).pack(pady=10)
        
        # Login button with custom style
        login_btn = self.create_button(form_frame, "Login", self.login)
        login_btn.configure(padding=[20, 10])
        
        # Error message
        self.error_var = tk.StringVar()
        error_label = ttk.Label(form_frame,
                              textvariable=self.error_var,
                              foreground=self.colors['danger'],
                              font=('Segoe UI', 10))
        error_label.pack(pady=10)
        
        # Version info
        ttk.Label(main_frame,
                 text="Smart Mart v1.0",
                 font=('Segoe UI', 8),
                 foreground=self.colors['gray']).pack(pady=10)
        
        # Bind enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus username entry
        self.username_entry.focus()

    def login(self):
        """Handle login attempt with improved feedback."""
        self.error_var.set("")  # Clear previous error
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username and not password:
            self.error_var.set("Please enter your username and password")
            self.username_entry.focus()
            return
        elif not username:
            self.error_var.set("Please enter your username")
            self.username_entry.focus()
            return
        elif not password:
            self.error_var.set("Please enter your password")
            self.password_entry.focus()
            return
            
        if self.login_type.get() == "admin":
            admin = Admin()
            if admin.login(username, password):
                if self.on_admin_login:
                    self.on_admin_login(username, password)
                self.close()
            else:
                self.error_var.set("Invalid administrator credentials")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        else:
            cashier = Cashier()
            if cashier.login(username, password):
                if self.on_cashier_login:
                    self.on_cashier_login(username, password)
                self.close()
            else:
                self.error_var.set("Invalid cashier credentials")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()

    def clear_error(self):
        """Clear the error message."""
        self.error_var.set("") 