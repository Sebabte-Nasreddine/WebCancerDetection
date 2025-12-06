"""
Routes pour les prédictions
"""
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from app_module.utils.models import ModelManager
from app_module.utils.data import prepare_prediction_input
from app_module.utils import APIResponse, get_logger

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/prediction')
logger = get_logger(__name__)


@prediction_bp.route('/', methods=['GET', 'POST'])
def predict():
    """Route pour les prédictions - Page principale"""
    result = None
    
    if request.method == 'POST':
        try:
            form_data = request.form
            
            # Valider que le modèle est sélectionné
            model_name = form_data.get('model_choice')
            if not model_name:
                logger.warning("Tentative de prédiction sans modèle sélectionné")
                result = {'error': 'Veuillez sélectionner un modèle'}
                return render_template('index.html', result=result)
            
            # Préparer les données
            df_input = prepare_prediction_input(form_data)
            
            # Charger le modèle
            model = ModelManager.get_model(model_name)
            if not model:
                logger.error(f"Modèle {model_name} non trouvé")
                result = {'error': f'Modèle {model_name} non disponible'}
                return render_template('index.html', result=result)
            
            # Prédiction
            prediction = model.predict(df_input)[0]
            probability = None
            
            if hasattr(model, 'predict_proba'):
                probability = model.predict_proba(df_input)[0][1]
            
            result = {
                'prediction': int(prediction),
                'probability': round(float(probability), 3) if probability else None,
                'model': model_name,
                'status': 'success'
            }
            
            logger.info(f"Prédiction réussie avec {model_name}: {result}")
            
        except ValueError as e:
            logger.error(f"Erreur de validation: {e}")
            result = {'error': f'Erreur de validation: {str(e)}'}
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            result = {'error': f'Erreur serveur: {str(e)}'}
    
    return render_template('index.html', result=result)


@prediction_bp.route('/api', methods=['POST'])
def predict_api():
    """API pour les prédictions (JSON)"""
    try:
        data = request.get_json()
        
        if not data or 'model_choice' not in data:
            return jsonify(APIResponse.error("Modèle non spécifié")), 400
        
        # Préparer les données
        df_input = prepare_prediction_input(data)
        
        # Charger le modèle
        model = ModelManager.get_model(data['model_choice'])
        if not model:
            return jsonify(APIResponse.error(f"Modèle {data['model_choice']} non trouvé")), 404
        
        # Prédiction
        prediction = model.predict(df_input)[0]
        probability = None
        
        if hasattr(model, 'predict_proba'):
            probability = float(model.predict_proba(df_input)[0][1])
        
        result = {
            'prediction': int(prediction),
            'probability': probability,
            'model': data['model_choice']
        }
        
        return jsonify(APIResponse.success(result)), 200
        
    except Exception as e:
        logger.error(f"Erreur API: {e}")
        return jsonify(APIResponse.error(str(e))), 500


@prediction_bp.route('/models', methods=['GET'])
def get_models():
    """Retourner la liste des modèles disponibles"""
    models = ModelManager.get_all_models()
    model_list = list(models.keys())
    return jsonify(APIResponse.success({'models': model_list})), 200
