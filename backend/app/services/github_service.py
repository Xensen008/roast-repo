from aiohttp import ClientSession
import base64
import re
from ..config import settings

class GitHubService:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
    
    async def get_repo_contents(self, owner: str, repo: str, path: str = "") -> dict:
        async with ClientSession() as session:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    async def analyze_repo_structure(self, owner: str, repo: str) -> dict:
        contents = await self.get_repo_contents(owner, repo)
        if not contents:
            return None
            
        analysis = {
            "has_readme": False,
            "readme_needs_update": False,
            "has_env": False,
            "exposed_secrets": [],
            "package_info": None,
            "file_structure": [],
            "recent_commits": await self.get_recent_commits(owner, repo),
            "open_issues": await self.get_open_issues(owner, repo)
        }
        
        for item in contents:
            name = item["name"].lower()
            if name == "readme.md":
                analysis["has_readme"] = True
                readme_content = await self._get_file_content(item["download_url"])
                analysis["readme_content"] = readme_content
                analysis["readme_needs_update"] = self._is_readme_incomplete(readme_content)
            elif ".env" in name:
                analysis["has_env"] = True
                content = await self._get_file_content(item["download_url"])
                analysis["exposed_secrets"].extend(self._find_secrets(content))
            elif name in ["package.json", "requirements.txt", "pyproject.toml"]:
                analysis["package_info"] = await self._get_file_content(item["download_url"])
            
            analysis["file_structure"].append(item["name"])
            
        return analysis
    
    async def _get_file_content(self, url: str) -> str:
        async with ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    if 'raw.githubusercontent.com' in url:
                        return await response.text()
                    data = await response.json()
                    if isinstance(data, dict) and "content" in data:
                        return base64.b64decode(data["content"]).decode('utf-8')
                    return str(data)
                return ""
    
    def _find_secrets(self, content: str) -> list:
        secret_patterns = [
            r"(?i)(api[_-]key|apikey|secret|password|token)[\w\d_-]*[\s]*[=:]\s*[\'\"]([^\'\"]*)[\'\"]",
            r"(?i)aws[_-]access[_-]key[_-]id[\s]*[=:]\s*[\'\"]([^\'\"]*)[\'\"]",
        ]
        found_secrets = []
        for pattern in secret_patterns:
            matches = re.finditer(pattern, content)
            found_secrets.extend(m.group(0) for m in matches)
        return found_secrets
    
    def _is_readme_incomplete(self, content: str) -> bool:
        if not content or len(content.strip()) < 50:
            return True
            
        # Check for default/template READMEs
        default_patterns = [
            r"# Getting Started with Create React App",
            r"This is a \[Next\.js\] project bootstrapped",
            r"This README would normally document whatever steps",
            r"<\?php\s+namespace\s+",
            r"# Getting Started with \[.*\]",
            r"# Default README"
        ]
        
        for pattern in default_patterns:
            if re.search(pattern, content):
                return True
                
        # Check for minimal content
        required_sections = [
            r"#.*installation|setup|getting started",
            r"#.*usage|features|functionality",
            r"#.*configuration|env|environment",
            r"#.*prerequisites|requirements",
        ]
        
        found_sections = 0
        for pattern in required_sections:
            if re.search(pattern, content, re.I):
                found_sections += 1
                
        return found_sections < 2  # README needs update if less than 2 key sections found
    
    async def get_recent_commits(self, owner: str, repo: str, limit: int = 5) -> list:
        async with ClientSession() as session:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            async with session.get(url, headers=self.headers, params={"per_page": limit}) as response:
                if response.status == 200:
                    commits = await response.json()
                    return [{"message": c["commit"]["message"], "author": c["commit"]["author"]["name"]} for c in commits]
                return []
    
    async def get_open_issues(self, owner: str, repo: str, limit: int = 5) -> list:
        async with ClientSession() as session:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            async with session.get(url, headers=self.headers, params={"state": "open", "per_page": limit}) as response:
                if response.status == 200:
                    issues = await response.json()
                    return [{"title": i["title"], "state": i["state"]} for i in issues]
                return []

# Create and export an instance
github_service = GitHubService(settings.GITHUB_TOKEN)