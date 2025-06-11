from flask import Flask
from app.config import Config
from app.extensions import db
from app.core.scheduler import Scheduler  # ta classe custom Scheduler

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialiser les extensions
    db.init_app(app)

    # Initialiser le scheduler custom si activé
    scheduler = None
    if app.config.get('SCHEDULER_API_ENABLED', False):
        scheduler = Scheduler(app)
        scheduler.start()

    # Initialisation spécifique à la config (optionnel)
    if hasattr(config_class, 'init_app'):
        config_class.init_app(app)
    
    # Importer et enregistrer les blueprints
    from app.routes.scripts import scripts_bp
    from app.routes.jobs import jobs_bp

    app.register_blueprint(scripts_bp, url_prefix='/api/v1')
    app.register_blueprint(jobs_bp, url_prefix='/api/v1')

    # Créer les tables dans le contexte de l'app
    with app.app_context():
        db.create_all()

    # Retourner l'app ET le scheduler si besoin (pour tests, commandes, etc.)
    return app
