export interface Project {
  id: number
  name: string
  description: string
  created_at: string
  updated_at: string
  image_count: number
}

export interface ProcessedImage {
  id?: number
  filename: string
  file_size: number
  image_dimensions: string
  ocr_text: string
  visual_description: string
  thumbnail_b64: string
  processing_mode: string
  processed_timestamp: string
  similarity_score?: number
  confidence_score?: number
  match_reason?: string
}

export interface SearchResult extends ProcessedImage {
  similarity_score: number
  confidence_score: number
  match_reason: string
}

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
}

export interface ProcessingStats {
  processed_count: number
  total_uploaded: number
  processed_images: ProcessedImage[]
}

export type ProcessingMode = 
  | 'Fast Local Vision'
  | 'Detailed - OpenAI'
  | 'Detailed - Gemini'

export type SearchMode = 
  | 'combined'
  | 'text only'
  | 'visual only'