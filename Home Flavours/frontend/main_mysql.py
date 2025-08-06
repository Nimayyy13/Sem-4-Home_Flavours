import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import json
import os
from database_config import db_manager

# Page configuration
st.set_page_config(
    page_title="Home Flavours",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    /* Modern Color Scheme */
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --accent-color: #FFE66D;
        --dark-color: #2C3E50;
        --light-color: #ECF0F1;
        --success-color: #2ECC71;
        --warning-color: #F39C12;
    }
    
    /* Main Header with Gradient */
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    /* Feature Cards with Hover Effects */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border-left: 5px solid var(--primary-color);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .feature-card:hover::before {
        transform: translateX(100%);
    }
    
    /* Menu Item Cards */
    .menu-item-card {
        background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .menu-item-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: var(--primary-color);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(255,107,107,0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
    }
    
    /* Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color) 0%, #27AE60 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Error Messages */
    .stError {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Food Icons */
    .food-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    /* Price Tags */
    .price-tag {
        background: linear-gradient(135deg, var(--accent-color) 0%, #F1C40F 100%);
        color: var(--dark-color);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Cart Badge */
    .cart-badge {
        background: var(--primary-color);
        color: white;
        border-radius: 50%;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header h3 {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Weekly menu data
WEEKLY_MENU = {
    'Monday': [
        {'name': 'Dal Khichdi with Ghee', 'price': 80, 'description': 'Comforting rice and lentil dish', 'icon': '🍚'},
        {'name': 'Roti Sabzi with Dal', 'price': 90, 'description': 'Fresh rotis with seasonal vegetables', 'icon': '🫓'},
        {'name': 'Pulao with Raita', 'price': 100, 'description': 'Fragrant rice with cooling raita', 'icon': '🍛'},
        {'name': 'Thali Special', 'price': 120, 'description': 'Complete meal with 3 sabzis, dal, rice, roti', 'icon': '🍽️'}
    ],
    'Tuesday': [
        {'name': 'Rajma Chawal', 'price': 85, 'description': 'Kidney beans with steamed rice', 'icon': '🫘'},
        {'name': 'Aloo Paratha with Curd', 'price': 75, 'description': 'Stuffed potato bread with yogurt', 'icon': '🥔'},
        {'name': 'Mixed Vegetable Curry', 'price': 95, 'description': 'Assorted vegetables in rich gravy', 'icon': '🥬'},
        {'name': 'Biryani Special', 'price': 130, 'description': 'Aromatic rice with tender meat/vegetables', 'icon': '🍚'}
    ],
    'Wednesday': [
        {'name': 'Chole Bhature', 'price': 90, 'description': 'Chickpeas with fluffy bread', 'icon': '🫓'},
        {'name': 'Kadhi Pakora', 'price': 80, 'description': 'Yogurt curry with gram flour fritters', 'icon': '🥣'},
        {'name': 'Paneer Butter Masala', 'price': 110, 'description': 'Cottage cheese in rich tomato gravy', 'icon': '🧀'},
        {'name': 'South Indian Thali', 'price': 125, 'description': 'Rice, sambar, rasam, curd rice', 'icon': '🍽️'}
    ],
    'Thursday': [
        {'name': 'Masala Dosa', 'price': 85, 'description': 'Crispy rice crepe with potato filling', 'icon': '🥞'},
        {'name': 'Dal Makhani', 'price': 95, 'description': 'Creamy black lentils', 'icon': '🫘'},
        {'name': 'Mixed Veg Pulao', 'price': 100, 'description': 'Vegetable rice with raita', 'icon': '🍛'},
        {'name': 'Gujarati Thali', 'price': 115, 'description': 'Traditional Gujarati meal', 'icon': '🍽️'}
    ],
    'Friday': [
        {'name': 'Fish Curry with Rice', 'price': 140, 'description': 'Spicy fish curry with steamed rice', 'icon': '🐟'},
        {'name': 'Chicken Biryani', 'price': 150, 'description': 'Aromatic chicken rice dish', 'icon': '🍗'},
        {'name': 'Veg Fried Rice', 'price': 90, 'description': 'Chinese style vegetable rice', 'icon': '🍚'},
        {'name': 'North Indian Thali', 'price': 130, 'description': 'Complete North Indian meal', 'icon': '🍽️'}
    ],
    'Saturday': [
        {'name': 'Pav Bhaji', 'price': 80, 'description': 'Spicy vegetable mash with bread', 'icon': '🥖'},
        {'name': 'Idli Sambar', 'price': 75, 'description': 'Steamed rice cakes with lentil soup', 'icon': '🥟'},
        {'name': 'Mushroom Masala', 'price': 100, 'description': 'Mushrooms in spicy gravy', 'icon': '🍄'},
        {'name': 'Maharashtrian Thali', 'price': 120, 'description': 'Traditional Maharashtrian meal', 'icon': '🍽️'}
    ],
    'Sunday': [
        {'name': 'Butter Chicken', 'price': 160, 'description': 'Creamy tomato-based chicken curry', 'icon': '🍗'},
        {'name': 'Palak Paneer', 'price': 110, 'description': 'Spinach with cottage cheese', 'icon': '🥬'},
        {'name': 'Jeera Rice with Dal', 'price': 85, 'description': 'Cumin rice with lentil soup', 'icon': '🍚'},
        {'name': 'Special Sunday Thali', 'price': 140, 'description': 'Festive Sunday meal', 'icon': '🍽️'}
    ]
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, full_name, phone, address, user_type='customer'):
    """Register a new user in the database"""
    try:
        # Check if user already exists
        existing_user = db_manager.execute_query(
            "SELECT id FROM users WHERE username = %s", (username,)
        )
        if existing_user:
            return False, "Username already exists"
        
        # Hash password and insert user
        password_hash = hash_password(password)
        user_id = db_manager.execute_update(
            """INSERT INTO users (username, email, password_hash, full_name, phone, address, user_type) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (username, email, password_hash, full_name, phone, address, user_type)
        )
        
        if user_id:
            return True, "Registration successful!"
        else:
            return False, "Registration failed"
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def login_user(username, password):
    """Login user and verify credentials"""
    try:
        user = db_manager.execute_query(
            "SELECT * FROM users WHERE username = %s", (username,)
        )
        
        if user and user[0]['password_hash'] == hash_password(password):
            st.session_state.authenticated = True
            st.session_state.current_user = user[0]
            return True, "Login successful!"
        else:
            return False, "Invalid username or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def logout_user():
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.rerun()

def get_user_cart(user_id):
    """Get user's cart items from database"""
    try:
        cart_items = db_manager.execute_query("""
            SELECT c.id, c.quantity, m.name, m.description, m.price, m.icon
            FROM cart c
            JOIN menu_items m ON c.menu_item_id = m.id
            WHERE c.user_id = %s
        """, (user_id,))
        return cart_items
    except Exception as e:
        print(f"Error getting cart: {e}")
        return []

def add_to_cart_db(user_id, menu_item_name, quantity):
    """Add item to user's cart in database"""
    try:
        # First, get or create menu item
        menu_item = db_manager.execute_query(
            "SELECT id FROM menu_items WHERE name = %s", (menu_item_name,)
        )
        
        if not menu_item:
            # Create menu item if it doesn't exist
            menu_item_id = db_manager.execute_update(
                "INSERT INTO menu_items (name, description, price, day_of_week, icon) VALUES (%s, %s, %s, %s, %s)",
                (menu_item_name, "Delicious homemade food", 100, "Monday", "🍽️")
            )
        else:
            menu_item_id = menu_item[0]['id']
        
        # Check if item already in cart
        existing_cart_item = db_manager.execute_query(
            "SELECT id, quantity FROM cart WHERE user_id = %s AND menu_item_id = %s",
            (user_id, menu_item_id)
        )
        
        if existing_cart_item:
            # Update quantity
            new_quantity = existing_cart_item[0]['quantity'] + quantity
            db_manager.execute_update(
                "UPDATE cart SET quantity = %s WHERE id = %s",
                (new_quantity, existing_cart_item[0]['id'])
            )
        else:
            # Add new item to cart
            db_manager.execute_update(
                "INSERT INTO cart (user_id, menu_item_id, quantity) VALUES (%s, %s, %s)",
                (user_id, menu_item_id, quantity)
            )
        
        return True
    except Exception as e:
        print(f"Error adding to cart: {e}")
        return False

def place_order_db(user_id, total_amount, payment_method="COD"):
    """Place order in database"""
    try:
        # Create order
        order_id = db_manager.execute_update(
            """INSERT INTO orders (customer_id, total_amount, payment_method, order_date) 
               VALUES (%s, %s, %s, %s)""",
            (user_id, total_amount, payment_method, datetime.now().date())
        )
        
        if order_id:
            # Get cart items and add to order_items
            cart_items = get_user_cart(user_id)
            for item in cart_items:
                db_manager.execute_update(
                    "INSERT INTO order_items (order_id, menu_item_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, item['id'], item['quantity'], item['price'])
                )
            
            # Clear cart
            db_manager.execute_update("DELETE FROM cart WHERE user_id = %s", (user_id,))
            return True
        return False
    except Exception as e:
        print(f"Error placing order: {e}")
        return False

def get_user_orders(user_id):
    """Get user's orders from database"""
    try:
        orders = db_manager.execute_query("""
            SELECT o.id, o.total_amount, o.status, o.payment_method, o.order_date,
                   GROUP_CONCAT(CONCAT(oi.quantity, 'x ', m.name) SEPARATOR ', ') as items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN menu_items m ON oi.menu_item_id = m.id
            WHERE o.customer_id = %s
            GROUP BY o.id
            ORDER BY o.created_at DESC
        """, (user_id,))
        return orders
    except Exception as e:
        print(f"Error getting orders: {e}")
        return []

def main():
    # Initialize database connection
    if not db_manager.connect():
        st.error("❌ Failed to connect to database. Please check your MySQL connection.")
        return
    
    # Create tables if they don't exist
    if not db_manager.create_tables():
        st.error("❌ Failed to create database tables.")
        return
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("""
        <div class="main-header">
            <h1>🏠 Home Flavours</h1>
            <p>Homemade Tiffin Service</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.authenticated:
            current_user = st.session_state.current_user
            st.success(f"Welcome, {current_user['full_name']}! 👋")
            
            # Cart indicator
            cart_items = get_user_cart(current_user['id'])
            cart_count = len(cart_items)
            if cart_count > 0:
                st.markdown(f"🛒 Cart: <span class='cart-badge'>{cart_count} items</span>", unsafe_allow_html=True)
            
            if st.button("🚪 Logout"):
                logout_user()
        else:
            st.info("Please login to access the dashboard 🔐")
    
    # Main content
    if not st.session_state.authenticated:
        show_landing_page()
    else:
        current_user = st.session_state.current_user
        if current_user['user_type'] == 'admin':
            show_admin_dashboard()
        elif current_user['user_type'] == 'tiffin_maker':
            show_tiffin_maker_dashboard()
        else:
            show_user_dashboard()

def show_landing_page():
    # Hero Section with Enhanced Design
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Home Flavours</h1>
        <h3>Delicious Homemade Tiffins Delivered to Your Doorstep</h3>
        <p>Connect with local home chefs for authentic, homemade meals</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section with Icons
    st.markdown("### ✨ Why Choose Home Flavours?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🍽️ Fresh Homemade Food</h3>
            <p>Authentic home-cooked meals prepared with love and care by local home chefs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📍 Local Tiffin Makers</h3>
            <p>Connect with verified home chefs in your neighborhood for fresh, local flavors.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🚚 Fast Delivery</h3>
            <p>Quick and reliable delivery to your doorstep with flexible payment options.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("---")
    st.markdown("### 🔄 How It Works")
    
    steps = [
        {"icon": "1️⃣", "title": "Browse Menu", "description": "Explore our weekly menu with fresh, homemade options for each day."},
        {"icon": "2️⃣", "title": "Add to Cart", "description": "Select your favorite dishes and add them to your cart."},
        {"icon": "3️⃣", "title": "Place Order", "description": "Choose delivery date, payment method (COD/GPay), and place your order."},
        {"icon": "4️⃣", "title": "Enjoy Fresh Food", "description": "Receive your delicious homemade tiffin at your doorstep."}
    ]
    
    cols = st.columns(4)
    for i, step in enumerate(steps):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <h3>{step['icon']} {step['title']}</h3>
                <p>{step['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Authentication section
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("🔐 Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username and password:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    with tab2:
        st.subheader("📝 Create New Account")
        
        with st.form("register_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
            
            with col2:
                full_name = st.text_input("Full Name")
                phone = st.text_input("Phone Number")
                address = st.text_area("Address")
                user_type = st.selectbox("User Type", ["customer", "tiffin_maker"])
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                if not all([username, email, password, confirm_password, full_name, phone, address]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = register_user(
                        username, email, password, full_name, phone, address, user_type
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

def show_user_dashboard():
    current_user = st.session_state.current_user
    
    st.title("🏠 Home Flavours - User Dashboard")
    st.markdown(f"Welcome back, **{current_user['full_name']}**! 👋")
    
    tab1, tab2, tab3 = st.tabs(["🍽️ Browse Menu", "🛒 My Cart", "📋 My Orders"])
    
    with tab1:
        show_menu_browser()
    
    with tab2:
        show_cart()
    
    with tab3:
        show_orders()

def show_menu_browser():
    st.subheader("🍽️ Weekly Menu")
    
    current_day = datetime.now().strftime('%A')
    selected_day = st.selectbox(
        "Select Day",
        list(WEEKLY_MENU.keys()),
        index=list(WEEKLY_MENU.keys()).index(current_day) if current_day in WEEKLY_MENU else 0
    )
    
    st.markdown(f"### {selected_day}'s Special Menu")
    
    for i, item in enumerate(WEEKLY_MENU[selected_day]):
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="menu-item-card">
                    <h4>{item['icon']} {item['name']}</h4>
                    <p><em>{item['description']}</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div class='price-tag'>₹{item['price']}</div>", unsafe_allow_html=True)
            
            with col3:
                quantity = st.number_input(
                    "Qty",
                    min_value=0,
                    max_value=10,
                    value=0,
                    key=f"qty_{selected_day}_{i}"
                )
                
                if quantity > 0:
                    if st.button("Add to Cart", key=f"add_{selected_day}_{i}"):
                        if add_to_cart_db(st.session_state.current_user['id'], item['name'], quantity):
                            st.success(f"Added {quantity} {item['name']} to cart! 🛒")
                        else:
                            st.error("Failed to add item to cart")

def show_cart():
    st.subheader("🛒 My Cart")
    
    cart_items = get_user_cart(st.session_state.current_user['id'])
    
    if not cart_items:
        st.info("Your cart is empty. Browse our menu to add items! 🍽️")
        return
    
    total = 0
    for item in cart_items:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div class="menu-item-card">
                    <h4>{item['icon']} {item['name']}</h4>
                    <p><em>{item['description']}</em></p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div class='price-tag'>₹{item['price']}</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**Qty: {item['quantity']}**")
            
            with col4:
                if st.button("Remove", key=f"remove_{item['id']}"):
                    db_manager.execute_update("DELETE FROM cart WHERE id = %s", (item['id'],))
                    st.success("Item removed from cart! 🗑️")
                    st.rerun()
            
            total += item['price'] * item['quantity']
    
    st.markdown("---")
    st.markdown(f"**Total: ₹{total}**")
    
    payment_method = st.selectbox("Payment Method", ["COD", "GPay"])
    
    if st.button("Place Order"):
        if place_order_db(st.session_state.current_user['id'], total, payment_method):
            st.success("Order placed successfully! 🎉")
            st.rerun()
        else:
            st.error("Failed to place order")

def show_orders():
    st.subheader("📋 My Orders")
    
    user_orders = get_user_orders(st.session_state.current_user['id'])
    
    if not user_orders:
        st.info("No orders yet. Place your first order! 🍽️")
        return
    
    for order in user_orders:
        with st.expander(f"Order #{order['id']} - ₹{order['total_amount']} - {order['order_date']}"):
            st.markdown(f"**Status:** {order['status'].title()}")
            st.markdown(f"**Payment Method:** {order['payment_method']}")
            st.markdown(f"**Total:** ₹{order['total_amount']}")
            st.markdown("**Items:**")
            st.markdown(f"- {order['items']}")

def show_tiffin_maker_dashboard():
    current_user = st.session_state.current_user
    
    st.title("👨‍🍳 Home Flavours - Tiffin Maker Dashboard")
    st.markdown(f"Welcome back, **{current_user['full_name']}**! 👋")
    
    tab1, tab2 = st.tabs(["📋 Orders", "🍽️ Menu Management"])
    
    with tab1:
        show_tiffin_maker_orders()
    
    with tab2:
        show_menu_management()

def show_tiffin_maker_orders():
    st.subheader("📋 Orders")
    
    # Get all orders
    orders = db_manager.execute_query("""
        SELECT o.id, o.total_amount, o.status, o.order_date, u.full_name as customer_name,
               GROUP_CONCAT(CONCAT(oi.quantity, 'x ', m.name) SEPARATOR ', ') as items
        FROM orders o
        JOIN users u ON o.customer_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN menu_items m ON oi.menu_item_id = m.id
        GROUP BY o.id
        ORDER BY o.created_at DESC
    """)
    
    if not orders:
        st.info("No orders yet. 🍽️")
        return
    
    for order in orders:
        with st.expander(f"Order #{order['id']} - {order['customer_name']} - ₹{order['total_amount']}"):
            st.markdown(f"**Customer:** {order['customer_name']}")
            st.markdown(f"**Status:** {order['status'].title()}")
            st.markdown(f"**Total:** ₹{order['total_amount']}")
            st.markdown("**Items:**")
            st.markdown(f"- {order['items']}")
            
            if order['status'] == 'pending':
                if st.button("Confirm Order", key=f"confirm_{order['id']}"):
                    db_manager.execute_update(
                        "UPDATE orders SET status = 'confirmed' WHERE id = %s",
                        (order['id'],)
                    )
                    st.success("Order confirmed! ✅")
                    st.rerun()

def show_menu_management():
    st.subheader("🍽️ Menu Management")
    st.info("Menu management feature coming soon! 🚧")

def show_admin_dashboard():
    current_user = st.session_state.current_user
    
    st.title("👨‍💼 Home Flavours - Admin Dashboard")
    st.markdown(f"Welcome back, **{current_user['full_name']}**! 👋")
    
    tab1, tab2 = st.tabs(["📊 Overview", "👥 Users"])
    
    with tab1:
        show_admin_overview()
    
    with tab2:
        show_user_management()

def show_admin_overview():
    st.subheader("📊 System Overview")
    
    # Get statistics
    total_users = db_manager.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
    total_orders = db_manager.execute_query("SELECT COUNT(*) as count FROM orders")[0]['count']
    total_revenue = db_manager.execute_query("SELECT SUM(total_amount) as total FROM orders")[0]['total'] or 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Users</h3>
            <h2>{total_users}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 Total Orders</h3>
            <h2>{total_orders}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Total Revenue</h3>
            <h2>₹{total_revenue}</h2>
        </div>
        """, unsafe_allow_html=True)

def show_user_management():
    st.subheader("👥 User Management")
    
    users = db_manager.execute_query("SELECT * FROM users ORDER BY created_at DESC")
    
    for user in users:
        with st.expander(f"{user['full_name']} ({user['user_type']})"):
            st.markdown(f"**Username:** {user['username']}")
            st.markdown(f"**Email:** {user['email']}")
            st.markdown(f"**Phone:** {user['phone']}")
            st.markdown(f"**Type:** {user['user_type'].title()}")
            st.markdown(f"**Created:** {user['created_at']}")

if __name__ == "__main__":
    # Create demo accounts if they don't exist
    demo_users = [
        ('admin', 'admin@homeflavours.com', 'admin123', 'System Administrator', '1234567890', 'Admin Address', 'admin'),
        ('chef1', 'chef1@homeflavours.com', 'chef123', 'Priya Sharma', '9876543210', '123 Cooking Street, Mumbai', 'tiffin_maker'),
        ('customer1', 'customer1@homeflavours.com', 'customer123', 'Rahul Kumar', '5555555555', '456 Customer Lane, Mumbai', 'customer')
    ]
    
    for username, email, password, full_name, phone, address, user_type in demo_users:
        existing_user = db_manager.execute_query("SELECT id FROM users WHERE username = %s", (username,))
        if not existing_user:
            register_user(username, email, password, full_name, phone, address, user_type)
    
    main() 