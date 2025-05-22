import os
from datetime import datetime

def setup_data():
    """Initialize the data directory with sample data."""
    # Create data directory
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create admin credentials
    admin_file = os.path.join(data_dir, 'admin.txt')
    with open(admin_file, 'w') as f:
        f.write('admin,admin123\n')
    
    # Create sample cashiers
    cashiers_file = os.path.join(data_dir, 'cashiers.txt')
    with open(cashiers_file, 'w') as f:
        f.write('cashier1,pass123\n')
        f.write('cashier2,pass123\n')
    
    # Create sample products
    products_file = os.path.join(data_dir, 'products.txt')
    with open(products_file, 'w') as f:
        # Electronics
        f.write('E001,Smartphone,Electronics,599.99,10\n')
        f.write('E002,Laptop,Electronics,999.99,5\n')
        f.write('E003,Headphones,Electronics,79.99,20\n')
        
        # Groceries
        f.write('G001,Milk,Groceries,3.99,50\n')
        f.write('G002,Bread,Groceries,2.99,30\n')
        f.write('G003,Eggs,Groceries,4.99,40\n')
        
        # Clothing
        f.write('C001,T-Shirt,Clothing,19.99,25\n')
        f.write('C002,Jeans,Clothing,49.99,15\n')
        f.write('C003,Socks,Clothing,9.99,50\n')
        
        # Home & Kitchen
        f.write('H001,Blender,Home & Kitchen,79.99,8\n')
        f.write('H002,Coffee Maker,Home & Kitchen,49.99,12\n')
        f.write('H003,Toaster,Home & Kitchen,29.99,10\n')
        
        # Sports
        f.write('S001,Basketball,Sports,24.99,15\n')
        f.write('S002,Yoga Mat,Sports,19.99,20\n')
        f.write('S003,Dumbbells,Sports,39.99,10\n')
    
    # Create empty bills file
    bills_file = os.path.join(data_dir, 'bills.txt')
    open(bills_file, 'w').close()
    
    print("Sample data has been initialized successfully!")

if __name__ == '__main__':
    setup_data() 