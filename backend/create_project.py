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
            raise ValueError("Project name is required")
        
        name = sys.argv[1]
        description = sys.argv[2] if len(sys.argv) > 2 else ""
        
        data_manager = DataManager()
        project_id = data_manager.create_project(name, description)
        
        if project_id:
            result = {
                'success': True,
                'data': {'id': project_id, 'name': name, 'description': description}
            }
        else:
            result = {
                'success': False,
                'error': 'Failed to create project'
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