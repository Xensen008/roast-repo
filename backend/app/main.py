from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import settings
from .services.github_service import github_service
from .services.ai_service import ai_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str

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
            
        # Generate roast and readme using AI
        roast = await ai_service.generate_roast(analysis)
        readme = await ai_service.generate_readme(analysis) if not analysis["has_readme"] else None
        
        return {
            "roast": roast,
            "has_readme": analysis["has_readme"],
            "generated_readme": readme,
            "analysis": {
                "file_structure": analysis["file_structure"],
                "open_issues": analysis["open_issues"],
                "recent_commits": analysis["recent_commits"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))