"""
List files in Supabase storage buckets
"""
import os
from supabase import create_client
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        raise EnvironmentError("Missing Supabase credentials")
    
    # Initialize client with service role
    supabase = create_client(url, service_key)
    print("[*] Connected to Supabase")
    
    try:
        # List all buckets
        print("\n[*] Available buckets:")
        buckets = supabase.storage.list_buckets()
        for bucket in buckets:
            print(f"\nBucket: {bucket.name}")
            
            # List contents of each bucket
            try:
                print("Contents:")
                files = supabase.storage.from_(bucket.name).list()
                for f in files:
                    print(f"  - {f['name']}")
            except Exception as e:
                print(f"  Error listing contents: {str(e)}")
            
    except Exception as e:
        print(f"\n[-] Error: {str(e)}")
        if hasattr(e, 'message'):
            print(f"[-] Error message: {e.message}")
        raise

if __name__ == "__main__":
    main()
