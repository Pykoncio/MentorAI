from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MentorAI API"
    OPENAI_API_KEY: str
    NEWS_API_KEY: str
    HOST: str
    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: int
    
    class Config:
        env_file = ".env"

settings = Settings()