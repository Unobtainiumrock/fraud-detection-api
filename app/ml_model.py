import joblib

# Load models from disk (you can further decouple this by loading on demand or in a separate service)
random_cut_forest_model = joblib.load('./trained_models/random_cut_forest_model.pkl')
xgboost_model = joblib.load('./trained_models/xgboost_model.pkl')
