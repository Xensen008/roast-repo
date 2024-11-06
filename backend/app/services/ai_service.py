import google.generativeai as genai
from ..config import settings

class AIService:
    def __init__(self):
        self.model = None
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        self.initialize(settings.GEMINI_API_KEY)
    
    def initialize(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_roast(self, repo_analysis: dict) -> str:
        try:
            prompt = self._create_roast_prompt(repo_analysis)
            response = await self.model.generate_content_async(
                prompt,
                safety_settings=self.safety_settings,
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'top_k': 40,
                }
            )
            return response.text
        except Exception as e:
            return f"Failed to generate roast: {str(e)}"
    
    async def generate_readme(self, repo_analysis: dict) -> str:
        prompt = self._create_readme_prompt(repo_analysis)
        
        response = await self.model.generate_content_async(
            prompt,
            safety_settings=self.safety_settings,
            generation_config={
                'temperature': 0.3,
                'top_p': 0.9,
                'top_k': 40,
            }
        )
        
        return response.text

    def _create_roast_prompt(self, analysis: dict) -> str:
        return f"""Roast this repository based on:
        Has README: {analysis.get('has_readme', False)}
        Recent Commits: {analysis.get('recent_commits', [])}
        Open Issues: {analysis.get('open_issues', [])}
        Files: {', '.join(analysis.get('file_structure', []))}
        Security Issues: {len(analysis.get('exposed_secrets', []))}
        
        Be creative, sarcastic, and use mild swear words. Point out:
        1. Code organization
        2. Commit messages
        3. Issue management
        4. Security practices
        5. Documentation quality"""

    def _create_readme_prompt(self, analysis: dict) -> str:
        return f"""Generate a comprehensive README.md for a repository with these files:
        {', '.join(analysis.get('file_structure', []))}
        
        Package Info: {analysis.get('package_info', 'No package info available')}
        
        Include sections for:
        - Project description
        - Installation
        - Usage
        - Features
        - Contributing
        - License"""

# Create and export an instance
ai_service = AIService()