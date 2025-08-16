# Visual Memory Search Application

## Overview

This is a Streamlit-based Visual Memory Search application that allows users to search through their screenshot collections using natural language queries. The app combines OCR text extraction with AI-powered visual description generation to create a comprehensive search experience. Users can upload screenshots and then search for them using both text-based queries ("error message about auth") and visual-based queries ("red dialog box with blue button").

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application providing an intuitive drag-and-drop interface
- **Session Management**: Utilizes Streamlit's session state to persist processed data across user interactions
- **Layout**: Sidebar for file upload and processing controls, main area for search interface and results display

### Backend Processing Pipeline
- **Image Processing**: Multi-stage OCR pipeline using Tesseract with OpenCV preprocessing for enhanced text extraction accuracy
- **Visual Analysis**: Integration with OpenAI's GPT-4o Vision API for generating semantic descriptions of UI elements, colors, layouts, and interactive components
- **Data Management**: Session-based storage system with JSON serialization for processed screenshot metadata

### Search Engine Architecture
- **Dual Search Strategy**: 
  - TF-IDF vectorization for keyword-based text matching
  - Sentence Transformers (all-MiniLM-L6-v2) for semantic similarity search
- **Ranking Algorithm**: Combined scoring system that weighs both text relevance and visual similarity
- **Result Processing**: Returns top 5 matches with confidence scores and match explanations

### Data Flow Design
1. **Input Stage**: File upload validation and format checking (PNG, JPG, JPEG, WebP)
2. **Processing Stage**: Parallel OCR text extraction and AI visual description generation
3. **Indexing Stage**: Feature vector creation using TF-IDF and semantic embeddings
4. **Query Stage**: Multi-modal search across text and visual features with relevance ranking

### Image Processing Strategy
- **OCR Enhancement**: Preprocessing pipeline including denoising, contrast enhancement, and grayscale conversion
- **Thumbnail Generation**: Automatic creation of preview images for result display
- **Format Normalization**: Standardized image handling across different input formats

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4o model for visual analysis and screenshot description generation
- **Sentence Transformers**: HuggingFace model (all-MiniLM-L6-v2) for semantic text embeddings

### Image Processing Libraries
- **Tesseract OCR**: Text extraction from screenshots with custom configuration
- **OpenCV**: Image preprocessing and enhancement for improved OCR accuracy
- **PIL/Pillow**: Image manipulation, format conversion, and thumbnail generation

### Machine Learning Stack
- **scikit-learn**: TF-IDF vectorization and cosine similarity calculations
- **pandas**: Data structure management for processed screenshot metadata
- **numpy**: Numerical operations for similarity scoring and ranking

### Web Framework
- **Streamlit**: Complete web application framework with built-in session management and file handling capabilities