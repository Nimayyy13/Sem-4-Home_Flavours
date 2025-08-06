import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import db
from auth import auth
from config import WEEKLY_MENU

class TiffinMakerDashboard:
    def __init__(self):
        self.current_user = auth.get_current_user()
        self.tiffin_maker_id = self.get_tiffin_maker_id()
    
    def get_tiffin_maker_id(self):
        """Get tiffin maker ID for current user"""
        result = db.execute_query(
            "SELECT id FROM tiffin_makers WHERE user_id = %s",
            (self.current_user['id'],)
        )
        return result[0]['id'] if result else None
    
    def show_dashboard(self):
        """Main tiffin maker dashboard"""
        st.title("👨‍🍳 Home Flavours - Tiffin Maker Dashboard")
        st.markdown(f"Welcome back, **{self.current_user['full_name']}**!")
        
        if not self.tiffin_maker_id:
            st.error("Tiffin maker profile not found. Please contact admin.")
            return
        
        # Navigation
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Orders", "🍽️ Menu Management", "📊 Analytics", "🏪 Profile"])
        
        with tab1:
            self.show_orders()
        with tab2:
            self.show_menu_management()
        with tab3:
            self.show_analytics()
        with tab4:
            self.show_profile()
    
    def show_orders(self):
        """Display orders for tiffin maker"""
        st.subheader("📋 Orders")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"]
            )
        
        with col2:
            date_filter = st.date_input(
                "Filter by Date",
                value=datetime.now().date()
            )
        
        # Build query
        query = """
            SELECT o.*, u.full_name, u.phone, u.address
            FROM orders o
            JOIN users u ON o.customer_id = u.id
            WHERE o.tiffin_maker_id = %s
        """
        params = [self.tiffin_maker_id]
        
        if status_filter != "All":
            query += " AND o.status = %s"
            params.append(status_filter)
        
        query += " AND o.delivery_date = %s ORDER BY o.created_at DESC"
        params.append(date_filter)
        
        orders = db.execute_query(query, tuple(params))
        
        if not orders:
            st.info("No orders found for the selected criteria.")
            return
        
        # Display orders
        for order in orders:
            with st.expander(f"Order #{order['id']} - {order['full_name']} - ₹{order['total_amount']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Customer:** {order['full_name']}")
                    st.markdown(f"**Phone:** {order['phone']}")
                    st.markdown(f"**Address:** {order['delivery_address']}")
                    if order['special_instructions']:
                        st.markdown(f"**Special Instructions:** {order['special_instructions']}")
                
                with col2:
                    st.markdown(f"**Order Date:** {order['order_date']}")
                    st.markdown(f"**Delivery Date:** {order['delivery_date']}")
                    st.markdown(f"**Payment:** {order['payment_method']}")
                    st.markdown(f"**Total:** ₹{order['total_amount']}")
                
                with col3:
                    st.markdown(f"**Status:** {order['status'].title()}")
                    
                    # Status update buttons
                    if order['status'] == 'pending':
                        if st.button("Confirm Order", key=f"confirm_{order['id']}"):
                            self.update_order_status(order['id'], 'confirmed')
                            st.success("Order confirmed!")
                            st.rerun()
                    
                    elif order['status'] == 'confirmed':
                        if st.button("Start Preparing", key=f"prepare_{order['id']}"):
                            self.update_order_status(order['id'], 'preparing')
                            st.success("Started preparing!")
                            st.rerun()
                    
                    elif order['status'] == 'preparing':
                        if st.button("Out for Delivery", key=f"deliver_{order['id']}"):
                            self.update_order_status(order['id'], 'out_for_delivery')
                            st.success("Marked as out for delivery!")
                            st.rerun()
                    
                    elif order['status'] == 'out_for_delivery':
                        if st.button("Delivered", key=f"delivered_{order['id']}"):
                            self.update_order_status(order['id'], 'delivered')
                            st.success("Order delivered!")
                            st.rerun()
                    
                    # Cancel order option
                    if order['status'] in ['pending', 'confirmed']:
                        if st.button("Cancel Order", key=f"cancel_{order['id']}"):
                            self.update_order_status(order['id'], 'cancelled')
                            st.success("Order cancelled!")
                            st.rerun()
                
                # Show order items
                order_items = db.execute_query("""
                    SELECT oi.*, mi.name, mi.description
                    FROM order_items oi
                    JOIN menu_items mi ON oi.menu_item_id = mi.id
                    WHERE oi.order_id = %s
                """, (order['id'],))
                
                st.markdown("**Order Items:**")
                for item in order_items:
                    st.markdown(f"- {item['name']} x{item['quantity']} @ ₹{item['price_per_unit']}")
    
    def update_order_status(self, order_id, new_status):
        """Update order status"""
        return db.execute_update(
            "UPDATE orders SET status = %s WHERE id = %s",
            (new_status, order_id)
        )
    
    def show_menu_management(self):
        """Manage menu items"""
        st.subheader("🍽️ Menu Management")
        
        # Add new menu item
        with st.expander("➕ Add New Menu Item"):
            with st.form("add_menu_item"):
                name = st.text_input("Item Name")
                description = st.text_area("Description")
                price = st.number_input("Price (₹)", min_value=0.0, value=0.0)
                day_of_week = st.selectbox("Day of Week", list(WEEKLY_MENU.keys()))
                is_available = st.checkbox("Available", value=True)
                
                if st.form_submit_button("Add Item"):
                    if name and price > 0:
                        success = db.execute_update("""
                            INSERT INTO menu_items (name, description, price, day_of_week, tiffin_maker_id, is_available)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (name, description, price, day_of_week, self.tiffin_maker_id, is_available))
                        
                        if success:
                            st.success("Menu item added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add menu item.")
                    else:
                        st.error("Please fill in all required fields.")
        
        # View and edit existing menu items
        st.markdown("### Current Menu Items")
        
        menu_items = db.execute_query("""
            SELECT * FROM menu_items WHERE tiffin_maker_id = %s ORDER BY day_of_week, name
        """, (self.tiffin_maker_id,))
        
        if not menu_items:
            st.info("No menu items found. Add your first item above!")
            return
        
        for item in menu_items:
            with st.expander(f"{item['name']} - ₹{item['price']} ({item['day_of_week']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Name:** {item['name']}")
                    st.markdown(f"**Description:** {item['description']}")
                    st.markdown(f"**Price:** ₹{item['price']}")
                
                with col2:
                    st.markdown(f"**Day:** {item['day_of_week']}")
                    st.markdown(f"**Available:** {'Yes' if item['is_available'] else 'No'}")
                    
                    # Toggle availability
                    if st.button("Toggle Availability", key=f"toggle_{item['id']}"):
                        new_status = not item['is_available']
                        db.execute_update(
                            "UPDATE menu_items SET is_available = %s WHERE id = %s",
                            (new_status, item['id'])
                        )
                        st.success("Availability updated!")
                        st.rerun()
                    
                    # Delete item
                    if st.button("Delete Item", key=f"delete_{item['id']}"):
                        db.execute_update("DELETE FROM menu_items WHERE id = %s", (item['id'],))
                        st.success("Item deleted!")
                        st.rerun()
    
    def show_analytics(self):
        """Show analytics and insights"""
        st.subheader("📊 Analytics")
        
        # Get date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date())
        
        # Revenue analytics
        revenue_data = db.execute_query("""
            SELECT DATE(created_at) as date, SUM(total_amount) as daily_revenue
            FROM orders 
            WHERE tiffin_maker_id = %s 
            AND created_at BETWEEN %s AND %s
            AND status != 'cancelled'
            GROUP BY DATE(created_at)
            ORDER BY date
        """, (self.tiffin_maker_id, start_date, end_date))
        
        if revenue_data:
            st.markdown("### Revenue Trend")
            df_revenue = pd.DataFrame(revenue_data)
            st.line_chart(df_revenue.set_index('date')['daily_revenue'])
            
            total_revenue = sum(item['daily_revenue'] for item in revenue_data)
            st.metric("Total Revenue", f"₹{total_revenue}")
        
        # Order status distribution
        status_data = db.execute_query("""
            SELECT status, COUNT(*) as count
            FROM orders 
            WHERE tiffin_maker_id = %s 
            AND created_at BETWEEN %s AND %s
            GROUP BY status
        """, (self.tiffin_maker_id, start_date, end_date))
        
        if status_data:
            st.markdown("### Order Status Distribution")
            df_status = pd.DataFrame(status_data)
            st.bar_chart(df_status.set_index('status')['count'])
        
        # Popular items
        popular_items = db.execute_query("""
            SELECT mi.name, SUM(oi.quantity) as total_ordered
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.tiffin_maker_id = %s 
            AND o.created_at BETWEEN %s AND %s
            AND o.status != 'cancelled'
            GROUP BY mi.id, mi.name
            ORDER BY total_ordered DESC
            LIMIT 5
        """, (self.tiffin_maker_id, start_date, end_date))
        
        if popular_items:
            st.markdown("### Most Popular Items")
            for item in popular_items:
                st.markdown(f"- **{item['name']}**: {item['total_ordered']} orders")
    
    def show_profile(self):
        """Display tiffin maker profile"""
        st.subheader("🏪 My Profile")
        
        # Get tiffin maker info
        tiffin_maker_info = db.execute_query("""
            SELECT tm.*, u.full_name, u.email, u.phone, u.address
            FROM tiffin_makers tm
            JOIN users u ON tm.user_id = u.id
            WHERE tm.id = %s
        """, (self.tiffin_maker_id,))[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Business Name:** {tiffin_maker_info['business_name']}")
            st.markdown(f"**Location:** {tiffin_maker_info['location']}")
            st.markdown(f"**Cuisine Specialty:** {tiffin_maker_info['cuisine_specialty']}")
            st.markdown(f"**Rating:** ⭐ {tiffin_maker_info['rating']}")
        
        with col2:
            st.markdown(f"**Owner:** {tiffin_maker_info['full_name']}")
            st.markdown(f"**Email:** {tiffin_maker_info['email']}")
            st.markdown(f"**Phone:** {tiffin_maker_info['phone']}")
            st.markdown(f"**Status:** {'Active' if tiffin_maker_info['is_active'] else 'Inactive'}")
        
        st.markdown("**Address:**")
        st.markdown(tiffin_maker_info['address'])
        
        # Edit profile
        with st.expander("Edit Profile"):
            st.info("Profile editing feature coming soon!") 