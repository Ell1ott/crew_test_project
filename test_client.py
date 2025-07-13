#!/usr/bin/env python
"""
Simple test client for the AI PR Analysis FastAPI server.
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

def test_analyze_pr(pr_title="Fix login validation bug", pr_description="Fixed validation logic in login form that was causing authentication failures", repo_readme="# My Web App\n\nA simple web application with user authentication and dashboard features."):
    """Test the analyze PR endpoint"""
    try:
        data = {
            "pr_title": pr_title,
            "pr_description": pr_description,
            "repo_readme": repo_readme
        }
        
        print(f"Analyzing PR: {pr_title}")
        print("This may take a few minutes...")
        
        response = requests.post(f"{BASE_URL}/analyze-pr", json=data)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Message: {result['message']}")
            
            if result['browser_flow']:
                print("\nBrowser Flow Preview (first 500 characters):")
                print(result['browser_flow'][:500] + "..." if len(result['browser_flow']) > 500 else result['browser_flow'])
                
                # Save browser flow to file
                with open(f"browser_flow_{pr_title.replace(' ', '_').lower()}.md", "w") as f:
                    f.write(result['browser_flow'])
                print(f"\nFull browser flow saved to: browser_flow_{pr_title.replace(' ', '_').lower()}.md")
            
            if result['pr_comment']:
                print("\nPR Comment Preview (first 500 characters):")
                print(result['pr_comment'][:500] + "..." if len(result['pr_comment']) > 500 else result['pr_comment'])
                
                # Save PR comment to file
                with open(f"pr_comment_{pr_title.replace(' ', '_').lower()}.md", "w") as f:
                    f.write(result['pr_comment'])
                print(f"\nFull PR comment saved to: pr_comment_{pr_title.replace(' ', '_').lower()}.md")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error analyzing PR: {e}")

def main():
    """Main function to test the API"""
    print("Testing AI PR Analysis FastAPI Server")
    print("=" * 40)
    
    # Test health endpoint
    if not test_health():
        print("Server is not running. Please start the server first.")
        return
    
    # Test PR analysis endpoint
    print("Testing PR analysis endpoint...")
    test_analyze_pr(
        pr_title="Add user dashboard feature",
        pr_description="Added a new dashboard page where users can view their profile information, recent activities, and account settings. Includes responsive design and proper authentication checks.",
        repo_readme="# My Web App\n\nA modern web application built with React and Node.js. Features include user authentication, profile management, and dashboard functionality. The app uses JWT tokens for authentication and includes a responsive UI."
    )

if __name__ == "__main__":
    main() 