import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get password from environment
    password = os.getenv('DB_PASSWORD', 'sanskruti14')
    
    try:
        # Try to connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL server!")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if 'home_flavours' in databases:
                print("✅ Database 'home_flavours' exists!")
                
                # Try to connect to the specific database
                connection.close()
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password=password,
                    database='home_flavours',
                    port=3306
                )
                
                if connection.is_connected():
                    print("✅ Successfully connected to the database!")
                    cursor = connection.cursor()
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    print(f"📊 MySQL Version: {version[0]}")
                    connection.close()
                    return True
                else:
                    print("❌ Failed to connect to the specific database")
                    return False
            else:
                print("❌ Database 'home_flavours' does not exist!")
                print("Creating database...")
                cursor.execute("CREATE DATABASE home_flavours")
                print("✅ Database 'home_flavours' created successfully!")
                connection.close()
                return True
                
        else:
            print("❌ Failed to connect to MySQL server")
            return False
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing MySQL Connection...")
    print("Host: localhost")
    print("User: root")
    print("Database: home_flavours")
    print("Port: 3306")
    print("-" * 50)
    
    if test_connection():
        print("\n🎉 Database connection successful!")
        print("You can now run the application with: python -m streamlit run main_mysql.py")
    else:
        print("\n❌ Database connection failed!")
        print("Please run: python configure_password.py to set your MySQL password") 