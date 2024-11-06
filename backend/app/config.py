from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    GITHUB_TOKEN: str
    GEMINI_API_KEYS: str
    CURRENT_KEY_INDEX: int = 0
    
    @property
    def api_keys_list(self) -> List[str]:
        return [key.strip() for key in self.GEMINI_API_KEYS.split(',')]
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()