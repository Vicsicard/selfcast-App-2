import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

def get_supabase_headers():
    """Get standard headers for Supabase API requests."""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def find_latest_uploads():
    """Find the latest uploads in the documents bucket."""
    # Get list of files in the documents bucket
    headers = get_supabase_headers()
    url = f"{SUPABASE_URL}/storage/v1/object/list/documents"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error listing files: {response.text}")
        return
    
    # Get all files
    files = response.json()
    
    # Print details of all files in documents bucket
    print(f"Found {len(files)} files in documents bucket")
    
    # Group files by parent folder (UUID)
    folders = {}
    for file in files:
        name = file.get('name', '')
        if '/' in name:  # Files are stored in UUID folders
            folder, filename = name.split('/', 1)
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(filename)
    
    # Print folders and their files
    print("\nFolders (UUIDs) and their files:")
    for folder, files in folders.items():
        print(f"\nUUID: {folder}")
        for file in files:
            print(f"  - {file}")
    
    # Also try to find specifically AnnieNew files by looking at content
    print("\nSearching for 'AnnieNew' in recently uploaded files...")
    
    # Get most recent files in each folder
    for folder, files in folders.items():
        for file in files:
            if file == 'style-profile.md':
                # Get file content
                file_url = f"{SUPABASE_URL}/storage/v1/object/documents/{folder}/{file}"
                file_response = requests.get(file_url, headers=headers)
                
                if file_response.status_code == 200:
                    content = file_response.text
                    if 'Annie' in content:
                        print(f"\nFound likely match!")
                        print(f"UUID: {folder}")
                        print(f"File: {file}")
                        print(f"Contains 'Annie' reference")
                        
                        # Print first 200 characters as preview
                        preview = content[:200].replace('\n', ' ')
                        print(f"Preview: {preview}...")

if __name__ == "__main__":
    find_latest_uploads()
