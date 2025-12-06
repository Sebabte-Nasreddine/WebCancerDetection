"""
Utilitaires pour le chargement et gestion des modèles
"""
import joblib
import os
from typing import Dict, Any
from app_module.config.settings import Config


class ModelManager:
    """Gestionnaire centralisé des modèles ML"""
    
    _models = {}
    
    @classmethod
    def load_models(cls) -> Dict[str, Any]:
        """Charger tous les modèles"""
        if cls._models:
            return cls._models
        
        for model_name, model_path in Config.MODELS.items():
            if os.path.exists(model_path):
                cls._models[model_name] = joblib.load(model_path)
                print(f"✓ Modèle chargé: {model_name}")
            else:
                print(f"✗ Erreur: Fichier {model_path} non trouvé")
        
        return cls._models
    
    @classmethod
    def get_model(cls, model_name: str) -> Any:
        """Obtenir un modèle spécifique"""
        if not cls._models:
            cls.load_models()
        return cls._models.get(model_name)
    
    @classmethod
    def get_all_models(cls) -> Dict[str, Any]:
        """Obtenir tous les modèles"""
        if not cls._models:
            cls.load_models()
        return cls._models
