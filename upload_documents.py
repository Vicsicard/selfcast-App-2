"""
Upload document files to Supabase storage.
"""
import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

def upload_file(supabase, bucket_name: str, file_path: Path, remote_path: str):
    """Upload a file to Supabase storage"""
    print(f"[*] Uploading {file_path} to {bucket_name}/{remote_path}")
    
    try:
        with open(file_path, 'rb') as f:
            supabase.storage.from_(bucket_name).upload(
                remote_path,
                f,
                {"content-type": "application/octet-stream"}
            )
        print(f"[+] Successfully uploaded {file_path}")
        return True
        
    except Exception as e:
        print(f"[-] Error uploading {file_path}: {str(e)}")
        if hasattr(e, 'message'):
            print(f"[-] Error message: {e.message}")
        return False

def main():
    # Load environment variables
    load_dotenv()
    
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        raise EnvironmentError("Missing Supabase credentials")
    
    # Initialize Supabase client
    supabase = create_client(url, service_key)
    print("[*] Connected to Supabase")
    
    # Define files to upload
    output_dir = Path("output/app2")
    files_to_upload = [
        "transcript_chunks.md",
        "chunk_metadata.json",
        "chunk_vectors.json",
        "video_index.json"
    ]
    
    success_count = 0
    
    # Upload each file
    for filename in files_to_upload:
        file_path = output_dir / filename
        
        if not file_path.exists():
            print(f"[-] File not found: {file_path}")
            continue
            
        if upload_file(supabase, "documents", file_path, filename):
            success_count += 1
    
    print(f"\n[*] Upload complete! {success_count}/{len(files_to_upload)} files processed")

if __name__ == "__main__":
    main()
