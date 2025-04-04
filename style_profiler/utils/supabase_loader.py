"""
Supabase data loader utility.
"""
import os
from typing import List, Dict
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

def get_chunks_for_user_project(project_id: str, user_id: str) -> List[Dict]:
    """
    Query Supabase for chunks matching project_id and user_id.
    
    Args:
        project_id (str): Project identifier
        user_id (str): User identifier
        
    Returns:
        List[Dict]: Sorted list of chunk dictionaries containing:
                   chunk_id, question_id, response_text, etc.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        raise EnvironmentError("Missing Supabase credentials in .env file")
        
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # Query chunks table with filters
    response = supabase.table("chunks")\
        .select("*")\
        .eq("project_id", project_id)\
        .eq("user_id", user_id)\
        .order("chunk_id")\
        .execute()
        
    return response.data
