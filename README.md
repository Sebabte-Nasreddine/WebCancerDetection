# SkinCheck Pro

Professional AI-powered application for skin cancer risk assessment and prediction.

##  Key Features
- **Multi-Model Prediction**: Utilizes Logistic Regression, Random Forest, Gradient Boosting, and KNN algorithms.
- **Interactive Dashboard**: Real-time analytics with filtering capabilities using Plotly Dash.
- **REST API**: Fully documented endpoints for integration.
- **Report Generation**: PDF reports with SHAP and LIME explainability.

##  Quick Start

### Option 1: Docker (Recommended)
Run the application in seconds with Docker Compose:

```bash
docker-compose up -d
```
Access the app at `http://localhost:5000`.

### Option 2: Local Installation
Prerequisites: Python 3.8+

```bash
# 1. Clone & Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env

# 3. Run
python app.py
```

##  API Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/predict` | Get prediction in JSON format |
| `GET` | `/api/health` | System health check |
| `GET` | `/dashboard/` | Interactive analytics dashboard |

##  Production Deployment
For production, it is recommended to run behind a reverse proxy (Apache/Nginx) with HTTPS.
- **VPS**: Deploy on a standard Linux VPS (Ubuntu/Debian).
- **Web Server**: Configure Apache as a reverse proxy to forward traffic to port 5000.
- **Security**: Always enable HTTPS and restrict access to the dashboard if necessary.

##  License
MIT License.
