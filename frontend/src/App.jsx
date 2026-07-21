import { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async (text, isUpdate = false) => {
    if (!text && !isUpdate) return
    
    // Route to the appropriate REST endpoint
    const userMsg = isUpdate ? 'Generate Leadership Brief' : text
    const endpoint = isUpdate ? '/api/leadership-update' : '/api/chat'
    const payload = isUpdate ? {} : { question: text }

    setMessages((prev) => [...prev, { role: 'user', content: userMsg }])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(`https://monday-bi-bknd.vercel.app${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      
      const data = await response.json()
      setMessages((prev) => [...prev, { role: 'agent', content: data.response }])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: 'agent', content: 'Error connecting to server. Is your backend running?' },
      ])
    }
    setLoading(false)
  }

  // Preset prompts for the evaluators to test your system quickly
  const promptChips = [
    'Calculate the total value of all open deals right now.',
    'How is our pipeline looking for the Powerline sector?',
    "Are there active work orders linked to 'On Hold' deals?",
  ]

  return (
    <main className="app-shell">
      <header className="hero">
        <p className="eyebrow">Intelligence Console</p>
        <h1>Monday.com BI Agent</h1>
        <p className="hero-subtitle">
          Ask about deals, pipeline movement, and operations in one place.
        </p>
      </header>

      <section className="actions">
        <button
          className="brief-button"
          onClick={() => sendMessage(null, true)}
          disabled={loading}
        >
          Generate Leadership Brief
        </button>

        <div className="chip-row">
          {promptChips.map((chip, idx) => (
            <button
              className="prompt-chip"
              key={idx}
              onClick={() => sendMessage(chip)}
              disabled={loading}
            >
              {chip}
            </button>
          ))}
        </div>
      </section>

      <section className="chat-window" aria-live="polite">
        {messages.length === 0 && (
          <p className="empty-state">
            Select a prompt above or ask a question to begin.
          </p>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`message-row ${m.role}`}>
            <div className={`message-bubble ${m.role}`}>
              {m.role === 'user' ? (
                <span>{m.content}</span>
              ) : (
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
              )}
            </div>
          </div>
        ))}

        {loading && <p className="loading-hint">Agent is querying monday.com and analyzing data...</p>}
        <div ref={chatEndRef} />
      </section>

      <form className="composer" onSubmit={(e) => { e.preventDefault(); sendMessage(input) }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage(input)}
          className="composer-input"
          placeholder="e.g., How's our pipeline looking for the energy sector?"
        />
        <button
          onClick={() => sendMessage(input)}
          disabled={loading}
          className="send-button"
        >
          Send
        </button>
      </form>
    </main>
  )
}

export default App