import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from typing import List, Dict, Any
import re

class SearchEngine:
    """Handle search functionality with semantic similarity and ranking"""
    
    def __init__(self):
        # Use TF-IDF for text search
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
    
    
    def build_index(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Build search index from processed data"""
        if data.empty:
            return {}
        
        try:
            # Combine text and visual descriptions for indexing
            combined_content = []
            for _, row in data.iterrows():
                content = f"{row['ocr_text']} {row['visual_description']}"
                combined_content.append(content)
            
            # Build TF-IDF index
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(combined_content)
            
            search_index = {
                'tfidf_matrix': tfidf_matrix,
                'combined_content': combined_content,
                'feature_names': self.tfidf_vectorizer.get_feature_names_out()
            }
            
            return search_index
            
        except Exception as e:
            st.error(f"Failed to build search index: {str(e)}")
            return {}
    
    def search(self, query: str, data: pd.DataFrame, search_index: Dict[str, Any], 
               mode: str = "combined", max_results: int = 5) -> pd.DataFrame:
        """Perform search and return ranked results"""
        
        if data.empty or not search_index:
            return pd.DataFrame()
        
        try:
            # Clean and prepare query
            clean_query = self._preprocess_query(query)
            
            # Get similarity scores
            similarity_scores = self._calculate_similarity_scores(
                clean_query, search_index, mode, data
            )
            
            # Rank and filter results
            results = self._rank_results(data, similarity_scores, query, max_results)
            
            return results
            
        except Exception as e:
            st.error(f"Search failed: {str(e)}")
            return pd.DataFrame()
    
    def _preprocess_query(self, query: str) -> str:
        """Clean and preprocess search query"""
        # Remove special characters and normalize
        clean_query = re.sub(r'[^\w\s]', ' ', query)
        clean_query = ' '.join(clean_query.split())
        return clean_query.lower()
    
    def _calculate_similarity_scores(self, query: str, search_index: Dict[str, Any], 
                                   mode: str, data: pd.DataFrame) -> np.ndarray:
        """Calculate similarity scores based on search mode"""
        
        tfidf_scores = np.zeros(len(data))
        
        try:
            # TF-IDF similarity
            if search_index.get('tfidf_matrix') is not None:
                query_vector = self.tfidf_vectorizer.transform([query])
                tfidf_similarities = cosine_similarity(query_vector, search_index['tfidf_matrix']).flatten()
                tfidf_scores = tfidf_similarities
        except Exception as e:
            st.warning(f"TF-IDF scoring failed: {str(e)}")
        
        # For now, just use TF-IDF scores regardless of mode
        return tfidf_scores
    
    def _rank_results(self, data: pd.DataFrame, similarity_scores: np.ndarray, 
                     original_query: str, max_results: int) -> pd.DataFrame:
        """Rank results and add confidence scores and match reasons"""
        
        if len(similarity_scores) == 0:
            return pd.DataFrame()
        
        # Create results dataframe
        results_data = data.copy()
        results_data['similarity_score'] = similarity_scores
        
        # Calculate confidence scores (0-100%)
        max_score = np.max(similarity_scores) if np.max(similarity_scores) > 0 else 1
        results_data['confidence_score'] = (similarity_scores / max_score) * 100
        
        # Generate match reasons
        results_data['match_reason'] = results_data.apply(
            lambda row: self._generate_match_reason(row, original_query), axis=1
        )
        
        # Sort by similarity score and take top results
        results_data = results_data.sort_values('similarity_score', ascending=False)
        results_data = results_data.head(max_results)
        
        # Filter out very low confidence results
        results_data = results_data[results_data['confidence_score'] > 10]
        
        # Reset index to ensure we return a proper DataFrame
        results_data = results_data.reset_index(drop=True)
        
        return results_data
    
    def _generate_match_reason(self, row: pd.Series, query: str) -> str:
        """Generate explanation for why this result matches the query"""
        
        query_words = set(query.lower().split())
        ocr_text = str(row['ocr_text']) if pd.notna(row['ocr_text']) else ""
        visual_desc = str(row['visual_description']) if pd.notna(row['visual_description']) else ""
        ocr_words = set(ocr_text.lower().split()) if ocr_text else set()
        visual_words = set(visual_desc.lower().split()) if visual_desc else set()
        
        # Find matching words
        text_matches = query_words.intersection(ocr_words)
        visual_matches = query_words.intersection(visual_words)
        
        reasons = []
        
        if text_matches:
            reasons.append(f"Text content matches: {', '.join(list(text_matches)[:3])}")
        
        if visual_matches:
            reasons.append(f"Visual elements match: {', '.join(list(visual_matches)[:3])}")
        
        if not reasons:
            reasons.append("Semantic similarity with query content")
        
        return "; ".join(reasons)
