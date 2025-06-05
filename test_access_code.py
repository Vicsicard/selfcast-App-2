#!/usr/bin/env python
"""
Test script for 4-digit access code integration with MongoDB
"""

import os
import json
import logging
from dotenv import load_dotenv
from src.utils.mongodb_client import (
    get_project_by_access_code,
    get_project_by_id,
    get_client_info,
    MongoDBError
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_access_code_lookup(access_code):
    """Test looking up a project by its 4-digit access code"""
    try:
        logger.info(f"Looking up project with access code: {access_code}")
        project = get_project_by_access_code(access_code)
        
        if not project:
            logger.warning(f"No project found with access code: {access_code}")
            return
        
        logger.info(f"Found project: {project.get('_id')}")
        logger.info(f"Project name: {project.get('name')}")
        logger.info(f"Project owner: {project.get('ownerEmail')}")
        
        # Get client info if available
        if project.get('ownerId'):
            client = get_client_info(project.get('ownerId'))
            if client:
                logger.info(f"Client name: {client.get('name')}")
                logger.info(f"Client email: {client.get('email')}")
        
        return project
    except MongoDBError as e:
        logger.error(f"MongoDB error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

def main():
    """Main function"""
    print("=== 4-Digit Access Code Integration Test ===")
    
    # Test with a valid access code
    access_code = input("Enter a 4-digit access code to test (or press Enter for '1234'): ")
    if not access_code:
        access_code = "1234"
    
    project = test_access_code_lookup(access_code)
    
    if project:
        print("\nProject details:")
        print(json.dumps(project, indent=2, default=str))
    else:
        print(f"\nNo project found with access code: {access_code}")
        print("Make sure the access code exists in the MongoDB 'projects' collection.")

if __name__ == "__main__":
    main()
