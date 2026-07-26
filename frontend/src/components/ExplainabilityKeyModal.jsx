import { useState, useEffect } from 'react'
import { Info, Key, CheckCircle, AlertCircle, X } from 'lucide-react'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8002/api'

export default function ExplainabilityKeyModal({ isOpen, onClose, onSaved }) {
  const [provider, setProvider] = useState('nvidia')
  const [key, setKey] = useState('')
  const [status, setStatus] = useState(null)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!isOpen) return
    fetch(`${API_BASE}/explainability/key`)
      .then(r => r.json())
      .then(data => {
        if (data.provider) setProvider(data.provider)
        if (data.present) setStatus('present')
        else setStatus(null)
      })
      .catch(() => {})
  }, [isOpen])

  const submit = async (e) => {
    if (e) e.preventDefault()
    if (!key.trim()) return
    setSaving(true)
    try {
      const res = await fetch(`${API_BASE}/explainability/key`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider, api_key: key.trim() })
      })
      if (res.ok) {
        setStatus('saved')
        if (onSaved) onSaved()
        onClose()
      } else {
        setStatus('error')
      }
    } catch (e) {
      setStatus('error')
    } finally {
      setSaving(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="bg-slate-900 border border-slate-700 text-white rounded-2xl shadow-2xl p-6 w-full max-w-md z-10 relative">
        <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <Key className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-semibold text-white">AI Explainability Key</h3>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white p-1 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {status === 'present' && (
          <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs px-3 py-2 rounded-lg mb-4">
            <CheckCircle className="w-4 h-4 flex-shrink-0" />
            <span>An API key is already configured on the server. You can update it below.</span>
          </div>
        )}

        {status === 'error' && (
          <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 text-red-400 text-xs px-3 py-2 rounded-lg mb-4">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>Failed to save API key. Please check your backend connection.</span>
          </div>
        )}

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Provider</label>
            <select
              value={provider}
              onChange={e => setProvider(e.target.value)}
              className="w-full p-2.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <option value="nvidia">NVIDIA NIM (Llama 3.1 70B)</option>
              <option value="gemini">Google Gemini</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              API Key ({provider === 'nvidia' ? 'nvapi-...' : 'AIzaSy...'})
            </label>
            <input
              type="password"
              value={key}
              onChange={e => setKey(e.target.value)}
              placeholder="Paste your API key here..."
              className="w-full p-2.5 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 font-mono"
              required
            />
            <p className="text-xs text-gray-400 mt-1.5 flex items-center gap-1">
              <Info className="w-3.5 h-3.5 text-slate-400" />
              <span>Keys are stored locally on your backend server and ignored by git.</span>
            </p>
          </div>

          <div className="pt-2 flex items-center justify-between border-t border-slate-800 mt-4">
            <a
              href={provider === 'nvidia' ? 'https://build.nvidia.com/' : 'https://aistudio.google.com/'}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-emerald-400 hover:underline flex items-center gap-1"
            >
              Get free {provider === 'nvidia' ? 'NVIDIA' : 'Gemini'} Key →
            </a>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-3.5 py-2 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-gray-300 rounded-lg transition"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving || !key.trim()}
                className="px-4 py-2 text-xs font-medium bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-black font-semibold rounded-lg transition"
              >
                {saving ? 'Saving...' : 'Save API Key'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}
