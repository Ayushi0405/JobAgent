import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.agent import JobAgent

app = FastAPI(title="Ghost Hunter API")

# Allow Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent_system = JobAgent()

class JobRequest(BaseModel):
    url: str
    resume: str

@app.post("/api/start")
async def start_job(req: JobRequest):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "job_url": req.url,
        "master_resume": req.resume,
        "logs": ["🚀 Starting Ghost Hunter..."]
    }
    
    # Run until interrupt
    async for event in agent_system.graph.astream(initial_state, config):
        pass
        
    return {"thread_id": thread_id, "status": "WAITING_FOR_APPROVAL"}

@app.post("/api/approve/{thread_id}")
async def approve_job(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    
    # Resume execution
    async for event in agent_system.graph.astream(None, config):
        pass
        
    return {"status": "COMPLETED"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)