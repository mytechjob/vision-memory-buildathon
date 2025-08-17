import { useProject } from '@/contexts/ProjectContext'
import { projectApi } from '@/utils/api'

export default function Header() {
  const { projects, selectedProject, setSelectedProject, setProjects } = useProject()

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
        }
      } catch (error) {
        console.error('Failed to delete project:', error)
        alert('Failed to delete project')
      }
    }
  }

  const headerStyle: React.CSSProperties = {
    background: 'linear-gradient(135deg, #0E1117 0%, #1A1D23 100%)',
    borderBottom: '1px solid #2D3139',
    padding: '24px',
    color: '#FAFAFA'
  }

  const titleStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontSize: '1.8rem',
    fontWeight: '600',
    margin: '0 0 24px 0'
  }

  const subtitleStyle: React.CSSProperties = {
    color: '#B3B3B3',
    fontSize: '0.9rem',
    marginBottom: '24px'
  }

  const selectStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    color: '#FAFAFA',
    padding: '8px 12px',
    borderRadius: '8px',
    minWidth: '300px',
    marginRight: '16px'
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '8px',
    padding: '24px'
  }

  return (
    <header style={headerStyle}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={titleStyle}>
          <span>🔍</span>
          ScreenSage
        </div>
        
        <p style={subtitleStyle}>
          Search through your screenshots using natural language queries
        </p>

        {projects.length > 0 && (
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <select
              value={selectedProject?.id || ''}
              onChange={(e) => handleProjectChange(e.target.value)}
              style={selectStyle}
            >
              <option value="">Select a project...</option>
              {projects.map(project => (
                <option key={project.id} value={project.id}>
                  {project.name} ({project.image_count} images)
                </option>
              ))}
            </select>
            
            {selectedProject && (
              <button
                onClick={handleDeleteProject}
                className="btn-danger"
                title="Delete selected project"
              >
                🗑️
              </button>
            )}
          </div>
        )}

        {projects.length === 0 && (
          <div style={cardStyle}>
            <h4 style={{ color: '#FAFAFA', fontSize: '1.2rem', margin: '0 0 8px 0' }}>No projects found</h4>
            <p style={{ color: '#B3B3B3', margin: 0 }}>Create your first project using the sidebar to get started.</p>
          </div>
        )}
      </div>
    </header>
  )
}