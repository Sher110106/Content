from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()


class OllamaModel:
    def __init__(
        self, model, system_prompt, temperature=0, stop=None
    ):
        """Initializes the OllamaModel with the given parameters."""
        self.model_endpoint = "http://localhost:11434/api/generate"
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.stop = stop
        self.headers = {"Content-Type": "application/json"}

    def generate_text(self, prompt):
        """Generates a response from the Ollama model based on the provided prompt."""
        try:
            payload = {
                "model": self.model,
                "format": "json",
                "prompt": prompt,
                "system": self.system_prompt,
                "stream": False,
                "temperature": self.temperature,
                "stop": self.stop,
            }
            request_response = requests.post(
                self.model_endpoint,
                headers=self.headers,
                data=json.dumps(payload),
            )
            request_response_json = request_response.json()
            response = request_response_json["response"]
            response_dict = json.loads(response)
            return response_dict
        except requests.RequestException as e:
            response = {"error": f"Error in invoking model: {str(e)}"}
            return response