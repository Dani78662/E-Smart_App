import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from .base_gui import BaseGUI
from models.cashier_model import Cashier

class CashierGUI(BaseGUI):
    def __init__(self, username: str, on_logout: Optional[Callable] = None):
        super().__init__("Cashier Panel")
        self.username = username
        self.on_logout = on_logout
        self.cashier = Cashier()
        
        # Create header with user info and logout
        self.create_header()
        
        # Create main layout
        self.create_layout()
        
        # Initialize cart display
        self.refresh_cart()

    def create_header(self):
        """Create header with user info and logout button."""
        header = ttk.Frame(self.main_container)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Welcome message with cashier name
        ttk.Label(header,
                 text=f"Welcome, {self.username}",
                 style='Header.TLabel').pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = ttk.Button(header,
                              text="Logout",
                              command=self.logout,
                              style='Danger.TButton')
        logout_btn.pack(side=tk.RIGHT)

    def create_layout(self):
        """Create the main layout."""
        # Create left and right panels
        left_panel = ttk.Frame(self.main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = ttk.Frame(self.main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.Y, width=400)
        
        # Left panel - Product catalog
        self.create_product_catalog(left_panel)
        
        # Right panel - Cart and billing
        self.create_cart_panel(right_panel)

    def create_product_catalog(self, container):
        """Create the product catalog section."""
        self.create_section(container, "Product Catalog")
        
        # Search and filter
        search_frame = ttk.Frame(container)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Category filter
        ttk.Label(search_frame, text="Category:").pack(side=tk.LEFT)
        self.category_var = tk.StringVar()
        categories = ['All'] + self.cashier.get_categories()
        category_combo = ttk.Combobox(search_frame,
                                    textvariable=self.category_var,
                                    values=categories,
                                    state='readonly',
                                    width=20)
        category_combo.pack(side=tk.LEFT, padx=5)
        category_combo.set('All')
        category_combo.bind('<<ComboboxSelected>>', lambda _: self.refresh_product_list())
        
        # Search box
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(10, 0))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *_: self.refresh_product_list())
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Product list
        tree_frame = ttk.Frame(container)
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
        
        # Double click to add to cart
        self.product_tree.bind('<Double-1>', self.add_to_cart)
        
        # Initial product list load
        self.refresh_product_list()

    def create_cart_panel(self, container):
        """Create the cart and billing section."""
        self.create_section(container, "Shopping Cart")
        
        # Cart list
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Price', 'Qty', 'Total')
        self.cart_tree = ttk.Treeview(tree_frame,
                                    columns=columns,
                                    show='headings',
                                    selectmode='browse')
        
        # Configure columns
        self.cart_tree.column('ID', width=80)
        self.cart_tree.column('Name', width=150)
        self.cart_tree.column('Price', width=70)
        self.cart_tree.column('Qty', width=50)
        self.cart_tree.column('Total', width=80)
        
        for col in columns:
            self.cart_tree.heading(col, text=col, anchor=tk.CENTER)
        
        # Add scrollbar
        y_scroll = ttk.Scrollbar(tree_frame,
                               orient=tk.VERTICAL,
                               command=self.cart_tree.yview)
        
        self.cart_tree.configure(yscrollcommand=y_scroll.set)
        
        # Pack scrollbar and tree
        self.cart_tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Cart controls
        controls_frame = ttk.Frame(container)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Quantity spinbox
        ttk.Label(controls_frame, text="Quantity:").pack(side=tk.LEFT)
        self.quantity_var = tk.StringVar(value="1")
        quantity_spinbox = ttk.Spinbox(controls_frame,
                                     from_=1,
                                     to=100,
                                     width=5,
                                     textvariable=self.quantity_var)
        quantity_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Remove button
        self.create_button(controls_frame,
                          "Remove",
                          self.remove_from_cart,
                          'Danger.TButton').pack(side=tk.RIGHT)
        
        # Total section
        total_frame = ttk.Frame(container)
        total_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(total_frame,
                 text="Total Amount:",
                 font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)
        
        self.total_label = ttk.Label(total_frame,
                                   text="$0.00",
                                   font=('Segoe UI', 12, 'bold'),
                                   foreground=self.colors['primary'])
        self.total_label.pack(side=tk.RIGHT)
        
        # Payment section
        payment_frame = ttk.Frame(container)
        payment_frame.pack(fill=tk.X, pady=10)
        
        # Amount received entry
        amount_frame = ttk.Frame(payment_frame)
        amount_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(amount_frame, text="Amount Received:").pack(side=tk.LEFT)
        self.amount_received_var = tk.StringVar()
        self.amount_received_var.trace('w', self.calculate_change)
        amount_entry = ttk.Entry(amount_frame,
                               textvariable=self.amount_received_var,
                               width=15)
        amount_entry.pack(side=tk.RIGHT)
        
        # Change display
        change_frame = ttk.Frame(payment_frame)
        change_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(change_frame, text="Change:").pack(side=tk.LEFT)
        self.change_label = ttk.Label(change_frame,
                                    text="$0.00",
                                    foreground=self.colors['success'])
        self.change_label.pack(side=tk.RIGHT)
        
        # Complete sale button
        complete_btn = self.create_button(container,
                                        "Complete Sale",
                                        self.complete_sale,
                                        'Success.TButton')
        complete_btn.configure(padding=[20, 10])
        
        # New sale button
        self.create_button(container, "New Sale", self.new_sale)

    def refresh_product_list(self):
        """Refresh the product list based on category and search filters."""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        category = self.category_var.get()
        search_term = self.search_var.get().lower()
        
        products = self.cashier.list_products(None if category == 'All' else category)
        
        for product in products:
            if search_term in product[1].lower():  # Search in product name
                self.product_tree.insert('', tk.END, values=product)

    def refresh_cart(self):
        """Refresh the cart display."""
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        cart_items = self.cashier.get_cart_items()
        total = 0.0
        
        for item in cart_items:
            item_total = item[3] * item[4]  # price * quantity
            total += item_total
            self.cart_tree.insert('', tk.END, values=(
                item[0],  # ID
                item[1],  # Name
                f"${item[3]:.2f}",  # Price
                item[4],  # Quantity
                f"${item_total:.2f}"  # Total
            ))
            
        self.total_label.configure(text=f"${total:.2f}")
        self.calculate_change()

    def add_to_cart(self, event=None):
        """Add selected product to cart."""
        selection = self.product_tree.selection()
        if not selection:
            return
            
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                self.show_error("Quantity must be positive!")
                return
        except ValueError:
            self.show_error("Invalid quantity!")
            return
            
        values = self.product_tree.item(selection[0])['values']
        product_id = values[0]
        
        if self.cashier.add_to_cart(product_id, quantity):
            self.refresh_cart()
            self.refresh_product_list()  # Refresh to update stock
        else:
            self.show_error("Failed to add item to cart!")

    def remove_from_cart(self):
        """Remove selected item from cart."""
        selection = self.cart_tree.selection()
        if not selection:
            self.show_error("Please select an item to remove!")
            return
            
        values = self.cart_tree.item(selection[0])['values']
        product_id = values[0]
        
        if self.cashier.remove_from_cart(product_id):
            self.refresh_cart()
            self.refresh_product_list()  # Refresh to update stock
        else:
            self.show_error("Failed to remove item from cart!")

    def calculate_change(self, *args):
        """Calculate and display change amount."""
        try:
            amount_received = float(self.amount_received_var.get() or 0)
            total = float(self.total_label.cget('text').replace('$', ''))
            change = amount_received - total
            self.change_label.configure(
                text=f"${change:.2f}",
                foreground=self.colors['success'] if change >= 0 else self.colors['danger']
            )
        except ValueError:
            self.change_label.configure(
                text="$0.00",
                foreground=self.colors['danger']
            )

    def complete_sale(self):
        """Complete the sale transaction."""
        cart_items = self.cashier.get_cart_items()
        if not cart_items:
            self.show_error("Cart is empty!")
            return
            
        try:
            amount_received = float(self.amount_received_var.get() or 0)
            total = float(self.total_label.cget('text').replace('$', ''))
            if amount_received < total:
                self.show_error("Insufficient payment amount!")
                return
        except ValueError:
            self.show_error("Invalid payment amount!")
            return
            
        # Convert cart items to the format expected by process_payment
        items_for_sale = [
            {
                'id': item[0],
                'name': item[1],
                'price': item[3],
                'quantity': item[4]
            }
            for item in cart_items
        ]
        
        # Process sale
        if self.cashier.process_sale(items_for_sale):
            change = amount_received - total
            self.show_success(f"Sale completed successfully!\nChange: ${change:.2f}")
            self.new_sale()
        else:
            self.show_error("Failed to process sale!")

    def new_sale(self):
        """Start a new sale."""
        self.cashier.clear_cart()
        self.amount_received_var.set("")
        self.quantity_var.set("1")
        self.refresh_cart()
        self.refresh_product_list()

    def logout(self):
        """Handle logout."""
        if self.on_logout:
            self.on_logout()
        self.close() 