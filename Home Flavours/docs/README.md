# 🏠 Home Flavours - Homemade Tiffin Service

A comprehensive web application for connecting customers with local home chefs for delicious homemade tiffin services. Built with Streamlit and MySQL.

## 🌟 Features

### 👥 Multi-User System
- **Customer Dashboard**: Browse menus, add to cart, place orders
- **Tiffin Maker Dashboard**: Manage orders, menu items, and analytics
- **Admin Dashboard**: Monitor system, manage users and orders

### 🍽️ Menu Management
- Weekly rotating menu with 3-4 options per day
- Location-based tiffin maker discovery
- Real-time menu availability updates

### 🛒 Order System
- Shopping cart functionality
- Multiple payment options (COD/GPay)
- Order tracking and status updates
- Special instructions support

### 📊 Analytics & Monitoring
- Revenue tracking and analytics
- Order status distribution
- Popular items analysis
- User activity monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd home-flavours
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database**
   - Create a MySQL database named `home_flavours`
   - Update database credentials in `env_example.txt` and rename to `.env`

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

## 🗄️ Database Setup

The application will automatically create all necessary tables on first run. The database schema includes:

- **users**: User accounts and profiles
- **tiffin_makers**: Home chef business profiles
- **menu_items**: Available food items
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **cart**: Shopping cart items

## 👤 Demo Accounts

The application creates demo accounts on first run:

### Admin Account
- Username: `admin`
- Password: `admin123`
- Email: `admin@homeflavours.com`

### Tiffin Maker Account
- Username: `chef1`
- Password: `chef123`
- Email: `chef1@homeflavours.com`

### Customer Account
- Username: `customer1`
- Password: `customer123`
- Email: `customer1@homeflavours.com`

## 📱 User Guide

### For Customers
1. **Register/Login**: Create an account or login with existing credentials
2. **Browse Menu**: Explore daily specials and weekly menu options
3. **Add to Cart**: Select items and quantities
4. **Place Order**: Choose delivery date, payment method, and place order
5. **Track Orders**: Monitor order status and delivery progress

### For Tiffin Makers
1. **Register as Tiffin Maker**: Create account with tiffin maker role
2. **Setup Profile**: Add business details, location, and cuisine specialty
3. **Manage Menu**: Add/edit menu items for different days
4. **Handle Orders**: Confirm, prepare, and deliver orders
5. **View Analytics**: Monitor revenue and popular items

### For Admins
1. **System Overview**: Monitor overall system metrics
2. **User Management**: Manage customer and tiffin maker accounts
3. **Order Monitoring**: Track all orders and resolve issues
4. **Tiffin Maker Management**: Approve and manage home chefs
5. **System Settings**: Configure application settings

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **Authentication**: Custom session management
- **Charts**: Plotly
- **Styling**: Custom CSS

## 📁 Project Structure

```
home-flavours/
├── main.py                 # Main application entry point
├── config.py              # Configuration and settings
├── database.py            # Database connection and operations
├── auth.py                # Authentication and user management
├── user_dashboard.py      # Customer dashboard
├── tiffin_maker_dashboard.py  # Tiffin maker dashboard
├── admin_dashboard.py     # Admin dashboard
├── requirements.txt       # Python dependencies
├── env_example.txt       # Environment variables template
└── README.md             # Project documentation
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env_example.txt`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=home_flavours
DB_PORT=3306
```

### Weekly Menu Configuration
Edit `config.py` to customize the weekly menu options for each day.

## 🚀 Deployment

### Local Development
```bash
streamlit run main.py
```

### Production Deployment
1. Set up a production MySQL server
2. Configure environment variables
3. Use a process manager like PM2 or systemd
4. Set up reverse proxy (nginx) if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Mobile app development
- Real-time notifications
- Advanced analytics
- Payment gateway integration
- Rating and review system
- Delivery tracking
- Multi-language support

---

**Made with ❤️ for homemade food lovers** 