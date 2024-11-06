import React, { useState, FormEvent } from 'react'
import { toast } from 'react-hot-toast'
import { analyzeRepository, generateReadme } from '../services/api'

const RepoAnalyzer: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [readmeLoading, setReadmeLoading] = useState(false)
  const [roast, setRoast] = useState<string | null>(null)
  const [generatedReadme, setGeneratedReadme] = useState<string | null>(null)

  const handleAnalyze = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const data = await analyzeRepository(repoUrl)
      setRoast(data.roast)
      toast.success('Analysis complete', {
        style: {
          background: '#000',
          color: '#fff',
          border: '1px solid rgba(255,255,255,0.1)'
        }
      });
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
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white p-4">
      <div className="max-w-4xl mx-auto pt-16 space-y-12">
        {/* Hero */}
        <div className="text-center space-y-6 animate-fade-in">
          <h1 className="text-7xl font-bold bg-gradient-to-r from-white via-gray-300 to-white bg-clip-text text-transparent animate-gradient">
            CODE CRITIC
          </h1>
          <p className="text-gray-400 text-xl font-light tracking-wide">
            Submit your repository for a brutal code review
          </p>
        </div>

        {/* Input */}
        <div className="glass border border-white/10 p-8 rounded-2xl backdrop-blur-lg shadow-2xl animate-fade-in">
          <form onSubmit={handleAnalyze} className="space-y-6">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repo"
              className="w-full p-6 rounded-xl bg-black/40 border border-white/20 focus:border-white/40 outline-none text-lg transition-all duration-300 hover:border-white/30"
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full p-6 rounded-xl bg-gradient-to-r from-white via-gray-200 to-white text-black text-lg font-medium disabled:opacity-50 transition-all duration-300 hover:shadow-lg hover:shadow-white/10 animate-pulse-slow"
            >
              {loading ? 'ANALYZING...' : 'ANALYZE REPOSITORY'}
            </button>
          </form>
        </div>

        {/* Results */}
        {roast && (
          <div className="space-y-8 animate-fade-in">
            <div className="glass border border-white/10 p-8 rounded-2xl backdrop-blur-lg shadow-2xl">
              <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                ANALYSIS COMPLETE
              </h2>
              <p className="text-xl text-gray-300 leading-relaxed">{roast}</p>
              
              <div className="mt-8 pt-8 border-t border-white/10">
                <button
                  onClick={handleGenerateReadme}
                  disabled={readmeLoading}
                  className="w-full p-6 rounded-xl bg-white/5 text-white border border-white/20 disabled:opacity-50 transition-all duration-300 hover:bg-white/10 hover:border-white/30"
                >
                  {readmeLoading ? 'GENERATING README...' : 'GENERATE PROPER README'}
                </button>
              </div>
            </div>

            {generatedReadme && (
              <div className="glass border border-white/10 p-8 rounded-2xl backdrop-blur-lg shadow-2xl animate-fade-in">
                <h2 className="text-3xl font-bold mb-6 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  GENERATED README
                </h2>
                <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap bg-black/50 p-8 rounded-xl border border-white/5">
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