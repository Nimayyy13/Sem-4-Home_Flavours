import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def test_mysql_connection():
    """Test MySQL connection with current settings"""
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'home_flavours'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    
    print("🔍 Testing MySQL Connection...")
    print(f"Host: {config['host']}")
    print(f"User: {config['user']}")
    print(f"Database: {config['database']}")
    print(f"Port: {config['port']}")
    print("-" * 50)
    
    try:
        # First try to connect without database
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL server!")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if config['database'] in databases:
                print(f"✅ Database '{config['database']}' exists!")
                
                # Try to connect to the specific database
                connection.close()
                connection = mysql.connector.connect(**config)
                
                if connection.is_connected():
                    print("✅ Successfully connected to the database!")
                    cursor = connection.cursor()
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    print(f"📊 MySQL Version: {version[0]}")
                    
                    # Test creating a simple table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS test_connection (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            test_field VARCHAR(50)
                        )
                    """)
                    connection.commit()
                    print("✅ Successfully created test table!")
                    
                    # Clean up test table
                    cursor.execute("DROP TABLE test_connection")
                    connection.commit()
                    print("✅ Successfully cleaned up test table!")
                    
                    connection.close()
                    return True
                else:
                    print("❌ Failed to connect to the specific database")
                    return False
            else:
                print(f"❌ Database '{config['database']}' does not exist!")
                print("Creating database...")
                cursor.execute(f"CREATE DATABASE {config['database']}")
                print(f"✅ Database '{config['database']}' created successfully!")
                connection.close()
                return True
                
        else:
            print("❌ Failed to connect to MySQL server")
            return False
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False

def setup_environment():
    """Help user set up environment variables"""
    print("🔧 Database Configuration Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found!")
        load_dotenv()
        
        # Show current settings
        print("\n📋 Current Settings:")
        print(f"Host: {os.getenv('DB_HOST', 'localhost')}")
        print(f"User: {os.getenv('DB_USER', 'root')}")
        print(f"Database: {os.getenv('DB_NAME', 'home_flavours')}")
        print(f"Port: {os.getenv('DB_PORT', '3306')}")
        password = os.getenv('DB_PASSWORD', '')
        print(f"Password: {'*' * len(password) if password else 'Not set'}")
        
        # Test connection
        if test_mysql_connection():
            print("\n🎉 Database connection successful!")
            print("You can now run the application with: python -m streamlit run main_mysql.py")
        else:
            print("\n❌ Database connection failed!")
            print("Please check your MySQL settings and update the .env file")
    else:
        print("❌ .env file not found!")
        print("Creating .env file with default settings...")
        
        # Create .env file
        with open('.env', 'w') as f:
            f.write("DB_HOST=localhost\n")
            f.write("DB_USER=root\n")
            f.write("DB_PASSWORD=your_mysql_password_here\n")
            f.write("DB_NAME=home_flavours\n")
            f.write("DB_PORT=3306\n")
        
        print("✅ .env file created!")
        print("Please update the DB_PASSWORD in the .env file with your MySQL password")
        print("Then run this script again to test the connection")

if __name__ == "__main__":
    print("🏠 Home Flavours - Database Setup")
    print("=" * 50)
    
    setup_environment()
    
    print("\n📝 Instructions:")
    print("1. Make sure MySQL is running on your system")
    print("2. Update the DB_PASSWORD in .env file with your MySQL password")
    print("3. Run this script again to test the connection")
    print("4. Once connection is successful, run: python -m streamlit run main_mysql.py") 