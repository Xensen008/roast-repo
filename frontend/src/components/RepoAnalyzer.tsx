import React, { useState, FormEvent } from 'react'
import { toast } from 'react-hot-toast'
import { analyzeRepository } from '../services/api'

const RepoAnalyzer: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [roast, setRoast] = useState<string | null>(null)

  const handleAnalyze = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const data = await analyzeRepository(repoUrl)
      setRoast(data.roast)
      toast.success('Roast served! 🔥')
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to roast')
      setRoast('Even if the repo doesn\'t exist, I can still roast your typing skills 😉')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-950 to-black text-gray-100 p-4">
      <div className="max-w-2xl mx-auto pt-16 space-y-8">
        {/* Hero */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-orange-400 to-rose-600 bg-clip-text text-transparent">
            Repo Roaster 🔥
          </h1>
          <p className="text-gray-400">Enter a GitHub repo URL and get ready for some constructive criticism</p>
        </div>

        {/* Input */}
        <div className="glass p-6 rounded-xl border border-gray-800/50 backdrop-blur-xl">
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
              {loading ? 'Preparing roast...' : 'Roast This Repo 🔥'}
            </button>
          </form>
        </div>

        {/* Result */}
        {roast && (
          <div className="glass p-6 rounded-xl border border-gray-800/50 backdrop-blur-xl">
            <h2 className="text-xl font-semibold mb-4 text-orange-400">The Roast 🔥</h2>
            <p className="text-gray-300 leading-relaxed">{roast}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default RepoAnalyzer