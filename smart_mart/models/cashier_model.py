import os
from typing import List, Tuple, Dict, Optional
from datetime import datetime

class Cashier:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.cart: Dict[str, int] = {}  # product_id: quantity
        self.ensure_data_files_exist()
        self.categories = ['Electronics', 'Groceries', 'Clothing', 'Home & Kitchen', 'Sports']

    def ensure_data_files_exist(self):
        """Create necessary data files if they don't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        required_files = ['products.txt', 'bills.txt']
        for filename in required_files:
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                open(filepath, 'a').close()

    def login(self, username: str, password: str) -> bool:
        """Verify cashier login credentials."""
        cashiers_file = os.path.join(self.data_dir, 'cashiers.txt')
        try:
            with open(cashiers_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split(',')
                    if username == stored_username and password == stored_password:
                        return True
            return False
        except:
            return False

    def get_product(self, product_id: str) -> Optional[Tuple[str, str, str, float, int]]:
        """Get product details by ID."""
        products_file = os.path.join(self.data_dir, 'products.txt')
        try:
            with open(products_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == product_id:
                        return (data[0], data[1], data[2], float(data[3]), int(data[4]))
            return None
        except:
            return None

    def list_products(self, category: Optional[str] = None) -> List[Tuple[str, str, str, float, int]]:
        """Get a list of all products, optionally filtered by category."""
        products_file = os.path.join(self.data_dir, 'products.txt')
        products = []
        try:
            with open(products_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if category is None or data[2] == category:
                        products.append((data[0], data[1], data[2], float(data[3]), int(data[4])))
            return products
        except:
            return []

    def get_categories(self) -> List[str]:
        """Get list of product categories."""
        return self.categories.copy()

    def process_sale(self, cart_items: List[Dict]) -> bool:
        """Process a sale transaction."""
        if not cart_items:
            return False
            
        # Update product quantities
        products_file = os.path.join(self.data_dir, 'products.txt')
        temp_file = os.path.join(self.data_dir, 'products_temp.txt')
        
        try:
            # Read current products
            products = {}
            with open(products_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    products[data[0]] = data
            
            # Update quantities
            for item in cart_items:
                product_id = item['id']
                if product_id not in products:
                    return False
                    
                new_quantity = int(products[product_id][4]) - item['quantity']
                if new_quantity < 0:  # Insufficient stock
                    return False
                    
                products[product_id][4] = str(new_quantity)
            
            # Write updated quantities
            with open(temp_file, 'w') as f:
                for data in products.values():
                    f.write(','.join(data) + '\n')
                    
            os.replace(temp_file, products_file)
            
            # Save bill
            total = sum(item['price'] * item['quantity'] for item in cart_items)
            bills_file = os.path.join(self.data_dir, 'bills.txt')
            with open(bills_file, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp},${total:.2f}\n")
                
            return True
            
        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def add_to_cart(self, product_id: str, quantity: int) -> bool:
        """Add a product to the shopping cart."""
        if quantity <= 0:
            return False
            
        product = self.get_product(product_id)
        if not product:
            return False
            
        if product[4] < quantity:  # Check available stock
            return False
            
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
            
        return True

    def remove_from_cart(self, product_id: str) -> bool:
        """Remove a product from the shopping cart."""
        if product_id in self.cart:
            del self.cart[product_id]
            return True
        return False

    def update_cart_quantity(self, product_id: str, quantity: int) -> bool:
        """Update quantity of a product in the cart."""
        if quantity <= 0:
            return self.remove_from_cart(product_id)
            
        product = self.get_product(product_id)
        if not product or product[4] < quantity:
            return False
            
        self.cart[product_id] = quantity
        return True

    def get_cart_items(self) -> List[Tuple[str, str, str, float, int]]:
        """Get all items in the cart with their details."""
        cart_items = []
        for product_id, quantity in self.cart.items():
            product = self.get_product(product_id)
            if product:
                cart_items.append((product[0], product[1], product[2], product[3], quantity))
        return cart_items

    def calculate_total(self, payment_method: str) -> float:
        """Calculate total price with discount if applicable."""
        total = sum(product[3] * quantity for product_id, quantity in self.cart.items()
                   if (product := self.get_product(product_id)))
                   
        if payment_method.lower() == 'card':
            total *= 0.9  # 10% discount for card payments
            
        return round(total, 2)

    def process_payment(self, payment_method: str) -> bool:
        """Process payment and update inventory."""
        if not self.cart:
            return False
            
        total = self.calculate_total(payment_method)
        
        # Update product quantities
        products_file = os.path.join(self.data_dir, 'products.txt')
        temp_file = os.path.join(self.data_dir, 'products_temp.txt')
        
        try:
            # Update product quantities
            products = {}
            with open(products_file, 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    product_id = data[0]
                    if product_id in self.cart:
                        new_quantity = int(data[4]) - self.cart[product_id]
                        if new_quantity < 0:  # Insufficient stock
                            return False
                        data[4] = str(new_quantity)
                    products[product_id] = ','.join(data)
                    
            # Write updated quantities
            with open(temp_file, 'w') as f:
                for line in products.values():
                    f.write(f"{line}\n")
                    
            os.replace(temp_file, products_file)
            
            # Save bill
            bills_file = os.path.join(self.data_dir, 'bills.txt')
            with open(bills_file, 'r') as f:
                bill_number = sum(1 for _ in f) + 1
                
            with open(bills_file, 'a') as f:
                f.write(f"Bill {bill_number}: {total}\n")
                
            # Clear cart after successful payment
            self.cart.clear()
            return True
            
        except:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def clear_cart(self):
        """Clear all items from the cart."""
        self.cart.clear() 