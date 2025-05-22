import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .base_gui import BaseGUI
from models.admin_model import Admin

class AdminGUI(BaseGUI):
    def __init__(self, on_logout: Optional[Callable] = None):
        super().__init__("Admin Panel")
        self.admin = Admin()
        self.on_logout = on_logout
        
        # Create header with user info and logout
        self.create_header()
        
        # Create notebook for tabs
        style = ttk.Style()
        style.configure('Admin.TNotebook', padding=5)
        
        self.notebook = ttk.Notebook(self.main_container, style='Admin.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_products_tab()
        self.create_cashiers_tab()
        self.create_settings_tab()

    def create_header(self):
        """Create header with user info and logout button."""
        header = ttk.Frame(self.main_container)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Welcome message
        ttk.Label(header,
                 text="Administrator Dashboard",
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = ttk.Button(header,
                              text="Logout",
                              command=self.logout,
                              style='Danger.TButton')
        logout_btn.pack(side=tk.RIGHT)

    def create_products_tab(self):
        """Create the products management tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=" Products ")
        
        # Split into left and right panels
        left_panel = ttk.Frame(tab)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = ttk.Frame(tab)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Left panel content
        self.create_section(left_panel, "Product List")
        
        # Category filter
        filter_frame = ttk.Frame(left_panel)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter by Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        categories = ['All'] + self.admin.get_categories()
        category_combo = ttk.Combobox(filter_frame,
                                    textvariable=self.category_var,
                                    values=categories,
                                    state='readonly',
                                    width=30)
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.set('All')
        category_combo.bind('<<ComboboxSelected>>', lambda _: self.refresh_product_list())
        
        # Product list with scrollbar
        tree_frame = ttk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
        self.product_tree = ttk.Treeview(tree_frame,
                                       columns=columns,
                                       show='headings',
                                       selectmode='browse')
        
        # Configure columns
        self.product_tree.column('ID', width=100)
        self.product_tree.column('Name', width=200)
        self.product_tree.column('Category', width=150)
        self.product_tree.column('Price', width=100)
        self.product_tree.column('Stock', width=100)
        
        for col in columns:
            self.product_tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame,
                               orient=tk.VERTICAL,
                               command=self.product_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame,
                               orient=tk.HORIZONTAL,
                               command=self.product_tree.xview)
        
        self.product_tree.configure(yscrollcommand=y_scroll.set,
                                  xscrollcommand=x_scroll.set)
        
        # Pack scrollbars and tree
        self.product_tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Right panel content
        self.create_section(right_panel, "Product Details")
        
        # Product form
        self.product_id_entry = self.create_entry_field(right_panel, "Product ID:")
        self.product_name_entry = self.create_entry_field(right_panel, "Name:")
        
        # Category selection
        category_frame = ttk.Frame(right_panel)
        category_frame.pack(fill=tk.X, pady=10)
        ttk.Label(category_frame, text="Category:").pack(side=tk.LEFT)
        
        self.product_category_var = tk.StringVar()
        category_combo = ttk.Combobox(category_frame,
                                    textvariable=self.product_category_var,
                                    values=self.admin.get_categories(),
                                    state='readonly',
                                    width=30)
        category_combo.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))
        
        self.product_price_entry = self.create_entry_field(right_panel, "Price ($):")
        self.product_quantity_entry = self.create_entry_field(right_panel, "Quantity:")
        
        # Buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.create_button(button_frame, "Add/Update Product", self.add_update_product, 'Success.TButton')
        self.create_button(button_frame, "Delete Product", self.delete_product, 'Danger.TButton')
        self.create_button(button_frame, "Clear Form", self.clear_product_form)
        
        # Initial product list load
        self.refresh_product_list()

    def create_cashiers_tab(self):
        """Create the cashiers management tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=" Cashiers ")
        
        # Split into left and right panels
        left_panel = ttk.Frame(tab)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = ttk.Frame(tab)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH)
        
        # Left panel content
        self.create_section(left_panel, "Cashier List")
        
        # Cashier list with scrollbar
        tree_frame = ttk.Frame(left_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Username',)
        self.cashier_tree = ttk.Treeview(tree_frame,
                                        columns=columns,
                                        show='headings',
                                        selectmode='browse')
        
        self.cashier_tree.column('Username', width=200)
        self.cashier_tree.heading('Username', text='Username', anchor=tk.CENTER)
        
        # Add scrollbar
        y_scroll = ttk.Scrollbar(tree_frame,
                               orient=tk.VERTICAL,
                               command=self.cashier_tree.yview)
        
        self.cashier_tree.configure(yscrollcommand=y_scroll.set)
        
        # Pack scrollbar and tree
        self.cashier_tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        self.cashier_tree.bind('<<TreeviewSelect>>', self.on_cashier_select)
        
        # Right panel content
        self.create_section(right_panel, "Cashier Details")
        
        # Cashier form
        self.cashier_username_entry = self.create_entry_field(right_panel, "Username:")
        self.cashier_password_entry = self.create_entry_field(right_panel, "Password:", show="*")
        
        # Buttons
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.create_button(button_frame, "Add Cashier", self.add_cashier, 'Success.TButton')
        self.create_button(button_frame, "Delete Cashier", self.delete_cashier, 'Danger.TButton')
        self.create_button(button_frame, "Clear Form", self.clear_cashier_form)
        
        # Initial cashier list load
        self.refresh_cashier_list()

    def create_settings_tab(self):
        """Create the settings tab."""
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=" Settings ")
        
        # Create centered container
        container = ttk.Frame(tab)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Password change section
        self.create_section(container, "Change Administrator Password")
        
        # Password form
        self.old_password_entry = self.create_entry_field(container,
                                                         "Current Password:",
                                                         show="*")
        self.new_password_entry = self.create_entry_field(container,
                                                         "New Password:",
                                                         show="*")
        self.confirm_password_entry = self.create_entry_field(container,
                                                            "Confirm Password:",
                                                            show="*")
        
        # Add some space
        ttk.Frame(container).pack(pady=10)
        
        # Change password button
        change_btn = self.create_button(container, "Change Password", self.change_password)
        change_btn.configure(padding=[20, 10])

    def refresh_product_list(self):
        """Refresh the product list in the treeview."""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        category = self.category_var.get()
        products = self.admin.list_products(None if category == 'All' else category)
        
        for product in products:
            self.product_tree.insert('', tk.END, values=product)

    def refresh_cashier_list(self):
        """Refresh the cashier list in the treeview."""
        for item in self.cashier_tree.get_children():
            self.cashier_tree.delete(item)
            
        cashiers = self.admin.list_cashiers()
        for cashier in cashiers:
            self.cashier_tree.insert('', tk.END, values=(cashier,))

    def on_product_select(self, event):
        """Handle product selection in the treeview."""
        selection = self.product_tree.selection()
        if not selection:
            return
            
        values = self.product_tree.item(selection[0])['values']
        self.product_id_entry.delete(0, tk.END)
        self.product_id_entry.insert(0, values[0])
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.insert(0, values[1])
        self.product_category_var.set(values[2])
        self.product_price_entry.delete(0, tk.END)
        self.product_price_entry.insert(0, values[3])
        self.product_quantity_entry.delete(0, tk.END)
        self.product_quantity_entry.insert(0, values[4])

    def on_cashier_select(self, event):
        """Handle cashier selection in the treeview."""
        selection = self.cashier_tree.selection()
        if not selection:
            return
            
        values = self.cashier_tree.item(selection[0])['values']
        self.cashier_username_entry.delete(0, tk.END)
        self.cashier_username_entry.insert(0, values[0])
        self.cashier_password_entry.delete(0, tk.END)

    def add_update_product(self):
        """Add or update a product."""
        try:
            product_id = self.product_id_entry.get().strip()
            name = self.product_name_entry.get().strip()
            category = self.product_category_var.get()
            price = float(self.product_price_entry.get())
            quantity = int(self.product_quantity_entry.get())
            
            if not all([product_id, name, category]):
                self.show_error("Please fill in all fields!")
                return
                
            if price < 0:
                self.show_error("Price cannot be negative!")
                return
                
            if quantity < 0:
                self.show_error("Quantity cannot be negative!")
                return
            
            if self.admin.add_product(product_id, name, category, price, quantity):
                self.show_success("Product saved successfully!")
                self.refresh_product_list()
                self.clear_product_form()
            else:
                self.show_error("Failed to save product!")
        except ValueError:
            self.show_error("Invalid price or quantity!")

    def delete_product(self):
        """Delete a product."""
        product_id = self.product_id_entry.get()
        if not product_id:
            self.show_error("Please select a product to delete!")
            return
            
        if self.admin.remove_product(product_id):
            self.show_success("Product deleted successfully!")
            self.refresh_product_list()
            self.clear_product_form()
        else:
            self.show_error("Failed to delete product!")

    def clear_product_form(self):
        """Clear the product form."""
        self.product_id_entry.delete(0, tk.END)
        self.product_name_entry.delete(0, tk.END)
        self.product_category_var.set('')
        self.product_price_entry.delete(0, tk.END)
        self.product_quantity_entry.delete(0, tk.END)
        self.product_id_entry.focus()

    def add_cashier(self):
        """Add a new cashier."""
        username = self.cashier_username_entry.get().strip()
        password = self.cashier_password_entry.get()
        
        if not username or not password:
            self.show_error("Please fill in all fields!")
            return
            
        if self.admin.add_cashier(username, password):
            self.show_success("Cashier added successfully!")
            self.refresh_cashier_list()
            self.clear_cashier_form()
        else:
            self.show_error("Failed to add cashier!")

    def delete_cashier(self):
        """Delete a cashier."""
        username = self.cashier_username_entry.get()
        if not username:
            self.show_error("Please select a cashier to delete!")
            return
            
        if self.admin.remove_cashier(username):
            self.show_success("Cashier deleted successfully!")
            self.refresh_cashier_list()
            self.clear_cashier_form()
        else:
            self.show_error("Failed to delete cashier!")

    def clear_cashier_form(self):
        """Clear the cashier form."""
        self.cashier_username_entry.delete(0, tk.END)
        self.cashier_password_entry.delete(0, tk.END)
        self.cashier_username_entry.focus()

    def change_password(self):
        """Change the admin password."""
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not all([old_password, new_password, confirm_password]):
            self.show_error("Please fill in all fields!")
            return
            
        if new_password != confirm_password:
            self.show_error("New passwords do not match!")
            self.new_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
            self.new_password_entry.focus()
            return
            
        if len(new_password) < 6:
            self.show_error("Password must be at least 6 characters long!")
            return
            
        if self.admin.change_admin_password(old_password, new_password):
            self.show_success("Password changed successfully!")
            self.old_password_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
        else:
            self.show_error("Failed to change password!")
            self.old_password_entry.delete(0, tk.END)
            self.old_password_entry.focus()

    def logout(self):
        """Handle logout."""
        if self.on_logout:
            self.on_logout()
        self.close() 