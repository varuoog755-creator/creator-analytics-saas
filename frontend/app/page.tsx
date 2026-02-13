import Link from 'next/link'

export default function Home() {
  return (
    <main style={{
      minHeight: '100vh',
      padding: '2rem',
      fontFamily: 'system-ui, sans-serif',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white'
    }}>
      <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
          🎬 Creator Analytics
        </h1>
        <p style={{ fontSize: '1.5rem', marginBottom: '2rem', opacity: 0.9 }}>
          All-in-One Creator Intelligence Platform
        </p>
        
        <div style={{ 
          background: 'rgba(255,255,255,0.1)', 
          padding: '2rem', 
          borderRadius: '1rem',
          marginBottom: '2rem'
        }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Track. Analyze. Grow.</h2>
          <p style={{ opacity: 0.8 }}>
            YouTube • TikTok • Instagram • Twitter/X • LinkedIn • Facebook • Twitch
          </p>
        </div>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button style={{
            padding: '1rem 2rem',
            fontSize: '1.1rem',
            background: 'white',
            color: '#667eea',
            border: 'none',
            borderRadius: '0.5rem',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}>
            Get Started Free
          </button>
          <button style={{
            padding: '1rem 2rem',
            fontSize: '1.1rem',
            background: 'transparent',
            color: 'white',
            border: '2px solid white',
            borderRadius: '0.5rem',
            cursor: 'pointer'
          }}>
            View Demo
          </button>
        </div>

        <p style={{ marginTop: '3rem', opacity: 0.6, fontSize: '0.9rem' }}>
          Coming Soon - Join the waitlist!
        </p>
      </div>
    </main>
  )
}
