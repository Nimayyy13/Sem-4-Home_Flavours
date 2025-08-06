# 🗄️ MySQL Database Setup Guide

## 📋 Prerequisites

✅ **MySQL Server**: You have MySQL 8.0.43 installed and running  
✅ **Python Packages**: Required packages are installed  
✅ **Database**: `home_flavours` database exists  

## 🔧 Setup Steps

### Step 1: Configure MySQL Password

Run the password configuration script:
```bash
python configure_password.py
```

When prompted, enter your MySQL root password (the same one you used when connecting via command line).

### Step 2: Test Database Connection

After configuring the password, test the connection:
```bash
python test_mysql.py
```

You should see:
```
✅ Successfully connected to MySQL server!
✅ Database 'home_flavours' exists!
✅ Successfully connected to the database!
📊 MySQL Version: 8.0.43
🎉 Database connection successful!
```

### Step 3: Run the MySQL Application

Once the connection test is successful, run the application:
```bash
python -m streamlit run main_mysql.py
```

## 🎯 Demo Accounts

The application will automatically create these demo accounts:

### 👨‍💼 Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Type**: Administrator

### 👨‍🍳 Tiffin Maker Account
- **Username**: `chef1`
- **Password**: `chef123`
- **Type**: Tiffin Maker

### 👤 Customer Account
- **Username**: `customer1`
- **Password**: `customer123`
- **Type**: Customer

## 🗄️ Database Schema

The application will automatically create these tables:

### 📊 Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Hashed password
- `full_name`: User's full name
- `phone`: Phone number
- `address`: Delivery address
- `user_type`: customer/tiffin_maker/admin
- `created_at`: Registration timestamp

### 🍽️ Menu Items Table
- `id`: Primary key
- `name`: Dish name
- `description`: Dish description
- `price`: Price in rupees
- `day_of_week`: Day of the week
- `icon`: Food emoji icon
- `is_active`: Whether item is available
- `created_at`: Creation timestamp

### 📋 Orders Table
- `id`: Primary key
- `customer_id`: Foreign key to users
- `total_amount`: Order total
- `status`: pending/confirmed/preparing/ready/delivered/cancelled
- `payment_method`: COD/GPay
- `delivery_address`: Delivery address
- `order_date`: Order date
- `created_at`: Order timestamp

### 🛒 Cart Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `menu_item_id`: Foreign key to menu_items
- `quantity`: Item quantity
- `created_at`: Added timestamp

### 📦 Order Items Table
- `id`: Primary key
- `order_id`: Foreign key to orders
- `menu_item_id`: Foreign key to menu_items
- `quantity`: Item quantity
- `price`: Price at time of order

## 🔍 Troubleshooting

### ❌ Connection Denied
If you get "Access denied" error:
1. Make sure MySQL is running
2. Verify your root password
3. Run `python configure_password.py` again

### ❌ Database Not Found
If the database doesn't exist:
1. The application will automatically create it
2. Or manually create: `CREATE DATABASE home_flavours;`

### ❌ Package Not Found
If you get import errors:
```bash
pip install mysql-connector-python python-dotenv
```

## 🚀 Features

### ✅ **MySQL Integration**
- Persistent data storage
- User authentication
- Order management
- Cart functionality
- Admin dashboard

### ✅ **Beautiful Interface**
- Modern design with gradients
- Interactive elements
- Food-themed icons
- Responsive layout

### ✅ **Multi-User System**
- Customer dashboard
- Tiffin maker dashboard
- Admin dashboard
- Role-based access

### ✅ **Order Management**
- Menu browsing
- Cart functionality
- Order placement
- Payment methods (COD/GPay)
- Order status tracking

## 🎉 Success!

Once everything is set up, you'll have a fully functional Home Flavours application with:

- 🗄️ **MySQL Database**: Persistent data storage
- 🎨 **Beautiful Interface**: Modern, attractive design
- 👥 **Multi-User System**: Admin, Tiffin Maker, Customer roles
- 🍽️ **Order Management**: Complete order workflow
- 📊 **Analytics**: Admin dashboard with statistics

**Access the application at: http://localhost:8501** 