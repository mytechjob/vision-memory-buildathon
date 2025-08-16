import os
import json
import streamlit as st
from openai import OpenAI
from PIL import Image
from utils.image_processor import ImageProcessor

class OpenAIClient:
    """Handle OpenAI API interactions for visual analysis"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            st.stop()
        
        self.client = OpenAI(api_key=self.api_key)
        self.image_processor = ImageProcessor()
    
    def analyze_screenshot(self, image: Image.Image) -> str:
        """Analyze a screenshot and generate visual description"""
        try:
            # Convert image to base64
            base64_image = self.image_processor.preprocess_for_vision(image)
            
            if not base64_image:
                return "Visual analysis failed - could not process image"
            
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
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            description = response.choices[0].message.content
            return description if description else "No visual description generated"
            
        except Exception as e:
            st.warning(f"OpenAI vision analysis failed: {str(e)}")
            return f"Visual analysis failed: {str(e)}"
    
    def analyze_query_intent(self, query: str) -> dict:
        """Analyze search query to understand intent and extract key terms"""
        try:
            prompt = f"""
            Analyze this search query for screenshot search: "{query}"
            
            Extract and categorize the key search terms:
            1. Visual elements (colors, UI components, layouts)
            2. Text content (specific words, phrases to find)
            3. Context clues (error messages, login forms, etc.)
            
            Return a JSON object with:
            {{
                "visual_keywords": ["list of visual terms"],
                "text_keywords": ["list of text terms"],
                "intent": "brief description of what user is looking for",
                "search_type": "text_focused" | "visual_focused" | "combined"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a search query analyzer. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                raise ValueError("Empty response from OpenAI")
            return result
            
        except Exception as e:
            st.warning(f"Query intent analysis failed: {str(e)}")
            # Return default structure
            return {
                "visual_keywords": [],
                "text_keywords": query.split(),
                "intent": "Search for screenshots",
                "search_type": "combined"
            }
