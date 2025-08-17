#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd
from PIL import Image

# Add the parent directory to the Python path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.image_processor import ImageProcessor
from utils.openai_client import OpenAIClient
from utils.gemini_client import GeminiClient
from utils.local_vision_client import LocalVisionClient
from utils.data_manager import DataManager

def main():
    try:
        if len(sys.argv) < 4:
            raise ValueError("Project ID, processing mode, and file paths are required")
        
        project_id = int(sys.argv[1])
        processing_mode = sys.argv[2]
        file_paths = json.loads(sys.argv[3])
        
        # Initialize components
        image_processor = ImageProcessor()
        openai_client = OpenAIClient()
        gemini_client = GeminiClient()
        local_vision_client = LocalVisionClient()
        data_manager = DataManager()
        
        processed_data = []
        
        for file_path in file_paths:
            try:
                # Load and validate image
                image = Image.open(file_path)
                
                # Skip if image is too small
                if image.size[0] < 50 or image.size[1] < 50:
                    continue
                
                filename = file_path.split('/')[-1]
                
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
                    ocr_text = image_processor.extract_text(image)
                    visual_description = openai_client.analyze_screenshot(image)
                elif "Gemini" in processing_mode:
                    ocr_text = image_processor.extract_text(image)
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
                
                # Get file size (estimate since we don't have the original file)
                file_size = len(open(file_path, 'rb').read())
                
                # Save to database
                success = data_manager.save_processed_image(
                    project_id=project_id,
                    filename=filename,
                    image=image,
                    ocr_text=ocr_text,
                    visual_description=visual_description,
                    thumbnail_b64=thumbnail_b64,
                    processing_mode=processing_mode,
                    file_size=file_size
                )
                
                if success:
                    processed_data.append({
                        'filename': filename,
                        'file_size': file_size,
                        'image_dimensions': f"{image.size[0]}x{image.size[1]}",
                        'ocr_text': ocr_text,
                        'visual_description': visual_description,
                        'thumbnail_b64': thumbnail_b64,
                        'processing_mode': processing_mode
                    })
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
                continue
        
        result = {
            'success': True,
            'data': {
                'processed_count': len(processed_data),
                'total_uploaded': len(file_paths),
                'processed_images': processed_data
            }
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(result))
        sys.exit(1)

if __name__ == "__main__":
    main()