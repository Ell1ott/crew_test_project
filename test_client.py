#!/usr/bin/env python
"""
Simple test client for the AI Crew FastAPI server.
"""

import requests
import json

# Server URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_run_crew(topic="Machine Learning", current_year=None):
    """Test the run crew endpoint"""
    try:
        data = {
            "topic": topic,
            "current_year": current_year
        }
        
        print(f"Running crew for topic: {topic}")
        print("This may take a few minutes...")
        
        response = requests.post(f"{BASE_URL}/run-crew", json=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Message: {result['message']}")
            
            if result['report']:
                print("\nReport Preview (first 500 characters):")
                print(result['report'][:500] + "..." if len(result['report']) > 500 else result['report'])
                
                # Save report to file
                with open(f"api_report_{topic.replace(' ', '_').lower()}.md", "w") as f:
                    f.write(result['report'])
                print(f"\nFull report saved to: api_report_{topic.replace(' ', '_').lower()}.md")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error running crew: {e}")

def main():
    """Main function to test the API"""
    print("Testing AI Crew FastAPI Server")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health():
        print("Server is not running. Please start the server first.")
        return
    
    # Test crew endpoint
    print("Testing crew endpoint...")
    test_run_crew("Artificial Intelligence", "2024")

if __name__ == "__main__":
    main() 