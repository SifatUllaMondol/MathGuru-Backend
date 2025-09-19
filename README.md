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

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
