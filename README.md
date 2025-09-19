# MathGuru Backend (Django)

This is the backend for the **MathGuru** project built with Django.

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/SifatUllaMondol/MathGuru-Backend
cd MathGuru-Backend
python -m venv venv
# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

In your project root (MathGuru-Backend/), create a file called .env with the following content (replace with your PostgreSQL details):
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=mathguru_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432


python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
