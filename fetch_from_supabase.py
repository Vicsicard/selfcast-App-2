"""
Download files from Supabase storage buckets.
"""
import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

def download_file(supabase, bucket_name: str, file_path: str, output_dir: Path):
    """Download a file from Supabase storage."""
    try:
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download file
        output_path = output_dir / os.path.basename(file_path)
        with open(output_path, 'wb+') as f:
            res = supabase.storage.from_(bucket_name).download(file_path)
            f.write(res)
            
        print(f"[+] Successfully downloaded to {output_path}")
        return True
        
    except Exception as e:
        print(f"[-] Error downloading {file_path}: {str(e)}")
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
    print("[*] Connected to Supabase\n")
    
    # Create output directories
    output_dir = Path("output/app2/documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Download files from documents bucket
    directory = "ac47654b-d391-4dc3-a7a2-96456aa86ce1"
    files_to_download = [
        f"{directory}/transcript_chunks.md",
        f"{directory}/chunk_metadata.json",
        f"{directory}/chunk_vectors.json",
        f"{directory}/video_index.json"
    ]
    
    for file_path in files_to_download:
        download_file(supabase, "documents", file_path, output_dir)
    
    print("\n[*] Download complete!")

if __name__ == "__main__":
    main()
