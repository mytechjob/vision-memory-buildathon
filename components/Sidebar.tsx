import { useState } from 'react'
import { useProject } from '@/contexts/ProjectContext'
import ProjectForm from './ProjectForm'
import FileUpload from './FileUpload'

export default function Sidebar() {
  const { selectedProject } = useProject()
  const [activeTab, setActiveTab] = useState<'projects' | 'upload'>('projects')

  const sidebarStyle: React.CSSProperties = {
    backgroundColor: '#0E1117',
    borderRight: '1px solid #2D3139',
    width: '350px',
    height: '100vh',
    overflow: 'auto',
    padding: '24px'
  }

  const tabBarStyle: React.CSSProperties = {
    display: 'flex',
    gap: '8px',
    marginBottom: '24px',
    padding: '4px',
    backgroundColor: '#1A1D23',
    borderRadius: '8px'
  }

  const tabStyle: React.CSSProperties = {
    flex: 1,
    padding: '8px 16px',
    border: 'none',
    background: 'transparent',
    color: '#B3B3B3',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
    transition: 'all 0.2s'
  }

  const activeTabStyle: React.CSSProperties = {
    ...tabStyle,
    backgroundColor: '#00C9A7',
    color: 'white'
  }

  const inactiveTabStyle: React.CSSProperties = {
    ...tabStyle
  }

  return (
    <aside style={sidebarStyle}>
      <div style={tabBarStyle}>
        <button
          onClick={() => setActiveTab('projects')}
          style={activeTab === 'projects' ? activeTabStyle : inactiveTabStyle}
        >
          Projects
        </button>
        <button
          onClick={() => setActiveTab('upload')}
          style={activeTab === 'upload' ? activeTabStyle : inactiveTabStyle}
        >
          Upload
        </button>
      </div>

      {activeTab === 'projects' && <ProjectForm />}
      {activeTab === 'upload' && (
        <div>
          {selectedProject ? (
            <FileUpload />
          ) : (
            <div
              style={{
                backgroundColor: '#1A1D23',
                border: '1px solid #2D3139',
                borderRadius: '8px',
                padding: '24px',
                textAlign: 'center'
              }}
            >
              <p style={{ color: '#B3B3B3', margin: 0 }}>
                Select a project first to upload screenshots
              </p>
            </div>
          )}
        </div>
      )}
    </aside>
  )
}