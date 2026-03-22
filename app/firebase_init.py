import os
import json
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

_app = None


def get_firebase_app():
    global _app
    if _app is not None:
        return _app

    key_value = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY", "")

    # Support inline JSON or file path
    if key_value.startswith("{"):
        cred = credentials.Certificate(json.loads(key_value))
    else:
        cred = credentials.Certificate(key_value)

    _app = firebase_admin.initialize_app(cred)
    return _app
