import React, { useState, FormEvent } from 'react'
import { toast } from 'react-hot-toast'
import { analyzeRepository, generateReadme } from '../services/api'

const RepoAnalyzer: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [readmeLoading, setReadmeLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)
  const [roast, setRoast] = useState<string | null>(null)
  const [generatedReadme, setGeneratedReadme] = useState<string | null>(null)

  const handleAnalyze = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const data = await analyzeRepository(repoUrl)
      setAnalysis(data.analysis)
      setRoast(data.roast)
      toast.success('Roast served! 🔥')
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to roast')
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateReadme = async () => {
    setReadmeLoading(true)
    try {
      const data = await generateReadme(repoUrl)
      setGeneratedReadme(data.readme)
      toast.success('README generated successfully! 📝')
    } catch (error) {
      toast.error('Failed to generate README')
    } finally {
      setReadmeLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 to-black text-gray-100 p-4">
      <div className="max-w-3xl mx-auto pt-16 space-y-8">
        {/* Hero */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-orange-400 to-rose-600 bg-clip-text text-transparent">
            Repo Roaster 🔥
          </h1>
          <p className="text-gray-400">Enter a GitHub repo URL and get ready for some constructive criticism</p>
        </div>

        {/* Input */}
        <div className="glass p-6 rounded-xl border border-gray-800/50">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repo"
              className="w-full p-3 rounded-lg bg-black/50 border border-gray-800 focus:border-orange-500 outline-none"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full p-3 rounded-lg bg-gradient-to-r from-orange-500 to-rose-600 hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {loading ? 'Analyzing...' : 'Roast This Repo 🔥'}
            </button>
          </form>
        </div>

        {/* Result */}
        {roast && (
          <div className="space-y-6">
            <div className="glass p-6 rounded-xl border border-gray-800/50">
              <h2 className="text-xl font-semibold mb-4 text-orange-400">The Roast 🔥</h2>
              <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">{roast}</p>
            </div>

            {analysis && !analysis.has_readme && (
              <div className="glass p-6 rounded-xl border border-gray-800/50">
                <h2 className="text-xl font-semibold mb-4 text-orange-400">Missing README? 📝</h2>
                <button
                  onClick={handleGenerateReadme}
                  disabled={readmeLoading}
                  className="w-full p-3 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 hover:opacity-90 transition-opacity disabled:opacity-50"
                >
                  {readmeLoading ? 'Generating...' : 'Generate README'}
                </button>
              </div>
            )}

            {generatedReadme && (
              <div className="glass p-6 rounded-xl border border-gray-800/50">
                <h2 className="text-xl font-semibold mb-4 text-orange-400">Generated README 📝</h2>
                <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap bg-black/30 p-4 rounded-lg">
                  {generatedReadme}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default RepoAnalyzer