import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types
from utils.image_processor import ImageProcessor

class GeminiClient:
    """Handle Google Gemini API interactions for visual analysis"""
    
    def __init__(self):
        # The newest Gemini model is "gemini-2.5-flash"
        # Do not change this unless explicitly requested by the user
        self.model = "gemini-2.5-flash"
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            self.client = None
            return
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.image_processor = ImageProcessor()
        except Exception as e:
            st.warning(f"Failed to initialize Gemini client: {str(e)}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Gemini client is available"""
        return self.client is not None
    
    def analyze_screenshot(self, image: Image.Image) -> str:
        """Analyze a screenshot using Gemini Flash"""
        if not self.client:
            return "Gemini API key not configured"
        
        try:
            # Convert image to bytes
            image_bytes = self._image_to_bytes(image)
            
            if not image_bytes:
                return "Failed to process image for Gemini analysis"
            
            # Prepare the prompt for screenshot analysis
            prompt = """
            Analyze this screenshot in detail. Focus on:
            
            1. UI Elements: Identify buttons, forms, menus, dialogs, navigation elements
            2. Colors: Describe the color scheme and prominent colors
            3. Layout: Describe the overall layout and positioning of elements
            4. Content Type: Identify if it's a webpage, application, error dialog, etc.
            5. Text Elements: Note any visible text or headings (don't transcribe all text, just describe what type of text is visible)
            6. Interactive Elements: Identify clickable elements, input fields, toggles, etc.
            
            Provide a concise but comprehensive description that would help someone search for this screenshot later.
            Focus on visual and structural elements rather than transcribing all text content.
            """
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg",
                    ),
                    prompt
                ]
            )
            
            description = response.text if response.text else "No visual description generated"
            return description
            
        except Exception as e:
            st.warning(f"Gemini vision analysis failed: {str(e)}")
            return f"Gemini analysis failed: {str(e)}"
    
    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes for Gemini API"""
        try:
            # Resize if image is too large (Gemini handles up to 20MB)
            max_size = 2048
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to bytes
            from io import BytesIO
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=90)
            return buffer.getvalue()
            
        except Exception as e:
            st.error(f"Image preprocessing for Gemini API failed: {str(e)}")
            return b""