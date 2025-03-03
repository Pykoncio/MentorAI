from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MentorAI API"
    OPENAI_API_KEY: str
    NEWS_API_KEY: str
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    
    class Config:
        env_file = ".env"

settings = Settings()