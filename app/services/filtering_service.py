import joblib
import os
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

class FilteringService:
    def __init__(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), '../models/filtering_model/toxic_classifier.joblib')
            model_path = os.path.abspath(model_path)
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found at path: {model_path}")
            
            loaded_data = joblib.load(model_path)
            
            if isinstance(loaded_data, dict):
                self.model = loaded_data.get('model')
                self.vectorizer = loaded_data.get('vectorizer')
            else:
                self.model = loaded_data
                self.vectorizer = TfidfVectorizer()
            
            if self.model is None or self.vectorizer is None:
                raise ValueError("Model or vectorizer not found in the loaded data.")
            
            logger.info("Toxic language model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading toxic language model: {str(e)}")
            raise
    
    def is_toxic(self, text: str) -> bool:
        text_vector = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vector)
        return prediction[0] == 1