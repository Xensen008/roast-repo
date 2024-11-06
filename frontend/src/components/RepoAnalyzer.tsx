import React, { useState, FormEvent } from 'react'
import { toast } from 'react-hot-toast'
import { analyzeRepository, generateReadme } from '../services/api'
import { CopyIcon } from './Icons'

const RepoAnalyzer: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [readmeLoading, setReadmeLoading] = useState(false)
  const [roast, setRoast] = useState<string | null>(null)
  const [generatedReadme, setGeneratedReadme] = useState<string | null>(null)
  const [_analysisData, setAnalysisData] = useState<any>(null)

  const handleAnalyze = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setRoast(null)
    setGeneratedReadme(null)
    
    try {
      const data = await analyzeRepository(repoUrl)
      setRoast(data.roast)
      setAnalysisData(data.analysis)
      const envCount = data.analysis.file_structure.filter(f => f.includes('.env')).length
      const readmeCount = data.analysis.file_structure.filter(f => f.toLowerCase().includes('readme')).length
      
      toast.success(
        <div>
          <div>Analysis complete</div>
          <div className="text-sm opacity-80">
            Found: {envCount} .env files, {readmeCount} README files
          </div>
        </div>,
        {
          style: {
            background: '#000',
            color: '#fff',
            border: '1px solid rgba(255,255,255,0.1)'
          }
        }
      );
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
        {/* GitHub Corner */}
        <a href="https://github.com/xensen008/repo-roaster" 
           className="github-corner absolute top-0 right-0" 
           aria-label="View source on GitHub">
          <svg width="80" height="80" viewBox="0 0 250 250" className="fill-white text-black" aria-hidden="true">
            <path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path>
            <path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" className="octo-arm"></path>
            <path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" className="octo-body"></path>
          </svg>
        </a>

        {/* Hero */}
        <div className="text-center space-y-4 animate-fade-in px-4">
          <h1 className="text-4xl md:text-7xl font-bold bg-gradient-to-r from-white via-gray-300 to-white bg-clip-text text-transparent animate-gradient">
            CODE CRITIC
          </h1>
          <p className="text-gray-400 text-lg md:text-xl font-light tracking-wide">
            Let's roast you and your code till it's well done 🔥
          </p>
        </div>

        {/* Input */}
        <div className="glass border border-white/10 p-4 md:p-8 rounded-2xl backdrop-blur-lg shadow-2xl animate-fade-in mx-4">
          <form onSubmit={handleAnalyze} className="space-y-4 md:space-y-6">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repo"
              className="w-full p-3 md:p-4 rounded-xl bg-black/40 border border-white/20 focus:border-white/40 outline-none text-base md:text-lg transition-all duration-300 hover:border-white/30"
            />
            <button
              type="submit"
              disabled={loading || !repoUrl.trim()}
              className="w-full p-3 md:p-4 rounded-xl bg-gradient-to-r from-white via-gray-200 to-white text-black text-base md:text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-lg hover:shadow-white/10 animate-pulse-slow"
            >
              {loading ? 'ANALYZING...' : 'ANALYZE REPOSITORY'}
            </button>
          </form>
        </div>

        {/* Results */}
        {roast && (
          <div className="space-y-8 animate-fade-in">
            <div className="glass border border-white/10 p-8 rounded-2xl backdrop-blur-lg shadow-2xl">
              <div className="flex flex-col space-y-4">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                  Roast as you deserve
                </h2>
                <div className="text-sm text-red-400 border-b border-white/10 pb-4">
                  Skill Issue Level: Maximum Cringe
                </div>
              </div>
              <p className="text-xl text-gray-300 leading-relaxed mt-6 whitespace-pre-line">{roast}</p>
              
              <div className="mt-8 pt-8 border-t border-white/10">
                <button
                  onClick={handleGenerateReadme}
                  disabled={readmeLoading || loading}
                  className="w-full p-4 rounded-xl bg-white/5 text-white border border-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:bg-white/10 hover:border-white/30"
                >
                  {readmeLoading ? 'GENERATING README...' : 'GENERATE PROPER README'}
                </button>
              </div>
            </div>

            {generatedReadme && (
              <div className="glass border border-white/10 p-4 md:p-8 rounded-2xl backdrop-blur-lg shadow-2xl animate-fade-in mx-4">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    GENERATED README
                  </h2>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(generatedReadme);
                      toast.success('README copied to clipboard!', {
                        style: {
                          background: '#000',
                          color: '#fff',
                          border: '1px solid rgba(255,255,255,0.1)'
                        }
                      });
                    }}
                    className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-all"
                  >
                    <CopyIcon className="w-5 h-5 md:w-6 md:h-6 text-white/70" />
                  </button>
                </div>
                <div className="overflow-x-auto">
                  <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap bg-black/50 p-4 md:p-8 rounded-xl border border-white/5 text-sm md:text-base">
                    {generatedReadme}
                  </pre>
                </div>
                <p className="text-gray-500 text-xs md:text-sm mt-4 text-right">Generated by Code Critic - For God's Sake!</p>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-gray-500 py-8 border-t border-white/10">
          <p>Developed with hate by <a href="https://arnabjk008.vercel.app" className="text-white hover:text-gray-300 underline">arnabjk</a></p>
        </footer>
      </div>
    </div>
  )
}

export default RepoAnalyzer