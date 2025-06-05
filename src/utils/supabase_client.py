"""
Supabase client for style profiler application.
Handles data retrieval and storage without video dependencies.
"""

import os
import json
import uuid
import requests
from dotenv import load_dotenv
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')  # Using service role key for server-side operations

# Error classes expected by App 2
class SupabaseError(Exception):
    """Base class for Supabase errors"""
    pass

class SupabaseConfigError(SupabaseError):
    """Error with Supabase configuration"""
    pass

class SupabaseStorageError(SupabaseError):
    """Error with Supabase storage operations"""
    pass

class SupabaseDatabaseError(SupabaseError):
    """Error with Supabase database operations"""
    pass

def get_supabase_headers():
    """Get standard headers for Supabase API requests"""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def get_client_info(client_id):
    """Get client information from Supabase"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/clients?id=eq.{client_id}",
            headers=get_supabase_headers()
        )
        
        if response.status_code == 200:
            clients = response.json()
            if clients:
                return clients[0]
        
        return None
    except Exception as e:
        print(f"Error getting client info: {str(e)}")
        return None

def get_transcript_chunks(client_id):
    """Get transcript chunks for a client (VTT-ONLY MODE, NO VIDEO)"""
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/transcript_chunks?client_id=eq.{client_id}&order=seq_num",
            headers=get_supabase_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        
        print(f"Error getting transcript chunks: {response.status_code} {response.text}")
        return []
    except Exception as e:
        print(f"Error getting transcript chunks: {str(e)}")
        return []

def save_style_profile(client_id, profile_data):
    """Save style profile to Supabase"""
    try:
        # Check if a profile already exists for this client
        existing_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/style_profiles?client_id=eq.{client_id}",
            headers=get_supabase_headers()
        )
        
        if existing_response.status_code == 200 and existing_response.json():
            # Update existing profile
            profile_id = existing_response.json()[0]['id']
            response = requests.patch(
                f"{SUPABASE_URL}/rest/v1/style_profiles?id=eq.{profile_id}",
                headers=get_supabase_headers(),
                json={
                    "profile_data": profile_data,
                    "updated_at": "now()"
                }
            )
        else:
            # Create new profile
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/style_profiles",
                headers=get_supabase_headers(),
                json={
                    "client_id": client_id,
                    "profile_data": profile_data
                }
            )
        
        if response.status_code in [200, 201, 204]:
            print(f"Successfully saved style profile for client {client_id}")
            return True
        else:
            print(f"Error saving style profile: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"Error saving style profile: {str(e)}")
        return False

def store_style_profile(display_name, profile_data, chunk_scores=None):
    """Save style profile to Supabase - this function is named to match what App 2 expects"""
    try:
        # Generate a valid UUID for project_id (required by Supabase)
        project_id = str(uuid.uuid4())
        logger.info(f"Generated UUID for {display_name}: {project_id}")
        
        # Prepare headers for Supabase API requests
        headers = get_supabase_headers()
        
        # Save profile data to Supabase Storage
        profile_path = f"{project_id}/style-profile.md"
        profile_upload_url = f"{SUPABASE_URL}/storage/v1/object/documents/{profile_path}"
        
        profile_response = requests.post(
            profile_upload_url,
            headers=headers,
            data=profile_data
        )
        
        if profile_response.status_code not in (200, 201):
            logger.error(f"Failed to upload style profile: {profile_response.text}")
            return False
            
        logger.info(f"Successfully saved style profile for {display_name} (ID: {project_id})")
        
        # Save chunk scores if provided
        if chunk_scores:
            try:
                # Convert dict to JSON string for storage
                scores_json = json.dumps(chunk_scores, indent=2)
                
                # Upload chunk scores to Supabase
                scores_path = f"{project_id}/video_chunk_scores.json"
                scores_upload_url = f"{SUPABASE_URL}/storage/v1/object/documents/{scores_path}"
                
                scores_response = requests.post(
                    scores_upload_url,
                    headers=headers,
                    data=scores_json
                )
                
                if scores_response.status_code not in (200, 201):
                    logger.error(f"Failed to upload chunk scores: {scores_response.text}")
                    return False
                    
                logger.info(f"Successfully uploaded chunk scores to {scores_path}")
                
            except Exception as e:
                logger.error(f"Error saving chunk scores: {str(e)}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error storing style profile: {str(e)}")
        return False

def save_keywords(client_id, keywords):
    """Save keywords to Supabase"""
    try:
        # Check if keywords already exist for this client
        existing_response = requests.get(
            f"{SUPABASE_URL}/rest/v1/client_keywords?client_id=eq.{client_id}",
            headers=get_supabase_headers()
        )
        
        if existing_response.status_code == 200 and existing_response.json():
            # Update existing keywords
            keyword_id = existing_response.json()[0]['id']
            response = requests.patch(
                f"{SUPABASE_URL}/rest/v1/client_keywords?id=eq.{keyword_id}",
                headers=get_supabase_headers(),
                json={
                    "keywords": keywords,
                    "updated_at": "now()"
                }
            )
        else:
            # Create new keywords
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/client_keywords",
                headers=get_supabase_headers(),
                json={
                    "client_id": client_id,
                    "keywords": keywords
                }
            )
        
        if response.status_code in [200, 201, 204]:
            print(f"Successfully saved keywords for client {client_id}")
            return True
        else:
            print(f"Error saving keywords: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"Error saving keywords: {str(e)}")
        return False

def update_job_status(job_id, status, error=None):
    """Update a job's status in Supabase"""
    try:
        update_data = {
            "status": status,
            "last_updated": "now()"
        }
        
        if error:
            update_data["error"] = error
        
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/processing_jobs?id=eq.{job_id}",
            headers=get_supabase_headers(),
            json=update_data
        )
        
        if response.status_code in [200, 204]:
            print(f"Updated job {job_id} status to {status}")
            return True
        else:
            print(f"Error updating job status: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"Error updating job status: {str(e)}")
        return False
