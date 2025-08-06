import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import db
from auth import auth
from config import WEEKLY_MENU

class UserDashboard:
    def __init__(self):
        self.current_user = auth.get_current_user()
    
    def show_dashboard(self):
        """Main user dashboard"""
        st.title("🏠 Home Flavours - User Dashboard")
        st.markdown(f"Welcome back, **{self.current_user['full_name']}**!")
        
        # Navigation
        tab1, tab2, tab3, tab4 = st.tabs(["🍽️ Browse Menu", "🛒 My Cart", "📋 My Orders", "👤 Profile"])
        
        with tab1:
            self.show_menu_browser()
        with tab2:
            self.show_cart()
        with tab3:
            self.show_orders()
        with tab4:
            self.show_profile()
    
    def show_menu_browser(self):
        """Display menu browser with weekly options"""
        st.subheader("🍽️ Weekly Menu")
        
        # Get current day
        current_day = datetime.now().strftime('%A')
        
        # Day selector
        selected_day = st.selectbox(
            "Select Day",
            list(WEEKLY_MENU.keys()),
            index=list(WEEKLY_MENU.keys()).index(current_day)
        )
        
        # Display menu for selected day
        st.markdown(f"### {selected_day}'s Special Menu")
        
        # Get available tiffin makers
        tiffin_makers = db.execute_query(
            "SELECT id, business_name, location, rating FROM tiffin_makers WHERE is_active = TRUE"
        )
        
        if not tiffin_makers:
            st.warning("No tiffin makers available in your area.")
            return
        
        # Display menu items
        for i, item in enumerate(WEEKLY_MENU[selected_day]):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{item['name']}**")
                    st.markdown(f"*{item['description']}*")
                
                with col2:
                    st.markdown(f"**₹{item['price']}**")
                
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
                            self.add_to_cart(item, quantity, selected_day)
                            st.success(f"Added {quantity} {item['name']} to cart!")
        
        # Show tiffin makers
        st.markdown("### 🏪 Available Tiffin Makers")
        for maker in tiffin_makers:
            with st.expander(f"🏪 {maker['business_name']} - {maker['location']} (⭐ {maker['rating']})"):
                st.markdown(f"**Location:** {maker['location']}")
                st.markdown(f"**Rating:** ⭐ {maker['rating']}")
    
    def add_to_cart(self, item, quantity, day):
        """Add item to cart"""
        try:
            # Check if item already in cart
            existing_item = db.execute_query(
                "SELECT id, quantity FROM cart WHERE customer_id = %s AND menu_item_id = %s",
                (self.current_user['id'], item.get('id', 0))
            )
            
            if existing_item:
                # Update quantity
                new_quantity = existing_item[0]['quantity'] + quantity
                db.execute_update(
                    "UPDATE cart SET quantity = %s WHERE id = %s",
                    (new_quantity, existing_item[0]['id'])
                )
            else:
                # Add new item to cart
                # First, create menu item if it doesn't exist
                menu_item_id = self.create_menu_item(item, day)
                
                db.execute_update(
                    "INSERT INTO cart (customer_id, menu_item_id, quantity) VALUES (%s, %s, %s)",
                    (self.current_user['id'], menu_item_id, quantity)
                )
        except Exception as e:
            st.error(f"Error adding to cart: {str(e)}")
    
    def create_menu_item(self, item, day):
        """Create menu item in database"""
        # Get first available tiffin maker
        tiffin_maker = db.execute_query(
            "SELECT id FROM tiffin_makers WHERE is_active = TRUE LIMIT 1"
        )
        
        if not tiffin_maker:
            return None
        
        # Insert menu item
        db.execute_update(
            """INSERT INTO menu_items (name, description, price, day_of_week, tiffin_maker_id) 
               VALUES (%s, %s, %s, %s, %s)""",
            (item['name'], item['description'], item['price'], day, tiffin_maker[0]['id'])
        )
        
        # Get the inserted item ID
        result = db.execute_query(
            "SELECT id FROM menu_items WHERE name = %s AND day_of_week = %s ORDER BY id DESC LIMIT 1",
            (item['name'], day)
        )
        
        return result[0]['id'] if result else None
    
    def show_cart(self):
        """Display user's cart"""
        st.subheader("🛒 My Cart")
        
        # Get cart items
        cart_items = db.execute_query("""
            SELECT c.id, c.quantity, mi.name, mi.price, mi.description, tm.business_name
            FROM cart c
            JOIN menu_items mi ON c.menu_item_id = mi.id
            JOIN tiffin_makers tm ON mi.tiffin_maker_id = tm.id
            WHERE c.customer_id = %s
        """, (self.current_user['id'],))
        
        if not cart_items:
            st.info("Your cart is empty. Browse our menu to add items!")
            return
        
        # Display cart items
        total = 0
        for item in cart_items:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"**{item['name']}**")
                    st.markdown(f"*{item['description']}*")
                    st.markdown(f"*By: {item['business_name']}*")
                
                with col2:
                    st.markdown(f"**₹{item['price']}**")
                
                with col3:
                    st.markdown(f"**Qty: {item['quantity']}**")
                
                with col4:
                    if st.button("Remove", key=f"remove_{item['id']}"):
                        db.execute_update("DELETE FROM cart WHERE id = %s", (item['id'],))
                        st.success("Item removed from cart!")
                        st.rerun()
                
                total += item['price'] * item['quantity']
        
        st.markdown("---")
        st.markdown(f"**Total: ₹{total}**")
        
        # Checkout section
        st.markdown("### 🚀 Checkout")
        
        with st.form("checkout_form"):
            delivery_date = st.date_input(
                "Delivery Date",
                min_value=datetime.now().date(),
                value=datetime.now().date() + timedelta(days=1)
            )
            
            delivery_address = st.text_area(
                "Delivery Address",
                value=self.get_user_address()
            )
            
            payment_method = st.selectbox(
                "Payment Method",
                ["COD", "GPay"]
            )
            
            special_instructions = st.text_area("Special Instructions (Optional)")
            
            if st.form_submit_button("Place Order"):
                if self.place_order(cart_items, total, delivery_date, delivery_address, payment_method, special_instructions):
                    st.success("Order placed successfully! You'll receive a confirmation soon.")
                    st.rerun()
                else:
                    st.error("Failed to place order. Please try again.")
    
    def get_user_address(self):
        """Get user's address from database"""
        user_info = db.execute_query(
            "SELECT address FROM users WHERE id = %s",
            (self.current_user['id'],)
        )
        return user_info[0]['address'] if user_info else ""
    
    def place_order(self, cart_items, total, delivery_date, delivery_address, payment_method, special_instructions):
        """Place order and clear cart"""
        try:
            # Get tiffin maker ID (assuming first item's tiffin maker)
            tiffin_maker_id = db.execute_query("""
                SELECT tm.id FROM tiffin_makers tm
                JOIN menu_items mi ON tm.id = mi.tiffin_maker_id
                WHERE mi.id = %s
            """, (cart_items[0]['id'],))[0]['id']
            
            # Create order
            order_success = db.execute_update("""
                INSERT INTO orders (customer_id, tiffin_maker_id, order_date, delivery_date, 
                                 total_amount, payment_method, delivery_address, special_instructions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.current_user['id'], tiffin_maker_id, datetime.now().date(), delivery_date,
                  total, payment_method, delivery_address, special_instructions))
            
            if not order_success:
                return False
            
            # Get order ID
            order_id = db.execute_query("""
                SELECT id FROM orders WHERE customer_id = %s ORDER BY created_at DESC LIMIT 1
            """, (self.current_user['id'],))[0]['id']
            
            # Add order items
            for item in cart_items:
                db.execute_update("""
                    INSERT INTO order_items (order_id, menu_item_id, quantity, price_per_unit)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item['id'], item['quantity'], item['price']))
            
            # Clear cart
            db.execute_update("DELETE FROM cart WHERE customer_id = %s", (self.current_user['id'],))
            
            return True
            
        except Exception as e:
            st.error(f"Error placing order: {str(e)}")
            return False
    
    def show_orders(self):
        """Display user's order history"""
        st.subheader("📋 My Orders")
        
        orders = db.execute_query("""
            SELECT o.*, tm.business_name, tm.location
            FROM orders o
            JOIN tiffin_makers tm ON o.tiffin_maker_id = tm.id
            WHERE o.customer_id = %s
            ORDER BY o.created_at DESC
        """, (self.current_user['id'],))
        
        if not orders:
            st.info("No orders yet. Place your first order!")
            return
        
        for order in orders:
            with st.expander(f"Order #{order['id']} - {order['delivery_date']} - ₹{order['total_amount']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Status:** {order['status'].title()}")
                    st.markdown(f"**Tiffin Maker:** {order['business_name']}")
                    st.markdown(f"**Location:** {order['location']}")
                    st.markdown(f"**Payment:** {order['payment_method']}")
                
                with col2:
                    st.markdown(f"**Order Date:** {order['order_date']}")
                    st.markdown(f"**Delivery Date:** {order['delivery_date']}")
                    st.markdown(f"**Total:** ₹{order['total_amount']}")
                    if order['special_instructions']:
                        st.markdown(f"**Special Instructions:** {order['special_instructions']}")
    
    def show_profile(self):
        """Display user profile"""
        st.subheader("👤 My Profile")
        
        user_info = db.execute_query(
            "SELECT * FROM users WHERE id = %s",
            (self.current_user['id'],)
        )[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Name:** {user_info['full_name']}")
            st.markdown(f"**Username:** {user_info['username']}")
            st.markdown(f"**Email:** {user_info['email']}")
        
        with col2:
            st.markdown(f"**Phone:** {user_info['phone']}")
            st.markdown(f"**User Type:** {user_info['user_type'].title()}")
            st.markdown(f"**Member Since:** {user_info['created_at'].strftime('%B %Y')}")
        
        st.markdown("**Address:**")
        st.markdown(user_info['address'])
        
        # Edit profile button
        if st.button("Edit Profile"):
            st.info("Profile editing feature coming soon!") 