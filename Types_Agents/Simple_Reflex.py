"""
Simple Reflex Agent Implementation - Vacuum Cleaner Example

This module demonstrates a basic AI agent architecture following the Simple Reflex Agent model.
A Simple Reflex Agent acts based solely on the current percept (what it senses right now),
without considering the history of percepts or maintaining internal state about the world.

The vacuum cleaner operates in a two-room environment (A and B) and follows simple rules:
- If the current location is dirty, clean it
- If the current location is clean, move to the other room
"""

class SimpleReflexVacuumAgent:  
    """
    A Simple Reflex Agent that cleans a two-room environment.
    
    This agent demonstrates the basic agent architecture:
    - Sensors: Perceive current location and dirt status
    - Actuators: Can suck dirt or move between rooms
    - Agent function: Maps percepts directly to actions without memory
    """
    
    def __init__(self):  
        """
        Initialize the vacuum agent.
        
        The agent starts in location A and maintains a list of actions
        taken for performance measurement and debugging purposes.
        """
        self.location = "A"  # Starting position
        self.actions = []    # History of actions taken (for analysis)
    
    def perceive_and_act(self, current_location, is_dirty):  
        """
        The agent function: maps percepts to actions.
        
        This is the core of the Simple Reflex Agent - it takes the current
        percept (location and dirt status) and immediately decides what action
        to take based on simple condition-action rules.
        
        Args:
            current_location (str): Current room ("A" or "B")
            is_dirty (bool): Whether the current location has dirt
        
        Agent Rules:
        1. If current location is dirty → Suck
        2. If current location is clean and in room A → Move to room B
        3. If current location is clean and in room B → Move to room A
        """
        if is_dirty:  
            # Rule 1: Clean dirty locations immediately
            self.actions.append("Suck")  
            print(f"Cleaned {current_location}")  
        else:  
            # Rule 2 & 3: Move to the other room when current room is clean
            if current_location == "A":  
                self.actions.append("MoveRight")  
                self.location = "B"  
            else:  
                self.actions.append("MoveLeft")  
                self.location = "A"  
            print(f"Moved to {self.location}")  

# Execution and Testing
print("=== Simple Reflex Vacuum Agent Simulation ===\n")

# Create the agent instance
agent = SimpleReflexVacuumAgent()  

# Define a sequence of percepts to test the agent
# Each tuple represents (location, is_dirty_status)
# This simulates the environment providing sensory input to the agent
percepts = [("A", True), ("A", False), ("B", True), ("B", False)]  

print("Starting simulation with percepts:", percepts)
print("Agent starting location:", agent.location)
print("\nAgent actions:")

# Simulate the agent responding to each percept
for i, (loc, dirt) in enumerate(percepts):  
    print(f"Step {i+1}: Percept = (Location: {loc}, Dirty: {dirt})")
    agent.perceive_and_act(loc, dirt)
    print()

# Display performance summary
print("=== Simulation Complete ===")
print(f"Total actions taken: {len(agent.actions)}")
print(f"Action sequence: {agent.actions}")
print(f"Final agent location: {agent.location}")