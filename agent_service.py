import os
import asyncio
from dotenv import load_dotenv
from pydantic import SecretStr
from datetime import datetime
import json

# Imports for the agent
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from my_system_prompt import MySystemPrompt, GenerateRoleDetails
from output_result import TableExtruction

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
        self.th_llm = ChatGoogleGenerativeAI(
            model='gemini-2.5-pro-preview-03-25',
            api_key=SecretStr(api_key),
        )
        email = os.getenv('MY_NAME') or ""
        my_pass = os.getenv('MY_PASS') or ""
        self.email = email        
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
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        recording_path = os.path.join(self.recordings_dir, f'{timestamp}')
        os.makedirs(recording_path, exist_ok=True)

        # Initialize metadata
        metadata = {
            "directory": recording_path,
            "recording_path": os.path.join(recording_path, "session.webm"),
            "metadata_path": os.path.join(recording_path, "metadata.json"),
            "start_time": datetime.now().isoformat(),
            "task": task_text
        }

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
        )

        # --- Run the Agent ---
        # Note: agent.run() is async and might take time
        history = await agent.run()
        result = history.final_result() # Assuming final_result() gives the desired output

        # Update metadata with end time, result, and URLs
        metadata["end_time"] = datetime.now().isoformat()
        metadata["result"] = str(result)
        metadata["urls"] = history.urls()
        metadata["errors"] = history.errors()
        metadata["action_names"] = history.action_names()
        # Save metadata
        with open(metadata["metadata_path"], 'w') as f:
            json.dump(metadata, f, indent=2)

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

        # Create a unique recording path for this session
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        recording_path = os.path.join(self.recordings_dir, f'{timestamp}')
        os.makedirs(recording_path, exist_ok=True)

        # Initialize metadata
        metadata = {
            "directory": recording_path,
            "recording_path": os.path.join(recording_path, "session.webm"),
            "metadata_path": os.path.join(recording_path, "metadata.json"),
            "start_time": datetime.now().isoformat(),
            "task": strTask
        }  

        # Store the generated details for later comparison
        generated_details = GenerateRoleDetails()

        retVal = {
            "createdName": generated_details["name"],
            "createdDesc": generated_details["description"],
            "foundName": "",
            "foundDesc": ""
        }

        fragmets = []        
        fragmets.append("NOTICE: Use the name and description provided below instead of generating new ones.")
        fragmets.append(
            f"Use the name: {generated_details["name"]} and description: {generated_details["description"]}."
        )
        fragmets.append('IMPORTANT LOGIN instruction: always email and password from sensitive data (secret)')
        # fragmets.append("IMPORTANT LOGIN instruction: First you provide login email (usually element with index 0) then click on the 'Next' button (usually element with index 1) and then provide password and only then click 'login' button.")
        #update strTask
        updatedTask = f"{strTask}\n {' \n'.join(fragmets)}"

        initial_actions = [
            {'open_tab': {'url': 'https://dev5.proofpointisolation.com/console'}},
            {'input_text': {'index': 0, 'text': self.email}},
        ]

        # Initialize Browser components for this run
        # Consider if browser/context should be reused across runs for performance
        browser = Browser(config=BrowserConfig(new_context_config=BrowserContextConfig(viewport_expansion=0)))
        browser_context = BrowserContext(
             config=BrowserContextConfig(
                  browser_window_size={'width': 1280, 'height': 1200},
                  locale='en-US',
                  save_recording_path=recording_path  # Enable video recording
             ),
             browser=browser
        )
        controller = Controller(output_model=TableExtruction)
        # Initialize the Agent for this specific task
        agent = Agent(
            task=updatedTask, # Use the task passed as argument
            llm=self.g_llm,
            sensitive_data=self.sensitive_data,
            initial_actions=initial_actions,
            controller=controller,
            max_actions_per_step=5,
            use_vision=True,
            browser_context=browser_context,
            save_conversation_path=None, # Disable saving logs for API endpoint
            planner_llm=self.th_llm,
            use_vision_for_planner=True,
            planner_interval=4,
            # tool_calling_method="json_mode", # Optional: specify if needed
        )

        await agent.run()
        agent.add_new_task(strFollowUpTask)
        agent.initial_actions = []
        history = await agent.run()
        result = history.final_result()       

        if result: 
            parsed = TableExtruction.model_validate_json(result)
            retVal["foundName"] = parsed.first_extracted_role_name
            retVal["foundDesc"] = parsed.first_extracted_role_description

        print(retVal)

        # Update metadata with end time, result, and URLs
        metadata["end_time"] = datetime.now().isoformat()
        metadata["result"] = str(result)
        metadata["urls"] = history.urls()
        metadata["errors"] = history.errors()
        metadata["action_names"] = history.action_names()
        # Save metadata
        with open(metadata["metadata_path"], 'w') as f:
            json.dump(metadata, f, indent=2)

        await browser_context.close()
        # Return the specified mock dictionary
        return retVal