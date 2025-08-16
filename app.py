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
from utils.data_manager import DataManager

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = pd.DataFrame()
if 'search_index' not in st.session_state:
    st.session_state.search_index = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

def main():
    st.title("🔍 Visual Memory Search")
    st.markdown("Search through your screenshots using natural language queries")
    
    # Initialize components
    image_processor = ImageProcessor()
    openai_client = OpenAIClient()
    data_manager = DataManager()
    
    # Sidebar for file upload and processing
    with st.sidebar:
        st.header("📁 Upload Screenshots")
        
        uploaded_files = st.file_uploader(
            "Choose screenshot files",
            type=['png', 'jpg', 'jpeg', 'webp'],
            accept_multiple_files=True,
            help="Upload PNG, JPG, JPEG, or WebP screenshot files"
        )
        
        if uploaded_files and st.button("🔄 Process Screenshots", type="primary"):
            process_screenshots(uploaded_files, image_processor, openai_client, data_manager)
    
    # Main content area
    if st.session_state.processing_complete and not st.session_state.processed_data.empty:
        search_interface()
    else:
        st.info("👆 Upload and process screenshots to start searching")
        
        # Display sample query examples
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

def process_screenshots(uploaded_files: List, image_processor: ImageProcessor, 
                       openai_client: OpenAIClient, data_manager: DataManager):
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
                
            # Extract OCR text
            ocr_text = image_processor.extract_text(image)
            
            # Generate visual description using OpenAI Vision
            visual_description = openai_client.analyze_screenshot(image)
            
            # Generate thumbnail
            thumbnail = image_processor.create_thumbnail(image)
            thumbnail_b64 = image_processor.image_to_base64(thumbnail)
            
            # Store processed data
            processed_data.append({
                'filename': uploaded_file.name,
                'file_size': uploaded_file.size,
                'image_dimensions': f"{image.size[0]}x{image.size[1]}",
                'ocr_text': ocr_text,
                'visual_description': visual_description,
                'thumbnail_b64': thumbnail_b64,
                'processed_timestamp': pd.Timestamp.now()
            })
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            continue
        
        # Update progress
        progress_bar.progress((idx + 1) / total_files)
    
    if processed_data:
        # Store processed data
        st.session_state.processed_data = pd.DataFrame(processed_data)
        
        # Initialize search engine
        search_engine = SearchEngine()
        st.session_state.search_index = search_engine.build_index(st.session_state.processed_data)
        
        st.session_state.processing_complete = True
        
        status_text.success(f"✅ Successfully processed {len(processed_data)} screenshots!")
        progress_bar.progress(1.0)
        
        # Show processing summary
        st.subheader("📊 Processing Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", len(processed_data))
        with col2:
            st.metric("Successfully Processed", len(processed_data))
        with col3:
            avg_text_length = st.session_state.processed_data['ocr_text'].str.len().mean()
            st.metric("Avg Text Length", f"{avg_text_length:.0f} chars")
        
        time.sleep(1)
        st.rerun()
    else:
        st.error("No files could be processed successfully")

def search_interface():
    """Main search interface"""
    st.header("🔍 Search Your Screenshots")
    
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
                        st.text_area("", str(row['ocr_text']), height=100, disabled=True, key=f"text_{idx}")
                
                if str(row['visual_description']).strip():
                    with st.expander("👁️ Visual Description"):
                        st.text_area("", str(row['visual_description']), height=100, disabled=True, key=f"visual_{idx}")
                
                # File metadata
                processed_time = pd.to_datetime(row['processed_timestamp']).strftime('%Y-%m-%d %H:%M')
                st.caption(f"Size: {row['image_dimensions']} | Processed: {processed_time}")
            
            st.divider()

if __name__ == "__main__":
    main()
