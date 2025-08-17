import { createContext, useContext, useState, ReactNode } from 'react'
import { Project } from '@/types'

interface ProjectContextType {
  projects: Project[]
  setProjects: (projects: Project[] | ((prev: Project[]) => Project[])) => void
  selectedProject: Project | null
  setSelectedProject: (project: Project | null) => void
}

const ProjectContext = createContext<ProjectContextType | undefined>(undefined)

export function ProjectProvider({ children }: { children: ReactNode }) {
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)

  return (
    <ProjectContext.Provider value={{
      projects,
      setProjects,
      selectedProject,
      setSelectedProject
    }}>
      {children}
    </ProjectContext.Provider>
  )
}

export function useProject() {
  const context = useContext(ProjectContext)
  if (context === undefined) {
    throw new Error('useProject must be used within a ProjectProvider')
  }
  return context
}