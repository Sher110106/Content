from Step2 import OllamaModel
from Step3 import basic_calculator, reverse_string
from Step4 import Agent

if __name__ == "__main__":
  """
    Instructions for using this agent:
    
    Example queries you can try:
    1. Calculator operations:
       - "Calculate 15 plus 7"
       - "What is 100 divided by 5?"
       - "Multiply 23 and 4"
    
    2. String reversal:
       - "Reverse the word 'hello world'"
       - "Can you reverse 'Python Programming'?"
    
    3. General questions (will get direct responses):
       - "Who are you?"
       - "What can you help me with?"
    
    Ollama Commands (run these in terminal):
    - Check available models:    'ollama list'
    - Check running models:      'ps aux | grep ollama'
    - List model tags:          'curl http://localhost:11434/api/tags'
    - Pull a new model:         'ollama pull mistral'
    - Run model server:         'ollama serve'
    """
tools = [basic_calculator, reverse_string]

# Using Ollama with llama2 model
model_service = OllamaModel
model_name = "llama3"  # Can be changed to other models like 'mistral', 'codellama'
stop = ["\n"]

agent = Agent(
    tools=tools,
    model_service=model_service,
    model_name=model_name,
    stop=stop,
)

print("Welcome to the AI Agent! Type 'exit' to quit.")
while True:
    prompt = input("Ask me anything: ")
    if prompt.lower() == "exit":
        break
    agent_work_response = agent.work(prompt)
    print(agent_work_response)