import mysql.connector
from mysql.connector import Error
import pandas as pd
from config import DB_CONFIG
import streamlit as st

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.create_tables()
        except Error as e:
            st.error(f"Error connecting to MySQL: {e}")
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(15),
                    address TEXT,
                    user_type ENUM('customer', 'tiffin_maker', 'admin') DEFAULT 'customer',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tiffin makers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tiffin_makers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    business_name VARCHAR(100) NOT NULL,
                    location VARCHAR(200) NOT NULL,
                    cuisine_specialty VARCHAR(100),
                    rating DECIMAL(3,2) DEFAULT 0.0,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Menu items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    day_of_week VARCHAR(20),
                    tiffin_maker_id INT,
                    is_available BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (tiffin_maker_id) REFERENCES tiffin_makers(id)
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    tiffin_maker_id INT,
                    order_date DATE NOT NULL,
                    delivery_date DATE NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    payment_method ENUM('COD', 'GPay') NOT NULL,
                    status ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') DEFAULT 'pending',
                    delivery_address TEXT,
                    special_instructions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES users(id),
                    FOREIGN KEY (tiffin_maker_id) REFERENCES tiffin_makers(id)
                )
            """)
            
            # Order items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT,
                    menu_item_id INT,
                    quantity INT NOT NULL,
                    price_per_unit DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id),
                    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
                )
            """)
            
            # Cart table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    menu_item_id INT,
                    quantity INT NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES users(id),
                    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
                )
            """)
            
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
            
        except Error as e:
            st.error(f"Error creating tables: {e}")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            st.error(f"Error executing query: {e}")
            return []
    
    def execute_update(self, query, params=None):
        """Execute an update query"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            st.error(f"Error executing update: {e}")
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

# Initialize database manager
db = DatabaseManager() 