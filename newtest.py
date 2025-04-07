import os
import asyncio
from browser_use import Agent
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from pydantic import SecretStr
from browser_use.controller.service import Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext, BrowserContextConfig

load_dotenv()
# gemma3:4b/not support tools  
# mistral:latest  
# granite3.2-vision:latest // stuck at thinking
# phi4-mini:latest  
# llama3.2:latest /not enaugh memory
# qwen2.5:14b // working with tool_calling_method="raw"

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')
# gemma-3-27b-it
# gemini-2.0-flash-lite
g_llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash', 
    api_key=SecretStr(api_key),   
)

th_llm = ChatAnthropic(model_name='claude-3-7-sonnet-20250219', temperature=0.0, timeout=30, stop=None)


o_llama = ChatOllama(
    model="gemma3:4b",
    num_ctx=32000,
)
# get neme or empty
email = os.getenv('MY_NAME') or ""
my_pass = os.getenv('MY_PASS') or ""

sensitive_data = {'x_email': email, 'x_password': my_pass}

initial_actions = [
	{'open_tab': {'url': 'https://dev5.proofpointisolation.com/console'}},
]

task=(
    '* Try to login with company email: x_email and password: x_password'  
    '* Navigate to the Browsing Roles by using nav bar on the left'
    '* Open a new role modal by clicking on the New Role button'
    '* Fill in the role name and description with random chars prefixed with "test_"'
    '* Select "VIP" option from the "User Groups" dropdown'
    '* Close the "User Groups" dropdown list by clicking on open/close caret'
    '* Click on the "Save" button in the top right cornder of the modal'
    # '* validate that the role was created successfully in the table of roles'
)

follow_up_task = (
    '* Click on the Browsing Roles nav item from nav bar on the left'
    '* get the first role name from the table of roles'
    'Call done'
)

create_role_task = (	
    
)

agent = Agent(
    task=task,
    llm=o_llama,
    sensitive_data=sensitive_data,
    initial_actions=initial_actions,
    max_actions_per_step=4,  
    tool_calling_method="json_mode", #'function_calling', 'json_mode', 'raw', 'auto'
    use_vision=False, 
)

#------------------------------------



browser = Browser(
	config=BrowserConfig(
		new_context_config=BrowserContextConfig(
			viewport_expansion=0,
		)
	)
)

browser_context = BrowserContext(
     config=BrowserContextConfig(
          browser_window_size={'width': 1280, 'height': 1200},
          locale='en-US',
     ),
     browser=browser
)
controller = Controller()
g_agent = Agent(
    task=task,
    llm=g_llm,
    # planner_llm=g_llm,
    # use_vision_for_planner=True,
    sensitive_data=sensitive_data,
    initial_actions=initial_actions,
    controller=controller,
    max_actions_per_step=5,
    use_vision=True,
    browser_context=browser_context,
    save_conversation_path="logs/conversation"  # Save chat logs
)

async def main():
    await g_agent.run()

    g_agent.add_new_task(follow_up_task)
    history = await g_agent.run()
    result = history.final_result()

    print("Result of the follow-up task:", result)
    
    input("Press Enter to close the browser...")

if __name__ == '__main__':
    asyncio.run(main())