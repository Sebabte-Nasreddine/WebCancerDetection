"""
Routes pour la santé et info
"""
from flask import Blueprint, jsonify
from app_module.utils.models import ModelManager
from app_module.utils import APIResponse, get_logger

health_bp = Blueprint('health', __name__, url_prefix='/api')
logger = get_logger(__name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Vérifier l'état de l'application"""
    try:
        models = ModelManager.get_all_models()
        return jsonify(APIResponse.success({
            'status': 'healthy',
            'models_loaded': len(models),
            'available_models': list(models.keys())
        })), 200
    except Exception as e:
        logger.error(f"Erreur health check: {e}")
        return jsonify(APIResponse.error("Service indisponible")), 503


@health_bp.route('/info', methods=['GET'])
def app_info():
    """Informations sur l'application"""
    return jsonify(APIResponse.success({
        'app_name': 'Cancer Prediction API',
        'version': '2.0.0',
        'endpoints': {
            'prediction': '/api/prediction',
            'health': '/api/health',
            'dashboard': '/dashboard/'
        }
    })), 200
