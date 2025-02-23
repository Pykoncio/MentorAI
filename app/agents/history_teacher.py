from app.services.openai_service import OpenAIService

class HistoryTeacher:
    def __init__(self):
        self.openai_service = OpenAIService()
    
    async def answer(self, question: str) -> str:
        prompt = f"""As a history teacher, please answer this question clearly and pedagogically: {question}"""
        return await self.openai_service.get_completion(prompt)