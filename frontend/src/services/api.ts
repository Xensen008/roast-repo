interface RepoAnalysisResponse {
  roast: string;
}

export const analyzeRepository = async (repoUrl: string): Promise<RepoAnalysisResponse> => {
  try {
    const response = await fetch('/api/analyze-repo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ repo_url: repoUrl })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to analyze repository')
    }

    return await response.json()
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}
