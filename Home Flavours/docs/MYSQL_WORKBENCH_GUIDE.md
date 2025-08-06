# 🗄️ MySQL Workbench Guide for Home Flavours Database

## ✅ Database Successfully Created!

Your Home Flavours database has been created with all tables and demo data. Here's how to view it in MySQL Workbench:

## 🔗 **Connecting to the Database**

### Step 1: Open MySQL Workbench
1. Launch MySQL Workbench from your Start Menu
2. You should see your existing connections:
   - **Local instance MySQL80** (root@localhost:3306)
   - **RSA Database** (rsa_user@localhost:3306)

### Step 2: Connect to MySQL
1. Click on **"Local instance MySQL80"** connection
2. Enter your password: `sanskruti14`
3. Click **"OK"**

## 📊 **Viewing the Home Flavours Database**

### Step 3: Select the Database
1. In the left sidebar, expand **"SCHEMAS"**
2. Look for **"home_flavours"** database
3. Click on the small arrow next to it to expand

### Step 4: Explore Tables
You'll see these tables:
- **users** - User accounts and profiles
- **tiffin_makers** - Tiffin maker businesses
- **menu_items** - Available menu items
- **orders** - Customer orders
- **order_items** - Items in each order

## 🔍 **Sample Queries to Run**

### View All Users:
```sql
USE home_flavours;
SELECT * FROM users;
```

### View Menu Items:
```sql
SELECT * FROM menu_items ORDER BY day_of_week, price;
```

### View Orders with Customer Details:
```sql
SELECT 
    o.id as order_id,
    u.full_name as customer_name,
    o.total_amount,
    o.status,
    o.order_date
FROM orders o
JOIN users u ON o.customer_id = u.id;
```

### View Tiffin Maker Details:
```sql
SELECT 
    tm.business_name,
    tm.location,
    tm.cuisine_specialty,
    tm.rating,
    u.full_name as chef_name
FROM tiffin_makers tm
JOIN users u ON tm.user_id = u.id;
```

## 👤 **Demo Data Available**

### Users:
- **admin** (admin123) - System Administrator
- **chef1** (chef123) - Chef Priya (Tiffin Maker)
- **customer1** (customer123) - Rahul Sharma
- **customer2** (customer123) - Priya Patel

### Menu Items:
- 12 different menu items across Monday, Tuesday, Wednesday
- Price range: ₹75 - ₹130
- Various cuisines: North Indian, South Indian, Continental

### Orders:
- 2 sample orders with different statuses
- Payment methods: COD and GPay
- Special instructions included

## 🎯 **How to Run Queries**

1. **Open Query Tab**: Click the "Create new SQL tab" button (yellow lightning bolt)
2. **Write Query**: Type your SQL query
3. **Execute**: Click the lightning bolt button or press Ctrl+Enter
4. **View Results**: Results appear in the bottom panel

## 📈 **Useful Queries for Analysis**

### Total Revenue:
```sql
SELECT SUM(total_amount) as total_revenue FROM orders;
```

### Orders by Status:
```sql
SELECT status, COUNT(*) as count 
FROM orders 
GROUP BY status;
```

### Popular Menu Items:
```sql
SELECT mi.name, COUNT(oi.id) as order_count
FROM menu_items mi
LEFT JOIN order_items oi ON mi.id = oi.menu_item_id
GROUP BY mi.id, mi.name
ORDER BY order_count DESC;
```

## 🎉 **Database is Ready!**

Your Home Flavours database is now fully set up with:
- ✅ 5 tables created
- ✅ 4 demo users
- ✅ 1 tiffin maker
- ✅ 12 menu items
- ✅ 2 sample orders
- ✅ 4 order items

You can now view all this data in MySQL Workbench and the application will use this database for all operations! 