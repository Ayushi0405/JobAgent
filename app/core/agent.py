from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.core.state import AgentState
from app.core.llm import ModelFactory
from app.services.browser import BrowserManager
from app.services.resume import ResumeTailor
from app.services.notification import NotificationService

class JobAgent:
    def __init__(self):
        self.llm = ModelFactory.create_model()
        self.browser_manager = BrowserManager()
        self.resume_tailor = ResumeTailor()
        self.notifier = NotificationService()
        self.graph = self._build_graph()

    async def _analyze_job(self, state: AgentState):
        """Scrapes JD and checks for Red Flags."""
        task = f"Go to {state['job_url']}, scrape the full job description, and check for salary info."
        result = await self.browser_manager.run_task(task, self.llm)
        
        # Simple logic to extract text from result (mocked for brevity)
        jd_text = str(result) 
        
        return {
            "job_description": jd_text,
            "logs": ["✅ Analyzed Job Description."]
        }

    async def _prepare_resume(self, state: AgentState):
        """Tailors resume using the Chameleon Service."""
        new_resume = await self.resume_tailor.tailor(state['master_resume'], state['job_description'])
        return {
            "tailored_resume": new_resume,
            "logs": ["🦎 Resume adapted to job keywords."]
        }

    async def _fill_form(self, state: AgentState):
        """Fills the form but STOPS before submitting."""
        task = f"""
        Go to {state['job_url']}.
        Fill every field using this resume: {state['tailored_resume']}.
        Upload 'resume.pdf' if requested.
        STOP before clicking 'Submit'.
        """
        # In a real run, we'd capture the actual screenshot path from browser-use
        await self.browser_manager.run_task(task, self.llm)
        
        # Notify user
        await self.notifier.send_alert("⚠️ Form filled. Waiting for approval.")
        
        return {
            "form_status": "PENDING_REVIEW",
            "logs": ["⏸️ Paused for Human Review."]
        }

    async def _submit(self, state: AgentState):
        """Clicks the final button."""
        await self.browser_manager.run_task("Click the 'Submit Application' button.", self.llm)
        return {
            "form_status": "SUBMITTED",
            "logs": ["🚀 Application Sent!"]
        }

    def _build_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("analyze", self._analyze_job)
        workflow.add_node("tailor", self._prepare_resume)
        workflow.add_node("fill", self._fill_form)
        workflow.add_node("submit", self._submit)

        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "tailor")
        workflow.add_edge("tailor", "fill")
        workflow.add_edge("fill", "submit")
        workflow.add_edge("submit", END)

        # 🛑 The HITL Magic: Interrupt before submit
        return workflow.compile(
            checkpointer=MemorySaver(),
            interrupt_before=["submit"]
        )