import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import json
import os
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import base64
from PIL import Image
from io import BytesIO
import hashlib

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to images
    images = relationship("ProcessedImage", back_populates="project")

class ProcessedImage(Base):
    __tablename__ = 'processed_images'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    filename = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)  # File hash for reference
    file_size = Column(Integer)
    image_dimensions = Column(String)
    original_image = Column(LargeBinary)  # Store original image
    thumbnail_b64 = Column(Text)  # Base64 encoded thumbnail
    ocr_text = Column(Text)
    visual_description = Column(Text)
    processing_mode = Column(String)
    processed_timestamp = Column(DateTime, default=datetime.now)
    
    # Relationship to project
    project = relationship("Project", back_populates="images")

class DataManager:
    """Handle data storage, retrieval, and management with persistent database storage"""
    
    def __init__(self):
        self.data_file = "processed_screenshots.json"
        self.session_data_key = "screenshot_data"
        self.engine = None
        self.Session = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database connection and create tables"""
        try:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                st.error("Database URL not found in environment variables")
                return
            
            self.engine = create_engine(database_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            
        except Exception as e:
            st.error(f"Failed to initialize database: {str(e)}")
    
    def _calculate_file_hash(self, image_data: bytes) -> str:
        """Calculate SHA-256 hash of image data for duplicate detection"""
        return hashlib.sha256(image_data).hexdigest()
    
    def _image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes"""
        img_byte_arr = BytesIO()
        # Save as JPEG to reduce size
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(img_byte_arr, format='JPEG', quality=85)
        return img_byte_arr.getvalue()
    
    def create_project(self, name: str, description: str = "") -> Optional[str]:
        """Create a new project and return its ID"""
        if not self.Session:
            return None
            
        try:
            session = self.Session()
            project = Project(name=name, description=description)
            session.add(project)
            session.commit()
            project_id = project.id
            session.close()
            return project_id
        except Exception as e:
            st.error(f"Failed to create project: {str(e)}")
            return None
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        if not self.Session:
            return []
            
        try:
            session = self.Session()
            projects = session.query(Project).order_by(Project.updated_at.desc()).all()
            project_list = []
            for project in projects:
                project_list.append({
                    'id': project.id,
                    'name': project.name,
                    'description': project.description,
                    'created_at': project.created_at,
                    'updated_at': project.updated_at,
                    'image_count': len(project.images)
                })
            session.close()
            return project_list
        except Exception as e:
            st.error(f"Failed to get projects: {str(e)}")
            return []
    
    def get_project_images(self, project_id: str) -> pd.DataFrame:
        """Get all images for a specific project"""
        if not self.Session:
            return pd.DataFrame()
            
        try:
            session = self.Session()
            images = session.query(ProcessedImage).filter_by(project_id=project_id).all()
            
            if not images:
                session.close()
                return pd.DataFrame()
            
            # Convert to DataFrame format expected by the app
            data = []
            for img in images:
                data.append({
                    'filename': img.filename,
                    'file_size': img.file_size,
                    'image_dimensions': img.image_dimensions,
                    'ocr_text': img.ocr_text,
                    'visual_description': img.visual_description,
                    'thumbnail_b64': img.thumbnail_b64,
                    'processed_timestamp': img.processed_timestamp,
                    'processing_mode': img.processing_mode
                })
            
            session.close()
            return pd.DataFrame(data)
            
        except Exception as e:
            st.error(f"Failed to get project images: {str(e)}")
            return pd.DataFrame()
    
    def image_exists(self, image_data: bytes) -> Tuple[bool, Optional[str]]:
        """Check if image already exists in database. Returns (exists, filename)"""
        if not self.Session:
            return False, None
            
        try:
            file_hash = self._calculate_file_hash(image_data)
            session = self.Session()
            existing_image = session.query(ProcessedImage).filter_by(file_hash=file_hash).first()
            session.close()
            
            if existing_image:
                return True, str(existing_image.filename)
            return False, None
            
        except Exception as e:
            st.warning(f"Failed to check image existence: {str(e)}")
            return False, None
    
    def save_processed_image(self, project_id: str, filename: str, image: Image.Image, 
                           ocr_text: str, visual_description: str, thumbnail_b64: str,
                           processing_mode: str, file_size: int) -> bool:
        """Save a single processed image to database"""
        if not self.Session:
            return False
            
        try:
            # Convert image to bytes and calculate hash
            image_bytes = self._image_to_bytes(image)
            file_hash = self._calculate_file_hash(image_bytes)
            
            session = self.Session()
            
            # Create new processed image record (allowing duplicates)
            processed_image = ProcessedImage(
                project_id=project_id,
                filename=filename,
                file_hash=file_hash,
                file_size=file_size,
                image_dimensions=f"{image.size[0]}x{image.size[1]}",
                original_image=image_bytes,
                thumbnail_b64=thumbnail_b64,
                ocr_text=ocr_text,
                visual_description=visual_description,
                processing_mode=processing_mode
            )
            
            session.add(processed_image)
            session.commit()
            
            # Update project's updated_at timestamp  
            session.query(Project).filter_by(id=project_id).update({"updated_at": datetime.now()})
            session.commit()
            
            session.close()
            return True
            
        except Exception as e:
            st.error(f"Failed to save processed image: {str(e)}")
            return False
    
    def save_processed_data(self, data: pd.DataFrame, project_id: str = None) -> bool:
        """Save processed screenshot data (legacy method for compatibility)"""
        try:
            # Convert dataframe to JSON-serializable format
            data_dict = data.to_dict('records')
            
            # Add metadata
            save_data = {
                'created_at': datetime.now().isoformat(),
                'total_screenshots': len(data_dict),
                'data': data_dict,
                'project_id': project_id
            }
            
            # Save to session state
            st.session_state[self.session_data_key] = save_data
            
            return True
            
        except Exception as e:
            if project_id:
                st.error(f"Failed to save processed data: {str(e)}")
            return False
    
    def load_processed_data(self) -> pd.DataFrame:
        """Load previously processed screenshot data"""
        try:
            if self.session_data_key in st.session_state:
                saved_data = st.session_state[self.session_data_key]
                data_records = saved_data.get('data', [])
                
                if data_records:
                    df = pd.DataFrame(data_records)
                    return df
            
            return pd.DataFrame()
            
        except Exception as e:
            st.warning(f"Failed to load processed data: {str(e)}")
            return pd.DataFrame()
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics of the processed data"""
        if data.empty:
            return {}
        
        try:
            summary = {
                'total_screenshots': len(data),
                'avg_text_length': data['ocr_text'].str.len().mean(),
                'files_with_text': (data['ocr_text'].str.len() > 0).sum(),
                'files_with_visual_desc': (data['visual_description'].str.len() > 0).sum(),
                'processing_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'file_types': self._get_file_types(data),
                'size_distribution': self._get_size_distribution(data)
            }
            
            return summary
            
        except Exception as e:
            st.warning(f"Failed to generate data summary: {str(e)}")
            return {}
    
    def _get_file_types(self, data: pd.DataFrame) -> Dict[str, int]:
        """Get distribution of file types"""
        try:
            file_extensions = data['filename'].str.extract(r'\.([^.]+)$')[0].str.lower()
            return file_extensions.value_counts().to_dict() if len(file_extensions) > 0 else {}
        except:
            return {}
    
    def _get_size_distribution(self, data: pd.DataFrame) -> Dict[str, int]:
        """Get distribution of file sizes"""
        try:
            if 'file_size' not in data.columns:
                return {}
            
            # Create size buckets
            size_buckets = pd.cut(
                data['file_size'], 
                bins=[0, 100*1024, 500*1024, 1024*1024, 5*1024*1024, float('inf')],
                labels=['<100KB', '100KB-500KB', '500KB-1MB', '1MB-5MB', '>5MB']
            )
            
            # Convert to Series and get value counts
            if hasattr(size_buckets, 'value_counts'):
                return size_buckets.value_counts().to_dict()
            else:
                # Fallback for when pd.cut returns a tuple
                size_series = pd.Series(size_buckets)
                return size_series.value_counts().to_dict()
        except:
            return {}
    
    def export_results(self, results: pd.DataFrame, query: str) -> str:
        """Export search results to JSON format"""
        try:
            export_data = {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(results),
                'results': []
            }
            
            for _, row in results.iterrows():
                result_item = {
                    'filename': row['filename'],
                    'confidence_score': float(row['confidence_score']),
                    'match_reason': row['match_reason'],
                    'ocr_text_preview': row['ocr_text'][:200] + '...' if len(row['ocr_text']) > 200 else row['ocr_text'],
                    'visual_description_preview': row['visual_description'][:200] + '...' if len(row['visual_description']) > 200 else row['visual_description']
                }
                export_data['results'].append(result_item)
            
            return json.dumps(export_data, indent=2)
            
        except Exception as e:
            st.error(f"Failed to export results: {str(e)}")
            return ""
    
    def clear_session_data(self):
        """Clear all session data"""
        try:
            if self.session_data_key in st.session_state:
                del st.session_state[self.session_data_key]
            
            if 'processed_data' in st.session_state:
                st.session_state.processed_data = pd.DataFrame()
            
            if 'search_index' in st.session_state:
                st.session_state.search_index = None
            
            if 'processing_complete' in st.session_state:
                st.session_state.processing_complete = False
            
            if 'selected_project_id' in st.session_state:
                st.session_state.selected_project_id = None
            
            return True
            
        except Exception as e:
            st.error(f"Failed to clear session data: {str(e)}")
            return False
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project and all its images"""
        if not self.Session:
            return False
            
        try:
            session = self.Session()
            
            # Delete all images in the project
            session.query(ProcessedImage).filter_by(project_id=project_id).delete()
            
            # Delete the project
            session.query(Project).filter_by(id=project_id).delete()
            
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            st.error(f"Failed to delete project: {str(e)}")
            return False
