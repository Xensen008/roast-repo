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
        try:
            prompt = self._create_readme_prompt(repo_analysis)
            response = await self.model.generate_content_async(
                prompt,
                safety_settings=self.safety_settings,
                generation_config={
                    'temperature': 0.2,  # Lower temperature for more accurate output
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 2048  # Ensure enough length for detailed README
                }
            )
            return response.text
        except Exception as e:
            if "429" in str(e) and self.current_key_index < len(self.api_keys) - 1:
                self.rotate_api_key()
                return await self.generate_readme(repo_analysis)
            raise e

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

    def _analyze_project_structure(self, analysis: dict) -> dict:
        """Deeply analyze project structure and tech stack"""
        files = analysis.get('file_structure', [])
        package_json = analysis.get('package_content', {})
        main_file = analysis.get('main_file_content', '')
        existing_readme = analysis.get('readme_content', '')

        # Framework Detection
        framework = {
            "name": None,
            "type": None,
            "version": None
        }

        if "next" in str(package_json):
            framework = {"name": "Next.js", "type": "fullstack", "version": package_json.get('dependencies', {}).get('next')}
        elif "react" in str(package_json):
            framework = {"name": "React", "type": "frontend", "version": package_json.get('dependencies', {}).get('react')}
        elif "vue" in str(package_json):
            framework = {"name": "Vue", "type": "frontend", "version": package_json.get('dependencies', {}).get('vue')}
        elif "express" in str(package_json):
            framework = {"name": "Express", "type": "backend", "version": package_json.get('dependencies', {}).get('express')}

        # Project Type Detection
        project_type = None
        if any(f.endswith(('.tsx', '.jsx', '.vue')) for f in files):
            project_type = "frontend"
        elif any(f.endswith(('.py', 'go', 'rs')) for f in files):
            project_type = "backend"
        elif framework["type"] == "fullstack":
            project_type = "fullstack"

        return {
            "framework": framework,
            "project_type": project_type,
            "dependencies": package_json.get('dependencies', {}),
            "dev_dependencies": package_json.get('devDependencies', {}),
            "scripts": package_json.get('scripts', {}),
            "has_typescript": any(f.endswith('.ts') or f.endswith('.tsx') for f in files),
            "has_tests": any('test' in f.lower() or 'spec' in f.lower() for f in files),
            "has_docker": any('dockerfile' in f.lower() or 'docker-compose' in f.lower() for f in files),
            "has_ci": any('.github/workflows' in f for f in files),
            "env_files": [f for f in files if '.env' in f.lower()],
            "existing_readme": existing_readme
        }

    def _create_readme_prompt(self, analysis: dict) -> str:
        project_info = self._analyze_project_structure(analysis)
        
        return f"""You are an expert technical writer. Generate a comprehensive README.md based on this project analysis:

Project Overview:
- Framework: {project_info['framework']['name']} ({project_info['framework']['version']})
- Type: {project_info['project_type']}
- TypeScript: {'Yes' if project_info['has_typescript'] else 'No'}
- Testing: {'Present' if project_info['has_tests'] else 'Not found'}
- Docker: {'Configured' if project_info['has_docker'] else 'Not found'}
- CI/CD: {'Setup' if project_info['has_ci'] else 'Not found'}
- Environment Files: {project_info['env_files']}

Dependencies: {project_info['dependencies']}
Dev Dependencies: {project_info['dev_dependencies']}
Scripts: {project_info['scripts']}

Existing README: {project_info['existing_readme'] if project_info['existing_readme'] else 'None'}

Instructions:
1. If existing README exists:
   - Keep useful information from existing README
   - Update tech stack and setup instructions
   - Modernize formatting and structure
   - Add missing critical sections

2. If no README exists:
   - Create clear project description based on codebase analysis
   - Document actual features visible in the code
   - Include accurate setup instructions for detected framework
   - List all available scripts with explanations
   - Add environment variable documentation if env files exist

3. Required Sections:
   - Project Title and Description
   - Features (based on actual code)
   - Prerequisites (based on dependencies)
   - Installation & Setup (framework-specific)
   - Available Scripts (from package.json)
   - Environment Variables (if env files exist)
   - Development Guide
   - Deployment Instructions (if Docker/CI present)

4. Important Rules:
   - Use modern markdown formatting with code blocks
   - Include relevant badges for detected tech
   - Be specific about versions and requirements
   - Focus on accuracy over comprehensiveness
   - No placeholder text or assumptions
   - Include actual commands from scripts

Remember: This is a professional README that developers will use to understand and set up the project. Be clear, accurate, and practical."""

# Create and export an instance
ai_service = AIService()