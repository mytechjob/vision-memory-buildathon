import streamlit as st
import os
import tempfile
import shutil
import pandas as pd
from PIL import Image
import time
from typing import List, Dict, Any
import base64
from io import BytesIO

from utils.image_processor import ImageProcessor
from utils.search_engine import SearchEngine
from utils.openai_client import OpenAIClient
from utils.gemini_client import GeminiClient
from utils.local_vision_client import LocalVisionClient
from utils.data_manager import DataManager

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = pd.DataFrame()
if 'search_index' not in st.session_state:
    st.session_state.search_index = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'selected_project_id' not in st.session_state:
    st.session_state.selected_project_id = None
if 'current_project_name' not in st.session_state:
    st.session_state.current_project_name = None

def main():
    # Custom CSS for modern dark theme matching the provided design
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0E1117 0%, #1A1D23 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        border: 1px solid #2D3139;
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #FAFAFA;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .header-subtitle {
        color: #B3B3B3;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .project-card {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #00C9A7;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #B3B3B3;
        margin: 0;
    }
    
    .search-container {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stSelectbox > div > div {
        background-color: #1A1D23;
        border: 1px solid #2D3139;
    }
    
    .stTextInput > div > div > input {
        background-color: #1A1D23;
        border: 1px solid #2D3139;
        color: #FAFAFA;
    }
    
    /* Table styling */
    .result-table {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    
    .table-header {
        background: #262B35;
        padding: 1rem;
        border-bottom: 1px solid #2D3139;
        font-weight: 600;
        color: #FAFAFA;
    }
    
    .table-row {
        padding: 1rem;
        border-bottom: 1px solid #2D3139;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .status-active { background-color: #00C9A7; }
    .status-processing { background-color: #FFB800; }
    .status-error { background-color: #FF4B4B; }
    
    .confidence-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .confidence-high { background-color: rgba(0, 201, 167, 0.2); color: #00C9A7; }
    .confidence-medium { background-color: rgba(255, 184, 0, 0.2); color: #FFB800; }
    .confidence-low { background-color: rgba(255, 75, 75, 0.2); color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <div class="header-title">
            <span>🔍</span>
            Visual Memory Search
        </div>
        <div class="header-subtitle">Search through your screenshots using natural language queries</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    image_processor = ImageProcessor()
    openai_client = OpenAIClient()
    gemini_client = GeminiClient()
    local_vision_client = LocalVisionClient()
    data_manager = DataManager()
    
    # Get existing projects
    projects = data_manager.get_projects()
    
    # Project management in main area
    st.markdown("### 📂 Project Management")
    
    # Set default selection to first project if none selected and projects exist
    if not st.session_state.selected_project_id and projects:
        st.session_state.selected_project_id = projects[0]['id']
        st.session_state.current_project_name = projects[0]['name']
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if projects:
            # Create options without "Create New Project" option
            project_options = [f"{p['name']} ({p['image_count']} images)" for p in projects]
            
            # Find current selected index
            current_index = 0
            if st.session_state.selected_project_id:
                for i, project in enumerate(projects):
                    if project['id'] == st.session_state.selected_project_id:
                        current_index = i
                        break
            
            selected_option = st.selectbox(
                "Choose a project:",
                project_options,
                index=current_index,
                key="project_selector"
            )
            
            # Handle project selection
            if selected_option:
                project_name = selected_option.split(" (")[0]
                selected_project = next((p for p in projects if p['name'] == project_name), None)
                if selected_project:
                    st.session_state.selected_project_id = selected_project['id']
                    st.session_state.current_project_name = selected_project['name']
        else:
            st.markdown("""
            <div class="project-card">
                <h4 style="color: #FAFAFA; margin-top: 0;">No projects found</h4>
                <p style="color: #B3B3B3;">Create your first project using the sidebar to get started.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if projects and st.session_state.selected_project_id:
            if st.button("Delete Project", type="secondary", help="Delete selected project"):
                # Find project to delete
                project_to_delete = next((p for p in projects if p['id'] == st.session_state.selected_project_id), None)
                if project_to_delete:
                    if data_manager.delete_project(project_to_delete['id']):
                        st.success(f"Deleted project: {project_to_delete['name']}")
                        st.session_state.selected_project_id = None
                        st.session_state.current_project_name = None
                        st.rerun()
    
    # Modern sidebar styling
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: #0E1117;
    }
    
    .upload-section {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .processing-stats {
        background: #1A1D23;
        border: 1px solid #2D3139;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .sidebar-header {
        color: #FAFAFA;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #2D3139;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for project creation and file upload
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🏗️ Project Controls</div>', unsafe_allow_html=True)
        
        # Project Creation Section
        if st.button("New Project", type="primary", use_container_width=True):
            # Toggle project creation form visibility
            if 'show_project_form' not in st.session_state:
                st.session_state.show_project_form = False
            st.session_state.show_project_form = not st.session_state.show_project_form
        
        # Show project creation form when button is clicked
        if st.session_state.get('show_project_form', False):
            st.subheader("Create New Project")
            
            new_project_name = st.text_input("Project Name:", placeholder="My Screenshots")
            new_project_desc = st.text_area("Description (optional):", placeholder="Brief description of this project...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create", type="primary", disabled=not new_project_name.strip()):
                    project_id = data_manager.create_project(new_project_name.strip(), new_project_desc.strip())
                    if project_id:
                        st.session_state.selected_project_id = project_id
                        st.session_state.current_project_name = new_project_name.strip()
                        st.session_state.show_project_form = False  # Hide form after creation
                        st.success(f"Created project: {new_project_name}")
                        time.sleep(1)
                        st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_project_form = False
                    st.rerun()
        
        st.divider()
        
        # File Upload Section (only show if project is selected)
        if st.session_state.selected_project_id:
            st.markdown('<div class="sidebar-header">📁 Upload Screenshots</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="color: #B3B3B3; font-size: 0.9rem; margin-bottom: 1rem;">Uploading to: <strong style="color: #00C9A7;">{st.session_state.current_project_name}</strong></div>', unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "Choose screenshot files",
                type=['png', 'jpg', 'jpeg', 'webp', 'heic'],
                accept_multiple_files=True,
                help="Upload PNG, JPG, or JPEG screenshot files",
                label_visibility="collapsed"
            )
        else:
            st.markdown("""
            <div class="upload-section">
                <div style="text-align: center; color: #B3B3B3;">
                    📂 Select a project above to upload screenshots
                </div>
            </div>
            """, unsafe_allow_html=True)
            uploaded_files = None
        
        st.markdown('<div class="sidebar-header">⚡ Processing Options</div>', unsafe_allow_html=True)
        
        processing_mode = st.selectbox(
            "Choose processing mode:",
            [
                "⚡ Fast Local Vision (Recommended)",
                "🔍 Detailed - OpenAI (More detailed, uses API)",
                "🔍 Detailed - Gemini (More detailed, uses API)"
            ],
            index=0,
            help="Fast Local Vision: OCR + computer vision analysis (no API required). Detailed options: OCR + advanced AI analysis (requires API keys, more expensive).",
            label_visibility="collapsed"
        )
        
        # Show provider availability in a compact card
        st.markdown("""
        <div class="processing-stats">
            <div style="color: #FAFAFA; font-weight: 500; margin-bottom: 0.5rem;">Provider Status</div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                <span style="color: #00C9A7;">✅ Local Vision</span>""" + f"""
                <span style="color: {'#00C9A7' if openai_client else '#FF4B4B'};">{'✅' if openai_client else '❌'} OpenAI</span>
                <span style="color: {'#00C9A7' if gemini_client.is_available() else '#FF4B4B'};">{'✅' if gemini_client.is_available() else '❌'} Gemini</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if uploaded_files and st.session_state.selected_project_id and st.button("🔄 Process Screenshots", type="primary"):
            process_screenshots(uploaded_files, image_processor, openai_client, gemini_client, local_vision_client, data_manager, processing_mode, st.session_state.selected_project_id)
        
        # Load existing project data if project is selected but no new upload
        if st.session_state.selected_project_id and not uploaded_files:
            load_project_data(data_manager, st.session_state.selected_project_id)
    
    # Main content area
    if st.session_state.selected_project_id:
        if st.session_state.processing_complete and not st.session_state.processed_data.empty:
            search_interface()
        else:
            # Check if project has existing images
            project_data = data_manager.get_project_images(st.session_state.selected_project_id)
            if not project_data.empty:
                # Load existing data
                load_project_data(data_manager, st.session_state.selected_project_id)
                st.rerun()
            else:
                st.info(f"📂 Project '{st.session_state.current_project_name}' is ready. Upload screenshots in the sidebar to start searching.")
    else:
        # Modern welcome screen when no project is selected
        st.markdown("### 💡 Getting Started")
        
        # Welcome card
        st.markdown("""
        <div class="project-card">
            <h4 style="color: #FAFAFA; margin-top: 0;">Welcome to Visual Memory Search</h4>
            <p style="color: #B3B3B3; margin-bottom: 1.5rem;">Create a project and upload screenshots to start searching through your visual memories using natural language.</p>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
                <div>
                    <h5 style="color: #00C9A7; margin-bottom: 1rem;">Text-based Searches</h5>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; font-family: monospace; font-size: 0.9rem;">error message about authentication</div>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; font-family: monospace; font-size: 0.9rem;">password reset email</div>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; font-family: monospace; font-size: 0.9rem;">API documentation</div>
                </div>
                
                <div>
                    <h5 style="color: #00C9A7; margin-bottom: 1rem;">Visual-based Searches</h5>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; font-family: monospace; font-size: 0.9rem;">screenshot with blue button</div>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; font-family: monospace; font-size: 0.9rem;">red error dialog box</div>
                    <div style="background: #262B35; padding: 0.75rem; border-radius: 4px; font-family: monospace; font-size: 0.9rem;">login form with input fields</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def load_project_data(data_manager: DataManager, project_id: int):
    """Load existing project data into session state"""
    try:
        project_data = data_manager.get_project_images(project_id)
        if not project_data.empty:
            st.session_state.processed_data = project_data
            
            # Build search index for existing data
            search_engine = SearchEngine()
            st.session_state.search_index = search_engine.build_index(project_data)
            st.session_state.processing_complete = True
        else:
            # Clear session state if no images in project
            st.session_state.processed_data = pd.DataFrame()
            st.session_state.search_index = None
            st.session_state.processing_complete = False
    except Exception as e:
        st.error(f"Failed to load project data: {str(e)}")

def process_screenshots(uploaded_files: List, image_processor: ImageProcessor, 
                       openai_client: OpenAIClient, gemini_client: GeminiClient, local_vision_client: LocalVisionClient, 
                       data_manager: DataManager, processing_mode: str, project_id: int):
    """Process uploaded screenshots with OCR and AI vision"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    processed_data = []
    total_files = len(uploaded_files)
    
    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            status_text.text(f"Processing {uploaded_file.name}... ({idx + 1}/{total_files})")
            
            # Load and validate image
            image = Image.open(uploaded_file)
            
            # Skip if image is too small or corrupted
            if image.size[0] < 50 or image.size[1] < 50:
                st.warning(f"Skipping {uploaded_file.name}: Image too small")
                continue
                
            # Extract OCR text and visual description based on processing mode
            if "Ultra Fast" in processing_mode:
                ocr_text = image_processor.extract_text_fast(image)
                visual_description = "No visual analysis (Ultra Fast mode)"
            elif "Fast Local Vision" in processing_mode:
                ocr_text = image_processor.extract_text_fast(image)
                visual_description = local_vision_client.analyze_screenshot(image)
            elif "Balanced" in processing_mode:
                ocr_text = image_processor.extract_text_balanced(image)
                visual_description = image_processor.analyze_basic(image)
            elif "OpenAI" in processing_mode:
                ocr_text = image_processor.extract_text(image)  # Current heavy preprocessing
                visual_description = openai_client.analyze_screenshot(image)
            elif "Gemini" in processing_mode:
                ocr_text = image_processor.extract_text(image)  # Current heavy preprocessing
                if gemini_client.is_available():
                    visual_description = gemini_client.analyze_screenshot(image)
                else:
                    visual_description = "Gemini API key not configured - using local vision analysis"
                    visual_description = local_vision_client.analyze_screenshot(image)
            else:
                # Fallback to fast local vision
                ocr_text = image_processor.extract_text_fast(image)
                visual_description = local_vision_client.analyze_screenshot(image)
            
            # Generate thumbnail
            thumbnail = image_processor.create_thumbnail(image)
            thumbnail_b64 = image_processor.image_to_base64(thumbnail)
            
            # Save to database
            success = data_manager.save_processed_image(
                project_id=project_id,
                filename=uploaded_file.name,
                image=image,
                ocr_text=ocr_text,
                visual_description=visual_description,
                thumbnail_b64=thumbnail_b64,
                processing_mode=processing_mode,
                file_size=uploaded_file.size
            )
            
            if success:
                # Store processed data for session
                processed_data.append({
                    'filename': uploaded_file.name,
                    'file_size': uploaded_file.size,
                    'image_dimensions': f"{image.size[0]}x{image.size[1]}",
                    'ocr_text': ocr_text,
                    'visual_description': visual_description,
                    'thumbnail_b64': thumbnail_b64,
                    'processed_timestamp': pd.Timestamp.now(),
                    'processing_mode': processing_mode
                })
            else:
                st.error(f"Failed to save {uploaded_file.name} to database")
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            continue
        
        # Update progress
        progress_bar.progress((idx + 1) / total_files)
    
    # Load all project data after processing
    load_project_data(data_manager, project_id)
    
    # Show processing summary
    total_processed = len(processed_data)
    total_uploaded = len(uploaded_files)
    
    if total_processed > 0:
        status_text.success(f"✅ Processing complete!")
        progress_bar.progress(1.0)
        
        # Show processing summary
        st.subheader("📊 Processing Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Uploaded", total_uploaded)
        with col2:
            st.metric("Successfully Processed", total_processed)
        with col3:
            if total_processed > 0:
                temp_df = pd.DataFrame(processed_data)
                avg_text_length = temp_df['ocr_text'].str.len().mean()
                st.metric("Avg Text Length", f"{avg_text_length:.0f} chars")
            else:
                st.metric("Avg Text Length", "N/A")
        
        time.sleep(1)
        st.rerun()
    else:
        st.warning("No files could be processed successfully.")

def search_interface():
    """Modern search interface with professional styling"""
    
    # Search interface
    st.markdown("### 🔍 Search Screenshots")
    
    # Search container with modern styling
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input(
            "Search query:",
            placeholder="e.g., 'error dialog with red button' or 'login form'",
            help="Search will automatically update as you type",
            key="search_query",
            label_visibility="collapsed"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Search options in expandable section
    with st.expander("⚙️ Advanced Search Options", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            search_mode = st.selectbox(
                "Search Mode",
                ["Combined (Text + Visual)", "Text Only", "Visual Only"],
                help="Choose how to search through your screenshots",
                key="search_mode"
            )
        with col2:
            max_results = st.slider("Max Results", 1, 20, 10, key="max_results")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Automatic search when query is entered or search button is clicked
    if (query and query.strip()) or search_button:
        if query and query.strip():
            perform_search(query, search_mode, max_results)
        else:
            st.warning("Please enter a search query")

def perform_search(query: str, search_mode: str, max_results: int):
    """Perform search and display results in modern table format"""
    
    with st.spinner("Searching screenshots..."):
        search_engine = SearchEngine()
        results = search_engine.search(
            query=query,
            data=st.session_state.processed_data,
            search_index=st.session_state.search_index,
            mode=search_mode.lower(),
            max_results=max_results
        )
    
    if results.empty:
        st.markdown("""
        <div class="result-table">
            <div class="table-header">No Results Found</div>
            <div style="padding: 2rem; text-align: center; color: #B3B3B3;">
                No matching screenshots found. Try a different query or search mode.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Results header with modern styling
    st.markdown(f"### 🎯 Search Results")
    st.markdown(f'<div style="color: #B3B3B3; margin-bottom: 1rem;">{len(results)} matches found for "{query}"</div>', unsafe_allow_html=True)
    
    # Modern table-style results display
    st.markdown("""
    <div class="result-table">
        <div class="table-header">
            <div style="display: grid; grid-template-columns: 120px 2fr 1fr 1fr 100px 150px; gap: 1rem; align-items: center;">
                <div>Preview</div>
                <div>Filename</div>
                <div>Match Reason</div>
                <div>Content Preview</div>
                <div>Confidence</div>
                <div>Processed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display results in table format
    for idx, row in results.iterrows():
        # Status indicator based on confidence
        confidence = row['confidence_score']
        if confidence >= 80:
            status_class = "status-active"
            confidence_class = "confidence-high"
        elif confidence >= 60:
            status_class = "status-processing" 
            confidence_class = "confidence-medium"
        else:
            status_class = "status-error"
            confidence_class = "confidence-low"
        
        # Process time formatting
        try:
            processed_time = pd.to_datetime(row['processed_timestamp']).strftime('%m/%d/%Y')
        except:
            processed_time = "N/A"
        
        # Truncate content for preview
        content_preview = str(row['ocr_text'])[:50] + "..." if len(str(row['ocr_text'])) > 50 else str(row['ocr_text'])
        match_reason = str(row['match_reason'])[:40] + "..." if len(str(row['match_reason'])) > 40 else str(row['match_reason'])
        
        # Create table row
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([120, 200, 150, 150, 100, 150])
            
            with col1:
                # Display thumbnail
                try:
                    thumbnail_bytes = base64.b64decode(str(row['thumbnail_b64']))
                    thumbnail_image = Image.open(BytesIO(thumbnail_bytes))
                    st.image(thumbnail_image, width=100)
                except:
                    st.markdown('<div style="text-align: center; color: #B3B3B3; padding: 20px;">📷</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="status-indicator {status_class}"></div><strong>{row["filename"]}</strong>', unsafe_allow_html=True)
                dimensions = row.get('image_dimensions', 'Unknown')
                st.markdown(f'<div style="color: #B3B3B3; font-size: 0.8rem;">{dimensions}</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div style="font-size: 0.9rem;">{match_reason}</div>', unsafe_allow_html=True)
            
            with col4:
                if content_preview.strip():
                    with st.expander("View Content", expanded=False):
                        st.text_area("OCR Text", str(row['ocr_text']), height=100, disabled=True, key=f"content_{idx}", label_visibility="collapsed")
                        if str(row['visual_description']).strip():
                            st.text_area("Visual Description", str(row['visual_description']), height=100, disabled=True, key=f"visual_{idx}", label_visibility="collapsed")
                else:
                    st.markdown('<div style="color: #B3B3B3; font-size: 0.8rem;">No text content</div>', unsafe_allow_html=True)
            
            with col5:
                st.markdown(f'<div class="confidence-badge {confidence_class}">{confidence:.0f}%</div>', unsafe_allow_html=True)
            
            with col6:
                st.markdown(f'<div style="font-size: 0.8rem;">{processed_time}</div>', unsafe_allow_html=True)
            
            st.divider()

if __name__ == "__main__":
    main()
