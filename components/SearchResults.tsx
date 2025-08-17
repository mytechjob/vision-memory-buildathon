import Image from 'next/image'

interface SearchResult {
  image_path: string
  confidence: number
  relevant_text: string
  description: string
}

interface SearchResultsProps {
  results: SearchResult[]
  query: string
  isLoading: boolean
}

export default function SearchResults({ results, query, isLoading }: SearchResultsProps) {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#00C9A7'
    if (confidence >= 0.6) return '#FFB800'
    return '#FF4B4B'
  }

  const getConfidenceLabel = (confidence: number) => {
    if (confidence >= 0.8) return 'High'
    if (confidence >= 0.6) return 'Medium'
    return 'Low'
  }

  const containerStyle: React.CSSProperties = {
    marginTop: '32px'
  }

  const headerStyle: React.CSSProperties = {
    marginBottom: '24px'
  }

  const titleStyle: React.CSSProperties = {
    color: '#FAFAFA',
    fontSize: '1.4rem',
    fontWeight: '600',
    margin: '0 0 8px 0'
  }

  const subtitleStyle: React.CSSProperties = {
    color: '#B3B3B3',
    fontSize: '1rem',
    margin: 0
  }

  const gridStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))',
    gap: '24px'
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '12px',
    overflow: 'hidden',
    transition: 'all 0.2s'
  }

  const imageContainerStyle: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    height: '250px',
    backgroundColor: '#0E1117'
  }

  const cardContentStyle: React.CSSProperties = {
    padding: '20px'
  }

  const confidenceBadgeStyle = (confidence: number): React.CSSProperties => ({
    display: 'inline-flex',
    alignItems: 'center',
    gap: '6px',
    backgroundColor: `${getConfidenceColor(confidence)}20`,
    color: getConfidenceColor(confidence),
    padding: '6px 12px',
    borderRadius: '16px',
    fontSize: '0.8rem',
    fontWeight: '500',
    marginBottom: '12px'
  })

  const noResultsStyle: React.CSSProperties = {
    textAlign: 'center',
    padding: '64px 32px',
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '12px'
  }

  const loadingStyle: React.CSSProperties = {
    textAlign: 'center',
    padding: '64px 32px',
    color: '#B3B3B3'
  }

  if (isLoading) {
    return (
      <div style={containerStyle}>
        <div style={loadingStyle}>
          <div style={{ fontSize: '2rem', marginBottom: '16px' }}>🔍</div>
          <h3 style={{ color: '#FAFAFA', margin: '0 0 8px 0' }}>Searching...</h3>
          <p style={{ margin: 0 }}>Analyzing images with AI to find the best matches</p>
        </div>
      </div>
    )
  }

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h2 style={titleStyle}>
          Search Results
        </h2>
        <p style={subtitleStyle}>
          {results.length > 0 
            ? `Found ${results.length} result${results.length === 1 ? '' : 's'} for "${query}"`
            : `No results found for "${query}"`
          }
        </p>
      </div>

      {results.length === 0 ? (
        <div style={noResultsStyle}>
          <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🔍</div>
          <h3 style={{ color: '#FAFAFA', margin: '0 0 12px 0' }}>No matches found</h3>
          <p style={{ color: '#B3B3B3', margin: '0 0 16px 0', maxWidth: '500px', marginLeft: 'auto', marginRight: 'auto' }}>
            Try adjusting your search terms or uploading more screenshots. 
            Our AI searches through both visible text and visual elements in your images.
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '8px', marginTop: '20px' }}>
            <span style={{ color: '#B3B3B3', fontSize: '0.9rem' }}>Try searching for:</span>
            <span style={{ color: '#00C9A7', fontSize: '0.9rem' }}>• UI elements</span>
            <span style={{ color: '#00C9A7', fontSize: '0.9rem' }}>• Text content</span>
            <span style={{ color: '#00C9A7', fontSize: '0.9rem' }}>• Colors and layouts</span>
          </div>
        </div>
      ) : (
        <div style={gridStyle}>
          {results.map((result, index) => (
            <div key={index} style={cardStyle}>
              <div style={imageContainerStyle}>
                <Image
                  src={result.image_path}
                  alt={`Search result ${index + 1}`}
                  fill
                  style={{ objectFit: 'contain' }}
                  unoptimized
                />
              </div>
              
              <div style={cardContentStyle}>
                <div style={confidenceBadgeStyle(result.confidence)}>
                  <div
                    style={{
                      width: '8px',
                      height: '8px',
                      backgroundColor: getConfidenceColor(result.confidence),
                      borderRadius: '50%'
                    }}
                  />
                  {getConfidenceLabel(result.confidence)} confidence
                  <span style={{ opacity: 0.8 }}>({Math.round(result.confidence * 100)}%)</span>
                </div>

                <h4 style={{ color: '#FAFAFA', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: '500' }}>
                  {result.description || 'Screenshot match'}
                </h4>
                
                {result.relevant_text && (
                  <p style={{ color: '#B3B3B3', margin: '0 0 12px 0', fontSize: '0.9rem', lineHeight: 1.5 }}>
                    <strong style={{ color: '#FAFAFA' }}>Detected text:</strong> {result.relevant_text}
                  </p>
                )}

                <p style={{ color: '#B3B3B3', margin: 0, fontSize: '0.8rem' }}>
                  {result.image_path.split('/').pop()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}