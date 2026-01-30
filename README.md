# RetroByteLab

**Retro computing. Modern engineering.**

RetroByteLab is a Django e-commerce project inspired by classic hardware and software platforms such as the Commodore 64, Amiga and DIY retro consoles.  

The project covers the complete purchase flow: product listing, cart, checkout, PayPal payments, order creation and HTML email confirmations.

>This project was built for learning and personal development purposes.

---

## Features

- Product listing with category filtering
- Product detail page  
- Shopping cart
- Guest & authenticated checkout
- PayPal payment integration
- Order & order items persistence
- Payment success / failure pages
- HTML order confirmation emails

---

## Tech Stack

- **Backend:** Django, Python
- **Database:** SQLite, Supabase
- **Frontend:** Django Templates, Bootstrap, SCSS, Vanilla JavaScript, HTMX (AJAX-based partial page updates)
- **Payments:** PayPal JavaScript SDK
- **Emails:** Django EmailMultiAlternatives (HTML + text)
- **Deployment:** Render  

---

## PayPal Sandbox Testing

This project uses **PayPal Sandbox** for development and testing. Sandbox lets you simulate real payments without using real money.

#### How to get the PayPal Client ID
- Go to the [PayPal Developer Dashboard](https://developer.paypal.com/home/).
- Sign in with your PayPal account (or create a free developer account).
- Navigate to My Apps & Credentials.
- Click Create App button.
- Give your app a name (e.g., RetroByteLabApp), select Merchant and use the Sandbox environment for testing.
- Once created, you’ll see the Client ID – copy this and paste it into your .env as PAYPAL_CLIENT_ID.

> ⚠️ Use the Sandbox Client ID for development/testing.  

#### Create Sandbox Test Users

- Login to the [PayPal Developer Dashboard](https://developer.paypal.com/home/)
- Navigate to **Testing Tools → Sandbox Accounts**.
- You will see two default accounts:
   - **Personal** (buyer)
   - **Business** (merchant)
- Click Create account button to create new users
- Create Personal and Business accounts with USD as currency and US as country by clicking "Do you want a more customized account? Create" (buyer has to to be US with USD otherwise you will get an error)


---  

## Getting Started

#### Clone the project

```bash
git clone https://github.com/filosoho/retrobytelab.git
cd retrobytelab
```

---

#### Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

(optional for local dev) 
```bash 
pip install -r requirements-dev.txt
```

#### Install dependencies

```bash
npm install
```

---

#### Environment Variables

This project uses a `.env` file. You need to create a `.env` file in the project root with the following variables:

```bash
DEBUG=True
SECRET_KEY=

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
PAYPAL_CLIENT_ID=
```

#### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

#### Create a superuser (optional)

```bash
python manage.py createsuperuser
```

---

#### Run the app

```bash
python manage.py runserver
```

---

#### Compile SCSS

```bash
npm run sass
```

#### Watch mode (recommended during development)

```bash
npm run sass:watch
```

---

#### Add Categories and Products

- Open the Django admin at http://127.0.0.1:8000/admin and log in with your superuser account.
- Add Categories first. Each category will appear in the store’s filter dropdown.
- Add Products and assign them to the categories you created. Make sure to upload images for your products so they display correctly in the store.
- Visit the store at http://127.0.0.1:8000/ to see the products and filter them by category.
- You can test the shopping cart, checkout and order confirmation features using your test user accounts.

---

## License

This project is for learning and personal development purposes.

© 2026 Anna Bedia. All rights reserved.