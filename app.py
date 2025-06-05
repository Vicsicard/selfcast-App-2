"""
Entry point for the Style Profiler API server (App 2)
This file imports the Flask app from api_server.py and serves as the entry point for Gunicorn
"""

from api_server import app

if __name__ == "__main__":
    # This block will be executed when running directly with Python
    # but not when running with Gunicorn
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
