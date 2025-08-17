export default function WelcomeScreen() {
  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    padding: '48px',
    textAlign: 'center'
  }

  const titleStyle: React.CSSProperties = {
    fontSize: '2.5rem',
    fontWeight: '700',
    color: '#FAFAFA',
    marginBottom: '16px'
  }

  const subtitleStyle: React.CSSProperties = {
    fontSize: '1.1rem',
    color: '#B3B3B3',
    marginBottom: '32px',
    maxWidth: '600px'
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '12px',
    padding: '32px',
    maxWidth: '500px',
    width: '100%'
  }

  const featureListStyle: React.CSSProperties = {
    listStyle: 'none',
    padding: 0,
    margin: '24px 0 0 0'
  }

  const featureItemStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '8px 0',
    color: '#B3B3B3'
  }

  const iconStyle: React.CSSProperties = {
    fontSize: '1.2rem'
  }

  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>Welcome to ScreenSage</h1>
      <p style={subtitleStyle}>
        Your intelligent screenshot search companion. Create a project and upload 
        your screenshots to start searching with natural language queries.
      </p>
      
      <div style={cardStyle}>
        <h3 style={{ color: '#FAFAFA', margin: '0 0 16px 0' }}>Getting Started</h3>
        <ol style={{ color: '#B3B3B3', paddingLeft: '20px', margin: 0 }}>
          <li style={{ marginBottom: '8px' }}>Create a new project in the sidebar</li>
          <li style={{ marginBottom: '8px' }}>Upload your screenshots to the project</li>
          <li style={{ marginBottom: '8px' }}>Use natural language to search through your images</li>
        </ol>

        <ul style={featureListStyle}>
          <li style={featureItemStyle}>
            <span style={iconStyle}>🔍</span>
            <span>Natural language search queries</span>
          </li>
          <li style={featureItemStyle}>
            <span style={iconStyle}>🤖</span>
            <span>AI-powered OCR and vision analysis</span>
          </li>
          <li style={featureItemStyle}>
            <span style={iconStyle}>📊</span>
            <span>Confidence scores for search results</span>
          </li>
          <li style={featureItemStyle}>
            <span style={iconStyle}>⚡</span>
            <span>Fast and accurate image processing</span>
          </li>
        </ul>
      </div>
    </div>
  )
}