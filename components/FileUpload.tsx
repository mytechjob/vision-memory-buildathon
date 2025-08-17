import { useState, useRef } from 'react'
import { useProject } from '@/contexts/ProjectContext'
import { uploadApi, projectApi } from '@/utils/api'

interface FileUploadProps {
  onImagesProcessed?: () => void
}

export default function FileUpload({ onImagesProcessed }: FileUploadProps) {
  const { selectedProject, setProjects } = useProject()
  const [isDragOver, setIsDragOver] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStatus, setUploadStatus] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = () => {
    setIsDragOver(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
    const files = Array.from(e.dataTransfer.files)
    handleFiles(files)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    handleFiles(files)
  }

  const handleFiles = async (files: File[]) => {
    if (!selectedProject || files.length === 0) return

    const imageFiles = files.filter(file => file.type.startsWith('image/'))
    if (imageFiles.length === 0) {
      alert('Please select image files only')
      return
    }

    setIsUploading(true)
    setUploadProgress(0)
    setUploadStatus(`Uploading ${imageFiles.length} image(s)...`)

    try {
      for (let i = 0; i < imageFiles.length; i++) {
        const file = imageFiles[i]
        setUploadStatus(`Uploading ${file.name}...`)
        
        const response = await uploadApi.uploadScreenshot(selectedProject.id, file)
        
        if (!response.success) {
          throw new Error(`Failed to upload ${file.name}`)
        }
        
        setUploadProgress(((i + 1) / imageFiles.length) * 100)
      }

      // Refresh project data to update image count
      const projectsResponse = await projectApi.getProjects()
      if (projectsResponse.success && projectsResponse.projects) {
        setProjects(projectsResponse.projects)
      }

      setUploadStatus('Upload completed successfully!')
      onImagesProcessed?.()
      setTimeout(() => {
        setUploadStatus('')
        setUploadProgress(0)
      }, 3000)

    } catch (error) {
      console.error('Upload failed:', error)
      setUploadStatus('Upload failed. Please try again.')
      setTimeout(() => {
        setUploadStatus('')
        setUploadProgress(0)
      }, 3000)
    } finally {
      setIsUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1A1D23',
    border: '1px solid #2D3139',
    borderRadius: '8px',
    padding: '24px'
  }

  const dropzoneStyle: React.CSSProperties = {
    border: `2px dashed ${isDragOver ? '#00C9A7' : '#2D3139'}`,
    borderRadius: '8px',
    padding: '32px',
    textAlign: 'center',
    backgroundColor: isDragOver ? 'rgba(0, 201, 167, 0.05)' : 'transparent',
    cursor: 'pointer',
    transition: 'all 0.2s',
    marginBottom: '16px'
  }

  const progressBarStyle: React.CSSProperties = {
    width: '100%',
    height: '8px',
    backgroundColor: '#2D3139',
    borderRadius: '4px',
    overflow: 'hidden',
    marginBottom: '8px'
  }

  const progressFillStyle: React.CSSProperties = {
    height: '100%',
    backgroundColor: '#00C9A7',
    width: `${uploadProgress}%`,
    transition: 'width 0.3s ease'
  }

  const buttonStyle: React.CSSProperties = {
    backgroundColor: '#00C9A7',
    color: 'white',
    border: 'none',
    padding: '12px 24px',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '500',
    cursor: isUploading ? 'not-allowed' : 'pointer',
    opacity: isUploading ? 0.7 : 1,
    transition: 'all 0.2s'
  }

  if (!selectedProject) {
    return (
      <div style={cardStyle}>
        <p style={{ color: '#B3B3B3', margin: 0, textAlign: 'center' }}>
          Select a project first to upload screenshots
        </p>
      </div>
    )
  }

  return (
    <div style={cardStyle}>
      <h3 style={{ color: '#FAFAFA', margin: '0 0 16px 0', fontSize: '1.2rem' }}>
        Upload Screenshots
      </h3>
      
      <p style={{ color: '#B3B3B3', margin: '0 0 16px 0', fontSize: '0.9rem' }}>
        Project: <span style={{ color: '#00C9A7', fontWeight: '500' }}>{selectedProject.name}</span>
      </p>

      <div
        style={dropzoneStyle}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div style={{ color: '#FAFAFA', fontSize: '2rem', marginBottom: '8px' }}>📁</div>
        <p style={{ color: '#FAFAFA', margin: '0 0 8px 0', fontSize: '1rem', fontWeight: '500' }}>
          {isDragOver ? 'Drop files here' : 'Drag and drop images here'}
        </p>
        <p style={{ color: '#B3B3B3', margin: 0, fontSize: '0.9rem' }}>
          or click to select files
        </p>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
      />

      <button
        onClick={() => fileInputRef.current?.click()}
        disabled={isUploading}
        style={buttonStyle}
      >
        {isUploading ? 'Uploading...' : 'Choose Files'}
      </button>

      {isUploading && (
        <div style={{ marginTop: '16px' }}>
          <div style={progressBarStyle}>
            <div style={progressFillStyle} />
          </div>
          <p style={{ color: '#B3B3B3', margin: 0, fontSize: '0.9rem', textAlign: 'center' }}>
            {Math.round(uploadProgress)}%
          </p>
        </div>
      )}

      {uploadStatus && (
        <div style={{ marginTop: '16px' }}>
          <p style={{ 
            color: uploadStatus.includes('failed') ? '#FF4B4B' : '#00C9A7', 
            margin: 0, 
            fontSize: '0.9rem',
            textAlign: 'center',
            fontWeight: '500'
          }}>
            {uploadStatus}
          </p>
        </div>
      )}
    </div>
  )
}