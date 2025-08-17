import { useState } from 'react'
import { useProject } from '@/contexts/ProjectContext'
import { projectApi } from '@/utils/api'

interface ProjectFormProps {
  onProjectCreated?: (project: any) => void
}

export default function ProjectForm({ onProjectCreated }: ProjectFormProps) {
  const { projects, setProjects, setSelectedProject } = useProject()
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  })
  const [isCreating, setIsCreating] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.name.trim()) return

    setIsCreating(true)
    try {
      const response = await projectApi.createProject(formData)
      if (response.success && response.project) {
        const newProject = response.project
        setProjects(prev => [...prev, newProject])
        setSelectedProject(newProject)
        setFormData({ name: '', description: '' })
        onProjectCreated?.(newProject)
      }
    } catch (error) {
      console.error('Failed to create project:', error)
      alert('Failed to create project')
    } finally {
      setIsCreating(false)
    }
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '8px',
    padding: '24px'
  }

  const inputStyle: React.CSSProperties = {
    width: '100%',
    backgroundColor: '#0E1117',
    border: '1px solid #2D3139',
    color: '#FAFAFA',
    padding: '12px',
    borderRadius: '8px',
    fontSize: '1rem',
    marginBottom: '16px',
    outline: 'none',
    transition: 'border-color 0.2s'
  }

  const textareaStyle: React.CSSProperties = {
    ...inputStyle,
    resize: 'vertical',
    minHeight: '80px',
    fontFamily: 'inherit'
  }

  const buttonStyle: React.CSSProperties = {
    width: '100%',
    backgroundColor: '#00C9A7',
    color: 'white',
    border: 'none',
    padding: '12px',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.2s',
    opacity: isCreating ? 0.7 : 1
  }

  const projectListStyle: React.CSSProperties = {
    marginTop: '24px'
  }

  const projectItemStyle: React.CSSProperties = {
    backgroundColor: '#0E1117',
    border: '1px solid #2D3139',
    borderRadius: '6px',
    padding: '16px',
    marginBottom: '8px',
    cursor: 'pointer',
    transition: 'all 0.2s'
  }

  return (
    <div>
      <div style={cardStyle}>
        <h3 style={{ color: '#FAFAFA', margin: '0 0 16px 0', fontSize: '1.2rem' }}>Create New Project</h3>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Project name"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            style={inputStyle}
            required
          />
          
          <textarea
            placeholder="Project description (optional)"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            style={textareaStyle}
          />
          
          <button
            type="submit"
            disabled={isCreating || !formData.name.trim()}
            style={buttonStyle}
          >
            {isCreating ? 'Creating...' : 'Create Project'}
          </button>
        </form>
      </div>

      {projects.length > 0 && (
        <div style={projectListStyle}>
          <h4 style={{ color: '#FAFAFA', margin: '0 0 16px 0', fontSize: '1rem' }}>
            Existing Projects ({projects.length})
          </h4>
          
          {projects.map(project => (
            <div
              key={project.id}
              style={projectItemStyle}
              onClick={() => setSelectedProject(project)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h5 style={{ color: '#FAFAFA', margin: '0 0 4px 0', fontSize: '0.9rem' }}>
                    {project.name}
                  </h5>
                  {project.description && (
                    <p style={{ color: '#B3B3B3', margin: 0, fontSize: '0.8rem' }}>
                      {project.description}
                    </p>
                  )}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ color: '#00C9A7', fontSize: '0.8rem', fontWeight: '500' }}>
                    {project.image_count} images
                  </span>
                  <div
                    style={{
                      width: '8px',
                      height: '8px',
                      backgroundColor: project.status === 'active' ? '#00C9A7' : '#FFB800',
                      borderRadius: '50%'
                    }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}