# Silver Jewellery Shop - Complete Setup Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- pip and npm

## Backend Setup

### Step 1: Clean install (if you have issues)
```bash
cd silver-jewellery-shop/backend

# Uninstall Django if corrupted
pip uninstall django -y

# Install setuptools first
pip install --upgrade pip setuptools

# Install Django separately first
pip install Django==5.1.4

# Then install all other dependencies
pip install -r requirements.txt
```

### Step 2: Verify Django installation
```bash
python -c "import django; print(django.get_version())"
# Should print: 4.2.7
```

### Step 3: Configure Database
Edit `.env` file and update your PostgreSQL credentials:
```
DB_PASSWORD=your_actual_postgres_password
```

### Step 4: Create Database (if not exists)
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE silver_jewellery_db;
\q
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
# Enter phone number (e.g., 9876543210)
# Enter name
# Enter password
```

### Step 7: Start Backend Server
```bash
python manage.py runserver
```

Backend will be available at: http://localhost:8000

## Frontend Setup

### Step 1: Install Dependencies
```bash
cd silver-jewellery-shop/frontend
npm install
```

### Step 2: Start Frontend Server
```bash
npm start
```

Frontend will be available at: http://localhost:4200

## Access Points

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'pkg_resources'
**Solution**: Install setuptools first
```bash
pip install --upgrade setuptools
```

### Issue: Password authentication failed for user "postgres"
**Solution**: Update DB_PASSWORD in .env file with correct PostgreSQL password

### Issue: relation "users" does not exist
**Solution**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Circular dependency error
**Solution**: Delete all migration files and recreate
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

## Quick Start Commands

### Backend
```bash
cd silver-jewellery-shop/backend
pip install --upgrade pip setuptools
pip install -r requirements.txt
# Update .env with your database password
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd silver-jewellery-shop/frontend
npm install
npm start
```

## Features

### Customer Features
- Phone number authentication
- Browse 7 jewellery categories
- Product search and filtering
- Shopping cart
- Razorpay payment integration
- Order tracking

### Admin Features
- Product management (CRUD)
- Category management
- Order management
- Banner management
- User management

## Categories
1. Chain with Pendant
2. Ear Rings
3. Pendant
4. Gold Polish Looks
5. Rings
6. Anklets
7. Bracelets

## Tech Stack
- **Backend**: Django 4.2.7, Django REST Framework, PostgreSQL
- **Frontend**: Angular 17
- **Payment**: Razorpay
- **Authentication**: JWT

## Support
For issues, check the troubleshooting section above or refer to the main README.md