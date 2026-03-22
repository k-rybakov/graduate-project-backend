# DevQuest Backend

REST API for [DevQuest](https://devquest-frontend.vercel.app) — a Python learning platform with theory lessons and interactive practice tasks.

Built with **FastAPI** + **PostgreSQL** + **Firebase Auth**.

---

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- PostgreSQL (Docker locally, Render in production)
- SQLAlchemy ORM + Alembic migrations
- Firebase Admin SDK (ID token verification)
- Pydantic v2

---

## Prerequisites

- Python 3.11+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for local PostgreSQL)
- A Firebase project with a service account key ([instructions](https://firebase.google.com/docs/admin/setup#initialize_the_sdk_in_non-google_environments))

---

## Local Setup

### 1. Clone and enter the directory

```bash
mkdir backend && cd backend
git clone https://github.com/k-rybakov/graduate-project-backend.git .
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/devquest
FIREBASE_PROJECT_ID=woolf-graduate-proj
FIREBASE_SERVICE_ACCOUNT_KEY=path/to/serviceAccountKey.json
FRONTEND_URL=https://<devquest-frontend>.vercel.app
```

#### Getting the Firebase service account key

The `FIREBASE_PROJECT_ID` is already set to `woolf-graduate-proj`. For the service account key:

1. Go to the [Firebase Console](https://console.firebase.google.com/) → **woolf-graduate-proj**
2. Click the gear icon → **Project settings** → **Service accounts** tab
3. Click **Generate new private key** → confirm → a JSON file will download
4. Set `FIREBASE_SERVICE_ACCOUNT_KEY` to either:
   - A **file path**: `FIREBASE_SERVICE_ACCOUNT_KEY=/path/to/downloaded-key.json`
   - Or the **raw JSON string** (paste the entire file content on one line — useful for Render):
     `FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account","project_id":"woolf-graduate-proj",...}`

### 4. Start PostgreSQL

```bash
docker-compose up -d
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uvicorn app.main:app --reload --port 8000
```

API is now available at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

---

## Project Structure

```
app/
  main.py              # FastAPI app, CORS, router registration
  database.py          # SQLAlchemy engine + session + Base
  firebase_init.py     # Firebase Admin SDK initialization
  dependencies.py      # Shared deps: get_db, get_current_user, require_admin
  models/              # SQLAlchemy ORM models
    user.py
    course.py
    lesson.py          # Lesson, LessonSection, PracticeTask
    progress.py        # UserProgress, UserCourseAccess
    payment.py
  schemas/             # Pydantic v2 request/response schemas
    user.py
    course.py
    lesson.py
    progress.py
    payment.py
  routers/             # FastAPI route handlers
    auth.py            # POST /auth/login, GET /auth/me
    courses.py         # GET /courses, /courses/:slug, /courses/:slug/lessons/:slug
    progress.py        # POST/GET /progress/...
    payments.py        # POST /payments/purchase
    admin.py           # GET/POST/PUT/DELETE /admin/...
  services/            # Business logic
    auth_service.py
    course_service.py
    progress_service.py
    payment_service.py
alembic/               # Migration files
docker-compose.yml
requirements.txt
```

---

## API Overview

| Method | Path                              | Auth              | Description                               |
| ------ | --------------------------------- | ----------------- | ----------------------------------------- |
| POST   | `/auth/login`                     | Firebase token    | Verify token, upsert user, return profile |
| GET    | `/auth/me`                        | Required          | Current user profile                      |
| GET    | `/courses`                        | Required          | List courses with access flags            |
| GET    | `/courses/{slug}`                 | Required          | Course detail + lesson list               |
| GET    | `/courses/{slug}/lessons/{slug}`  | Required + access | Full lesson content                       |
| POST   | `/progress/lessons/{id}/complete` | Required          | Mark lesson complete                      |
| GET    | `/progress/courses/{id}`          | Required          | Course completion progress                |
| POST   | `/payments/purchase`              | Required          | Attempt course purchase                   |
| GET    | `/admin/users`                    | Admin             | List all users                            |
| GET    | `/admin/courses`                  | Admin             | List all courses                          |
| POST   | `/admin/courses`                  | Admin             | Create course                             |
| PUT    | `/admin/courses/{id}`             | Admin             | Update course                             |
| DELETE | `/admin/courses/{id}`             | Admin             | Soft-delete course                        |

All protected endpoints require `Authorization: Bearer <firebase-id-token>`.

---

## Payment Demo

This is a **fake payment** for demo purposes. No real gateway is used.

| Card number        | Result                         |
| ------------------ | ------------------------------ |
| `4444333322221111` | Success — grants course access |
| Any other number   | Failed                         |

---

## Database Migrations

```bash
# After changing a model, generate a new migration
alembic revision --autogenerate -m "describe your change"

# Apply pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```

---

## Deployment (Render)

1. Create a **Render PostgreSQL** instance → copy the `DATABASE_URL`
2. Create a **Render Web Service** pointing to this repo
3. Set environment variables in the Render dashboard:
   ```
   DATABASE_URL=<from render postgres>
   FIREBASE_PROJECT_ID=woolf-graduate-proj
   FIREBASE_SERVICE_ACCOUNT_KEY=<inline JSON string>
   FRONTEND_URL=https://<devquest-frontend>.vercel.app
   ```
4. Set the start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
