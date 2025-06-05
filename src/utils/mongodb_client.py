"""
MongoDB client for style profiler application.
Handles data retrieval and storage for transcript chunks and style profiles.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://vicsicard:Z6T46srM9kEGZfLJ@cluster0.tfi0dul.mongodb.net/new-self-website-5-15-25?retryWrites=true&w=majority&appName=Cluster0')
MONGODB_DB = os.environ.get('MONGODB_DB', 'new-self-website-5-15-25')

# Error classes to maintain compatibility with existing code
class MongoDBError(Exception):
    """Base class for MongoDB errors"""
    pass

class MongoDBConfigError(MongoDBError):
    """Error with MongoDB configuration"""
    pass

class MongoDBConnectionError(MongoDBError):
    """Error with MongoDB connection"""
    pass

class MongoDBQueryError(MongoDBError):
    """Error with MongoDB query operations"""
    pass

def get_mongodb_client():
    """Get MongoDB client instance"""
    try:
        client = MongoClient(MONGODB_URI)
        # Test connection
        client.admin.command('ping')
        logger.info("Connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise MongoDBConnectionError(f"Failed to connect to MongoDB: {str(e)}")

def get_client_info(client_id):
    """Get client information from MongoDB
    
    Args:
        client_id: The client's UUID
        
    Returns:
        dict: Client information
        
    Raises:
        MongoDBQueryError: If query fails
    """
    try:
        db = _get_database()
        client_info = db.clients.find_one({"_id": client_id})
        return client_info
    except Exception as e:
        logger.error(f"Error getting client info: {str(e)}")
        raise MongoDBQueryError(f"Failed to get client info: {str(e)}")

def get_project_by_access_code(access_code):
    """Get project information by 4-digit access code.
    
    Args:
        access_code: The 4-digit access code
        
    Returns:
        dict: Project information or None if not found
    """
    try:
        db = _get_database()
        project = db.projects.find_one({"accessCode": access_code})
        return project
    except Exception as e:
        logger.error(f"Error getting project by access code: {str(e)}")
        raise MongoDBQueryError(f"Failed to get project by access code: {str(e)}")

def get_project_by_id(project_id):
    """Get project information by project ID.
    
    Args:
        project_id: The project ID
        
    Returns:
        dict: Project information or None if not found
    """
    try:
        db = _get_database()
        project = db.projects.find_one({"_id": project_id})
        return project
    except Exception as e:
        logger.error(f"Error getting project by ID: {str(e)}")
        raise MongoDBQueryError(f"Failed to get project by ID: {str(e)}")

def get_transcript_chunks(client_id):
    """Get transcript chunks for a client
    
    Args:
        client_id: The client's UUID
        
    Returns:
        dict: Transcript chunks data
        
    Raises:
        MongoDBQueryError: If query fails
    """
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DB]
        
        # Find the project associated with this client
        project = db.projects.find_one({"clientId": client_id})
        
        if not project:
            logger.warning(f"No project found for client {client_id}")
            return None
            
        # Get transcript chunks from transcript_chunks collection
        chunks = list(db.transcript_chunks.find({"projectId": project["_id"]}))
        
        if not chunks:
            logger.warning(f"No transcript chunks found for project {project['_id']}")
            return None
            
        # Format the response to match what the application expects
        return {
            "chunks": chunks,
            "metadata": {
                "projectId": str(project["_id"]),
                "clientId": client_id,
                "chunkCount": len(chunks)
            }
        }
    except Exception as e:
        logger.error(f"Error getting transcript chunks: {str(e)}")
        raise MongoDBQueryError(f"Error getting transcript chunks: {str(e)}")

def save_style_profile(client_id, profile_data):
    """Save style profile to MongoDB
    
    Args:
        client_id: The client's UUID
        profile_data: Style profile data
        
    Returns:
        dict: Result of the operation
        
    Raises:
        MongoDBQueryError: If operation fails
    """
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DB]
        
        # Find the project associated with this client
        project = db.projects.find_one({"clientId": client_id})
        
        if not project:
            logger.warning(f"No project found for client {client_id}")
            return {"success": False, "error": "Project not found"}
        
        # Prepare style profile document
        style_profile = {
            "projectId": project["_id"],
            "clientId": client_id,
            "profile": profile_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        # Insert or update style profile
        result = db.style_profiles.update_one(
            {"projectId": project["_id"]},
            {"$set": style_profile},
            upsert=True
        )
        
        # Update project with style profile status
        db.projects.update_one(
            {"_id": project["_id"]},
            {"$set": {
                "hasStyleProfile": True,
                "styleProfileUpdatedAt": datetime.utcnow()
            }}
        )
        
        return {
            "success": True,
            "inserted": result.upserted_id is not None,
            "modified": result.modified_count > 0
        }
    except Exception as e:
        logger.error(f"Error saving style profile: {str(e)}")
        raise MongoDBQueryError(f"Error saving style profile: {str(e)}")

def store_style_profile(display_name, profile_data, chunk_scores=None):
    """Store style profile to MongoDB - compatible with App 2's expected interface
    
    Args:
        display_name: Display name for the client
        profile_data: Style profile data
        chunk_scores: Optional scores for each chunk
        
    Returns:
        dict: Result of the operation
        
    Raises:
        MongoDBQueryError: If operation fails
    """
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DB]
        
        # Find client by display name
        client_info = db.clients.find_one({"displayName": display_name})
        
        if not client_info:
            # Create a new client if not found
            client_id = str(uuid.uuid4())
            client_info = {
                "clientId": client_id,
                "displayName": display_name,
                "createdAt": datetime.utcnow()
            }
            db.clients.insert_one(client_info)
        else:
            client_id = client_info["clientId"]
        
        # Find or create project
        project = db.projects.find_one({"clientId": client_id})
        
        if not project:
            project_id = str(uuid.uuid4())
            project = {
                "_id": project_id,
                "clientId": client_id,
                "displayName": display_name,
                "createdAt": datetime.utcnow()
            }
            db.projects.insert_one(project)
        else:
            project_id = project["_id"]
        
        # Store style profile
        style_profile = {
            "projectId": project_id,
            "clientId": client_id,
            "profile": profile_data,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        # Insert or update style profile
        db.style_profiles.update_one(
            {"projectId": project_id},
            {"$set": style_profile},
            upsert=True
        )
        
        # Store chunk scores if provided
        if chunk_scores:
            for chunk_id, score in chunk_scores.items():
                db.chunk_scores.update_one(
                    {"chunkId": chunk_id, "projectId": project_id},
                    {"$set": {
                        "score": score,
                        "updatedAt": datetime.utcnow()
                    }},
                    upsert=True
                )
        
        # Update project with style profile status
        db.projects.update_one(
            {"_id": project_id},
            {"$set": {
                "hasStyleProfile": True,
                "styleProfileUpdatedAt": datetime.utcnow()
            }}
        )
        
        # Create a processing task for App 3
        processing_task = {
            "type": "generate_content",
            "projectId": project_id,
            "clientId": client_id,
            "status": "pending",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
        
        db.processing_tasks.insert_one(processing_task)
        
        return {
            "success": True,
            "clientId": client_id,
            "projectId": project_id,
            "taskCreated": True
        }
    except Exception as e:
        logger.error(f"Error storing style profile: {str(e)}")
        raise MongoDBQueryError(f"Error storing style profile: {str(e)}")

def save_keywords(client_id, keywords):
    """Save keywords to MongoDB
    
    Args:
        client_id: The client's UUID
        keywords: Keywords data
        
    Returns:
        dict: Result of the operation
        
    Raises:
        MongoDBQueryError: If operation fails
    """
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DB]
        
        # Find the project associated with this client
        project = db.projects.find_one({"clientId": client_id})
        
        if not project:
            logger.warning(f"No project found for client {client_id}")
            return {"success": False, "error": "Project not found"}
        
        # Update style profile with keywords
        result = db.style_profiles.update_one(
            {"projectId": project["_id"]},
            {"$set": {
                "keywords": keywords,
                "updatedAt": datetime.utcnow()
            }}
        )
        
        return {
            "success": True,
            "modified": result.modified_count > 0
        }
    except Exception as e:
        logger.error(f"Error saving keywords: {str(e)}")
        raise MongoDBQueryError(f"Error saving keywords: {str(e)}")

def update_job_status(job_id, status, error=None):
    """Update a job's status in MongoDB
    
    Args:
        job_id: The job's UUID
        status: New status
        error: Optional error message
        
    Returns:
        dict: Result of the operation
        
    Raises:
        MongoDBQueryError: If operation fails
    """
    try:
        client = get_mongodb_client()
        db = client[MONGODB_DB]
        
        update_data = {
            "status": status,
            "updatedAt": datetime.utcnow()
        }
        
        if error:
            update_data["error"] = error
        
        result = db.processing_tasks.update_one(
            {"_id": job_id},
            {"$set": update_data}
        )
        
        return {
            "success": True,
            "modified": result.modified_count > 0
        }
    except Exception as e:
        logger.error(f"Error updating job status: {str(e)}")
        raise MongoDBQueryError(f"Error updating job status: {str(e)}")
