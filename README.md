# TeeStore - T-Shirt E-Commerce Platform

A modern e-commerce web application built with Django and Tailwind CSS for selling t-shirts online.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-blue.svg)

## Features

### For Customers
- **Product Browsing** - View all available t-shirts with images, prices, and sizes
- **Product Details** - Detailed view with size selection and quantity picker
- **Shopping Cart** - Add, update, or remove items from cart
- **Guest Cart** - Cart works for non-logged-in users (session-based)
- **Checkout** - Simple checkout with shipping information
- **Order History** - View past orders and their status
- **User Authentication** - Register, login, and logout

### For Admin
- **Product Management** - Add, edit, or delete products via Django Admin
- **Order Management** - View and manage customer orders
- **Stock Control** - Track inventory levels

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6.0 |
| Database | SQLite |
| Frontend | HTML + Tailwind CSS (CDN) |
| Icons | Heroicons (SVG) |
| Fonts | Inter (Google Fonts) |

## Project Structure

```
t-ecommerce/
├── manage.py                 # Django CLI
├── requirements.txt           # Dependencies
├── t_ecommerce/             # Project settings
│   ├── settings.py          # Configuration
│   └── urls.py              # Root URL configuration
├── accounts/                  # User authentication
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── store/                    # Product catalog
│   ├── models.py            # Product model
│   ├── views.py
│   └── urls.py
├── cart/                     # Shopping cart
│   ├── models.py            # CartItem model
│   ├── views.py             # Cart operations
│   ├── urls.py
│   └── context_processors.py # Cart data for all pages
├── orders/                   # Order management
│   ├── models.py            # Order & OrderItem models
│   ├── views.py
│   └── urls.py
├── core/                     # Core utilities
│   └── models.py            # Address model
├── templates/                # HTML templates
│   ├── base.html
│   ├── store/
│   ├── cart/
│   ├── orders/
│   ├── accounts/
│   └── includes/
├── static/                   # Static assets
└── media/                    # User uploads
```

## Core Concepts

### 1. Django Apps Architecture

The project follows Django's app-based architecture:

- **accounts/** - Handles user registration, login, logout using Django's built-in auth system
- **store/** - Manages product catalog with the Product model
- **cart/** - Handles shopping cart functionality with session support
- **orders/** - Manages order placement and order history

### 2. User Authentication Flow

```
Register → Login → Authenticated User
              ↓
    Can: Checkout, View Orders, Profile
```

- Uses Django's built-in `UserAuthenticationForm`
- Custom registration with email field
- Session-based cart for guests merges on login (optional enhancement)

### 3. Shopping Cart Strategy

**Guest Users:**
- Cart stored in session (`request.session.session_key`)
- Persists until session expires

**Logged-in Users:**
- Cart stored in database (`CartItem.user`)
- Persists across sessions

**Context Processor:**
- Cart data available in all templates via `cart_items_count` variable

### 4. Product Model

```python
Product:
├── name          # Product title
├── slug          # URL-friendly identifier
├── description   # Full description
├── price         # Decimal price
├── image         # Product photo
├── stock         # Inventory count
├── sizes         # Available sizes (stored as CSV: "S,M,L,XL")
└── is_active     # Product visibility
```

### 5. Order Flow

```
Cart → Checkout Form → Place Order → Order Created
                                   ↓
                         Stock decremented
                                   ↓
                         Cart cleared
                                   ↓
                         Order confirmation
```

### 6. Template Inheritance

All pages extend `base.html`:

```
base.html (navbar, footer, messages)
    ↓
    ├── home.html
    ├── product_list.html
    ├── product_detail.html
    ├── cart.html
    ├── checkout.html
    ├── order_history.html
    ├── order_detail.html
    ├── login.html
    ├── register.html
    └── profile.html
```

### 7. URL Routing

```
/                       → Home page (featured products)
/products/              → All products listing
/products/<slug>/       → Product detail page
/cart/                  → View cart
/cart/add/<id>/         → Add to cart
/cart/update/<id>/      → Update quantity
/cart/remove/<id>/      → Remove item
/orders/checkout/        → Checkout page
/orders/place-order/     → Submit order
/orders/                → Order history
/orders/<id>/           → Order detail
/accounts/login/         → Login
/accounts/register/      → Register
/accounts/logout/        → Logout
/accounts/profile/       → User profile
/admin/                  → Django admin
```

### 8. Database Schema

```
User (Django built-in)
    ↓
CartItem ←──────────── Product
    │ (FK)                 ↑
    │                      │
    └──── OrderItem ←──────┘ (FK)
             │
             └──── Order (FK)
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone or navigate to project:**
```bash
cd t-ecommerce
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create admin user:**
```bash
python manage.py createsuperuser
```

6. **Add sample products (optional):**
```python
python manage.py shell
```
```python
from store.models import Product
products = [
    {'name': 'Classic White Tee', 'description': 'A timeless white t-shirt', 'price': '24.99', 'stock': 50, 'sizes': 'S,M,L,XL'},
    {'name': 'Essential Black Tee', 'description': 'Perfect black t-shirt', 'price': '24.99', 'stock': 50, 'sizes': 'S,M,L,XL'},
]
for p in products:
    Product.objects.get_or_create(name=p['name'], defaults=p)
```

7. **Run the server:**
```bash
python manage.py runserver
```

8. **Visit:**
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Admin Panel

Access the Django admin panel to:

1. **Manage Products**
   - Add new t-shirts with images
   - Set prices and stock
   - Configure available sizes

2. **View Orders**
   - See all customer orders
   - Update order status
   - View order items

## Design System

### Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary | #0ea5e9 | Buttons, links, accents |
| Dark | #0f172a | Text, backgrounds |
| Gray | Various | UI elements |

### Typography
- **Font:** Inter (Google Fonts)
- **Weights:** 300, 400, 500, 600, 700

### Components
- Cards with rounded corners and shadows
- Hover effects on interactive elements
- Status badges for order states
- Modern form inputs with focus states

## Future Enhancements

Potential improvements for the project:

- [ ] Product categories (Men, Women, Kids)
- [ ] Search functionality
- [ ] Product reviews/ratings
- [ ] Email notifications
- [ ] Payment gateway integration (Stripe)
- [ ] Wishlist feature
- [ ] Guest checkout email capture
- [ ] Password reset functionality
- [ ] Image gallery for products
- [ ] Related products section

## License

This project is for educational purposes.

## Acknowledgments

- Django Framework
- Tailwind CSS
- Heroicons
- Google Fonts (Inter)
# ecommerce_django
