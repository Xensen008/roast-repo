from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import settings
from .services import github_service, ai_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://codecritic.vercel.app"],
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
            
        # Generate roast using AI
        roast = await ai_service.generate_roast(analysis)
        
        return {
            "roast": roast,
            "analysis": {
                "has_readme": analysis.get("has_readme", False),
                "file_structure": analysis.get("file_structure", []),
                "open_issues": analysis.get("open_issues", []),
                "recent_commits": analysis.get("recent_commits", [])
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
            
        # Generate readme using AI
        readme = await ai_service.generate_readme(analysis)
        
        return {
            "readme": readme
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))