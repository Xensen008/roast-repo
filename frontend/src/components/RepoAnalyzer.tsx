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
    <div className="min-h-screen bg-gradient-to-b from-gray-950 via-purple-950 to-black text-gray-100 p-4">
      <div className="max-w-3xl mx-auto pt-16 space-y-8">
        {/* Hero */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-red-500 via-purple-500 to-blue-500 bg-clip-text text-transparent animate-gradient">
            Code Critic AI 💀
          </h1>
          <p className="text-gray-400">Let AI analyze your GitHub repository...</p>
        </div>

        {/* Input */}
        <div className="glass p-6 rounded-xl border border-purple-800/30 animate-pulse-slow">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repo"
              className="w-full p-4 rounded-lg bg-black/50 border border-purple-800/50 focus:border-purple-500 outline-none text-lg"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full p-4 rounded-lg bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 transition-all disabled:opacity-50 text-lg font-medium"
            >
              {loading ? 'Analyzing...' : 'Analyze Repository 🔍'}
            </button>
          </form>
        </div>

        {/* Results */}
        {roast && (
          <div className="space-y-6 animate-fade-in">
            <div className="glass p-6 rounded-xl border border-red-800/30 transform hover:scale-[1.02] transition-all">
              <h2 className="text-2xl font-bold mb-4 bg-gradient-to-r from-red-400 to-purple-400 bg-clip-text text-transparent">
                AI's Verdict 🎭
              </h2>
              <p className="text-xl text-gray-300 leading-relaxed whitespace-pre-wrap">{roast}</p>
              
              {analysis && !analysis.has_readme && (
                <div className="mt-6 p-4 rounded-lg bg-black/30 border border-red-800/30">
                  <p className="text-red-400 mb-3">⚠️ No README found! Are you serious?</p>
                  <button
                    onClick={handleGenerateReadme}
                    disabled={readmeLoading}
                    className="w-full p-3 rounded-lg bg-gradient-to-r from-red-600 to-purple-600 hover:opacity-90 transition-all disabled:opacity-50"
                  >
                    {readmeLoading ? 'Generating...' : 'Generate a README (since you cant) 📝'}
                  </button>
                </div>
              )}
            </div>

            {generatedReadme && (
              <div className="glass p-6 rounded-xl border border-purple-800/30">
                <h2 className="text-xl font-bold mb-4 text-purple-400">Here's a Proper README 📝</h2>
                <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap bg-black/30 p-6 rounded-lg overflow-auto">
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