import tkinter as tk
from views.login_gui import LoginGUI
from views.admin_gui import AdminGUI
from views.cashier_gui import CashierGUI

class SmartMart:
    def __init__(self):
        self.current_window = None
        self.show_login()

    def show_login(self):
        """Show the login screen."""
        if self.current_window:
            self.current_window.close()
            
        self.current_window = LoginGUI(
            on_admin_login=self.show_admin_panel,
            on_cashier_login=self.show_cashier_panel
        )
        self.current_window.run()

    def show_admin_panel(self, username: str, password: str):
        """Show the admin panel."""
        if self.current_window:
            self.current_window.close()
            
        self.current_window = AdminGUI(on_logout=self.show_login)
        self.current_window.run()

    def show_cashier_panel(self, username: str, password: str):
        """Show the cashier panel."""
        if self.current_window:
            self.current_window.close()
            
        self.current_window = CashierGUI(username, on_logout=self.show_login)
        self.current_window.run()

def main():
    app = SmartMart()

if __name__ == "__main__":
    main() 