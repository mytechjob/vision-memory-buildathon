import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import base64
from io import BytesIO
import streamlit as st

class ImageProcessor:
    """Handle image processing, OCR, and thumbnail generation"""
    
    def __init__(self):
        self.thumbnail_size = (200, 200)
        
    def extract_text(self, image: Image.Image) -> str:
        """Extract text from image using OCR"""
        try:
            # Convert PIL image to numpy array for OpenCV processing
            img_array = np.array(image)
            
            # Convert to grayscale if needed
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # Apply image preprocessing for better OCR
            # Denoise
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Increase contrast
            enhanced = cv2.convertScaleAbs(denoised, alpha=1.2, beta=20)
            
            # Convert back to PIL Image
            processed_image = Image.fromarray(enhanced)
            
            # Configure tesseract
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%^&*()_+-=[]{}|;:,.<>?/~` '
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            # Clean and normalize text
            text = self._clean_text(text)
            
            return text
            
        except Exception as e:
            st.warning(f"OCR extraction failed: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')
        text = text.replace('0', 'O') if text.count('0') < text.count('O') else text
        
        # Filter out very short words that might be OCR noise
        words = text.split()
        filtered_words = [word for word in words if len(word) > 1 or word.isalnum()]
        
        return ' '.join(filtered_words)
    
    def create_thumbnail(self, image: Image.Image) -> Image.Image:
        """Create a thumbnail of the image"""
        try:
            # Create a copy to avoid modifying original
            thumbnail = image.copy()
            
            # Convert to RGB if necessary
            if thumbnail.mode != 'RGB':
                thumbnail = thumbnail.convert('RGB')
            
            # Create thumbnail maintaining aspect ratio
            thumbnail.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            
            # Create a square thumbnail with padding if needed
            square_thumb = Image.new('RGB', self.thumbnail_size, (255, 255, 255))
            
            # Center the thumbnail
            offset = ((self.thumbnail_size[0] - thumbnail.size[0]) // 2,
                     (self.thumbnail_size[1] - thumbnail.size[1]) // 2)
            square_thumb.paste(thumbnail, offset)
            
            return square_thumb
            
        except Exception as e:
            st.warning(f"Thumbnail creation failed: {str(e)}")
            # Return a blank thumbnail
            return Image.new('RGB', self.thumbnail_size, (240, 240, 240))
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        try:
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return img_str
        except Exception as e:
            st.warning(f"Base64 conversion failed: {str(e)}")
            return ""
    
    def preprocess_for_vision(self, image: Image.Image) -> str:
        """Convert image to base64 for OpenAI Vision API"""
        try:
            # Resize if image is too large (max 2048x2048 for OpenAI)
            max_size = 2048
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to base64
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=90)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            st.error(f"Image preprocessing for vision API failed: {str(e)}")
            return ""
