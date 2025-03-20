from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .config import settings
from .services import github_service, ai_service

app = FastAPI()

# Add root endpoint for health check
@app.get("/")
async def root():
    return {"status": "ok", "message": "Code Critic API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codecritic.arnabjk008.tech/", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str
    project_description: Optional[str] = None
    features: Optional[str] = None
    setup: Optional[str] = None
    environment: Optional[str] = None

@app.post("/analyze-repo")
async def analyze_repo(repo_request: RepoRequest):
    try:
        parts = repo_request.repo_url.rstrip('/').split('/')
        if len(parts) < 5:
            raise HTTPException(status_code=400, detail="Invalid repository URL")
        
        owner, repo = parts[-2:]
        
        # Analyze repository structure
        analysis = await github_service.analyze_repo_structure(owner, repo)
        if not analysis:
            raise HTTPException(status_code=404, detail="Repository not found")
            
        # Generate roast using AI
        roast = await ai_service.generate_roast(analysis)
        
        # Determine README status message
        readme_status = {
            "has_readme": analysis.get("has_readme", False),
            "needs_update": analysis.get("readme_needs_update", False),
            "message": None
        }
        
        if analysis.get("has_readme"):
            readme_status["message"] = "To generate a new README, please delete the existing README.md from your repository first."
        
        return {
            "roast": roast,
            "analysis": {
                "has_readme": analysis.get("has_readme", False),
                "readme_needs_update": analysis.get("readme_needs_update", False),
                "file_structure": analysis.get("file_structure", []),
                "open_issues": analysis.get("open_issues", []),
                "recent_commits": analysis.get("recent_commits", []),
                "readme_status": readme_status
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-readme")
async def generate_readme(repo_request: RepoRequest):
    try:
        parts = repo_request.repo_url.rstrip('/').split('/')
        if len(parts) < 5:
            raise HTTPException(status_code=400, detail="Invalid repository URL")
        
        owner, repo = parts[-2:]
        
        # Analyze repository structure
        analysis = await github_service.analyze_repo_structure(owner, repo)
        if not analysis:
            raise HTTPException(status_code=404, detail="Repository not found")
        
        # Check if we need project description
        if not analysis.get('readme_content') and not repo_request.project_description:
            return {
                "needsDescription": True,
                "analysis": {
                    "readme_needs_update": True
                }
            }
            
        # Add description and other details to analysis if provided
        if repo_request.project_description:
            analysis['project_description'] = repo_request.project_description
        if repo_request.features:
            analysis['project_features'] = repo_request.features
        if repo_request.setup:
            analysis['setup_instructions'] = repo_request.setup
        if repo_request.environment:
            analysis['environment_variables'] = repo_request.environment
            
        # Generate readme using AI
        readme = await ai_service.generate_readme(analysis)
        
        return {
            "readme": readme,
            "needsDescription": False,
            "analysis": {
                "readme_needs_update": analysis.get("readme_needs_update", False)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))