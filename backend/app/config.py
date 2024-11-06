from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GITHUB_TOKEN: str
    GEMINI_API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields in settings

settings = Settings()