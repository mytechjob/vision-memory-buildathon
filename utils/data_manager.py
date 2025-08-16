import pandas as pd
import streamlit as st
from typing import Dict, List, Any
import json
import os
from datetime import datetime

class DataManager:
    """Handle data storage, retrieval, and management"""
    
    def __init__(self):
        self.data_file = "processed_screenshots.json"
        self.session_data_key = "screenshot_data"
    
    def save_processed_data(self, data: pd.DataFrame) -> bool:
        """Save processed screenshot data"""
        try:
            # Convert dataframe to JSON-serializable format
            data_dict = data.to_dict('records')
            
            # Add metadata
            save_data = {
                'created_at': datetime.now().isoformat(),
                'total_screenshots': len(data_dict),
                'data': data_dict
            }
            
            # Save to session state
            st.session_state[self.session_data_key] = save_data
            
            return True
            
        except Exception as e:
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
            
            # Convert to Series if it's not already
            if hasattr(size_buckets, 'value_counts'):
                return size_buckets.value_counts().to_dict()
            else:
                return {}
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
            
            return True
            
        except Exception as e:
            st.error(f"Failed to clear session data: {str(e)}")
            return False
