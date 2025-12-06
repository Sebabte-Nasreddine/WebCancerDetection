"""
Application Factory pour initialiser l'application Flask
"""
from flask import Flask
from flask_cors import CORS
from app_module.config.settings import get_config


def create_app(config_name=None):
    """
    Application Factory
    """
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # Configuration
    config = get_config()
    app.config.from_object(config)
    
    # CORS
    CORS(app)
    
    # Enregistrer les blueprints
    from app_module.routes.prediction import prediction_bp
    from app_module.routes.dashboard import dashboard_bp
    from app_module.routes.health import health_bp
    
    app.register_blueprint(prediction_bp)
    app.register_blueprint(health_bp)
    dashboard_bp(app)  # Dash intégré
    
    return app
