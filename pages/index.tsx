import { useState, useEffect } from 'react'
import Head from 'next/head'
import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
import MainContent from '@/components/MainContent'
import { useProject } from '@/contexts/ProjectContext'
import { Project, ProcessedImage } from '@/types'
import { projectApi } from '@/utils/api'

export default function Home() {
  const { selectedProject, setSelectedProject, projects, setProjects } = useProject()
  const [isLoading, setIsLoading] = useState(true)
  const [projectImages, setProjectImages] = useState<ProcessedImage[]>([])

  useEffect(() => {
    loadProjects()
  }, [])

  useEffect(() => {
    if (selectedProject) {
      loadProjectImages()
    } else {
      setProjectImages([])
    }
  }, [selectedProject])

  const loadProjects = async () => {
    try {
      setIsLoading(true)
      const response = await projectApi.getProjects()
      if (response.success) {
        setProjects(response.projects)
        // Auto-select first project if available
        if (response.projects.length > 0 && !selectedProject) {
          setSelectedProject(response.projects[0])
        }
      }
    } catch (error) {
      console.error('Failed to load projects:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadProjectImages = async () => {
    if (!selectedProject) return
    
    try {
      const response = await projectApi.getProjectImages(selectedProject.id)
      if (response.success) {
        setProjectImages(response.data)
      }
    } catch (error) {
      console.error('Failed to load project images:', error)
    }
  }

  const handleProjectCreated = (newProject: Project) => {
    setProjects(prev => [newProject, ...prev])
    setSelectedProject(newProject)
  }

  const handleProjectDeleted = (deletedProjectId: number) => {
    setProjects(prev => prev.filter(p => p.id !== deletedProjectId))
    if (selectedProject?.id === deletedProjectId) {
      const remainingProjects = projects.filter(p => p.id !== deletedProjectId)
      setSelectedProject(remainingProjects.length > 0 ? remainingProjects[0] : null)
    }
  }

  const handleImagesProcessed = () => {
    loadProjectImages()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-dark-500 text-dark-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent-success mx-auto mb-4"></div>
          <p className="text-dark-200">Loading ScreenSage...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <Head>
        <title>ScreenSage - Visual Memory Search</title>
        <meta name="description" content="Search through your screenshots using natural language queries" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-dark-500 text-dark-100">
        <Header />
        
        <div className="flex">
          <Sidebar 
            onProjectCreated={handleProjectCreated}
            onImagesProcessed={handleImagesProcessed}
          />
          
          <MainContent 
            images={projectImages}
            onProjectDeleted={handleProjectDeleted}
          />
        </div>
      </div>
    </>
  )
}