"""
Supabase client configuration and document retrieval utilities.
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from supabase import create_client, Client, StorageException

# Load environment variables
load_dotenv()

class SupabaseError(Exception):
    """Base exception for Supabase-related errors."""
    pass

class SupabaseConfigError(SupabaseError):
    """Raised when there are configuration issues."""
    pass

class SupabaseStorageError(SupabaseError):
    """Raised when there are storage-related issues."""
    pass

class SupabaseDatabaseError(SupabaseError):
    """Raised when there are database-related issues."""
    pass

def get_supabase_client() -> Client:
    """Initialize and return Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        error_msg = "Missing Supabase credentials. Please check .env file."
        logger.error(error_msg)
        raise SupabaseConfigError(error_msg)
    
    try:
        client = create_client(url, key)
        logger.debug("Successfully initialized Supabase client")
        return client
    except Exception as e:
        error_msg = f"Failed to create Supabase client: {str(e)}"
        logger.error(error_msg)
        raise SupabaseConfigError(error_msg) from e

def check_analysis_exists(project_id: str) -> Optional[Dict[str, str]]:
    """
    Check if analysis results already exist for the project.
    
    Args:
        project_id: The unique identifier for the project
        
    Returns:
        Optional[Dict[str, str]]: Paths to existing files if found, None otherwise
    """
    try:
        supabase = get_supabase_client()
        
        response = supabase.table("transcript_files")\
            .select("style_profile_path, chunk_scores_path")\
            .eq("project_id", project_id)\
            .eq("status", "analyzed")\
            .execute()
        
        if response.data:
            logger.info(f"Found existing analysis for project {project_id}")
            return response.data[0]
        
        logger.debug(f"No existing analysis found for project {project_id}")
        return None
        
    except Exception as e:
        error_msg = f"Error checking analysis status: {str(e)}"
        logger.error(error_msg)
        raise SupabaseDatabaseError(error_msg) from e

def fetch_transcript_chunks(project_id: str) -> str:
    """
    Fetch transcript_chunks.md from Supabase storage for a given project.
    
    Args:
        project_id: The unique identifier for the project
        
    Returns:
        str: Content of transcript_chunks.md file
    """
    try:
        supabase = get_supabase_client()
        
        # Construct the path in the documents bucket
        file_path = f"{project_id}/transcript_chunks.md"
        
        try:
            # Download the file from the documents bucket
            response = supabase.storage.from_("documents").download(file_path)
            
            # Decode the binary content to string
            content = response.decode('utf-8')
            
            logger.info(f"Successfully fetched transcript_chunks.md for project {project_id}")
            return content
            
        except StorageException as e:
            error_msg = f"Storage error fetching transcript: {str(e)}"
            logger.error(error_msg)
            raise SupabaseStorageError(error_msg) from e
            
    except SupabaseConfigError:
        raise
    except Exception as e:
        error_msg = f"Unexpected error fetching transcript: {str(e)}"
        logger.error(error_msg)
        raise SupabaseError(error_msg) from e

def store_style_profile(project_id: str, profile_content: str, chunk_scores: Dict[str, Any]) -> None:
    """
    Store style profile and chunk scores in Supabase for a given project.
    
    Args:
        project_id: The unique identifier for the project
        profile_content: Content of style-profile.md
        chunk_scores: Dictionary of chunk scores
    """
    try:
        supabase = get_supabase_client()
        
        # Check if analysis already exists
        existing = check_analysis_exists(project_id)
        if existing:
            logger.warning(f"Overwriting existing analysis for project {project_id}")
        
        try:
            # Store style profile markdown
            profile_path = f"{project_id}/style-profile.md"
            profile_bytes = profile_content.encode('utf-8')
            supabase.storage.from_("documents").upload(
                path=profile_path,
                file=profile_bytes,
                file_options={"content-type": "text/markdown", "upsert": True}
            )
            logger.info(f"Stored style profile at {profile_path}")
            
            # Store chunk scores JSON
            scores_path = f"{project_id}/video_chunk_scores.json"
            scores_bytes = json.dumps(chunk_scores, indent=2).encode('utf-8')
            supabase.storage.from_("documents").upload(
                path=scores_path,
                file=scores_bytes,
                file_options={"content-type": "application/json", "upsert": True}
            )
            logger.info(f"Stored chunk scores at {scores_path}")
            
            try:
                # Update the transcript_files table
                supabase.table("transcript_files").upsert([{
                    "project_id": project_id,
                    "style_profile_path": profile_path,
                    "chunk_scores_path": scores_path,
                    "status": "analyzed",
                    "updated_at": "now()"
                }]).execute()
                
                logger.info(f"Successfully updated transcript_files for project {project_id}")
                
            except Exception as e:
                error_msg = f"Database error updating transcript_files: {str(e)}"
                logger.error(error_msg)
                raise SupabaseDatabaseError(error_msg) from e
            
        except StorageException as e:
            error_msg = f"Storage error storing analysis results: {str(e)}"
            logger.error(error_msg)
            raise SupabaseStorageError(error_msg) from e
            
    except SupabaseConfigError:
        raise
    except Exception as e:
        error_msg = f"Unexpected error storing analysis results: {str(e)}"
        logger.error(error_msg)
        raise SupabaseError(error_msg) from e
