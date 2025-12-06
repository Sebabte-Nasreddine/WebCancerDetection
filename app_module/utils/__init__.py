"""
Utilitaires généraux
"""
import logging
from typing import Any, Dict


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class APIResponse:
    """Classe pour formater les réponses API"""
    
    @staticmethod
    def success(data: Any = None, message: str = "Succès") -> Dict:
        """Réponse réussie"""
        return {
            "status": "success",
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str = "Erreur", code: int = 400) -> Dict:
        """Réponse avec erreur"""
        return {
            "status": "error",
            "message": message,
            "code": code
        }


def get_logger(name: str) -> logging.Logger:
    """Obtenir un logger"""
    return logging.getLogger(name)
