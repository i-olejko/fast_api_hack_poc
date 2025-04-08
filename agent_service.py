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

        # Set up recording configuration
        self.recordings_dir = os.path.join(os.getcwd(), 'recordings')
        os.makedirs(self.recordings_dir, exist_ok=True)

    async def run(self, task_text: str):
        """
        Sets up and runs the agent for the given task.
        """
        if not self.g_llm:
             # If LLM wasn't initialized due to missing key, raise error here
             raise ValueError("AgentService cannot run: GEMINI_API_KEY is not configured.")

        # Initialize Browser components for this run
        # Consider if browser/context should be reused across runs for performance
        browser = Browser(config=BrowserConfig(new_context_config=BrowserContextConfig(viewport_expansion=0)))
        
        # Create a unique recording path for this session
        session_id = asyncio.current_task().get_name()
        recording_path = os.path.join(self.recordings_dir, f'session_{session_id}')
        os.makedirs(recording_path, exist_ok=True)

        browser_context = BrowserContext(
             config=BrowserContextConfig(
                  browser_window_size={'width': 1920, 'height': 1080},  # HD resolution
                  locale='en-US',
                  save_recording_path=recording_path  # Enable video recording
             ),
             browser=browser
        )
        controller = Controller()

        # Initialize the Agent for this specific task
        agent = Agent(
            task=task_text, # Use the task passed as argument
            llm=self.g_llm,
            sensitive_data=self.sensitive_data,
            initial_actions=[{'go_to_url': {'url': 'https://www.google.com'}}],  # Use goto_url to navigate in the current tab
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

    async def run_console(self, strTask: str, strFollowUpTask: str):
        """
        Placeholder method for running a console-based task.
        Currently returns a mock dictionary.
        """
        # TODO: Implement actual logic for console task execution
        print(f"Received console task: {strTask}")
        print(f"Received follow-up task: {strFollowUpTask}")

        # Return the specified mock dictionary
        return {
            "createdName": "mock_created_name",
            "createdDesc": "mock_created_description",
            "foundName": "mock_found_name",
            "fondDesc": "mock_found_description" # Using 'fondDesc' as requested
        }