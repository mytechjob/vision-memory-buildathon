import { useState } from 'react'
import { useProject } from '@/contexts/ProjectContext'
import { searchApi } from '@/utils/api'
import SearchResults from './SearchResults'

interface SearchResult {
  image_path: string
  confidence: number
  relevant_text: string
  description: string
}

export default function SearchInterface() {
  const { selectedProject } = useProject()
  const [query, setQuery] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedProject || !query.trim()) return

    setIsSearching(true)
    setHasSearched(true)
    
    try {
      const response = await searchApi.searchScreenshots(selectedProject.id, query)
      console.log('Search response:', response) // Debug log
      if (response.success && response.data) {
        setSearchResults(response.data)
      } else {
        setSearchResults([])
      }
    } catch (error) {
      console.error('Search failed:', error)
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  const containerStyle: React.CSSProperties = {
    padding: '32px',
    height: '100vh',
    overflow: 'auto'
  }

  const headerStyle: React.CSSProperties = {
    marginBottom: '32px'
  }

  const titleStyle: React.CSSProperties = {
    color: '#FAFAFA',
    fontSize: '1.8rem',
    fontWeight: '600',
    margin: '0 0 8px 0'
  }

  const subtitleStyle: React.CSSProperties = {
    color: '#B3B3B3',
    fontSize: '1rem',
    margin: '0 0 24px 0'
  }

  const searchFormStyle: React.CSSProperties = {
    display: 'flex',
    gap: '16px',
    marginBottom: '32px',
    alignItems: 'center'
  }

  const inputStyle: React.CSSProperties = {
    flex: 1,
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    color: '#FAFAFA',
    padding: '16px',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
    transition: 'border-color 0.2s'
  }

  const buttonStyle: React.CSSProperties = {
    backgroundColor: '#00C9A7',
    color: 'white',
    border: 'none',
    padding: '16px 32px',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: isSearching ? 'not-allowed' : 'pointer',
    opacity: isSearching ? 0.7 : 1,
    transition: 'all 0.2s',
    whiteSpace: 'nowrap'
  }

  const exampleQueriesStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '32px'
  }

  const exampleButtonStyle: React.CSSProperties = {
    backgroundColor: 'transparent',
    border: '1px solid #2D3139',
    color: '#B3B3B3',
    padding: '8px 16px',
    borderRadius: '6px',
    fontSize: '0.9rem',
    cursor: 'pointer',
    margin: '4px 8px 4px 0',
    transition: 'all 0.2s'
  }

  const exampleQueries = [
    'screenshots with login forms',
    'images containing error messages',
    'buttons with blue background',
    'dashboard or analytics views',
    'mobile app interfaces',
    'settings or configuration pages'
  ]

  if (!selectedProject) {
    return (
      <div style={containerStyle}>
        <div style={{ textAlign: 'center', color: '#B3B3B3', marginTop: '200px' }}>
          <p>Select a project to start searching</p>
        </div>
      </div>
    )
  }

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <h1 style={titleStyle}>Search Screenshots</h1>
        <p style={subtitleStyle}>
          Project: <span style={{ color: '#00C9A7', fontWeight: '500' }}>{selectedProject.name}</span>
          {selectedProject.image_count > 0 && (
            <span> • {selectedProject.image_count} images available</span>
          )}
        </p>
      </div>

      <form onSubmit={handleSearch} style={searchFormStyle}>
        <input
          type="text"
          placeholder="Describe what you're looking for... (e.g., 'login screen with blue button')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={inputStyle}
          disabled={isSearching}
        />
        <button
          type="submit"
          disabled={isSearching || !query.trim()}
          style={buttonStyle}
        >
          {isSearching ? 'Searching...' : 'Search'}
        </button>
      </form>

      {!hasSearched && selectedProject.image_count > 0 && (
        <div style={exampleQueriesStyle}>
          <h3 style={{ color: '#FAFAFA', margin: '0 0 16px 0', fontSize: '1.1rem' }}>
            Try these example searches:
          </h3>
          <div>
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                style={exampleButtonStyle}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedProject.image_count === 0 && (
        <div style={exampleQueriesStyle}>
          <h3 style={{ color: '#FAFAFA', margin: '0 0 8px 0', fontSize: '1.1rem' }}>
            No images found
          </h3>
          <p style={{ color: '#B3B3B3', margin: 0 }}>
            Upload some screenshots to this project first, then you can search through them.
          </p>
        </div>
      )}

      {hasSearched && (
        <SearchResults
          results={searchResults}
          query={query}
          isLoading={isSearching}
        />
      )}
    </div>
  )
}