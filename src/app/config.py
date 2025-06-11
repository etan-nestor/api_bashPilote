import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    API_KEYS = os.getenv('API_KEYS', '').split(',')  # Liste des clés autorisées
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCRIPTS_DIR = BASE_DIR / 'scripts'
    LOGS_DIR = BASE_DIR / 'logs'
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        # Créer les répertoires si inexistants
        Config.SCRIPTS_DIR.mkdir(exist_ok=True)
        Config.LOGS_DIR.mkdir(exist_ok=True)