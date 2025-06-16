## 🚀 Deployment to Render

The ioVote project is live at: [https://vote-cast-5.onrender.com](https://vote-cast-5.onrender.com)

### ✅ Render Deployment Summary

1. **Platform:** Render (Free Plan)
2. **Web Service:** Python/Django
3. **Database:** PostgreSQL (Free)
4. **Static Files:** Collected with `collectstatic`
5. **Production WSGI Server:** Gunicorn

> ⚠️ **Note:**  
> For demo purposes, the app currently uses **SQLite** in production due to Render’s PostgreSQL pricing model.  
> While the app runs correctly, the deployed **Admin Panel cannot save data** — a known SQLite limitation on Render.  
> For full backend functionality, **PostgreSQL is recommended and fully supported**.
---

### 🔧 Deployment Setup Steps

#### 1. **render.yaml**
Make sure your repository includes a `render.yaml` file like this:

```yaml
# See render_deploy_config.yaml in this repo
```

#### 2. **Environment Variables on Render**
Go to your Render Dashboard → your Web Service → **Environment** tab, and add the following:

- `DJANGO_SETTINGS_MODULE=iovote.settings`
- `DATABASE_URL=<autoconfigured>`
- `DEBUG=False`
- `EMAIL_HOST=smtp.gmail.com`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=True`
- `EMAIL_HOST_USER=postvezha@gmail.com`
- `EMAIL_HOST_PASSWORD=<your app password>` (Mark as Secret)

#### 3. **buildCommand**
```bash
./manage.py collectstatic --noinput
```

#### 4. **startCommand**
```bash
gunicorn iovote.wsgi:application
```

---

### 🛡️ Email Security Best Practices
- Use **App Passwords** instead of your main Gmail password.
- Store sensitive info like `EMAIL_HOST_PASSWORD` as **Secret environment variables**.
- Avoid committing passwords to GitHub or anywhere in plaintext.

---

### 🧪 Testing Email in Production
Use the admin panel to add a session and trigger a confirmation email. Ensure the SMTP settings work by checking Gmail's "Sent" folder.

---

### 📁 Recommended File Structure for Render Deployment
```
iovote/
├── iovote/
│   ├── settings.py
│   ├── wsgi.py
├── manage.py
├── render.yaml
├── requirements.txt
```

---

### 👥 Author
**Vladimir Shkurko**  
Django Developer  
[LinkedIn](https://www.linkedin.com/in/vladimir-shkurko-07962333a) | [GitHub](https://github.com/Wolodmr) | [Email](mailto:postvezha@gmail.com)
