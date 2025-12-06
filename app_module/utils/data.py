"""
Utilitaires pour traitement des données
"""
import pandas as pd
from typing import Dict, List


def binary_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transformer les colonnes 'Yes'/'No' en 1/0"""
    return df.applymap(lambda x: 1 if x == "Yes" else 0)


def prepare_prediction_input(form_data: Dict) -> pd.DataFrame:
    """
    Préparer les données du formulaire pour la prédiction
    
    Args:
        form_data: Données du formulaire Flask
        
    Returns:
        DataFrame prêt pour la prédiction
    """
    data = {
        'HeartDisease': [form_data.get('HeartDisease', 'No')],
        'BMI': [float(form_data.get('BMI', 25.0))],
        'Smoking': [form_data.get('Smoking', 'No')],
        'AlcoholDrinking': [form_data.get('AlcoholDrinking', 'No')],
        'Stroke': [form_data.get('Stroke', 'No')],
        'PhysicalHealth': [float(form_data.get('PhysicalHealth', 0.0))],
        'MentalHealth': [float(form_data.get('MentalHealth', 0.0))],
        'DiffWalking': [form_data.get('DiffWalking', 'No')],
        'Sex': [form_data.get('Sex', 'Male')],
        'AgeCategory': [form_data.get('AgeCategory', '18-24')],
        'Race': [form_data.get('Race', 'White')],
        'Diabetic': [form_data.get('Diabetic', 'No')],
        'PhysicalActivity': [form_data.get('PhysicalActivity', 'Yes')],
        'GenHealth': [form_data.get('GenHealth', 'Fair')],
        'SleepTime': [float(form_data.get('SleepTime', 7.0))],
        'Asthma': [form_data.get('Asthma', 'No')],
        'KidneyDisease': [form_data.get('KidneyDisease', 'No')]
    }
    return pd.DataFrame(data)


def load_dataset(dataset_path: str) -> pd.DataFrame:
    """Charger le dataset"""
    try:
        return pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Erreur lors du chargement du dataset: {e}")
        return pd.DataFrame()


def get_value_options(df: pd.DataFrame, column: str) -> List[Dict]:
    """Obtenir les options pour un dropdown"""
    try:
        values = sorted(df[column].unique())
        return [{'label': str(v), 'value': v} for v in values]
    except Exception as e:
        print(f"Erreur: {e}")
        return []
