from app.services.openai_service import OpenAIService
from app.agents.news_agent import NewsAgent
import datetime

class BiologyTeacher:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.news_agent = NewsAgent()
        self.teacher_name = "Biology Teacher"
        self.subject = "biology"
    
    async def answer(self, question: str) -> str:
        keywords = [
            "news", "latest", "new discovery", "discovery", "recent", "breaking", 
            "current", "trending", "update", "just in", 
            "fresh", "announcement", "hot off the press", 
            "recent development", "new finding", "new research", "new study", 
            "new publication", "new paper", "new article"
        ]
        
        extra_info = ""
        if any(keyword in question.lower() for keyword in keywords):
            news_data = await self.news_agent.get_news("Latest Biology Discoveries")

            if news_data:
                extra_info_lines = ["\nLatest Biology News:"]
                for idx, article in enumerate(news_data, start=1):
                    extra_info_lines.append(f"\nArticle {idx}:")
                    extra_info_lines.append(f"Title: {article.get('title')}")
                    extra_info_lines.append(f"Date: {article.get('date')}")
                    extra_info_lines.append(f"Summary: {article.get('summary')}")
                extra_info = "\n".join(extra_info_lines)
            else:
                extra_info = "No recent news available."
        else:
            extra_info = "No recent news available."
        
        current_date = datetime.datetime.now().strftime("%B %d, %Y")

        prompt = f"""
            You are a biology expert with deep insights into molecular biology, genetics, ecology, and evolutionary biology.
            Provide real-world examples to help users visualize abstract biological concepts.
            If the user asks for exercises, suggest some exercises to solve without revealing the answers.
            Your answer should be clear, structured, and pedagogical.
            If relevant, incorporate the latest biology news provided below.
            -------------------------------------------------
            Current Date: {current_date}
            News Update:
            {extra_info.strip()}
            -------------------------------------------------
            Question: {question}
        """
        answer_text = await self.openai_service.get_completion(prompt)
        return {"teacher": self.teacher_name, "subject": self.subject, "message": answer_text}
