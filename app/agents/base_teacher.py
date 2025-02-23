from abc import ABC, abstractmethod
from app.services.openai_service import OpenAIService
from typing import List
from app.schemas.chat import Message

class BaseTeacher(ABC):
    def __init__(self):
        self.openai_service = OpenAIService()
        self.subject = "general"
        self.name = "Base Teacher"
    
    @abstractmethod
    async def get_prompt(self, question: str) -> str:
        pass
    
    async def answer(self, question: str, context: List[Message] = None) -> str:
        prompt = await self.get_prompt(question)
        return await self.openai_service.get_completion(prompt, context)