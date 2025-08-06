# 🏗️ Home Flavours - Project Structure

## 📁 Organized Folder Structure

```
Home Flavours/
├── 📁 frontend/                    # Frontend/UI Components
│   ├── simple_main.py             # Main Streamlit application (working version)
│   ├── main_mysql.py              # MySQL version of main app
│   ├── admin_dashboard.py         # Admin dashboard components
│   ├── tiffin_maker_dashboard.py  # Tiffin maker dashboard components
│   └── user_dashboard.py          # Customer dashboard components
│
├── 📁 backend/                     # Backend/Logic Components
│   ├── auth.py                    # Authentication system
│   ├── config.py                  # Application configuration
│   ├── database.py                # Database connection and operations
│   ├── database_config.py         # Database configuration
│   ├── setup_database.py          # Database setup utilities
│   ├── configure_password.py      # Password configuration
│   └── test_mysql.py              # MySQL connection testing
│
├── 📁 database/                    # Database Configuration
│   ├── .env                       # Environment variables
│   └── env_example.txt            # Environment template
│
├── 📁 docs/                        # Documentation
│   ├── README.md                  # Main project documentation
│   ├── QUICK_START.md             # Quick start guide
│   ├── MYSQL_SETUP_GUIDE.md       # MySQL setup instructions
│   ├── MYSQL_WORKBENCH_GUIDE.md   # MySQL Workbench guide
│   └── DESIGN_ENHANCEMENTS.md     # Design improvements
│
├── 📄 main.py                      # Main entry point
├── 📄 setup.py                     # Project setup script
├── 📄 requirements.txt             # Python dependencies
├── 📄 simple_requirements.txt      # Minimal dependencies
└── 📄 PROJECT_STRUCTURE.md         # This file
```

## 🎯 **Folder Purposes**

### 📁 **frontend/**
Contains all user interface components and Streamlit applications:
- **simple_main.py**: Main working application (recommended)
- **main_mysql.py**: Full-featured version with MySQL
- **admin_dashboard.py**: Admin interface components
- **tiffin_maker_dashboard.py**: Tiffin maker interface
- **user_dashboard.py**: Customer interface

### 📁 **backend/**
Contains all business logic and backend functionality:
- **auth.py**: User authentication and session management
- **config.py**: Application settings and configuration
- **database.py**: Database operations and connections
- **database_config.py**: Database setup and configuration
- **setup_database.py**: Database initialization utilities
- **configure_password.py**: Password management
- **test_mysql.py**: Database connection testing

### 📁 **database/**
Contains database configuration files:
- **.env**: Environment variables (database credentials)
- **env_example.txt**: Template for environment setup

### 📁 **docs/**
Contains all project documentation:
- **README.md**: Main project overview
- **QUICK_START.md**: Getting started guide
- **MYSQL_SETUP_GUIDE.md**: MySQL installation guide
- **MYSQL_WORKBENCH_GUIDE.md**: Database viewing guide
- **DESIGN_ENHANCEMENTS.md**: UI/UX improvements

## 🚀 **How to Run the Application**

### Option 1: Run from Root Directory (Recommended)
```bash
python -m streamlit run main.py
```

### Option 2: Run Frontend Directly
```bash
python -m streamlit run frontend/simple_main.py
```

### Option 3: Run MySQL Version
```bash
python -m streamlit run frontend/main_mysql.py
```

## 🔧 **Development Workflow**

### Adding New Frontend Components:
1. Create new files in `frontend/` folder
2. Import from `backend/` for business logic
3. Update main.py if needed

### Adding New Backend Logic:
1. Create new files in `backend/` folder
2. Keep database operations in `backend/`
3. Import in frontend components as needed

### Database Changes:
1. Update files in `backend/` folder
2. Modify `database/.env` for configuration
3. Test with `backend/test_mysql.py`

## 📊 **Database Structure**

The application uses MySQL with these tables:
- **users**: User accounts and profiles
- **tiffin_makers**: Tiffin maker businesses
- **menu_items**: Available menu items
- **orders**: Customer orders
- **order_items**: Items in each order

## 🎨 **Features by Component**

### Frontend Features:
- ✅ Multi-user authentication interface
- ✅ Responsive dashboard designs
- ✅ Shopping cart functionality
- ✅ Order management interface
- ✅ Menu browsing system

### Backend Features:
- ✅ User authentication system
- ✅ Database connection management
- ✅ Session handling
- ✅ Data validation
- ✅ Business logic implementation

### Database Features:
- ✅ MySQL integration
- ✅ Demo data setup
- ✅ Environment configuration
- ✅ Connection testing

## 🔍 **File Dependencies**

### Frontend Dependencies:
- `frontend/simple_main.py` → `backend/auth.py`
- `frontend/admin_dashboard.py` → `backend/database.py`
- `frontend/user_dashboard.py` → `backend/config.py`

### Backend Dependencies:
- `backend/database.py` → `backend/config.py`
- `backend/auth.py` → `backend/database.py`
- `backend/setup_database.py` → `database/.env`

## 🎉 **Benefits of This Structure**

1. **🧹 Clean Organization**: Files are logically grouped
2. **🔧 Easy Maintenance**: Related files are together
3. **📚 Clear Documentation**: All docs in one place
4. **🚀 Simple Deployment**: Clear entry points
5. **🔄 Scalable**: Easy to add new features
6. **👥 Team Friendly**: Clear separation of concerns

This organized structure makes the project more professional and easier to maintain! 🏠🍽️✨ 