import google.generativeai as genai
from ..config import settings

class AIService:
    def __init__(self):
        self.model = None
        self.current_key_index = 0
        self.api_keys = settings.api_keys_list
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        self.initialize(self.api_keys[0])
    
    def rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        new_key = self.api_keys[self.current_key_index]
        self.initialize(new_key)
        return new_key

    def initialize(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    async def generate_roast(self, repo_analysis: dict) -> str:
        for _ in range(len(self.api_keys)):  # Try all keys
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
                if "429" in str(e) and self.current_key_index < len(self.api_keys) - 1:
                    self.rotate_api_key()
                    continue
                return f"Failed to generate roast: {str(e)}"
        return "All API keys have been exhausted. Please try again later."
    
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
        1. Generate 5 to 10 lines of merciless roasts that hit harder than a hangover.
        2. Use the most offensive language and sarcasm you can muster.
        3. Tear apart their coding practices, career choices, and every pathetic life decision they've made.
        4. Each line should be a gut punch—painful, precise, and unforgettable.
        5. Wrap it up with the most savage, sarcastic suggestion that leaves them questioning their existence.
        6. Don't hold back on the jabs about their sorry .env and README management—make it sting.
        7. Sprinkle in some foul language and slang to crank up the intensity to eleven.
        8. If they dare to have no README, unleash an extra wave of ridicule for their utter incompetence.
        """

    def _detect_tech_stack(self, files: list, package_info: str) -> dict:
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "deployment": [],
            "framework": []
        }
        
        # Frontend detection
        if any(f.endswith(('.jsx', '.tsx')) for f in files):
            tech_stack["frontend"].append("React")
            if "next" in package_info.lower():
                tech_stack["framework"].append("Next.js")
        elif any(f.endswith('.vue') for f in files):
            tech_stack["frontend"].append("Vue.js")
        elif any(f.endswith('.svelte') for f in files):
            tech_stack["frontend"].append("Svelte")

        # Backend detection
        if any(f.endswith('.py') for f in files):
            tech_stack["backend"].append("Python")
            if "fastapi" in package_info.lower():
                tech_stack["framework"].append("FastAPI")
            elif "django" in package_info.lower():
                tech_stack["framework"].append("Django")
        elif any(f.endswith('.js') for f in files) and ("express" in package_info.lower()):
            tech_stack["backend"].append("Node.js")
            tech_stack["framework"].append("Express.js")

        # Database detection
        if "mongodb" in package_info.lower():
            tech_stack["database"].append("MongoDB")
        elif "postgresql" in package_info.lower():
            tech_stack["database"].append("PostgreSQL")
        elif "prisma" in package_info.lower():
            tech_stack["database"].append("Prisma ORM")

        # Deployment detection
        if "vercel.json" in files or "next.config.js" in files:
            tech_stack["deployment"].append("Vercel")
        elif "netlify.toml" in files:
            tech_stack["deployment"].append("Netlify")
        
        return tech_stack

    def _create_readme_prompt(self, analysis: dict) -> str:
        files = analysis.get('file_structure', [])
        package_info = analysis.get('package_info', '')
        tech_stack = self._detect_tech_stack(files, package_info)
        
        return f"""You are a technical documentation expert. Generate a comprehensive README.md for this project.

Project Analysis:
- Tech Stack:
  Frontend: {', '.join(tech_stack['frontend']) or 'Not detected'}
  Backend: {', '.join(tech_stack['backend']) or 'Not detected'}
  Framework: {', '.join(tech_stack['framework']) or 'Not detected'}
  Database: {', '.join(tech_stack['database']) or 'Not detected'}
  Deployment: {', '.join(tech_stack['deployment']) or 'Not detected'}
- Package Info: {package_info}

Instructions:
1. Focus on accurately describing the detected technology stack
2. Structure the README as follows:
   - Project Title and Description
   - Features (based on the actual project structure)
   - Tech Stack (only include detected technologies)
   - Installation & Setup (specific to the detected framework)
   - Environment Variables (if any detected)
   - Deployment (based on detected deployment configuration)

Important:
- Only mention technologies and features that are actually detected
- describe nicely and make it direcly ready to use Readme
- Don't make assumptions about undetected features
- Keep descriptions accurate and specific to this project
- Use proper markdown formatting
- Include relevant badges only for detected technologies

Format the README in clear, professional markdown."""

# Create and export an instance
ai_service = AIService()