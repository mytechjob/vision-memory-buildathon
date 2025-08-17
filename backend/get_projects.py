#!/usr/bin/env python3
import sys
import os
import json

# Add the parent directory to the Python path so we can import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_manager import DataManager

def main():
    try:
        data_manager = DataManager()
        projects_list = data_manager.get_projects()
        
        # Convert datetime objects to strings for JSON serialization
        projects_data = []
        for project in projects_list:
            project_copy = project.copy()
            # Convert datetime objects to strings
            for key, value in project_copy.items():
                if hasattr(value, 'strftime'):  # Check if it's a datetime object
                    project_copy[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            projects_data.append(project_copy)
        
        result = {
            'success': True,
            'projects': projects_data
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