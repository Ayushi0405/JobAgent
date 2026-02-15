from typing import TypedDict, List, Annotated
import operator

class AgentState(TypedDict):
    job_url: str
    master_resume: str
    tailored_resume: str
    job_description: str
    form_status: str
    logs: Annotated[List[str], operator.add]
    screenshot: str