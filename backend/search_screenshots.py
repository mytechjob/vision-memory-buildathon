#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd

# Add the parent directory to the Python path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.search_engine import SearchEngine
from utils.data_manager import DataManager

def main():
    try:
        if len(sys.argv) < 3:
            raise ValueError("Project ID and query are required")
        
        project_id = int(sys.argv[1])
        query = sys.argv[2]
        search_mode = sys.argv[3] if len(sys.argv) > 3 else "combined"
        max_results = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        
        # Get project data
        data_manager = DataManager()
        project_data = data_manager.get_project_images(project_id)
        
        if project_data.empty:
            result = {
                'success': True,
                'data': []
            }
            print(json.dumps(result))
            return
        
        # Build search index and perform search
        search_engine = SearchEngine()
        search_index = search_engine.build_index(project_data)
        
        results = search_engine.search(
            query=query,
            data=project_data,
            search_index=search_index,
            mode=search_mode.lower(),
            max_results=max_results
        )
        
        # Convert results to JSON-serializable format
        if not results.empty:
            # Convert timestamps to strings
            if 'processed_timestamp' in results.columns:
                results['processed_timestamp'] = results['processed_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            results_data = results.to_dict('records')
        else:
            results_data = []
        
        result = {
            'success': True,
            'data': results_data
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