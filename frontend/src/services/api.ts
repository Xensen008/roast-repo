interface RepoAnalysisResponse {
  roast: string;
  analysis: {
    has_readme: boolean;
    file_structure: string[];
    open_issues: any[];
    recent_commits: any[];
  };
}

interface ReadmeResponse {
  readme: string;
}

export const analyzeRepository = async (repoUrl: string): Promise<RepoAnalysisResponse> => {
  const response = await fetch('/api/analyze-repo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to analyze repository')
  }

  return await response.json()
}

export const generateReadme = async (repoUrl: string): Promise<ReadmeResponse> => {
  const response = await fetch('/api/generate-readme', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to generate README')
  }

  return await response.json()
}
