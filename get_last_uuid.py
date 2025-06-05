import re
import os
from pathlib import Path

def extract_uuid_from_log():
    log_path = Path('output/style_profiler.log')
    
    if not log_path.exists():
        print("Log file not found")
        return None
    
    # Read the log file
    with open(log_path, 'r') as f:
        log_content = f.read()
    
    # Look for the line with UUID information
    uuid_pattern = r"Generated UUID for AnnieNew5-2-25-GG: ([0-9a-f-]+)"
    uuid_match = re.search(uuid_pattern, log_content)
    
    if uuid_match:
        uuid = uuid_match.group(1)
        print(f"Found UUID: {uuid}")
        return uuid
    else:
        print("UUID not found in log file")
        return None

if __name__ == "__main__":
    extract_uuid_from_log()
