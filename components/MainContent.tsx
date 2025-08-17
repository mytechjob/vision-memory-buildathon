import { useState } from 'react'
import { useProject } from '@/contexts/ProjectContext'
import { projectApi } from '@/utils/api'
import { Project } from '@/types'
import WelcomeScreen from './WelcomeScreen'
import SearchInterface from './SearchInterface'
import Sidebar from './Sidebar'

interface MainContentProps {
  images?: any[]
  onProjectDeleted: (projectId: number) => void
  onProjectCreated: (project: Project) => void
  onImagesProcessed: () => void
}

export default function MainContent({ 
  images, 
  onProjectDeleted, 
  onProjectCreated, 
  onImagesProcessed 
}: MainContentProps) {
  const { selectedProject, projects, setSelectedProject, setProjects } = useProject()
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)

  const handleProjectChange = (projectId: string) => {
    const project = projects.find(p => p.id === parseInt(projectId))
    setSelectedProject(project || null)
  }

  const handleDeleteProject = async () => {
    if (!selectedProject) return
    
    if (confirm(`Are you sure you want to delete "${selectedProject.name}"?`)) {
      try {
        const response = await projectApi.deleteProject(selectedProject.id)
        if (response.success) {
          setProjects(prev => prev.filter(p => p.id !== selectedProject.id))
          const remainingProjects = projects.filter(p => p.id !== selectedProject.id)
          setSelectedProject(remainingProjects.length > 0 ? remainingProjects[0] : null)
          onProjectDeleted(selectedProject.id)
        }
      } catch (error) {
        console.error('Failed to delete project:', error)
        alert('Failed to delete project')
      }
    }
  }

  const containerStyle: React.CSSProperties = {
    position: 'relative',
    backgroundColor: '#0E1117',
    height: '100vh',
    overflow: 'hidden'
  }

  const topBarStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '16px 24px',
    backgroundColor: '#1A1D23',
    borderBottom: '1px solid #2D3139',
    position: 'relative',
    zIndex: 10
  }

  const leftSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  }

  const newProjectButtonStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    backgroundColor: '#00C9A7',
    color: 'white',
    border: 'none',
    padding: '10px 16px',
    borderRadius: '8px',
    fontSize: '0.9rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s'
  }

  const titleStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontSize: '1.5rem',
    fontWeight: '600',
    color: '#FAFAFA'
  }

  const projectSelectorStyle: React.CSSProperties = {
    backgroundColor: '#0E1117',
    border: '1px solid #2D3139',
    color: '#FAFAFA',
    padding: '8px 12px',
    borderRadius: '8px',
    minWidth: '250px'
  }

  const contentStyle: React.CSSProperties = {
    height: 'calc(100vh - 64px)',
    overflow: 'auto',
    position: 'relative'
  }

  const overlayStyle: React.CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 20,
    opacity: isSidebarOpen ? 1 : 0,
    visibility: isSidebarOpen ? 'visible' : 'hidden',
    transition: 'opacity 0.3s ease, visibility 0.3s ease'
  }

  const sidebarStyle: React.CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '380px',
    height: '100vh',
    backgroundColor: '#0E1117',
    borderRight: '1px solid #2D3139',
    transform: isSidebarOpen ? 'translateX(0)' : 'translateX(-100%)',
    transition: 'transform 0.3s ease',
    zIndex: 30,
    overflow: 'auto'
  }

  return (
    <main style={containerStyle}>
      {/* Top Navigation Bar */}
      <div style={topBarStyle}>
        <div style={leftSectionStyle}>
          <button
            onClick={() => setIsSidebarOpen(true)}
            style={newProjectButtonStyle}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#00B59A'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#00C9A7'
            }}
          >
            <span style={{ fontSize: '1.2rem' }}>+</span>
            New Project
          </button>
          
          <div style={titleStyle}>
            <span>🔍</span>
            ScreenSage
          </div>
        </div>

        {projects.length > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <select
              value={selectedProject?.id || ''}
              onChange={(e) => handleProjectChange(e.target.value)}
              style={projectSelectorStyle}
            >
              <option value="">Select a project...</option>
              {projects.map(project => (
                <option key={project.id} value={project.id}>
                  {project.name} ({project.image_count} images)
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div style={contentStyle}>
        {selectedProject ? <SearchInterface /> : <WelcomeScreen />}
      </div>

      {/* Overlay */}
      <div 
        style={overlayStyle}
        onClick={() => setIsSidebarOpen(false)}
      />

      {/* Sliding Sidebar */}
      <div style={sidebarStyle}>
        <div style={{ padding: '24px' }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '24px'
          }}>
            <h2 style={{ color: '#FAFAFA', margin: 0, fontSize: '1.2rem' }}>Project Management</h2>
            <button
              onClick={() => setIsSidebarOpen(false)}
              style={{
                backgroundColor: 'transparent',
                border: 'none',
                color: '#B3B3B3',
                fontSize: '1.5rem',
                cursor: 'pointer',
                padding: '4px'
              }}
            >
              ×
            </button>
          </div>
          <Sidebar 
            onProjectCreated={(project) => {
              onProjectCreated(project)
              setIsSidebarOpen(false)
            }}
            onImagesProcessed={onImagesProcessed}
          />
        </div>
      </div>
    </main>
  )
}