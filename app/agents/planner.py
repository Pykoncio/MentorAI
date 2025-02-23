from app.services.openai_service import OpenAIService
from app.services.filtering_service import FilteringService
from app.agents.math_teacher import MathTeacher
from app.agents.science_teacher import ScienceTeacher
from app.agents.history_teacher import HistoryTeacher
import logging

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.filtering_service = FilteringService()
        self.teachers = {
            "math": MathTeacher(),
            "arithmetic": MathTeacher(),  # Añadir soporte para aritmética
            "science": ScienceTeacher(),
            "history": HistoryTeacher()
        }
    
    async def process_message(self, message: str):
        try:
            # Filtrar lenguaje soez
            if self.filtering_service.is_toxic(message):
                return "Your message contains inappropriate language. Please rephrase your question."
            
            # Clasificar la pregunta
            subject = await self._classify_question(message)
            logger.debug(f"Question classified as: {subject}")
            
            if subject in self.teachers:
                return await self.teachers[subject].answer(message)
            return "I'm not sure how to help with that question."
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            raise Exception(f"Error in process_message: {str(e)}")
    
    async def _classify_question(self, message: str):
        prompt = f"Classify this question into one category (math, arithmetic, science, history): {message}"
        response = await self.openai_service.get_completion(prompt)
        return response.lower().strip()