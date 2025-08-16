#!/usr/bin/env python3
"""
Standalone script to test different screenshot processing approaches with timing
"""

import time
import os
import sys
from pathlib import Path
from PIL import Image
import pytesseract
import cv2
import numpy as np
import base64
from io import BytesIO

# Add utils to path for imports
sys.path.append('utils')

def time_function(func, *args, **kwargs):
    """Time a function execution"""
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return result, end - start

def load_test_image(image_path):
    """Load a test image"""
    try:
        return Image.open(image_path)
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None

# OCR Approaches
def ocr_basic(image):
    """Basic OCR with minimal preprocessing"""
    text = pytesseract.image_to_string(image)
    return text.strip()

def ocr_fast_config(image):
    """OCR with fast configuration"""
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=config)
    return text.strip()

def ocr_optimized_config(image):
    """OCR with optimized configuration for screenshots"""
    config = r'--oem 3 --psm 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?@#$%^&*()_+-=[]{}|;:,.<>?/~` '
    text = pytesseract.image_to_string(image, config=config)
    return text.strip()

def ocr_with_light_preprocessing(image):
    """OCR with minimal preprocessing"""
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale if needed
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Light preprocessing - just contrast enhancement
    enhanced = cv2.convertScaleAbs(gray, alpha=1.1, beta=10)
    
    # Convert back to PIL
    processed_image = Image.fromarray(enhanced)
    
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=config)
    return text.strip()

def ocr_with_heavy_preprocessing(image):
    """OCR with heavy preprocessing (current approach)"""
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
    return text.strip()

# Vision Analysis Approaches
def vision_openai_simple(image):
    """Simple OpenAI vision analysis"""
    try:
        from openai_client import OpenAIClient
        client = OpenAIClient()
        return client.analyze_screenshot(image)
    except Exception as e:
        return f"OpenAI analysis failed: {e}"

def vision_gemini_simple(image):
    """Simple Gemini vision analysis"""
    try:
        from gemini_client import GeminiClient
        client = GeminiClient()
        if client.is_available():
            return client.analyze_screenshot(image)
        else:
            return "Gemini API key not configured"
    except Exception as e:
        return f"Gemini analysis failed: {e}"

def vision_basic_analysis(image):
    """Basic local image analysis without AI"""
    # Simple color and size analysis
    width, height = image.size
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get dominant colors
    colors = image.getcolors(maxcolors=256*256*256)
    if colors:
        dominant_color = max(colors, key=lambda item: item[0])
        color_info = f"Dominant color count: {dominant_color[0]}"
    else:
        color_info = "Could not determine dominant colors"
    
    description = f"Image dimensions: {width}x{height}. {color_info}. Basic screenshot analysis."
    return description

def vision_no_analysis(image):
    """Skip vision analysis entirely"""
    return "No visual analysis performed"

# Test different processing approaches
def run_processing_tests(image_path):
    """Run all processing tests on a single image"""
    print(f"\n🧪 Testing processing approaches on: {os.path.basename(image_path)}")
    print("=" * 70)
    
    image = load_test_image(image_path)
    if not image:
        return
    
    print(f"Image size: {image.size}")
    print()
    
    # OCR Tests
    print("📝 OCR APPROACHES:")
    print("-" * 30)
    
    ocr_approaches = [
        ("Basic OCR", ocr_basic),
        ("Fast Config OCR", ocr_fast_config),
        ("Optimized Config OCR", ocr_optimized_config),
        ("Light Preprocessing OCR", ocr_with_light_preprocessing),
        ("Heavy Preprocessing OCR (Current)", ocr_with_heavy_preprocessing),
    ]
    
    ocr_results = {}
    for name, func in ocr_approaches:
        try:
            result, duration = time_function(func, image)
            ocr_results[name] = (result, duration)
            text_preview = (result[:50] + '...') if len(result) > 50 else result
            print(f"{name:25} | {duration:6.2f}s | {len(result):3d} chars | {text_preview}")
        except Exception as e:
            print(f"{name:25} | ERROR: {e}")
    
    print()
    
    # Vision Analysis Tests
    print("👁️  VISION ANALYSIS APPROACHES:")
    print("-" * 40)
    
    vision_approaches = [
        ("No Analysis", vision_no_analysis),
        ("Basic Local Analysis", vision_basic_analysis),
        ("OpenAI Vision", vision_openai_simple),
        ("Gemini Vision (Flash)", vision_gemini_simple),
    ]
    
    vision_results = {}
    for name, func in vision_approaches:
        try:
            result, duration = time_function(func, image)
            vision_results[name] = (result, duration)
            desc_preview = (result[:50] + '...') if len(result) > 50 else result
            print(f"{name:25} | {duration:6.2f}s | {len(result):3d} chars | {desc_preview}")
        except Exception as e:
            print(f"{name:25} | ERROR: {e}")
    
    print()
    
    # Combined Performance Summary
    print("⚡ PERFORMANCE SUMMARY:")
    print("-" * 25)
    
    fastest_ocr = min(ocr_results.items(), key=lambda x: x[1][1])
    fastest_vision = min(vision_results.items(), key=lambda x: x[1][1])
    
    print(f"Fastest OCR:    {fastest_ocr[0]} ({fastest_ocr[1][1]:.2f}s)")
    print(f"Fastest Vision: {fastest_vision[0]} ({fastest_vision[1][1]:.2f}s)")
    
    total_fastest = fastest_ocr[1][1] + fastest_vision[1][1]
    
    # Find current approach time
    current_ocr_time = ocr_results.get("Heavy Preprocessing OCR (Current)", (None, 0))[1]
    openai_vision_time = vision_results.get("OpenAI Vision", (None, 0))[1]
    gemini_vision_time = vision_results.get("Gemini Vision (Flash)", (None, 0))[1]
    
    # Use the faster of the two AI vision approaches
    if openai_vision_time > 0 and gemini_vision_time > 0:
        current_vision_time = min(openai_vision_time, gemini_vision_time)
        faster_ai = "Gemini" if gemini_vision_time < openai_vision_time else "OpenAI"
    elif openai_vision_time > 0:
        current_vision_time = openai_vision_time
        faster_ai = "OpenAI"
    elif gemini_vision_time > 0:
        current_vision_time = gemini_vision_time
        faster_ai = "Gemini"
    else:
        current_vision_time = 0
        faster_ai = "None"
    
    total_current = current_ocr_time + current_vision_time
    
    print(f"Fastest Total:  {total_fastest:.2f}s")
    print(f"Best AI Total:  {total_current:.2f}s ({faster_ai})")
    
    if openai_vision_time > 0 and gemini_vision_time > 0:
        if gemini_vision_time < openai_vision_time:
            speedup_ai = openai_vision_time / gemini_vision_time
            print(f"Gemini vs OpenAI: {speedup_ai:.1f}x faster")
        else:
            speedup_ai = gemini_vision_time / openai_vision_time
            print(f"OpenAI vs Gemini: {speedup_ai:.1f}x faster")
    
    if total_current > 0:
        speedup = total_current / total_fastest
        print(f"Potential Speedup: {speedup:.1f}x faster")
    
    return ocr_results, vision_results

def test_multiple_images():
    """Test on multiple images if available"""
    # Look for test images in common locations
    test_paths = [
        "attached_assets",
        "test_images",
        "screenshots",
        "."
    ]
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.heic']
    test_images = []
    
    for path in test_paths:
        if os.path.exists(path):
            for ext in image_extensions:
                test_images.extend(Path(path).glob(f"*{ext}"))
                test_images.extend(Path(path).glob(f"*{ext.upper()}"))
    
    if not test_images:
        print("❌ No test images found. Please add some images to test with.")
        print("   Try putting test images in: attached_assets/, test_images/, or current directory")
        return
    
    print(f"🖼️  Found {len(test_images)} test images")
    
    # Test up to 3 images to avoid overwhelming output
    for image_path in list(test_images)[:3]:
        try:
            run_processing_tests(str(image_path))
        except Exception as e:
            print(f"Error testing {image_path}: {e}")

def main():
    print("🚀 Screenshot Processing Speed Test")
    print("=" * 50)
    
    # Check if specific image path provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            run_processing_tests(image_path)
        else:
            print(f"❌ Image not found: {image_path}")
    else:
        # Test multiple images
        test_multiple_images()
    
    print("\n💡 RECOMMENDATIONS:")
    print("-" * 20)
    print("• For fastest processing: Use 'Fast Config OCR' + 'No Analysis'")
    print("• For balanced speed/quality: Use 'Light Preprocessing OCR' + 'Basic Local Analysis'")
    print("• For best AI quality: Use 'Heavy Preprocessing OCR' + faster AI vision (OpenAI vs Gemini)")
    print("• Gemini is typically faster and cheaper than OpenAI for vision tasks")
    print("• Consider making vision analysis optional for users")
    print("• Consider processing images in background/async")

if __name__ == "__main__":
    main()