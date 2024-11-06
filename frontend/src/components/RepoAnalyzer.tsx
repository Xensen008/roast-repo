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
  const [analysisData, setAnalysisData] = useState<any>(null)

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
              className="w-full p-4 rounded-xl bg-black/40 border border-white/20 focus:border-white/40 outline-none text-lg transition-all duration-300 hover:border-white/30"
            />
            <button
              type="submit"
              disabled={loading || !repoUrl.trim()}
              className="w-full p-4 rounded-xl bg-gradient-to-r from-white via-gray-200 to-white text-black text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-lg hover:shadow-white/10 animate-pulse-slow"
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
                  ANALYSIS COMPLETE
                </h2>
                <div className="flex gap-4 text-sm text-gray-400 border-b border-white/10 pb-4">
                  <span className="px-2 py-1 rounded bg-white/5">
                    {analysisData?.file_structure.filter((f: string) => f.includes('.env')).length} .env files
                  </span>
                  <span className="px-2 py-1 rounded bg-white/5">
                    {analysisData?.file_structure.filter((f: string) => f.toLowerCase().includes('readme')).length} README files
                  </span>
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
              <div className="glass border border-white/10 p-8 rounded-2xl backdrop-blur-lg shadow-2xl animate-fade-in">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
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
                    <CopyIcon className="w-6 h-6 text-white/70" />
                  </button>
                </div>
                <pre className="text-gray-300 leading-relaxed whitespace-pre-wrap bg-black/50 p-8 rounded-xl border border-white/5">
                  {generatedReadme}
                </pre>
                <p className="text-gray-500 text-sm mt-4 text-right">Generated by Code Critic - For God's Sake!</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default RepoAnalyzer