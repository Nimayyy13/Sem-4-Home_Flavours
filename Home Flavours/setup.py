#!/usr/bin/env python3
"""
Home Flavours Setup Script
Helps with initial project configuration and database setup
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print("✅ Python version check passed")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        print("🔧 Creating .env file...")
        try:
            with open('env_example.txt', 'r') as template:
                content = template.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(content)
            
            print("✅ .env file created")
            print("⚠️  Please update the database credentials in .env file")
        except FileNotFoundError:
            print("❌ env_example.txt not found")
            sys.exit(1)
    else:
        print("✅ .env file already exists")

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'sanskruti14'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Database connection successful")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            db_name = os.getenv('DB_NAME', 'home_flavours')
            if db_name in databases:
                print(f"✅ Database '{db_name}' exists")
            else:
                print(f"⚠️  Database '{db_name}' does not exist")
                print("Creating database...")
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"✅ Database '{db_name}' created")
            
            cursor.close()
            connection.close()
            
        else:
            print("❌ Database connection failed")
            return False
            
    except Error as e:
        print(f"❌ Database connection error: {e}")
        print("Please check your database credentials in .env file")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🏠 Home Flavours Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Test database connection
    if test_database_connection():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Update database credentials in .env file if needed")
        print("2. Run: streamlit run main.py")
        print("3. Access the application in your browser")
        print("\nDemo accounts will be created automatically on first run:")
        print("- Admin: admin/admin123")
        print("- Tiffin Maker: chef1/chef123")
        print("- Customer: customer1/customer123")
    else:
        print("\n❌ Setup failed. Please check your database configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main() 