from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
import os

class BrowserManager:
    def __init__(self):
        # Persistent storage for cookies/login sessions
        self.chrome_path = os.path.abspath("./chrome_data")
        os.makedirs(self.chrome_path, exist_ok=True)

    def create_browser(self):
        """Creates a browser instance that REMEMBERS logins."""
        return Browser(
            config=BrowserConfig(
                headless=False,  # Visible for 'Stealth' mode
                user_data_dir=self.chrome_path
            )
        )

    async def run_task(self, task: str, llm):
        """Helper to run a quick browser task."""
        agent = Agent(task=task, llm=llm, browser=self.create_browser())
        return await agent.run()