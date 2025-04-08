from browser_use import SystemPrompt
from typing import TypedDict
import random
import string


class RoleDetails(TypedDict):
    name: str
    description: str


def generate_random_string(length=5):
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def GenerateRoleDetails() -> RoleDetails:
    """Generate role details with a random suffix."""
    suffix = generate_random_string()
    return {
        "name": f'test_{suffix}',
        "description": f'test_desc_{suffix}'
    }


class MySystemPrompt(SystemPrompt):
    def important_rules(self) -> str:
        existing_rules = super().important_rules()
        # Add your custom rules
        new_rules = """MOST IMPORTANT RULE:If only one filed is displayed then only email if 2 input fields is displayed then to is email and second is password. Alwasy close popups"""

        # Make sure to use this pattern otherwise the exiting rules will be lost
        return f'{existing_rules}\n{new_rules}'