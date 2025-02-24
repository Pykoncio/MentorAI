import joblib
import os

model_path = 'app/models/filtering_model/toxic_classifier.joblib'
model_path = os.path.abspath(model_path)

if not os.path.exists(model_path):
    print(f"Model file not found at path: {model_path}")
else:
    loaded_data = joblib.load(model_path)
    print(f"Model loaded successfully from path: {model_path}")
    print(type(loaded_data))
    if isinstance(loaded_data, dict):
        print("Model:", type(loaded_data.get('model')))
        print("Vectorizer:", type(loaded_data.get('vectorizer')))
    else:
        print("Loaded data is not a dictionary.")