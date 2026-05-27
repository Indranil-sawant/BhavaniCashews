🌰 Bhavani Cashews

Bhavani Cashews is a premium full-stack e-commerce platform built with Django for a luxury artisanal cashew brand.
The platform delivers a modern digital shopping experience with elegant UI design, secure checkout flows, product management, and scalable backend architecture.

Designed for both retail customers and B2B wholesale buyers, the system combines performance, usability, and production-ready architecture.

✨ Core Features
🛍 Product Catalog
Browse products by categories and grades
Detailed product pages with:
Image galleries
Product descriptions
Pricing
Customer reviews
🔍 Advanced Search
Real-time product search across the catalog
Optimized browsing experience
👤 User Authentication
Secure registration & login system
User profile dashboard
Order history tracking
🛒 Smart Shopping Cart
Session-based dynamic cart system
Add, update, and remove products
Frontend cart synchronization using localStorage
💳 Multi-Step Checkout
Guided checkout process
Shipping information collection
Order review before confirmation
💰 Payment System

Supports multiple payment methods:

UPI Payments
QR Code Payments
Screenshot verification flow
Cash On Delivery (COD)
📦 Order Management
Order tracking
Payment status management
Order history and details
📱 Responsive UI
Mobile-first premium design
Built using Tailwind CSS
Smooth and modern user experience
⚙️ Admin Dashboard
Manage:
Products
Categories
Orders
Payments
Customer data
🛠 Technology Stack
Layer	Technology
Backend	Python, Django
Frontend	HTML, Tailwind CSS, JavaScript
Database	SQLite (Development), PostgreSQL (Production)
Deployment	Gunicorn, Whitenoise, Render
🚀 Installation Guide
1. Clone Repository
git clone https://github.com/indranil-sawant/BhavaniCashews.git
cd Bhavanicashews
2. Create Virtual Environment
macOS/Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Seed Database (Optional)

Populate the platform with sample products, categories, and reviews.

python seed_db.py
6. Create Superuser
python manage.py createsuperuser
7. Run Development Server
python manage.py runserver

Application URL:

http://127.0.0.1:8000/

Admin Panel:

http://127.0.0.1:8000/admin
📂 Project Architecture
config/

Main Django configuration:

settings.py
urls.py
deployment configuration
products/

Handles:

Product management
Categories
Reviews
Homepage
Product listing pages
accounts/

Responsible for:

Authentication
Registration
Login/Logout
User profiles
cart/

Implements:

Session cart logic
Cart synchronization
Quantity management
orders/

Handles:

Checkout system
Shipping information
Order processing
payments/

Manages:

UPI workflow
QR payment verification
COD system
Payment statuses
dashboard/

Internal analytics and admin overview.

🌍 Deployment

The project is configured for deployment on Render.

Important Deployment Files
File	Purpose
render.yaml	Infrastructure configuration
build.sh	Static collection & migrations
Procfile	Gunicorn startup process
requirements.txt	Dependency management
🎯 Highlights
Production-ready Django architecture
Elegant premium UI
Secure authentication system
Multiple payment workflows
Mobile-first responsive design
Scalable deployment structure
Full-stack implementation
📸 Future Improvements
Razorpay/Stripe integration
Wishlist functionality
AI-powered recommendations
Inventory analytics dashboard
Email notifications
Coupon & discount system
Multi-vendor support
