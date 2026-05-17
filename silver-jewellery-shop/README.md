# Silver Jewellery E-Commerce Website

A full-stack e-commerce platform for selling 925 silver jewellery with Angular frontend, Django backend, PostgreSQL database, and Razorpay payment integration.

## Features

### Customer Features
- User authentication with phone number
- Browse silver jewellery by categories
- Product search and filtering
- Product details with multiple images
- Shopping cart management
- Razorpay payment integration
- Order tracking
- Product reviews and ratings

### Admin Features
- Product management (CRUD operations)
- Category management
- Order management
- Banner/notification management
- User management
- Inventory tracking

### Categories
1. Chain with Pendant
2. Ear Rings
3. Pendant
4. Gold Polish Looks
5. Rings
6. Anklets
7. Bracelets

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **Payment Gateway**: Razorpay
- **Image Handling**: Pillow

### Frontend
- **Framework**: Angular 17
- **HTTP Client**: Angular HttpClient
- **State Management**: RxJS
- **Styling**: CSS

## Project Structure

```
silver-jewellery-shop/
├── backend/
│   ├── jewellery_shop/          # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                    # User management app
│   │   ├── models.py            # User, Order, Cart, Enquiry models
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── products/                 # Product management app
│   │   ├── models.py            # Product, Category, Review models
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── notifications/            # Banner/notification app
│   │   ├── models.py            # Banner model
│   │   ├── views.py
│   │   └── urls.py
│   ├── payments/                 # Payment processing app
│   │   ├── models.py            # Payment model
│   │   ├── views.py
│   │   └── urls.py
│   ├── requirements.txt
│   ├── manage.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/      # Angular components
│   │   │   │   ├── login/
│   │   │   │   ├── landing/
│   │   │   │   ├── product-list/
│   │   │   │   ├── product-detail/
│   │   │   │   ├── cart/
│   │   │   │   └── admin/
│   │   │   ├── services/        # Angular services
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── product.service.ts
│   │   │   │   ├── cart.service.ts
│   │   │   │   └── payment.service.ts
│   │   │   ├── models/          # TypeScript interfaces
│   │   │   │   ├── user.model.ts
│   │   │   │   └── product.model.ts
│   │   │   └── guards/          # Route guards
│   │   │       └── auth.guard.ts
│   │   ├── environments/
│   │   └── assets/
│   ├── package.json
│   ├── angular.json
│   └── tsconfig.json
└── README.md
```

## Database Schema

### Users Table
- id, phone_number, name, email, role (admin/user)
- password, is_active, date_joined

### Products Table
- id, name, title, description, category
- price, discounted_price, image (multiple)
- in_stock, stock_quantity, weight, purity
- slug, is_featured, views_count

### Categories Table
- id, name, display_name, description, image

### Orders Table
- id, order_id, user, total_amount, status
- shipping_address, phone_number
- payment_id, payment_status, created_at

### Cart Table
- id, user, product, quantity, added_at

### Banners Table
- id, title, description, image, discount_offer
- is_visible, display_order, start_date, end_date

### Payments Table
- id, order, razorpay_order_id, razorpay_payment_id
- amount, currency, status, created_at

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Razorpay Account

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE silver_jewellery_db;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE silver_jewellery_db TO postgres;
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your settings:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=silver_jewellery_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   Edit `src/environments/environment.ts`:
   ```typescript
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api',
     razorpayKeyId: 'YOUR_RAZORPAY_KEY_ID'
   };
   ```

4. **Run development server**
   ```bash
   npm start
   ```

Frontend will be available at `http://localhost:4200`

## API Endpoints

### Authentication
- `POST /api/users/users/` - Register user
- `POST /api/users/users/login/` - Login
- `GET /api/users/users/profile/` - Get user profile
- `PUT /api/users/users/update_profile/` - Update profile

### Products
- `GET /api/products/categories/` - List categories
- `GET /api/products/products/` - List products
- `GET /api/products/products/{id}/` - Product detail
- `GET /api/products/products/featured/` - Featured products
- `GET /api/products/products/search/?q={query}` - Search products
- `POST /api/products/products/` - Create product (Admin)
- `PUT /api/products/products/{id}/` - Update product (Admin)
- `DELETE /api/products/products/{id}/` - Delete product (Admin)

### Cart
- `GET /api/users/cart/` - Get cart items
- `POST /api/users/cart/` - Add to cart
- `PATCH /api/users/cart/{id}/` - Update cart item
- `DELETE /api/users/cart/{id}/` - Remove from cart
- `DELETE /api/users/cart/clear/` - Clear cart
- `GET /api/users/cart/total/` - Get cart total

### Orders
- `GET /api/users/orders/` - List orders
- `GET /api/users/orders/{id}/` - Order detail
- `POST /api/users/orders/{id}/cancel/` - Cancel order

### Payments
- `POST /api/payments/create_order/` - Create Razorpay order
- `POST /api/payments/verify_payment/` - Verify payment
- `POST /api/payments/payment_failed/` - Handle payment failure

### Banners
- `GET /api/notifications/banners/` - List active banners
- `POST /api/notifications/banners/` - Create banner (Admin)

## Admin Panel

Access Django admin at `http://localhost:8000/admin`

Features:
- Manage products, categories, and inventory
- View and manage orders
- Manage users and permissions
- Configure banners and promotions
- View payment transactions

## Payment Integration

The application uses Razorpay for payment processing:

1. User adds items to cart
2. Proceeds to checkout with shipping details
3. Razorpay payment modal opens
4. User completes payment
5. Payment verification on backend
6. Order confirmation and cart clearance

## Development Notes

- Backend runs on port 8000
- Frontend runs on port 4200
- CORS is configured for local development
- JWT tokens expire after 24 hours
- Media files are stored in `backend/media/`
- Static files are collected in `backend/staticfiles/`

## Production Deployment

### Backend
1. Set `DEBUG=False` in environment
2. Configure allowed hosts
3. Set up proper database credentials
4. Configure static/media file serving (e.g., AWS S3)
5. Use production WSGI server (Gunicorn)
6. Set up SSL certificate

### Frontend
1. Build production bundle: `ng build --configuration production`
2. Deploy to web server (Nginx, Apache)
3. Configure environment variables
4. Set up SSL certificate

## Security Considerations

- Use strong SECRET_KEY in production
- Enable HTTPS
- Implement rate limiting
- Validate all user inputs
- Use environment variables for sensitive data
- Regular security updates
- Implement CSRF protection
- Use secure password hashing

## Support

For issues and questions, please create an issue in the repository.

## License

This project is proprietary software.