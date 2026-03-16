# Paisa — Voice Expense Tracker

A voice-and-text expense tracker built with Django + DRF, deployable to Render, Railway, or any Linux server.

---

## Features
- Natural language expense logging ("spent ₹300 on dinner yesterday")
- Smart NLP category detection (Food, Travel, Groceries, Health, etc.)
- Voice input via Web Speech API (Chrome/Edge)
- Monthly summaries & category breakdowns
- SMS and Gmail importers (optional)
- REST API + Django Admin panel
- Production-ready: PostgreSQL, Whitenoise, Gunicorn, security headers

---

## Project Structure

```
voice_expense_tracker/
├── manage.py
├── requirements.txt
├── Procfile
├── render.yaml
├── .env.example
├── .gitignore
├── voice_tracker/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── expenses/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── web_views.py
    ├── urls.py
    ├── web_urls.py
    ├── llm_handler.py
    ├── tasks.py
    ├── sms_importer.py
    ├── email_importer.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── templates/
        └── expenses/
            └── index.html
```

---

## Local Development

### 1. Clone and set up environment

```bash
git clone <your-repo-url>
cd voice_expense_tracker

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY, DEBUG=True, leave DATABASE_URL blank for SQLite
```

### 3. Run migrations and start

```bash
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## Deploy to Render (Free Tier)

### Option A — One-click via render.yaml
1. Push this repo to GitHub.
2. Go to https://render.com → New → Blueprint.
3. Connect your repo. Render reads `render.yaml` and creates the web service + PostgreSQL automatically.
4. Set any missing env vars in the Render dashboard.

### Option B — Manual
1. Push to GitHub.
2. Render → New → Web Service → connect repo.
3. Set:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `gunicorn voice_tracker.wsgi:application --bind 0.0.0.0:$PORT`
4. Add env vars:
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | (generate a random string) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app.onrender.com` |
   | `DATABASE_URL` | (from Render PostgreSQL dashboard) |
   | `TIME_ZONE` | `Asia/Kolkata` |

---

## Deploy to Railway

```bash
railway login
railway init
railway add postgresql
railway up
```

Set the same env vars in the Railway dashboard.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/log/` | Log an expense from text |
| GET | `/api/transactions/?user_id=&year_month=YYYYMM` | List transactions |
| DELETE | `/api/transactions/<uuid>/` | Delete a transaction |
| GET | `/api/summary/?user_id=&year_month=YYYYMM` | Monthly summary |
| GET | `/api/all-time-summary/?user_id=` | All-time totals |

### POST /api/log/ — Example

```bash
curl -X POST https://your-app.onrender.com/api/log/ \
  -H "Content-Type: application/json" \
  -d '{"text": "spent 350 on lunch today", "user_id": "alice"}'
```

Response:
```json
{
  "id": "uuid...",
  "user_id": "alice",
  "amount_minor": 35000,
  "currency": "INR",
  "description": "spent  on  ",
  "category": "Food",
  "event_ts": "2025-03-16T14:22:00",
  "source": "web"
}
```

---

## Django Admin

Visit `/admin/` and log in with your superuser credentials to browse and manage all transactions.

---

## Gmail / SMS Import (Optional)

### SMS
Call `parse_sms_text(sms_body, user_id)` from `expenses/sms_importer.py`.

### Gmail
1. Create a Google Cloud project, enable Gmail API.
2. Download `token.json` and set `GMAIL_TOKEN_PATH=/path/to/token.json` in `.env`.
3. Call `import_gmail_transactions(user_id)` from `expenses/email_importer.py`.

---

## Generating a SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```
