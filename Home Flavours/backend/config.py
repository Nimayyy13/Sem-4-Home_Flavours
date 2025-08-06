import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'home_flavours'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Application Configuration
APP_CONFIG = {
    'title': 'Home Flavours',
    'page_icon': '🍽️',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Menu Configuration
WEEKLY_MENU = {
    'Monday': [
        {'name': 'Dal Khichdi with Ghee', 'price': 80, 'description': 'Comforting rice and lentil dish'},
        {'name': 'Roti Sabzi with Dal', 'price': 90, 'description': 'Fresh rotis with seasonal vegetables'},
        {'name': 'Pulao with Raita', 'price': 100, 'description': 'Fragrant rice with cooling raita'},
        {'name': 'Thali Special', 'price': 120, 'description': 'Complete meal with 3 sabzis, dal, rice, roti'}
    ],
    'Tuesday': [
        {'name': 'Rajma Chawal', 'price': 85, 'description': 'Kidney beans with steamed rice'},
        {'name': 'Aloo Paratha with Curd', 'price': 75, 'description': 'Stuffed potato bread with yogurt'},
        {'name': 'Mixed Vegetable Curry', 'price': 95, 'description': 'Assorted vegetables in rich gravy'},
        {'name': 'Biryani Special', 'price': 130, 'description': 'Aromatic rice with tender meat/vegetables'}
    ],
    'Wednesday': [
        {'name': 'Chole Bhature', 'price': 90, 'description': 'Chickpeas with fluffy bread'},
        {'name': 'Kadhi Pakora', 'price': 80, 'description': 'Yogurt curry with gram flour fritters'},
        {'name': 'Paneer Butter Masala', 'price': 110, 'description': 'Cottage cheese in rich tomato gravy'},
        {'name': 'South Indian Thali', 'price': 125, 'description': 'Rice, sambar, rasam, curd rice'}
    ],
    'Thursday': [
        {'name': 'Masala Dosa', 'price': 85, 'description': 'Crispy rice crepe with potato filling'},
        {'name': 'Dal Makhani', 'price': 95, 'description': 'Creamy black lentils'},
        {'name': 'Mixed Veg Pulao', 'price': 100, 'description': 'Vegetable rice with raita'},
        {'name': 'Gujarati Thali', 'price': 115, 'description': 'Traditional Gujarati meal'}
    ],
    'Friday': [
        {'name': 'Fish Curry with Rice', 'price': 140, 'description': 'Spicy fish curry with steamed rice'},
        {'name': 'Chicken Biryani', 'price': 150, 'description': 'Aromatic chicken rice dish'},
        {'name': 'Veg Fried Rice', 'price': 90, 'description': 'Chinese style vegetable rice'},
        {'name': 'North Indian Thali', 'price': 130, 'description': 'Complete North Indian meal'}
    ],
    'Saturday': [
        {'name': 'Pav Bhaji', 'price': 80, 'description': 'Spicy vegetable mash with bread'},
        {'name': 'Idli Sambar', 'price': 75, 'description': 'Steamed rice cakes with lentil soup'},
        {'name': 'Mushroom Masala', 'price': 100, 'description': 'Mushrooms in spicy gravy'},
        {'name': 'Maharashtrian Thali', 'price': 120, 'description': 'Traditional Maharashtrian meal'}
    ],
    'Sunday': [
        {'name': 'Butter Chicken', 'price': 160, 'description': 'Creamy tomato-based chicken curry'},
        {'name': 'Palak Paneer', 'price': 110, 'description': 'Spinach with cottage cheese'},
        {'name': 'Jeera Rice with Dal', 'price': 85, 'description': 'Cumin rice with lentil soup'},
        {'name': 'Special Sunday Thali', 'price': 140, 'description': 'Festive Sunday meal'}
    ]
} 