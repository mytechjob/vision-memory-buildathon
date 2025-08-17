import axios from 'axios'

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-app-domain.com' 
  : ''

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

export const projectApi = {
  async getProjects() {
    const response = await api.get('/api/projects')
    return response.data
  },

  async createProject(projectData: { name: string; description?: string }) {
    const response = await api.post('/api/projects', projectData)
    return response.data
  },

  async deleteProject(id: number) {
    const response = await api.delete(`/api/projects/${id}`)
    return response.data
  },

  async getProjectImages(id: number) {
    const response = await api.get(`/api/projects/${id}/images`)
    return response.data
  }
}

export const uploadApi = {
  async uploadScreenshot(projectId: number, file: File, onProgress?: (progress: number) => void) {
    const formData = new FormData()
    formData.append('screenshots', file)
    formData.append('processingMode', 'Fast Local Vision')

    const response = await api.post(`/api/projects/${projectId}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      },
    })
    
    return response.data
  }
}

export const searchApi = {
  async searchScreenshots(projectId: number, query: string, searchMode: string = 'combined', maxResults: number = 10) {
    const response = await api.post('/api/search', {
      projectId,
      query,
      searchMode,
      maxResults
    })
    return response.data
  }
}

export const healthApi = {
  async check() {
    const response = await api.get('/api/health')
    return response.data
  }
}