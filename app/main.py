import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import auth, courses, progress, payments, admin

load_dotenv()

app = FastAPI(title="DevQuest API")

_origins = ["http://localhost:5173", "https://*.vercel.app"]
_frontend_url = os.environ.get("FRONTEND_URL")
if _frontend_url:
    _origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(progress.router)
app.include_router(payments.router)
app.include_router(admin.router)
