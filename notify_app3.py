"""
Notification script for App 3 (Content Generator)
Sends a webhook notification to App 3 when style profiling is complete
"""

import os
import json
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('notify_app3.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
APP3_WEBHOOK_URL = os.environ.get('APP3_WEBHOOK_URL', '')
API_KEY = os.environ.get('API_KEY', 'default_api_key')

def notify_app3(project_id, client_id, job_id=None, style_profile_path=None):
    """
    Notify App 3 that style profiling is complete
    
    Args:
        project_id: The project ID
        client_id: The client ID
        job_id: Optional job ID
        style_profile_path: Optional path to the style profile
    
    Returns:
        bool: True if notification was successful, False otherwise
    """
    if not APP3_WEBHOOK_URL:
        logger.error("APP3_WEBHOOK_URL environment variable not set")
        return False
    
    # Prepare payload
    payload = {
        "projectId": project_id,
        "clientId": client_id,
        "source": "style_profiler",
        "status": "completed"
    }
    
    if job_id:
        payload["jobId"] = job_id
    
    # Add style profile data if available
    if style_profile_path and Path(style_profile_path).exists():
        try:
            with open(style_profile_path, 'r') as f:
                profile_data = json.load(f)
            payload["styleProfile"] = profile_data
        except Exception as e:
            logger.error(f"Error reading style profile: {str(e)}")
    
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    # Send notification
    try:
        logger.info(f"Sending notification to App 3: {APP3_WEBHOOK_URL}")
        response = requests.post(
            APP3_WEBHOOK_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"Notification sent successfully: {response.status_code}")
            return True
        else:
            logger.error(f"Notification failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Notify App 3 that style profiling is complete")
    parser.add_argument("--project-id", required=True, help="Project ID")
    parser.add_argument("--client-id", required=True, help="Client ID")
    parser.add_argument("--job-id", help="Job ID")
    parser.add_argument("--profile-path", help="Path to style profile JSON")
    
    args = parser.parse_args()
    
    success = notify_app3(
        args.project_id,
        args.client_id,
        args.job_id,
        args.profile_path
    )
    
    if not success:
        exit(1)
