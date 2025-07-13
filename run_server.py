#!/usr/bin/env python
"""
Simple script to run the FastAPI server for the AI crew.
"""

import uvicorn

if __name__ == "__main__":
    print("Starting AI Crew FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "src.crew_test_project.server:app",  # Use import string instead of direct import
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 