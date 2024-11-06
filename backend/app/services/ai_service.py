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
        readme_status = "no README"
        if analysis.get('has_readme'):
            readme_content = analysis.get('readme_content', '').strip()
            readme_status = "empty README" if not readme_content else "useless README"
        
        return f"""You are a brutal code critic. Analyze this repository:
        README Status: {readme_status}
        Latest Commits: {analysis.get('recent_commits', [])}
        Issues: {analysis.get('open_issues', [])}
        Files: {', '.join(analysis.get('file_structure', []))}
        Security Issues: {len(analysis.get('exposed_secrets', []))}
        
        Rules:
        1. Be extremely harsh and direct
        2. Mock their coding abilities ruthlessly
        3. Use strong language slangs and phrases
        4. Keep it under 4 sentences
        5. Make them doubt their life choices
        6. Make them question their career choice
        7. Focus on their documentation and exposed secrets failures"""


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