import os

class Config:
    def __init__(self):
        self.env_variables = {}
        self.load_env_variables()

    def load_env_variables(self):
        if os.path.exists('.env2'):
            with open('.env2', 'r', encoding='utf-8') as env_file:
                content = env_file.read()
                prompts = content.split('<<<PROMPT_DELIMITER>>>')
                for prompt in prompts:
                    if '=' in prompt:
                        key, value = prompt.split('=', 1)
                        self.env_variables[key.strip()] = value.strip()
        else:
            print("Warning: .env2 file not found.")

    def get_prompt(self, key: str) -> str:
        return self.env_variables.get(key, f"Prompt for {key} not found")