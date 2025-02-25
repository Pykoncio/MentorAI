import aiohttp
from app.core.config import settings

class NewsAgent:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"

    async def get_news(self, query: str) -> list:
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "language": "en",
            "pageSize": 5
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()

        articles = data.get("articles", [])
        news_data = []
        for article in articles:
            news_data.append({
                "title": article.get("title", "No Title"),
                "date": article.get("publishedAt", "Unknown Date"),
                "summary": article.get("description", "No Description Provided")
            })

        return news_data