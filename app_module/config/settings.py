"""
Configuration centralisée de l'application
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Chemins
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    # Models
    MODELS = {
        "log_reg": os.path.join(MODELS_DIR, "pipeline_logistic_regression.pkl"),
        "random_forest": os.path.join(MODELS_DIR, "pipeline_random_forest.pkl"),
        "gradient_boosting": os.path.join(MODELS_DIR, "pipeline_gradient_boosting.pkl"),
        "knn": os.path.join(MODELS_DIR, "pipeline_knn.pkl")
    }
    
    # Dataset
    DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
    
    # Server
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))


class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    

class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    

class TestingConfig(Config):
    """Configuration de test"""
    TESTING = True
    

# Sélectionner la configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retourner la configuration basée sur l'environnement"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
