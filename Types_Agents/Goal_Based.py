"""
Goal-Based Agent Implementation - Path Planning Example

This module demonstrates a Goal-Based Agent that makes decisions based on desired
future states (goals). Key characteristics of Goal-Based Agents:

- Goal-Oriented: Actions are chosen to achieve specific target states
- Forward Planning: Considers future consequences of current actions
- Search-Based: Uses algorithms to find sequences of actions leading to goals
- Flexible: Can adapt behavior when goals change or obstacles appear

This example shows a simplified navigation agent that plans paths to reach
target locations using basic pathfinding logic.
"""

class GoalBasedAgent:  
    """
    A Goal-Based Agent that plans actions to achieve target states.
    
    This agent demonstrates core Goal-Based Agent capabilities:
    - Goal Representation: Maintains explicit target states
    - Path Planning: Calculates action sequences to reach goals
    - Progress Tracking: Monitors advancement toward goal achievement
    - Adaptive Behavior: Can handle changing goals and obstacles
    """
    
    def __init__(self, target_goal):  
        """
        Initialize the goal-based agent with a specific target.
        
        Args:
            target_goal: The desired state/position the agent wants to reach
        """
        self.goal = target_goal          # Target state to achieve
        self.actions = []                # History of actions taken
        self.current_plan = []           # Current sequence of planned actions
        
        print(f"Goal-Based Agent initialized with target goal: {self.goal}")
        print("Agent will plan actions to achieve this goal state")
    
    def set_new_goal(self, new_target):
        """
        Update the agent's goal and reset planning.
        
        This demonstrates the flexibility of Goal-Based Agents to adapt
        when objectives change.
        
        Args:
            new_target: The new goal state to pursue
        """
        print(f"Goal changed from {self.goal} to {new_target}")
        self.goal = new_target
        self.current_plan = []  # Reset plan for new goal
        self.actions.append(f"Goal_Change_To_{new_target}")
    
    def path_planning(self, current_state, obstacles=None):  
        """
        Core planning algorithm - determines actions needed to reach the goal.
        
        This method implements simplified A* pathfinding logic, demonstrating
        how Goal-Based Agents use search algorithms to find optimal action sequences.
        
        Args:
            current_state: Agent's current position/state
            obstacles (list, optional): List of blocked positions to avoid
            
        Returns:
            str: The recommended action or status message
        """
        if obstacles is None:
            obstacles = []
            
        print(f"\n🎯 Planning path from {current_state} to goal {self.goal}")
        print(f"   Obstacles to avoid: {obstacles if obstacles else 'None'}")
        
        # Goal achievement check
        if current_state == self.goal:  
            print("✅ Goal achieved! No further action needed.")
            self.actions.append("Goal_Achieved")
            return "Goal achieved"  
        
        # Obstacle avoidance logic
        if current_state in obstacles:
            print("⚠️  Current position is blocked - replanning required")
            self.actions.append("Avoid_Obstacle")
            return "Replan to avoid obstacle"
        
        # Simple heuristic-based pathfinding
        distance_to_goal = abs(current_state - self.goal)
        print(f"   Distance to goal: {distance_to_goal}")
        
        # Determine optimal direction
        if current_state < self.goal:  
            # Need to move forward/increase position
            next_position = current_state + 1
            if next_position in obstacles:
                print("   Direct path blocked - considering alternative route")
                self.actions.append("Path_Blocked")
                return "Find alternative path"
            else:
                print(f"   Optimal action: Move forward to {next_position}")
                self.actions.append("Move_Forward")
                return "Move closer"  
        else:  
            # Need to move backward/decrease position
            next_position = current_state - 1
            if next_position in obstacles:
                print("   Direct path blocked - considering alternative route")
                self.actions.append("Path_Blocked")
                return "Find alternative path"
            else:
                print(f"   Optimal action: Move backward to {next_position}")
                self.actions.append("Move_Backward")
                return "Adjust path"
    
    def execute_plan(self, start_state, obstacles=None):
        """
        Execute a complete plan from start state to goal.
        
        This demonstrates how Goal-Based Agents can execute multi-step plans
        to achieve their objectives.
        
        Args:
            start_state: Starting position
            obstacles (list, optional): Positions to avoid
        """
        current_state = start_state
        max_steps = 20  # Prevent infinite loops
        step_count = 0
        
        print(f"\n🚀 Executing complete plan from {start_state} to {self.goal}")
        
        while current_state != self.goal and step_count < max_steps:
            step_count += 1
            print(f"\nStep {step_count}: Current position = {current_state}")
            
            action = self.path_planning(current_state, obstacles)
            
            if action == "Goal achieved":
                break
            elif action == "Move closer":
                current_state += 1
            elif action == "Adjust path":
                current_state -= 1
            elif "alternative path" in action or "obstacle" in action:
                print("   Planning alternative route...")
                # Simple obstacle avoidance - try different direction
                if current_state < self.goal:
                    current_state += 2  # Jump over obstacle
                else:
                    current_state -= 2
            
            print(f"   New position: {current_state}")
        
        if current_state == self.goal:
            print(f"\n🎉 SUCCESS: Goal {self.goal} reached in {step_count} steps!")
        else:
            print(f"\n⚠️  Plan execution stopped after {max_steps} steps")
        
        return current_state

# Demonstration and Testing
print("=== Goal-Based Agent Simulation ===")
print("Navigation and Path Planning Demo")
print("-" * 40)

# Test 1: Basic goal achievement
print("\n📋 TEST 1: Basic Navigation")
agent = GoalBasedAgent(100)  
result1 = agent.path_planning(75)  
print(f"Planning result: {result1}")

print("\n" + "="*50)

# Test 2: Goal already achieved
print("\n📋 TEST 2: Already at Goal")
result2 = agent.path_planning(100)
print(f"Planning result: {result2}")

print("\n" + "="*50)

# Test 3: Navigation with obstacles
print("\n📋 TEST 3: Obstacle Avoidance")
obstacles = [85, 90, 95]
result3 = agent.path_planning(80, obstacles)
print(f"Planning result: {result3}")

print("\n" + "="*50)

# Test 4: Complete plan execution
print("\n📋 TEST 4: Complete Plan Execution")
agent2 = GoalBasedAgent(50)
final_position = agent2.execute_plan(45, obstacles=[47, 48])

print("\n" + "="*50)

# Test 5: Goal change demonstration
print("\n📋 TEST 5: Dynamic Goal Change")
agent2.set_new_goal(30)
agent2.path_planning(final_position)

print(f"\nAgent action history: {agent.actions}")
print(f"Agent2 action history: {agent2.actions}")

print("\n=== Goal-Based Agent Key Features ===")
print("🎯 Goal-oriented decision making")
print("🗺️  Path planning and search algorithms") 
print("🔄 Adaptive behavior when goals change")
print("🚧 Obstacle avoidance and replanning")
print("📈 Progress tracking toward objectives")
print("⚡ Optimal action selection based on goal distance")