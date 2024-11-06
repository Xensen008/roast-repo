from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    GITHUB_TOKEN: str
    GEMINI_API_KEYS: List[str] 
    CURRENT_KEY_INDEX: int = 0  
    
    class Config:
        env_file = ".env"
        extra = "allow" 
settings = Settings()