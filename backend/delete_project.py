#!/usr/bin/env python3
import sys
import os
import json

# Add the parent directory to the Python path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_manager import DataManager

def main():
    try:
        if len(sys.argv) < 2:
            raise ValueError("Project ID is required")
        
        project_id = int(sys.argv[1])
        
        data_manager = DataManager()
        success = data_manager.delete_project(project_id)
        
        result = {
            'success': success,
            'data': {'deleted': success}
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