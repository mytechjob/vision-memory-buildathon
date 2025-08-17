import { useProject } from '@/contexts/ProjectContext'
import WelcomeScreen from './WelcomeScreen'
import SearchInterface from './SearchInterface'

export default function MainContent() {
  const { selectedProject } = useProject()

  const containerStyle: React.CSSProperties = {
    flex: 1,
    backgroundColor: '#0E1117',
    height: '100vh',
    overflow: 'auto'
  }

  return (
    <main style={containerStyle}>
      {selectedProject ? <SearchInterface /> : <WelcomeScreen />}
    </main>
  )
}