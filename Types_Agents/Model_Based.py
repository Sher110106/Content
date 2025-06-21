"""
Model-Based Agent Implementation - Vacuum Cleaner Example

This module demonstrates a Model-Based Agent that maintains an internal representation
of the world state. Unlike Simple Reflex Agents, Model-Based Agents:
- Keep track of the world state even when not directly perceiving it
- Make decisions based on their internal model of the environment
- Can handle partially observable environments more effectively

The vacuum agent maintains a model of which rooms are clean/dirty and can
make intelligent decisions like shutting down when all rooms are clean.
"""

class ModelBasedVacuumAgent:  
    """
    A Model-Based Agent that maintains an internal world model.
    
    This agent demonstrates key Model-Based Agent characteristics:
    - Internal State: Tracks the cleanliness status of all rooms
    - World Model: Maintains beliefs about unobserved locations
    - Intelligent Decision Making: Can decide to shutdown when task is complete
    """
    
    def __init__(self):  
        """
        Initialize the model-based vacuum agent.
        
        The agent starts with an unknown model of the world and builds
        knowledge through perception and action.
        """
        # Internal world model: tracks the state of each room
        # "Unknown" = haven't visited yet, "Clean" = verified clean, "Dirty" = needs cleaning
        self.model = {"A": "Unknown", "B": "Unknown"}  
        self.location = "A"  # Current agent location

    def update_model(self, loc, is_clean):  
        """
        Update the internal world model based on current perception.
        
        This is a key capability of Model-Based Agents - they update their
        internal representation of the world based on sensory input.
        
        Args:
            loc (str): The location being observed ("A" or "B")
            is_clean (bool): Whether the location is currently clean (True) or dirty (False)
        """
        # Update our belief about this location's state
        self.model[loc] = "Clean" if is_clean else "Dirty"  
        print(f"Model updated: Room {loc} is {'Clean' if is_clean else 'Dirty'}")
        print(f"Current world model: {self.model}")

    def decide_action(self, current_loc, is_dirty):  
        """
        Make intelligent decisions based on current perception and world model.
        
        This method showcases the Model-Based Agent's ability to:
        1. Update its world model with new information
        2. Reason about the complete state of the environment
        3. Make optimal decisions (like shutdown when task is complete)
        
        Args:
            current_loc (str): Current location ("A" or "B")
            is_dirty (bool): Whether current location has dirt
            
        Returns:
            str: The action to take ("Suck", "MoveRight", "MoveLeft", or "Shutdown")
        """
        # First, update our model with current observation
        self.update_model(current_loc, not is_dirty)  # not is_dirty = is_clean
        
        # Decision logic based on current state and world model
        if is_dirty:  
            # Rule 1: Clean dirty locations immediately
            print(f"Action: Cleaning dirt at location {current_loc}")
            return "Suck"  
        elif self.model["A"] == "Clean" and self.model["B"] == "Clean":  
            # Rule 2: Shutdown when all known areas are clean (task complete)
            print("Action: All areas clean - shutting down efficiently")
            return "Shutdown"  
        else:  
            # Rule 3: Move to explore/clean other areas
            next_action = "MoveRight" if current_loc == "A" else "MoveLeft"
            next_location = "B" if current_loc == "A" else "A"
            print(f"Action: Moving to {next_location} to continue cleaning")
            return next_action

# Demonstration and Testing
print("=== Model-Based Vacuum Agent Simulation ===\n")

# Create the agent instance
agent = ModelBasedVacuumAgent()  
print("Agent initialized with world model:", agent.model)
print("Starting location:", agent.location)
print()

# Test scenario: Clean room A, then check room B
print("Scenario 1: Room A is dirty")
action1 = agent.decide_action("A", True)  # Room A is dirty
print(f"Decision: {action1}\n")

print("Scenario 2: Room A is now clean")
action2 = agent.decide_action("A", False)  # Room A is now clean
print(f"Decision: {action2}\n")

print("Scenario 3: Room B is clean too")
action3 = agent.decide_action("B", False)  # Room B is also clean
print(f"Decision: {action3}\n")

print("=== Key Model-Based Agent Advantages Demonstrated ===")
print("1. Maintains memory of world state across time")
print("2. Makes intelligent shutdown decision when task is complete")
print("3. Can reason about unobserved locations using internal model")
print(f"Final world model: {agent.model}")