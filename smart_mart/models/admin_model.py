import os
from typing import List, Tuple, Optional, Dict
from datetime import datetime

class Admin:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.ensure_data_files_exist()
        self.categories = ['Electronics', 'Groceries', 'Clothing', 'Home & Kitchen', 'Sports']
        
    def ensure_data_files_exist(self):
        """Create necessary data files if they don't exist."""
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # Create admin.txt with default credentials if it doesn't exist
        admin_file = os.path.join(self.data_dir, 'admin.txt')
        if not os.path.exists(admin_file):
            with open(admin_file, 'w') as f:
                f.write('admin,admin123\n')
                
        # Create other required files
        required_files = ['cashiers.txt', 'products.txt', 'bills.txt']
        for filename in required_files:
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                open(filepath, 'a').close()

    def login(self, username: str, password: str) -> bool:
        """Verify admin login credentials."""
        admin_file = os.path.join(self.data_dir, 'admin.txt')
        try:
            with open(admin_file, 'r') as f:
                stored_creds = f.readline().strip().split(',')
                return username == stored_creds[0] and password == stored_creds[1]
        except:
            return False

    def add_cashier(self, username: str, password: str) -> bool:
        """Add a new cashier to the system."""
        if not username or not password:
            return False
            
        cashiers_file = os.path.join(self.data_dir, 'cashiers.txt')
        try:
            # Check if cashier already exists
            with open(cashiers_file, 'r') as f:
                for line in f:
                    if line.strip().split(',')[0] == username:
                        return False
                        
            # Add new cashier
            with open(cashiers_file, 'a') as f:
                f.write(f"{username},{password}\n")
            return True
        except:
            return False

    def remove_cashier(self, username: str) -> bool:
        """Remove a cashier from the system."""
        cashiers_file = os.path.join(self.data_dir, 'cashiers.txt')
        temp_file = os.path.join(self.data_dir, 'cashiers_temp.txt')
        
        try:
            found = False
            with open(cashiers_file, 'r') as f, open(temp_file, 'w') as temp:
                for line in f:
                    if line.strip().split(',')[0] != username:
                        temp.write(line)
                    else:
                        found = True
                        
            if found:
                os.replace(temp_file, cashiers_file)
                return True
            else:
                os.remove(temp_file)
                return False
        except:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def list_cashiers(self) -> List[str]:
        """Get a list of all cashiers."""
        cashiers_file = os.path.join(self.data_dir, 'cashiers.txt')
        cashiers = []
        try:
            with open(cashiers_file, 'r') as f:
                for line in f:
                    username = line.strip().split(',')[0]
                    cashiers.append(username)
            return cashiers
        except:
            return []

    def add_product(self, product_id: str, name: str, category: str, price: float, quantity: int) -> bool:
        """Add a new product or update existing product."""
        if not all([product_id, name, category, price >= 0, quantity >= 0]):
            return False
        
        if category not in self.categories:
            return False
            
        products_file = os.path.join(self.data_dir, 'products.txt')
        temp_file = os.path.join(self.data_dir, 'products_temp.txt')
        
        try:
            updated = False
            with open(products_file, 'r') as f, open(temp_file, 'w') as temp:
                for line in f:
                    curr_id = line.strip().split(',')[0]
                    if curr_id == product_id:
                        temp.write(f"{product_id},{name},{category},{price},{quantity}\n")
                        updated = True
                    else:
                        temp.write(line)
                        
                if not updated:
                    temp.write(f"{product_id},{name},{category},{price},{quantity}\n")
                    
            os.replace(temp_file, products_file)
            return True
        except:
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def remove_product(self, product_id: str) -> bool:
        """Remove a product from the system."""
        products_file = os.path.join(self.data_dir, 'products.txt')
        temp_file = os.path.join(self.data_dir, 'products_temp.txt')
        
        try:
            found = False
            with open(products_file, 'r') as f, open(temp_file, 'w') as temp:
                for line in f:
                    if line.strip().split(',')[0] != product_id:
                        temp.write(line)
                    else:
                        found = True
                        
            if found:
                os.replace(temp_file, products_file)
                return True
            else:
                os.remove(temp_file)
                return False
        except:
            if os.path.exists(temp_file):
                os.remove(temp_file)
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

    def update_product_quantity(self, product_id: str, quantity: int) -> bool:
        """Update the quantity of a product."""
        if quantity < 0:
            return False
            
        product = self.get_product(product_id)
        if not product:
            return False
            
        return self.add_product(product_id, product[1], product[2], product[3], quantity)

    def change_admin_password(self, old_password: str, new_password: str) -> bool:
        """Change the admin password."""
        if not old_password or not new_password:
            return False
            
        admin_file = os.path.join(self.data_dir, 'admin.txt')
        try:
            # Verify old password
            with open(admin_file, 'r') as f:
                stored_creds = f.readline().strip().split(',')
                if stored_creds[1] != old_password:
                    return False
                    
            # Update password
            with open(admin_file, 'w') as f:
                f.write(f"{stored_creds[0]},{new_password}\n")
            return True
        except:
            return False 