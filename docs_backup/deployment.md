# Deployment Guide

Deploying *Vote Cast* to a production environment ensures that it is accessible to users in a secure and scalable manner. This guide will walk you through the steps to deploy the project on a cloud-based hosting provider.

---

## 1. Choosing a Hosting Provider

There are several options for hosting a Django application. Some popular choices include:

- **Heroku** – Easy deployment, managed PostgreSQL, free tier available.
- **DigitalOcean** – Full control over the server, requires manual setup.
- **AWS (EC2, RDS)** – Scalable and highly configurable, but complex to set up.
- **PythonAnywhere** – A simpler, Python-specific hosting platform.

For this guide, we will focus on **deploying using Heroku** as it is beginner-friendly and requires minimal setup.

---

## 2. Setting Up a Production Environment

Before deploying, prepare your production environment:

```bash
git clone https://github.com/Wolodmr/vote_cast.git
cd vote_cast
```

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py migrate`

## 3. Configuring Environment Variables

In production, sensitive information should not be hardcoded. Instead, use an .env file.

```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=your-database-url
```

Update settings.py:

```
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

(And continue with the rest of the guide following this structure.)  







