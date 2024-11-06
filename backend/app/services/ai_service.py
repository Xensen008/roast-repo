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
        env_files = [f for f in analysis.get('file_structure', []) if '.env' in f]
        readme_files = [f for f in analysis.get('file_structure', []) if 'readme' in f.lower()]
        
        if analysis.get('has_readme'):
            readme_content = analysis.get('readme_content', '').strip()
            readme_status = "empty README" if not readme_content else analysis.get('readme_content')
        
        file_stats = f"""
        Repository Stats:
        - {len(env_files)} .env files found: {', '.join(env_files) or 'None'}
        - {len(readme_files)} README files found: {', '.join(readme_files) or 'None'}
        """
        
        return f"""You are a brutal code critic who finds flaws in everything. Generate exactly 5-6 lines of brutal roasts.

        Repository Analysis:
        {file_stats}
        - README Status: {readme_status}
        - Latest Commits: {analysis.get('recent_commits', [])}
        - Open Issues: {analysis.get('open_issues', [])}
        - File Structure: {', '.join(analysis.get('file_structure', []))}
        - Security Issues: {len(analysis.get('exposed_secrets', []))}
        - Package Info: {analysis.get('package_info', 'No dependencies found')}

        Rules for Roasting:
        1. Generate EXACTLY 5-6 lines of brutal roasts
        2. Use extremely simple, offensive language and sarcasm
        3. Mock their coding practices, career choices, and life decisions
        4. Make each line as painful and accurate as possible
        5. End with the most brutal sarcastic suggestion
        6. Include specific criticisms about their .env and README management"""

    def _create_readme_prompt(self, analysis: dict) -> str:
        existing_readme = analysis.get('readme_content', '').strip()
        files = ', '.join(analysis.get('file_structure', []))
        package_info = analysis.get('package_info', 'No package info available')

        return f"""Generate a professional README.md for this repository.
        
        Current Repository State:
        - Existing README: {existing_readme if existing_readme else 'None'}
        - Files: {files}
        - Package Info: {package_info}
        
        Instructions:
        1. {f'Improve the existing README while maintaining its core structure' if existing_readme else 'Create a comprehensive new README'}
        2. Include all standard sections (Description, Installation, Usage, etc.)
        3. Add specific setup instructions based on package info
        4. Document any environment variables needed
        5. Add badges for build status, version, etc.
        6. Include code examples where relevant
        7. Maintain a professional tone
        
        Format the README in proper markdown with clear sections."""

# Create and export an instance
ai_service = AIService()