from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import asyncio
import warnings
from typing import Optional

from crew_test_project.crew import CrewTestProject

# Suppress warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(
    title="AI Crew API",
    description="API for running AI research crew",
    version="1.0.0"
)

class CrewRequest(BaseModel):
    topic: str
    current_year: Optional[str] = None

class CrewResponse(BaseModel):
    success: bool
    message: str
    report: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Crew API",
        "version": "1.0.0",
        "endpoints": {
            "POST /run-crew": "Run the AI crew with a topic",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/run-crew", response_model=CrewResponse)
async def run_crew(request: CrewRequest):
    """
    Run the AI crew with the provided topic.
    
    Args:
        request: CrewRequest object containing topic and optional current_year
        
    Returns:
        CrewResponse with success status and report content
    """
    try:
        # Use provided year or default to current year
        current_year = request.current_year or str(datetime.now().year)
        
        inputs = {
            'topic': request.topic,
            'current_year': current_year
        }
        
        # Run the crew in a thread pool to avoid blocking the async event loop
        crew_instance = CrewTestProject()
        
        # Create a function to run the crew synchronously
        def run_crew_sync():
            return crew_instance.crew().kickoff(inputs=inputs)
        
        # Run the crew in a separate thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_crew_sync)
        
        # Try to read the generated report
        report_content = None
        try:
            with open('report.md', 'r', encoding='utf-8') as f:
                report_content = f.read()
        except FileNotFoundError:
            report_content = "Report file not found, but crew execution completed."
        
        return CrewResponse(
            success=True,
            message=f"Crew execution completed successfully for topic: {request.topic}",
            report=report_content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while running the crew: {str(e)}"
        )

@app.post("/run-crew-sync", response_model=CrewResponse)
async def run_crew_sync_endpoint(request: CrewRequest):
    """
    Run the AI crew synchronously (blocking).
    Use this endpoint if you prefer synchronous execution.
    """
    try:
        current_year = request.current_year or str(datetime.now().year)
        
        inputs = {
            'topic': request.topic,
            'current_year': current_year
        }
        
        crew_instance = CrewTestProject()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Try to read the generated report
        report_content = None
        try:
            with open('report.md', 'r', encoding='utf-8') as f:
                report_content = f.read()
        except FileNotFoundError:
            report_content = "Report file not found, but crew execution completed."
        
        return CrewResponse(
            success=True,
            message=f"Crew execution completed successfully for topic: {request.topic}",
            report=report_content
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while running the crew: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 