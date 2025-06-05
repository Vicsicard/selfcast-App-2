"""
API Server for Style Profiler (App 2)
Provides webhook endpoints for integration with App 1 and App 3.
"""

import os
import json
import uuid
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import subprocess
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('api_server.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
API_KEY = os.environ.get('API_KEY', 'default_api_key')  # Should be set in .env
OUTPUT_DIR = Path(os.environ.get('OUTPUT_DIR', 'output'))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def validate_api_key(request):
    """Validate API key from request"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return False
    
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return False
        
    return parts[1] == API_KEY

def run_style_profiler(project_id, client_id, display_name):
    """Run style profiler as a subprocess"""
    try:
        # Create a unique job ID
        job_id = str(uuid.uuid4())
        
        # Create job directory
        job_dir = OUTPUT_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Create job metadata file
        job_metadata = {
            "job_id": job_id,
            "project_id": project_id,
            "client_id": client_id,
            "display_name": display_name,
            "status": "running",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        with open(job_dir / "job_metadata.json", 'w') as f:
            json.dump(job_metadata, f, indent=2)
        
        # Run style profiler in a separate process
        cmd = [
            "python", "style_profiler.py",
            "--client-id", client_id,
            "--project-id", project_id,
            "--display-name", display_name,
            "--output-dir", str(job_dir),
            "--job-id", job_id,
            "--mongodb"  # Flag to use MongoDB instead of Supabase
        ]
        
        logger.info(f"Starting style profiler: {' '.join(cmd)}")
        
        # Run in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Start threads to handle stdout and stderr
        def log_output(stream, log_func):
            for line in stream:
                log_func(line.strip())
            
        threading.Thread(target=log_output, args=(process.stdout, logger.info)).start()
        threading.Thread(target=log_output, args=(process.stderr, logger.error)).start()
        
        # Start a thread to monitor job completion and notify App 3
        def monitor_job_completion():
            # Wait for process to complete
            process.wait()
            
            # Check job status by reading metadata file
            try:
                with open(job_dir / "job_metadata.json", 'r') as f:
                    metadata = json.load(f)
                
                if metadata.get('status') == 'completed':
                    # Job completed successfully, notify App 3
                    logger.info(f"Job {job_id} completed successfully, notifying App 3")
                    
                    # Run notify_app3.py
                    notify_cmd = [
                        "python", "notify_app3.py",
                        "--project-id", project_id,
                        "--client-id", client_id,
                        "--job-id", job_id,
                        "--profile-path", str(job_dir / "chunk_scores.json")
                    ]
                    
                    subprocess.run(notify_cmd)
            except Exception as e:
                logger.error(f"Error monitoring job completion: {str(e)}")
        
        threading.Thread(target=monitor_job_completion).start()
        
        return job_id
    except Exception as e:
        logger.error(f"Error running style profiler: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/webhook/process-transcript', methods=['POST'])
def process_transcript():
    """Webhook endpoint to process a transcript"""
    # Validate API key
    if not validate_api_key(request):
        return jsonify({
            "success": False,
            "error": "Invalid API key"
        }), 401
    
    try:
        # Parse request data
        data = request.json
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Extract fields from request
        project_id = data.get('projectId')
        client_id = data.get('clientId')
        access_code = data.get('accessCode')  # 4-digit code
        display_name = data.get('displayName')
        
        # Import MongoDB client here to avoid circular imports
        from src.utils.mongodb_client import get_project_by_access_code, get_project_by_id
        
        # If we have an access code but no project_id, look up the project
        if access_code and not project_id:
            try:
                logger.info(f"Looking up project by access code: {access_code}")
                project = get_project_by_access_code(access_code)
                if project:
                    project_id = project.get('_id')
                    logger.info(f"Found project {project_id} for access code {access_code}")
                    
                    # If no client_id was provided, use the project owner's client_id
                    if not client_id and project.get('ownerId'):
                        client_id = project.get('ownerId')
                        logger.info(f"Using project owner as client: {client_id}")
            except Exception as e:
                logger.error(f"Error looking up project by access code: {str(e)}")
        
        # Validate we have the necessary information
        if not project_id or not client_id:
            return jsonify({
                "success": False,
                "error": "Missing required fields: projectId, clientId or valid accessCode"
            }), 400
        
        # Set default display name if not provided
        if not display_name:
            # Try to get a better display name from the project
            try:
                project = get_project_by_id(project_id)
                if project and project.get('name'):
                    display_name = project.get('name')
                else:
                    display_name = f"Client-{client_id[:8]}"
            except Exception:
                display_name = f"Client-{client_id[:8]}"
        
        # Log the processing request
        logger.info(f"Processing transcript for project: {project_id}, client: {client_id}, access code: {access_code}")
        
        # Run style profiler
        job_id = run_style_profiler(project_id, client_id, display_name)
        
        if not job_id:
            return jsonify({
                "success": False,
                "error": "Failed to start style profiler"
            }), 500
        
        return jsonify({
            "success": True,
            "jobId": job_id,
            "projectId": project_id,
            "message": "Style profiler job started"
        })
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get status of a job"""
    # Validate API key
    if not validate_api_key(request):
        return jsonify({
            "success": False,
            "error": "Invalid API key"
        }), 401
    
    try:
        job_dir = OUTPUT_DIR / job_id
        
        if not job_dir.exists():
            return jsonify({
                "success": False,
                "error": "Job not found"
            }), 404
        
        # Read job metadata
        with open(job_dir / "job_metadata.json", 'r') as f:
            job_metadata = json.load(f)
        
        return jsonify({
            "success": True,
            "job": job_metadata
        })
    except Exception as e:
        logger.error(f"Error getting job status: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
