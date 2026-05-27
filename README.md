Bhavani Cashews


Bhavani Cashews is a comprehensive, full-stack e-commerce platform built with Django, designed for a luxury artisanal cashew brand. It features a sophisticated, modern user interface powered by Tailwind CSS and provides a complete digital shopping experience, from browsing rich product catalogs to a secure, multi-step checkout process.

The platform is designed for both retail customers and B2B wholesale partners, with a robust backend for managing products, orders, and payments.

Key Features
Product Catalog: Browse products by categories, view detailed product pages with image galleries, and read customer reviews.
Search Functionality: Users can search for products across the entire catalog.
User Authentication: Secure user registration, login, logout, and a dedicated profile page to view order history.
Shopping Cart: A dynamic, session-based shopping cart to add, remove, and update product quantities. The cart state is synchronized between the frontend (localStorage) and backend (session).
Multi-Step Checkout: A guided checkout process for shipping, payment, and order review.
Payment Integration: Supports multiple payment methods, including a mock UPI/QR flow with screenshot verification and Cash On Delivery (COD).
Order Management: Users can view their order history and details. The backend includes a system to manage order and payment statuses.
Responsive Design: A premium, mobile-first design built with Tailwind CSS ensures a seamless experience on all devices.
Admin Dashboard: A custom-styled admin panel for managing products, categories, orders, and payments.
Technology Stack
Backend: Python, Django
Frontend: HTML, Tailwind CSS, Vanilla JavaScript
Database: SQLite (for development), PostgreSQL (for production)
Deployment: Gunicorn, Whitenoise, Render
Setup and Installation
Follow these steps to get the project running on your local machine.

1. Clone the repository:

git clone https://github.com/indranil-sawant/BhavaniCashews.git
cd Bhavanicashews
2. Create and activate a virtual environment:

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
3. Install dependencies:

pip install -r requirements.txt
4. Apply database migrations:

python manage.py migrate
5. Seed the database (Optional but Recommended):

To populate the website with sample products, categories, and reviews, run the seeding script. This will download product images and create initial data.

python seed_db.py
6. Create a superuser:

This will allow you to access the Django admin panel.

python manage.py createsuperuser
Follow the prompts to create an administrator account.

7. Run the development server:

python manage.py runserver
The application will be available at http://127.0.0.1:8000/. You can access the admin panel at http://127.0.0.1:8000/admin.

Project Structure
The project is organized into several Django apps, each responsible for a specific domain:

config/: The main Django project configuration, including settings.py and root urls.py.
products/: Manages product information, categories, grades, reviews, and the main public-facing views like the homepage and product listings.
accounts/: Handles user authentication (registration, login, logout) and customer profiles.
cart/: Implements the session-based shopping cart logic.
orders/: Manages the checkout process, shipping information, and order models.
payments/: Contains the logic for handling payment methods (UPI, QR, COD) and transaction verification.
dashboard/: A simple dashboard for internal analytics and overview.
Deployment
The repository is configured for deployment on Render. The following files are key to the deployment process:

render.yaml: A declarative infrastructure-as-code file that defines the web service and database for Render.
build.sh: A shell script that runs during deployment to collect static files and apply database migrations.
Procfile & gunicorn: Used to run the application server in the production environment.
