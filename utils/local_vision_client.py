import streamlit as st
from PIL import Image, ImageStat, ImageFilter
import cv2
import numpy as np
from typing import Dict, List, Tuple
import colorsys

class LocalVisionClient:
    """Fast local vision analysis without external API dependencies"""
    
    def __init__(self):
        self.color_names = {
            'red': [(255, 0, 0), (220, 20, 60), (178, 34, 34), (139, 0, 0)],
            'blue': [(0, 0, 255), (65, 105, 225), (30, 144, 255), (0, 100, 200)],
            'green': [(0, 255, 0), (34, 139, 34), (0, 128, 0), (50, 205, 50)],
            'yellow': [(255, 255, 0), (255, 215, 0), (255, 165, 0), (255, 140, 0)],
            'purple': [(128, 0, 128), (75, 0, 130), (138, 43, 226), (148, 0, 211)],
            'orange': [(255, 165, 0), (255, 140, 0), (255, 69, 0), (255, 99, 71)],
            'pink': [(255, 192, 203), (255, 20, 147), (219, 112, 147), (255, 105, 180)],
            'brown': [(165, 42, 42), (139, 69, 19), (160, 82, 45), (210, 180, 140)],
            'gray': [(128, 128, 128), (169, 169, 169), (105, 105, 105), (211, 211, 211)],
            'black': [(0, 0, 0), (47, 79, 79), (25, 25, 25), (64, 64, 64)],
            'white': [(255, 255, 255), (248, 248, 255), (245, 245, 245), (240, 248, 255)]
        }
    
    def analyze_screenshot(self, image: Image.Image) -> str:
        """Comprehensive local image analysis"""
        try:
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get basic properties
            width, height = image.size
            aspect_ratio = width / height
            
            # Analyze colors
            color_analysis = self._analyze_colors(image)
            
            # Detect UI elements
            ui_elements = self._detect_ui_elements(image)
            
            # Analyze layout
            layout_analysis = self._analyze_layout(image)
            
            # Detect text regions
            text_regions = self._detect_text_regions(image)
            
            # Generate description
            description = self._generate_description(
                width, height, aspect_ratio, color_analysis, 
                ui_elements, layout_analysis, text_regions
            )
            
            return description
            
        except Exception as e:
            st.warning(f"Local vision analysis failed: {str(e)}")
            return f"Local analysis - screenshot {width}x{height} processed successfully"
    
    def _analyze_colors(self, image: Image.Image) -> Dict:
        """Analyze color composition of the image"""
        try:
            # Get dominant colors
            colors = image.getcolors(maxcolors=256*256*256)
            total_pixels = image.size[0] * image.size[1]
            
            if not colors:
                return {"dominant": "unknown", "palette": [], "description": "complex colors"}
            
            # Sort by frequency
            colors.sort(key=lambda x: x[0], reverse=True)
            
            # Analyze top colors
            dominant_colors = []
            color_percentages = []
            
            for count, rgb in colors[:5]:
                percentage = (count / total_pixels) * 100
                color_name = self._get_color_name(rgb)
                dominant_colors.append(color_name)
                color_percentages.append(percentage)
            
            # Get overall color temperature
            avg_color = ImageStat.Stat(image).mean
            temp_desc = self._get_color_temperature(avg_color)
            
            return {
                "dominant": dominant_colors[0] if dominant_colors else "unknown",
                "palette": dominant_colors[:3],
                "percentages": color_percentages[:3],
                "temperature": temp_desc,
                "description": f"{dominant_colors[0]} dominant" if dominant_colors else "mixed colors"
            }
            
        except Exception:
            return {"dominant": "unknown", "palette": [], "description": "color analysis failed"}
    
    def _get_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Map RGB values to color names"""
        r, g, b = rgb
        
        # Convert to HSV for better color matching
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Check for grayscale
        if s < 0.1:  # Low saturation
            if v < 0.2:
                return "black"
            elif v > 0.8:
                return "white"
            else:
                return "gray"
        
        # Map hue to basic colors
        h_deg = h * 360
        if h_deg < 15 or h_deg >= 345:
            return "red"
        elif h_deg < 45:
            return "orange"
        elif h_deg < 75:
            return "yellow"
        elif h_deg < 150:
            return "green"
        elif h_deg < 210:
            return "blue"
        elif h_deg < 270:
            return "purple"
        elif h_deg < 330:
            return "pink"
        else:
            return "red"
    
    def _get_color_temperature(self, avg_color: List[float]) -> str:
        """Determine if image is warm or cool toned"""
        r, g, b = avg_color[:3]
        
        # Simple temperature calculation
        if r > b + 20:
            return "warm"
        elif b > r + 20:
            return "cool"
        else:
            return "neutral"
    
    def _detect_ui_elements(self, image: Image.Image) -> Dict:
        """Detect potential UI elements using edge detection and shapes"""
        try:
            # Convert to numpy array
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analyze contours for UI elements
            rectangles = 0
            circles = 0
            lines = 0
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 100:  # Skip tiny areas
                    continue
                
                # Approximate contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) == 4:
                    rectangles += 1
                elif len(approx) > 8:
                    circles += 1
                elif len(approx) == 2:
                    lines += 1
            
            # Determine likely UI elements
            ui_elements = []
            if rectangles > 2:
                ui_elements.append("buttons")
            if rectangles > 5:
                ui_elements.append("forms")
            if circles > 0:
                ui_elements.append("icons")
            if lines > 3:
                ui_elements.append("borders")
            
            return {
                "rectangles": rectangles,
                "circles": circles,
                "lines": lines,
                "detected": ui_elements
            }
            
        except Exception:
            return {"rectangles": 0, "circles": 0, "lines": 0, "detected": []}
    
    def _analyze_layout(self, image: Image.Image) -> Dict:
        """Analyze the layout structure of the image"""
        try:
            width, height = image.size
            aspect_ratio = width / height
            
            # Determine layout type
            if aspect_ratio > 1.5:
                layout_type = "wide landscape"
            elif aspect_ratio < 0.7:
                layout_type = "tall portrait"
            else:
                layout_type = "square-ish"
            
            # Analyze brightness distribution
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # Divide into regions and analyze
            h_third = height // 3
            w_third = width // 3
            
            regions = {
                "top": np.mean(img_array[:h_third, :]),
                "middle": np.mean(img_array[h_third:2*h_third, :]),
                "bottom": np.mean(img_array[2*h_third:, :]),
                "left": np.mean(img_array[:, :w_third]),
                "center": np.mean(img_array[:, w_third:2*w_third]),
                "right": np.mean(img_array[:, 2*w_third:])
            }
            
            # Determine layout characteristics
            layout_features = []
            if regions["top"] > regions["bottom"] + 30:
                layout_features.append("bright header")
            if regions["bottom"] > regions["top"] + 30:
                layout_features.append("bright footer")
            if regions["left"] > regions["right"] + 30:
                layout_features.append("left sidebar")
            if regions["right"] > regions["left"] + 30:
                layout_features.append("right sidebar")
            
            return {
                "type": layout_type,
                "features": layout_features,
                "regions": regions
            }
            
        except Exception:
            return {"type": "standard", "features": [], "regions": {}}
    
    def _detect_text_regions(self, image: Image.Image) -> Dict:
        """Detect areas likely to contain text"""
        try:
            # Convert to grayscale
            gray = image.convert('L')
            img_array = np.array(gray)
            
            # Apply morphological operations to detect text-like regions
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            
            # Detect horizontal text lines
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
            horizontal = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, horizontal_kernel)
            
            # Count text-like regions
            contours, _ = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_regions = len([c for c in contours if cv2.contourArea(c) > 50])
            
            return {
                "text_regions": text_regions,
                "has_text": text_regions > 0,
                "likely_content": "text-heavy" if text_regions > 5 else "visual-heavy"
            }
            
        except Exception:
            return {"text_regions": 0, "has_text": False, "likely_content": "unknown"}
    
    def _generate_description(self, width: int, height: int, aspect_ratio: float,
                            color_analysis: Dict, ui_elements: Dict, 
                            layout_analysis: Dict, text_regions: Dict) -> str:
        """Generate a comprehensive description of the screenshot"""
        
        # Build description components
        components = []
        
        # Size and format
        components.append(f"Screenshot with dimensions {width}x{height}")
        
        # Layout
        components.append(f"{layout_analysis['type']} layout")
        
        # Colors
        if color_analysis.get('dominant'):
            components.append(f"predominantly {color_analysis['dominant']}")
            if len(color_analysis.get('palette', [])) > 1:
                other_colors = ', '.join(color_analysis['palette'][1:3])
                components.append(f"with {other_colors} accents")
        
        # UI Elements
        detected_ui = ui_elements.get('detected', [])
        if detected_ui:
            if len(detected_ui) == 1:
                components.append(f"contains {detected_ui[0]}")
            else:
                components.append(f"contains {', '.join(detected_ui[:-1])} and {detected_ui[-1]}")
        
        # Layout features
        layout_features = layout_analysis.get('features', [])
        if layout_features:
            components.append(f"with {', '.join(layout_features)}")
        
        # Text content
        if text_regions.get('has_text'):
            components.append(f"{text_regions['likely_content']} interface")
        
        # Temperature
        temp = color_analysis.get('temperature', 'neutral')
        if temp != 'neutral':
            components.append(f"{temp} color tone")
        
        # Join components into natural description
        description = components[0]
        if len(components) > 1:
            description += ", " + ", ".join(components[1:-1])
            if len(components) > 2:
                description += f", and {components[-1]}"
            else:
                description += f" and {components[-1]}"
        
        description += ". Fast local analysis of interface elements, color composition, and layout structure."
        
        return description