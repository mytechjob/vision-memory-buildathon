#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd

# Add the parent directory to the Python path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_manager import DataManager

def main():
    try:
        if len(sys.argv) < 2:
            raise ValueError("Project ID is required")
        
        project_id = int(sys.argv[1])
        
        data_manager = DataManager()
        images_df = data_manager.get_project_images(project_id)
        
        # Convert DataFrame to list of dictionaries
        if not images_df.empty:
            # Convert timestamps to strings for JSON serialization
            images_df['processed_timestamp'] = images_df['processed_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            images_data = images_df.to_dict('records')
        else:
            images_data = []
        
        result = {
            'success': True,
            'data': images_data
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