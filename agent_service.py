import os
import asyncio
from dotenv import load_dotenv
from pydantic import SecretStr

# Imports for the agent
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

# Load environment variables - needed for API keys etc. within the service
load_dotenv()

class AgentService:
    def __init__(self):
        # Initialize LLM and potentially other shared resources once
        # Or initialize them within the run method if they need to be fresh each time
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            # Handle missing API key appropriately - maybe raise an error
            # For now, we'll let the run method handle it, but initializing here is better
            print("Warning: GEMINI_API_KEY not found during AgentService initialization.")
            self.g_llm = None
        else:
             self.g_llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash', # Or choose another compatible model
                api_key=SecretStr(api_key),
            )
        # Pre-load sensitive data if it's static
        email = os.getenv('MY_NAME') or ""
        my_pass = os.getenv('MY_PASS') or ""
        self.sensitive_data = {'x_email': email, 'x_password': my_pass}


    async def run(self, task_text: str):
        """
        Sets up and runs the agent for the given task.
        """
        if not self.g_llm:
             # If LLM wasn't initialized due to missing key, raise error here
             raise ValueError("AgentService cannot run: GEMINI_API_KEY is not configured.")

        # Define initial actions if needed, or leave empty if task starts from blank slate
        initial_actions = [
            {'open_tab': {'url': 'https://www.google.com'}}, # Example: start at Google
        ]

        # Initialize Browser components for this run
        # Consider if browser/context should be reused across runs for performance
        browser = Browser(config=BrowserConfig(new_context_config=BrowserContextConfig(viewport_expansion=0)))
        browser_context = BrowserContext(
             config=BrowserContextConfig(
                  browser_window_size={'width': 1280, 'height': 1200},
                  locale='en-US',
             ),
             browser=browser
        )
        controller = Controller()

        # Initialize the Agent for this specific task
        agent = Agent(
            task=task_text, # Use the task passed as argument
            llm=self.g_llm,
            sensitive_data=self.sensitive_data,
            initial_actions=initial_actions,
            controller=controller,
            max_actions_per_step=5,
            use_vision=True,
            browser_context=browser_context,
            save_conversation_path=None # Disable saving logs for API endpoint
            # tool_calling_method="json_mode", # Optional: specify if needed
        )

        # --- Run the Agent ---
        # Note: agent.run() is async and might take time
        history = await agent.run()
        result = history.final_result() # Assuming final_result() gives the desired output

        # Close browser context after task completion
        await browser_context.close()

        return result # Return the final result