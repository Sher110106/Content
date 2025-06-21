"""
Utility-Based Agent Implementation - Decision Making Example

This module demonstrates a Utility-Based Agent that makes decisions by evaluating
the expected utility (desirability) of different actions. Key characteristics:

- Multi-Criteria Decision Making: Considers multiple factors simultaneously
- Quantitative Evaluation: Uses mathematical functions to score options
- Optimal Selection: Chooses actions that maximize expected utility
- Trade-off Analysis: Balances competing objectives (cost vs. time vs. risk)

This example shows a decision-making agent that evaluates business actions
based on cost, time, and risk factors to find the optimal choice.
"""

def utility_function(cost, time, risk):  
    """
    Calculate the utility (desirability) of an action based on multiple criteria.
    
    This is the core of Utility-Based Agent decision making - a mathematical
    function that converts multiple factors into a single comparable score.
    
    The utility function demonstrates how agents can:
    - Weight different criteria according to their importance
    - Handle trade-offs between competing objectives
    - Provide quantitative basis for decision making
    
    Args:
        cost (float): Financial cost of the action (lower is better)
        time (float): Time required to complete action (lower is better)  
        risk (float): Risk level of the action (lower is better, 0-1 scale)
        
    Returns:
        float: Utility score (higher values indicate more desirable actions)
        
    Utility Formula Breakdown:
    - Cost component (50% weight): 1/cost (inverse relationship - lower cost = higher utility)
    - Time component (30% weight): 1/time (inverse relationship - less time = higher utility)  
    - Risk component (20% weight): -risk (negative relationship - lower risk = higher utility)
    """
    # Weighted utility calculation
    cost_utility = 0.5 * (1/cost)      # 50% weight - favor lower costs
    time_utility = 0.3 * (1/time)      # 30% weight - favor faster completion
    risk_penalty = 0.2 * risk          # 20% weight - penalize higher risk
    
    total_utility = cost_utility + time_utility - risk_penalty
    
    # Debug information for transparency
    print(f"   Utility breakdown:")
    print(f"     Cost factor ({cost}): {cost_utility:.4f}")
    print(f"     Time factor ({time}): {time_utility:.4f}")  
    print(f"     Risk penalty ({risk}): -{risk_penalty:.4f}")
    print(f"     Total utility: {total_utility:.4f}")
    
    return total_utility

class UtilityBasedAgent:
    """
    An agent that makes decisions by maximizing expected utility.
    
    This agent demonstrates how Utility-Based Agents:
    - Evaluate multiple action alternatives
    - Use quantitative methods for decision making
    - Handle complex trade-offs between competing objectives
    - Provide transparent, explainable decision rationale
    """
    
    def __init__(self, name="UtilityAgent"):
        """
        Initialize the utility-based decision agent.
        
        Args:
            name (str): Identifier for this agent instance
        """
        self.name = name
        self.decision_history = []
        print(f"Utility-Based Agent '{self.name}' initialized")
        print("Ready to evaluate actions based on cost, time, and risk factors")
    
    def evaluate_actions(self, actions):
        """
        Evaluate a set of possible actions and select the optimal one.
        
        This method demonstrates the core Utility-Based Agent process:
        1. Calculate utility for each possible action
        2. Compare utilities to find the maximum
        3. Select and return the action with highest utility
        4. Provide transparent reasoning for the decision
        
        Args:
            actions (list): List of action dictionaries, each containing:
                          'cost', 'time', 'risk', and optional 'name' keys
                          
        Returns:
            dict: The action with the highest utility score
        """
        print(f"\n🤔 {self.name} evaluating {len(actions)} possible actions...")
        print("-" * 50)
        
        action_utilities = []
        
        # Calculate utility for each action
        for i, action in enumerate(actions):
            action_name = action.get('name', f'Action {i+1}')
            print(f"\n📊 Evaluating {action_name}:")
            print(f"   Cost: ${action['cost']}, Time: {action['time']} hours, Risk: {action['risk']}")
            
            utility_score = utility_function(action['cost'], action['time'], action['risk'])
            
            # Store action with its utility score
            action_with_utility = action.copy()
            action_with_utility['utility'] = utility_score
            action_with_utility['name'] = action_name
            action_utilities.append(action_with_utility)
        
        # Find the action with maximum utility
        best_action = max(action_utilities, key=lambda x: x['utility'])
        
        print(f"\n🏆 DECISION RESULT:")
        print(f"   Optimal choice: {best_action['name']}")
        print(f"   Utility score: {best_action['utility']:.4f}")
        print(f"   Rationale: Highest utility among all evaluated options")
        
        # Record decision for history tracking
        decision_record = {
            'chosen_action': best_action,
            'alternatives_considered': len(actions),
            'utility_scores': [a['utility'] for a in action_utilities]
        }
        self.decision_history.append(decision_record)
        
        return best_action
    
    def compare_actions(self, action1, action2):
        """
        Compare two specific actions and explain the preference.
        
        Args:
            action1, action2 (dict): Actions to compare
            
        Returns:
            dict: The preferred action with explanation
        """
        print(f"\n⚖️  {self.name} comparing two actions:")
        
        utility1 = utility_function(action1['cost'], action1['time'], action1['risk'])
        utility2 = utility_function(action2['cost'], action2['time'], action2['risk'])
        
        if utility1 > utility2:
            preferred = action1.copy()
            preferred['utility'] = utility1
            print(f"✅ Action 1 preferred (utility: {utility1:.4f} vs {utility2:.4f})")
        else:
            preferred = action2.copy()
            preferred['utility'] = utility2
            print(f"✅ Action 2 preferred (utility: {utility2:.4f} vs {utility1:.4f})")
            
        return preferred

# Demonstration and Testing
print("=== Utility-Based Agent Simulation ===")
print("Business Decision Making Example")
print("-" * 40)

# Create agent instance
agent = UtilityBasedAgent("BusinessDecisionAgent")

# Define business action alternatives
business_actions = [  
    {
        "name": "Budget Option",
        "cost": 200, 
        "time": 5, 
        "risk": 0.1,
        "description": "Low-cost, slower approach with minimal risk"
    },  
    {
        "name": "Premium Option", 
        "cost": 300, 
        "time": 3, 
        "risk": 0.2,
        "description": "Higher-cost, faster approach with moderate risk"
    },
    {
        "name": "Aggressive Option",
        "cost": 150,
        "time": 2,
        "risk": 0.4,
        "description": "Lowest-cost, fastest approach with high risk"
    }
]  

print("\n📋 SCENARIO: Choosing Business Strategy")
print("Available options:")
for action in business_actions:
    print(f"  • {action['name']}: {action['description']}")

# Agent evaluates all options
optimal_action = agent.evaluate_actions(business_actions)

print(f"\n" + "="*60)

# Test direct comparison
print("\n📋 SCENARIO: Direct Comparison")
print("Comparing Budget vs Premium options only...")
comparison_result = agent.compare_actions(business_actions[0], business_actions[1])

print(f"\n" + "="*60)

# Show decision history
print(f"\n📈 {agent.name} Decision History:")
for i, decision in enumerate(agent.decision_history):
    print(f"Decision {i+1}: {decision['chosen_action']['name']} "
          f"(utility: {decision['chosen_action']['utility']:.4f})")

print("\n=== Utility-Based Agent Advantages ===")
print("🎯 Quantitative decision making with clear rationale")
print("⚖️  Handles complex trade-offs between multiple criteria")
print("🔍 Transparent and explainable decision process")
print("📊 Consistent evaluation framework across different scenarios")
print("🎛️  Configurable weights allow customization for different priorities")
print("📈 Optimal selection based on mathematical optimization")

print(f"\n=== Utility Function Analysis ===")
print("Current weights: Cost (50%), Time (30%), Risk (20%)")
print("• Prioritizes cost-effectiveness over speed")
print("• Moderate consideration of time constraints") 
print("• Conservative approach to risk management")
print("• Weights can be adjusted based on business priorities")