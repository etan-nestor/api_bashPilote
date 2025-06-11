from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from app.config import Config
import os
from app.extensions import db

def init_db(app):
    db.init_app(app)
    
    # Créer une sauvegarde automatique avant chaque modification
    @event.listens_for(db.session, 'before_commit')
    def backup_before_commit(session):
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                backup_path = f"{db_path}.backup"
                with open(db_path, 'rb') as src, open(backup_path, 'wb') as dst:
                    dst.write(src.read())

def backup_database():
    """Fonction pour sauvegarder la base de données"""
    if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        backup_path = f"{db_path}.backup"
        with open(db_path, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        return backup_path
    return None