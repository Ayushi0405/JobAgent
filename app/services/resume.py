from app.core.llm import ModelFactory

class ResumeTailor:
    def __init__(self):
        self.llm = ModelFactory.create_model()

    async def tailor(self, master_resume: str, job_description: str) -> str:
        """Rewrites the resume to match the specific job keywords."""
        prompt = f"""
        You are an expert ATS optimizer.
        JOB: {job_description[:2000]}
        RESUME: {master_resume}
        
        Task: Rewrite the 'Summary' and 'Skills' section of the resume to 
        match the job description keywords. Keep it truthful but optimized.
        Return ONLY the new resume text.
        """
        response = await self.llm.ainvoke(prompt)
        return response.content