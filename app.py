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
    st.title("🔍 Visual Memory Search")
    st.markdown("Search through your screenshots using natural language queries")
    
    # Initialize components
    image_processor = ImageProcessor()
    openai_client = OpenAIClient()
    gemini_client = GeminiClient()
    local_vision_client = LocalVisionClient()
    data_manager = DataManager()
    
    # Get existing projects
    projects = data_manager.get_projects()
    
    # Project selection in main area (under header)
    st.subheader("📂 Select Project")
    
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
            st.info("No projects found. Create your first project in the sidebar.")
    
    with col2:
        if projects and st.session_state.selected_project_id:
            if st.button("🗑️", help="Delete selected project"):
                # Find project to delete
                project_to_delete = next((p for p in projects if p['id'] == st.session_state.selected_project_id), None)
                if project_to_delete:
                    if data_manager.delete_project(project_to_delete['id']):
                        st.success(f"Deleted project: {project_to_delete['name']}")
                        st.session_state.selected_project_id = None
                        st.session_state.current_project_name = None
                        st.rerun()
    
    # Show selected project info
    if st.session_state.selected_project_id and projects:
        selected_project = next((p for p in projects if p['id'] == st.session_state.selected_project_id), None)
        if selected_project:
            with st.expander("📋 Project Details", expanded=False):
                st.write(f"**Description:** {selected_project['description'] or 'No description'}")
                st.write(f"**Created:** {selected_project['created_at'].strftime('%Y-%m-%d')}")
                st.write(f"**Images:** {selected_project['image_count']}")
    
    st.divider()
    
    # Sidebar for project creation and file upload
    with st.sidebar:
        # Project Creation Section
        st.header("➕ Create New Project")
        
        new_project_name = st.text_input("Project Name:", placeholder="My Screenshots")
        new_project_desc = st.text_area("Description (optional):", placeholder="Brief description of this project...")
        
        if st.button("Create Project", type="primary", disabled=not new_project_name.strip()):
            project_id = data_manager.create_project(new_project_name.strip(), new_project_desc.strip())
            if project_id:
                st.session_state.selected_project_id = project_id
                st.session_state.current_project_name = new_project_name.strip()
                st.success(f"Created project: {new_project_name}")
                time.sleep(1)
                st.rerun()
        
        st.divider()
        
        # File Upload Section (only show if project is selected)
        if st.session_state.selected_project_id:
            st.header("📁 Upload Screenshots")
            st.caption(f"Uploading to: **{st.session_state.current_project_name}**")
            
            uploaded_files = st.file_uploader(
                "Choose screenshot files",
                type=['png', 'jpg', 'jpeg', 'webp', 'heic'],
                accept_multiple_files=True,
                help="Upload PNG, JPG, or JPEG screenshot files"
            )
        else:
            st.info("Select a project above to upload screenshots")
            uploaded_files = None
        
        st.subheader("⚡ Processing Mode")
        processing_mode = st.selectbox(
            "Choose processing speed:",
            [
                "⚡ Fast Local Vision (Recommended)",
                "🔍 Detailed - OpenAI (More detailed, uses API)",
                "🔍 Detailed - Gemini (More detailed, uses API)"
            ],
            index=0,  # Default to Fast Local Vision
            help="Fast Local Vision: OCR + computer vision analysis (no API required). Detailed options: OCR + advanced AI analysis (requires API keys, more expensive)."
        )
        
        # Show provider availability
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("✅ Local Vision")
        with col2:
            openai_status = "✅" if openai_client else "❌"
            st.caption(f"{openai_status} OpenAI")
        with col3:
            gemini_status = "✅" if gemini_client.is_available() else "❌"
            st.caption(f"{gemini_status} Gemini")
        
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
        # Display sample query examples when no project is selected
        st.subheader("💡 Example Queries")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Text-based searches:**")
            st.code("error message about authentication")
            st.code("password reset email")
            st.code("API documentation")
            
        with col2:
            st.markdown("**Visual-based searches:**")
            st.code("screenshot with blue button")
            st.code("red error dialog box")
            st.code("login form with input fields")

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
    """Main search interface"""
    st.header(f"🔍 Search: {st.session_state.current_project_name}")
    
    # Search input
    query = st.text_input(
        "Enter your search query:",
        placeholder="e.g., 'error dialog with red button' or 'login form'",
        help="You can search for text content, visual elements, or combinations of both"
    )
    
    # Search options
    with st.expander("⚙️ Search Options"):
        col1, col2 = st.columns(2)
        with col1:
            search_mode = st.selectbox(
                "Search Mode",
                ["Combined (Text + Visual)", "Text Only", "Visual Only"],
                help="Choose how to search through your screenshots"
            )
        with col2:
            max_results = st.slider("Max Results", 1, 10, 5)
    
    if query and st.button("🔍 Search", type="primary"):
        perform_search(query, search_mode, max_results)

def perform_search(query: str, search_mode: str, max_results: int):
    """Perform search and display results"""
    
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
        st.warning("No matching screenshots found. Try a different query.")
        return
    
    st.subheader(f"🎯 Search Results ({len(results)} matches)")
    
    # Display results
    for idx, row in results.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display thumbnail
                try:
                    thumbnail_bytes = base64.b64decode(str(row['thumbnail_b64']))
                    thumbnail_image = Image.open(BytesIO(thumbnail_bytes))
                    st.image(thumbnail_image, width=150)
                except:
                    st.write("📷 Preview unavailable")
            
            with col2:
                # File info and confidence
                st.markdown(f"**📁 {row['filename']}**")
                
                # Confidence score with color coding
                confidence = row['confidence_score']
                if confidence >= 80:
                    color = "green"
                elif confidence >= 60:
                    color = "orange"
                else:
                    color = "red"
                
                st.markdown(f"**Confidence:** :{color}[{confidence:.1f}%]")
                
                # Match reasoning
                st.markdown(f"**Match Reason:** {row['match_reason']}")
                
                # Content preview
                if str(row['ocr_text']).strip():
                    with st.expander("📝 Text Content"):
                        st.text_area("OCR Text Content", str(row['ocr_text']), height=100, disabled=True, key=f"text_{idx}", label_visibility="collapsed")
                
                if str(row['visual_description']).strip():
                    with st.expander("👁️ Visual Description"):
                        st.text_area("Visual Description", str(row['visual_description']), height=100, disabled=True, key=f"visual_{idx}", label_visibility="collapsed")
                
                # File metadata
                processed_time = pd.to_datetime(row['processed_timestamp']).strftime('%Y-%m-%d %H:%M')
                st.caption(f"Size: {row['image_dimensions']} | Processed: {processed_time}")
            
            st.divider()

if __name__ == "__main__":
    main()
