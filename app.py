from flask import Flask, render_template, request, jsonify, redirect
import pandas as pd
import joblib

app = Flask(__name__)

def binary_transform(df):
    return df.applymap(lambda x: 1 if x == "Yes" else 0)

MODELS = {
    "log_reg": joblib.load("models/pipeline_logistic_regression.pkl"),
    "random_forest": joblib.load("models/pipeline_random_forest.pkl"),
    "gradient_boosting": joblib.load("models/pipeline_gradient_boosting.pkl"),
    "knn": joblib.load("models/pipeline_knn.pkl")
}

def prepare_input(form):
    data = {
        'HeartDisease': [form['HeartDisease']],
        'BMI': [float(form['BMI'])],
        'Smoking': [form['Smoking']],
        'AlcoholDrinking': ['No'],
        'Stroke': ['No'],
        'PhysicalHealth': [0.0],
        'MentalHealth': [0.0],
        'DiffWalking': ['No'],
        'Sex': [form['Sex']],
        'AgeCategory': [form['AgeCategory']],
        'Race': ['White'],
        'Diabetic': ['No'],
        'PhysicalActivity': [form['PhysicalActivity']],
        'GenHealth': [form['GenHealth']],
        'SleepTime': [7.0],
        'Asthma': ['No'],
        'KidneyDisease': ['No']
    }
    return pd.DataFrame(data)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        form = request.form
        df_input = prepare_input(form)
        
        pipeline = MODELS[form['model_choice']]
        
        pred = pipeline.predict(df_input)[0]
        prob = pipeline.predict_proba(df_input)[0][1] if hasattr(pipeline, "predict_proba") else "N/A"
        
        result = {'prediction': int(pred), 'probability': round(prob, 3) if prob != "N/A" else "N/A"}
    
    return render_template('index.html', result=result)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint pour les prédictions en JSON"""
    try:
        form = request.form
        df_input = prepare_input(form)
        
        model_choice = form.get('model_choice', 'log_reg')
        pipeline = MODELS.get(model_choice, MODELS['log_reg'])
        
        pred = pipeline.predict(df_input)[0]
        prob = pipeline.predict_proba(df_input)[0][1] if hasattr(pipeline, "predict_proba") else 0
        
        return jsonify({
            'success': True,
            'prediction': int(pred),
            'probability': float(prob),
            'model': model_choice
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# Enregistrer le dashboard modular
from app_module.routes.dashboard import dashboard_bp
dashboard_bp(app)

# Redirection pour /dashboard sans slash final
@app.route('/dashboard')
def redirect_dashboard():
    return redirect('/dashboard/')

# Page d'accueil Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
