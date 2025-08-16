
# Visual Memory Search Application

## Overview

**Visual Memory Search** is a Streamlit-based web application that allows users to upload screenshot images and search through them using natural language queries. The app combines OCR text extraction with AI-powered visual analysis to enable both text-based and visual-based searching.

## Technology Stack

### **Web Framework**
- **Streamlit**: Complete web application framework providing the user interface, session management, file handling, and real-time updates

### **AI & Machine Learning**
- **OpenAI GPT-4o**: Latest vision model for analyzing screenshot content and generating visual descriptions
- **scikit-learn**: 
  - TF-IDF vectorization for text similarity scoring
  - Cosine similarity calculations for search ranking
- **NumPy**: Numerical operations for similarity scoring and result ranking

### **Image Processing & OCR**
- **Tesseract OCR**: Text extraction from screenshots with custom configuration for better accuracy
- **OpenCV (cv2)**: Advanced image preprocessing including:
  - Noise reduction with `fastNlMeansDenoising`
  - Contrast enhancement with `convertScaleAbs`
  - Grayscale conversion for optimal OCR
- **PIL/Pillow**: Image manipulation, format conversion, thumbnail generation, and base64 encoding

### **Data Management**
- **Pandas**: Data structure management for processed screenshot metadata, search results, and analytics
- **Base64 encoding**: Image data serialization for storage and API transmission

### **Development Environment**
- **Python 3.11**: Runtime environment
- **Replit**: Cloud-based development and hosting platform
- **UV package manager**: Modern Python dependency management (as seen in pyproject.toml)

## Key Features Implemented

### **Multi-Modal Search**
- Text-based search through OCR-extracted content
- Visual search through AI-generated descriptions
- Combined search mode for comprehensive results

### **Advanced Image Processing Pipeline**
- Image validation and size checking
- OCR preprocessing with noise reduction and contrast enhancement
- Thumbnail generation with aspect ratio preservation
- Base64 encoding for efficient storage and transmission

### **Search Engine Architecture**
- TF-IDF vectorization for semantic text matching
- Confidence scoring (0-100%) for result ranking
- Match reasoning explanations for transparency
- Configurable result limits and filtering

### **User Experience**
- Real-time progress tracking during processing
- Interactive search interface with expandable content previews
- Processing summaries with file statistics
- Responsive layout with image thumbnails

## Project Structure

The application follows a modular architecture with specialized utility classes:

### **Core Components**
- `ImageProcessor`: Handles OCR, image preprocessing, and thumbnail generation
- `OpenAIClient`: Manages AI vision analysis and query intent understanding
- `SearchEngine`: Implements TF-IDF-based similarity search and result ranking
- `DataManager`: Handles data persistence and session management

### **Main Application**
- `app.py`: Main Streamlit application with user interface and workflow orchestration

### **Configuration**
- `.replit`: Deployment and workflow configuration
- `pyproject.toml`: Python dependencies and project metadata
- `.streamlit/config.toml`: Streamlit-specific configuration

## System Architecture

### **Frontend Architecture**
- **Framework**: Streamlit web application providing an intuitive drag-and-drop interface
- **Session Management**: Utilizes Streamlit's session state to persist processed data across user interactions
- **Layout**: Sidebar for file upload and processing controls, main area for search interface and results display

### **Backend Processing Pipeline**
- **Image Processing**: Multi-stage OCR pipeline using Tesseract with OpenCV preprocessing for enhanced text extraction accuracy
- **Visual Analysis**: Integration with OpenAI's GPT-4o Vision API for generating semantic descriptions of UI elements, colors, layouts, and interactive components
- **Data Management**: Session-based storage system with JSON serialization for processed screenshot metadata

## Installation & Dependencies

The project uses UV package manager with the following key dependencies:

```toml
dependencies = [
    "numpy>=2.3.2",
    "openai>=1.99.9",
    "opencv-python>=4.11.0.86",
    "pandas>=2.3.1",
    "pillow>=11.3.0",
    "pytesseract>=0.3.13",
    "scikit-learn>=1.7.1",
    "streamlit>=1.48.1",
]
```

## Deployment

The application is configured to run on **Replit** with the following specifications:
- **Port**: 5000 (forwarded to 80/443 in production)
- **Runtime**: Python 3.11 with Nix package management
- **Deployment Target**: Autoscale for production deployments
- **Start Command**: `streamlit run app.py --server.port 5000`

## Environment Requirements

- **Python**: 3.11+
- **System Dependencies**: 
  - Tesseract OCR engine
  - OpenGL libraries for image processing
  - Standard image format libraries (JPEG, PNG, TIFF, WebP)
- **API Keys**: OpenAI API key required for visual analysis features

## Usage

1. **Upload Screenshots**: Drag and drop or select screenshot images
2. **Processing**: App automatically extracts text via OCR and generates visual descriptions
3. **Search**: Use natural language queries to find specific screenshots
4. **Results**: View ranked results with confidence scores and match explanations

The app supports various search modes including text-only, visual-only, and combined search for optimal flexibility.
