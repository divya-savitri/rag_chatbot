import os
import requests
from dotenv import load_dotenv


class MistralLLM:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("MISTRAL_API_KEY")

        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in .env")

        self.url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-small-latest"

    def invoke(self, prompt):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post(self.url, headers=headers, json=payload)

        result = response.json()

        class LLMResponse:
            content = result["choices"][0]["message"]["content"]

        return LLMResponse()


def get_llm():
    return MistralLLM()