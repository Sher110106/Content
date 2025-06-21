agent_system_prompt_template = """
You are an intelligent AI assistant with access to specific tools. Your responses must be in valid JSON format.

Based on the user's request, you must decide which tool to use from the available list.
Your response should be a JSON object with two keys:
- "tool_choice": The name of the tool to use, or "no tool" if none are suitable.
- "tool_input": The input to be passed to the chosen tool.

TOOLS AND WHEN TO USE THEM:
1. basic_calculator: use for ANY mathematical calculations
   - Input format: {{"num1": number, "num2": number, "operation": "add/subtract/multiply/divide"}}
   - Example Input: "what is 100 divided by 5?"
   - Output: {{"tool_choice": "basic_calculator", "tool_input": {{"num1": 100, "num2": 5, "operation": "divide"}}}}

2. reverse_string: use for ANY request involving reversing text
   - Input format: Just the text to be reversed as a string
   - Example Input: "Reverse 'Hooooow'"
   - Output: {{"tool_choice": "reverse_string", "tool_input": "Hooooow"}}

3. no tool: use for general conversation and questions
   - Example Input: "How are you?"
   - Output: {{"tool_choice": "no tool", "tool_input": "I'm functioning well, thank you"}}

STRICT RULES:
- Always respond with valid JSON format
- Choose the most appropriate tool based on the user's request
- If no tool is suitable, use "no tool" and provide a helpful response
- Extract numbers and operations accurately from natural language

Here is a list of your tools along with their descriptions:
{tool_descriptions}

Remember: Your response must ALWAYS be valid JSON with "tool_choice" and "tool_input" keys.
"""
class ToolBox:
    def __init__(self):
        self._tools = []

    def store(self, tools):
        self._tools = tools

    def tools(self):
        descriptions = []
        for tool in self._tools:
            if tool.__doc__:
                descriptions.append(f"- {tool.__name__}: {tool.__doc__.strip()}")
            else:
                descriptions.append(f"- {tool.__name__}: No documentation available.")
        return "\n".join(descriptions)


class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        """Initializes the agent with a list of tools and a model."""
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop

    def prepare_tools(self):
        """Stores the tools in the toolbox and returns their descriptions."""
        toolbox = ToolBox()
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions

    def think(self, prompt):
        """Runs the generate_text method on the model using the system prompt template and user prompt."""
        tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(
            tool_descriptions=tool_descriptions
        )
        # Create an instance of the model service with the system prompt
        model_instance = self.model_service(
            model=self.model_name,
            system_prompt=agent_system_prompt,
            temperature=0,
            stop=self.stop,
        )
        # Generate and return the response dictionary
        agent_response_dict = model_instance.generate_text(prompt)
        return agent_response_dict

    def work(self, prompt):
        """Parses the dictionary returned from think and executes the appropriate tool."""
        agent_response_dict = self.think(prompt)
        if agent_response_dict and "error" not in agent_response_dict:
            tool_choice = agent_response_dict.get("tool_choice")
            tool_input = agent_response_dict.get("tool_input")

            for tool in self.tools:
                if tool.__name__ == tool_choice:
                    response = tool(tool_input)
                    return response
            return tool_input
        return "Error processing request"