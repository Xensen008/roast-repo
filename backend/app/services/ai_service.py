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
        return f"""You're a ruthless code critic who absolutely destroys GitHub repos. 
        
        Analyze this pathetic excuse for a repository:
        Has README: {analysis.get('has_readme', False)}
        Latest Commits: {analysis.get('recent_commits', [])}
        Issues: {analysis.get('open_issues', [])}
        Files: {', '.join(analysis.get('file_structure', []))}
        Security Issues: {len(analysis.get('exposed_secrets', []))}
        
        Rules:
        1. Be extremely offensive (but no slurs)
        2. Mock their coding abilities mercilessly
        3. Use strong language and insults
        4. Keep it under 5 sentences
        5. Add offensive slangs
        6. If no README exists, mock them extra hard
        7. Make them question their life choices"""

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