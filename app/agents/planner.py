from app.services.openai_service import OpenAIService
from app.services.filtering_service import FilteringService
from app.agents import MathTeacher, BiologyTeacher, ChemistryTeacher, EconomyTeacher, HistoryTeacher, LanguageTeacher, PhysicsTeacher, ProgrammingTeacher
import logging

logger = logging.getLogger(__name__)

class Planner:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.filtering_service = FilteringService()
        self.teachers = {
            "math": MathTeacher(),
            "history": HistoryTeacher(),
            "language": LanguageTeacher(),
            "physics": PhysicsTeacher(),
            "biology": BiologyTeacher(),
            "chemistry": ChemistryTeacher(),
            "economy": EconomyTeacher(),
            "programming": ProgrammingTeacher()
        }
    
    async def process_message(self, message: str):
        try:
            if self.filtering_service.is_toxic(message):
                return {
                    "teacher": "🚫 Moderator", 
                    "subject": "", 
                    "message": "Your message contains inappropriate language. Please rephrase your question."
                }
            
            subject = await self._classify_question(message)
            logger.debug(f"Question classified as: {subject}")

            if subject == "other":
                return {
                    "teacher": "❓ Teacher",
                    "subject": subject,
                    "message": "I'm sorry, but I currently don't have a teacher specialized for that question."
                }
    
            if subject in self.teachers:
                return await self.teachers[subject].answer(message)
            return "I'm sorry, but I currently don't have a teacher specialized for that question."
        
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            raise Exception(f"Error in process_message: {str(e)}")
    
    async def _classify_question(self, message: str):
        prompt = f"""Classify this question into one of the following categories and just respond with the subject: 
            math, history, language, physics, biology, chemistry, economy or programming.
            If the question explicitly mentions one of these subjects, classify it under that subject. 
            If the question does not clearly belong to any of these categories, respond with 'other'.
            Question: {message}"""
        response = await self.openai_service.get_completion(prompt)
        return response.lower().strip()