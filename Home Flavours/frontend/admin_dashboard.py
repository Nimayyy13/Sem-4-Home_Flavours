import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import db
from auth import auth

class AdminDashboard:
    def __init__(self):
        self.current_user = auth.get_current_user()
    
    def show_dashboard(self):
        """Main admin dashboard"""
        st.title("👨‍💼 Home Flavours - Admin Dashboard")
        st.markdown(f"Welcome back, **{self.current_user['full_name']}**!")
        
        # Navigation
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", "👥 Users", "📋 Orders", "🏪 Tiffin Makers", "⚙️ Settings"
        ])
        
        with tab1:
            self.show_overview()
        with tab2:
            self.show_users()
        with tab3:
            self.show_orders()
        with tab4:
            self.show_tiffin_makers()
        with tab5:
            self.show_settings()
    
    def show_overview(self):
        """Show system overview and analytics"""
        st.subheader("📊 System Overview")
        
        # Get date range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", value=datetime.now().date())
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        # Total users
        total_users = db.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
        with col1:
            st.metric("Total Users", total_users)
        
        # Total orders
        total_orders = db.execute_query("""
            SELECT COUNT(*) as count FROM orders 
            WHERE created_at BETWEEN %s AND %s
        """, (start_date, end_date))[0]['count']
        with col2:
            st.metric("Total Orders", total_orders)
        
        # Total revenue
        total_revenue = db.execute_query("""
            SELECT SUM(total_amount) as total FROM orders 
            WHERE created_at BETWEEN %s AND %s AND status != 'cancelled'
        """, (start_date, end_date))[0]['total'] or 0
        with col3:
            st.metric("Total Revenue", f"₹{total_revenue}")
        
        # Active tiffin makers
        active_makers = db.execute_query("SELECT COUNT(*) as count FROM tiffin_makers WHERE is_active = TRUE")[0]['count']
        with col4:
            st.metric("Active Tiffin Makers", active_makers)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Order status distribution
            status_data = db.execute_query("""
                SELECT status, COUNT(*) as count
                FROM orders 
                WHERE created_at BETWEEN %s AND %s
                GROUP BY status
            """, (start_date, end_date))
            
            if status_data:
                df_status = pd.DataFrame(status_data)
                fig_status = px.pie(df_status, values='count', names='status', title='Order Status Distribution')
                st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Revenue trend
            revenue_data = db.execute_query("""
                SELECT DATE(created_at) as date, SUM(total_amount) as daily_revenue
                FROM orders 
                WHERE created_at BETWEEN %s AND %s AND status != 'cancelled'
                GROUP BY DATE(created_at)
                ORDER BY date
            """, (start_date, end_date))
            
            if revenue_data:
                df_revenue = pd.DataFrame(revenue_data)
                fig_revenue = px.line(df_revenue, x='date', y='daily_revenue', title='Revenue Trend')
                st.plotly_chart(fig_revenue, use_container_width=True)
        
        # Recent activity
        st.markdown("### Recent Activity")
        recent_orders = db.execute_query("""
            SELECT o.*, u.full_name, tm.business_name
            FROM orders o
            JOIN users u ON o.customer_id = u.id
            JOIN tiffin_makers tm ON o.tiffin_maker_id = tm.id
            ORDER BY o.created_at DESC
            LIMIT 10
        """)
        
        if recent_orders:
            for order in recent_orders:
                st.markdown(f"**Order #{order['id']}** - {order['full_name']} → {order['business_name']} - ₹{order['total_amount']} ({order['status']})")
        else:
            st.info("No recent orders")
    
    def show_users(self):
        """Manage users"""
        st.subheader("👥 User Management")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            user_type_filter = st.selectbox("Filter by Type", ["All", "customer", "tiffin_maker", "admin"])
        with col2:
            search_term = st.text_input("Search by name or email")
        
        # Build query
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        
        if user_type_filter != "All":
            query += " AND user_type = %s"
            params.append(user_type_filter)
        
        if search_term:
            query += " AND (full_name LIKE %s OR email LIKE %s)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        query += " ORDER BY created_at DESC"
        
        users = db.execute_query(query, tuple(params))
        
        if not users:
            st.info("No users found.")
            return
        
        # Display users
        for user in users:
            with st.expander(f"{user['full_name']} ({user['user_type']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Name:** {user['full_name']}")
                    st.markdown(f"**Email:** {user['email']}")
                    st.markdown(f"**Phone:** {user['phone']}")
                
                with col2:
                    st.markdown(f"**Username:** {user['username']}")
                    st.markdown(f"**Type:** {user['user_type'].title()}")
                    st.markdown(f"**Joined:** {user['created_at'].strftime('%B %Y')}")
                
                with col3:
                    # Actions
                    if st.button("View Details", key=f"view_{user['id']}"):
                        st.markdown(f"**Address:** {user['address']}")
                    
                    if st.button("Delete User", key=f"delete_{user['id']}"):
                        if user['user_type'] != 'admin':
                            db.execute_update("DELETE FROM users WHERE id = %s", (user['id'],))
                            st.success("User deleted!")
                            st.rerun()
                        else:
                            st.error("Cannot delete admin user!")
    
    def show_orders(self):
        """Manage orders"""
        st.subheader("📋 Order Management")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"]
            )
        
        with col2:
            date_filter = st.date_input("Filter by Date", value=datetime.now().date())
        
        with col3:
            search_term = st.text_input("Search by customer name")
        
        # Build query
        query = """
            SELECT o.*, u.full_name, u.phone, tm.business_name
            FROM orders o
            JOIN users u ON o.customer_id = u.id
            JOIN tiffin_makers tm ON o.tiffin_maker_id = tm.id
            WHERE 1=1
        """
        params = []
        
        if status_filter != "All":
            query += " AND o.status = %s"
            params.append(status_filter)
        
        query += " AND o.delivery_date = %s"
        params.append(date_filter)
        
        if search_term:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{search_term}%")
        
        query += " ORDER BY o.created_at DESC"
        
        orders = db.execute_query(query, tuple(params))
        
        if not orders:
            st.info("No orders found for the selected criteria.")
            return
        
        # Display orders
        for order in orders:
            with st.expander(f"Order #{order['id']} - {order['full_name']} → {order['business_name']} - ₹{order['total_amount']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Customer:** {order['full_name']}")
                    st.markdown(f"**Phone:** {order['phone']}")
                    st.markdown(f"**Address:** {order['delivery_address']}")
                    if order['special_instructions']:
                        st.markdown(f"**Special Instructions:** {order['special_instructions']}")
                
                with col2:
                    st.markdown(f"**Tiffin Maker:** {order['business_name']}")
                    st.markdown(f"**Order Date:** {order['order_date']}")
                    st.markdown(f"**Delivery Date:** {order['delivery_date']}")
                    st.markdown(f"**Payment:** {order['payment_method']}")
                
                with col3:
                    st.markdown(f"**Status:** {order['status'].title()}")
                    st.markdown(f"**Total:** ₹{order['total_amount']}")
                    
                    # Admin actions
                    if order['status'] == 'pending':
                        if st.button("Confirm Order", key=f"admin_confirm_{order['id']}"):
                            db.execute_update("UPDATE orders SET status = 'confirmed' WHERE id = %s", (order['id'],))
                            st.success("Order confirmed!")
                            st.rerun()
                    
                    if order['status'] in ['pending', 'confirmed']:
                        if st.button("Cancel Order", key=f"admin_cancel_{order['id']}"):
                            db.execute_update("UPDATE orders SET status = 'cancelled' WHERE id = %s", (order['id'],))
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
    
    def show_tiffin_makers(self):
        """Manage tiffin makers"""
        st.subheader("🏪 Tiffin Maker Management")
        
        # Add new tiffin maker
        with st.expander("➕ Add New Tiffin Maker"):
            with st.form("add_tiffin_maker"):
                col1, col2 = st.columns(2)
                
                with col1:
                    business_name = st.text_input("Business Name")
                    location = st.text_input("Location")
                    cuisine_specialty = st.text_input("Cuisine Specialty")
                
                with col2:
                    user_id = st.selectbox(
                        "Select User",
                        options=[(u['id'], f"{u['full_name']} ({u['email']})") 
                                for u in db.execute_query("SELECT id, full_name, email FROM users WHERE user_type = 'tiffin_maker'")]
                    )
                    rating = st.number_input("Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
                    is_active = st.checkbox("Active", value=True)
                
                if st.form_submit_button("Add Tiffin Maker"):
                    if business_name and location and user_id:
                        success = db.execute_update("""
                            INSERT INTO tiffin_makers (user_id, business_name, location, cuisine_specialty, rating, is_active)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (user_id[0], business_name, location, cuisine_specialty, rating, is_active))
                        
                        if success:
                            st.success("Tiffin maker added successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to add tiffin maker.")
                    else:
                        st.error("Please fill in all required fields.")
        
        # View existing tiffin makers
        st.markdown("### Current Tiffin Makers")
        
        tiffin_makers = db.execute_query("""
            SELECT tm.*, u.full_name, u.email, u.phone
            FROM tiffin_makers tm
            JOIN users u ON tm.user_id = u.id
            ORDER BY tm.business_name
        """)
        
        if not tiffin_makers:
            st.info("No tiffin makers found.")
            return
        
        for maker in tiffin_makers:
            with st.expander(f"{maker['business_name']} - {maker['location']} (⭐ {maker['rating']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Business:** {maker['business_name']}")
                    st.markdown(f"**Location:** {maker['location']}")
                    st.markdown(f"**Cuisine:** {maker['cuisine_specialty']}")
                
                with col2:
                    st.markdown(f"**Owner:** {maker['full_name']}")
                    st.markdown(f"**Email:** {maker['email']}")
                    st.markdown(f"**Phone:** {maker['phone']}")
                
                with col3:
                    st.markdown(f"**Rating:** ⭐ {maker['rating']}")
                    st.markdown(f"**Status:** {'Active' if maker['is_active'] else 'Inactive'}")
                    
                    # Actions
                    if st.button("Toggle Status", key=f"toggle_{maker['id']}"):
                        new_status = not maker['is_active']
                        db.execute_update(
                            "UPDATE tiffin_makers SET is_active = %s WHERE id = %s",
                            (new_status, maker['id'])
                        )
                        st.success("Status updated!")
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_maker_{maker['id']}"):
                        db.execute_update("DELETE FROM tiffin_makers WHERE id = %s", (maker['id'],))
                        st.success("Tiffin maker deleted!")
                        st.rerun()
    
    def show_settings(self):
        """System settings"""
        st.subheader("⚙️ System Settings")
        
        st.markdown("### Database Information")
        
        # Get database stats
        total_users = db.execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
        total_orders = db.execute_query("SELECT COUNT(*) as count FROM orders")[0]['count']
        total_tiffin_makers = db.execute_query("SELECT COUNT(*) as count FROM tiffin_makers")[0]['count']
        total_menu_items = db.execute_query("SELECT COUNT(*) as count FROM menu_items")[0]['count']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Users", total_users)
            st.metric("Total Orders", total_orders)
        
        with col2:
            st.metric("Total Tiffin Makers", total_tiffin_makers)
            st.metric("Total Menu Items", total_menu_items)
        
        st.markdown("### System Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear All Carts"):
                db.execute_update("DELETE FROM cart")
                st.success("All carts cleared!")
        
        with col2:
            if st.button("Reset Demo Data"):
                st.info("Demo data reset feature coming soon!")
        
        st.markdown("### Backup & Maintenance")
        st.info("Backup and maintenance features coming soon!") 