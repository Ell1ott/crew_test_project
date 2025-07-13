from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncio
import warnings
# import weave
from typing import Optional

from crew_test_project.crew import CrewTestProject

# Suppress warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Initialize Weave for debugging and observability
# weave.init(project_name="crew-test-project-api")

app = FastAPI(
    title="AI PR Analysis API",
    description="API for analyzing PRs with AI agents",
    version="1.0.0"
)

class PRRequest(BaseModel):
    pr_title: str
    pr_description: str
    repo_readme: str

class PRResponse(BaseModel):
    success: bool
    message: str
    browser_flow: Optional[str] = None
    pr_comment: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI PR Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze-pr": "Analyze PR and generate browser flow and PR comment",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze-pr", response_model=PRResponse)
async def analyze_pr(request: PRRequest):
    """
    Analyze a PR and generate browser flow and PR comment.
    
    Args:
        request: PRRequest object containing pr_title, pr_description, and repo_readme
        
    Returns:
        PRResponse with success status and generated content
    """
    try:
        inputs = {
            'pr_title': request.pr_title,
            'pr_description': request.pr_description,
            'repo_readme': request.repo_readme
        }
        
        # Run the crew in a thread pool to avoid blocking the async event loop
        crew_instance = CrewTestProject()
        
        # Create a function to run the crew synchronously
        def run_crew_sync():
            return crew_instance.crew().kickoff(inputs=inputs)
        
        # Run the crew in a separate thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_crew_sync)
        
        # Try to read the generated PR comment
        pr_comment_content = None
        try:
            with open('pr_comment.md', 'r', encoding='utf-8') as f:
                pr_comment_content = f.read()
        except FileNotFoundError:
            pr_comment_content = "PR comment file not found, but crew execution completed."
        
        # The browser flow should be in the result from the first task
        browser_flow_content = str(result)
        
        return PRResponse(
            success=True,
            message=f"PR analysis completed successfully for: {request.pr_title}",
            browser_flow=browser_flow_content,
            pr_comment=pr_comment_content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing the PR: {str(e)}"
        )

@app.post("/analyze-pr-sync", response_model=PRResponse)
async def analyze_pr_sync_endpoint(request: PRRequest):
    """
    Analyze a PR synchronously (blocking).
    Use this endpoint if you prefer synchronous execution.
    """
    try:
        inputs = {
            'pr_title': request.pr_title,
            'pr_description': request.pr_description,
            'repo_readme': request.repo_readme
        }
        
        crew_instance = CrewTestProject()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Try to read the generated PR comment
        pr_comment_content = None
        try:
            with open('pr_comment.md', 'r', encoding='utf-8') as f:
                pr_comment_content = f.read()
        except FileNotFoundError:
            pr_comment_content = "PR comment file not found, but crew execution completed."
        
        # The browser flow should be in the result from the first task
        browser_flow_content = str(result)
        
        return PRResponse(
            success=True,
            message=f"PR analysis completed successfully for: {request.pr_title}",
            browser_flow=browser_flow_content,
            pr_comment=pr_comment_content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing the PR: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 