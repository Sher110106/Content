"""
Learning Agent Implementation - Q-Learning Example

This module demonstrates a Learning Agent that improves its performance over time
through experience using Reinforcement Learning. Key characteristics:

- Adaptive Behavior: Performance improves through trial and error
- Experience-Based Learning: Uses past interactions to make better decisions
- Exploration vs Exploitation: Balances trying new actions vs using known good ones
- Temporal Learning: Updates knowledge based on delayed rewards and consequences

This example implements Q-Learning, a popular reinforcement learning algorithm
where the agent learns the quality (Q-value) of state-action pairs through experience.
"""

import numpy as np  

class QLearningAgent:  
    """
    A Learning Agent that uses Q-Learning to improve decision making over time.
    
    Q-Learning is a model-free reinforcement learning algorithm that learns
    the quality of actions, telling an agent what action to take under what
    circumstances without needing a model of the environment.
    
    Key Components:
    - Q-Table: Stores learned values for each state-action pair
    - Learning Rate (α): Controls how much new information overrides old
    - Discount Factor (γ): Determines importance of future rewards
    - Exploration Strategy: Balances exploration of new actions vs exploitation
    """
    
    def __init__(self, states, actions, alpha=0.1, gamma=0.9, epsilon=0.1):  
        """
        Initialize the Q-Learning agent with learning parameters.
        
        Args:
            states (int): Number of possible states in the environment
            actions (int): Number of possible actions the agent can take
            alpha (float): Learning rate (0-1), how much to update Q-values
            gamma (float): Discount factor (0-1), importance of future rewards
            epsilon (float): Exploration rate (0-1), probability of random action
        """
        # Q-Table: Matrix storing quality values for each state-action pair
        # Initially all zeros - agent starts with no knowledge
        self.q_table = np.zeros((states, actions))  
        
        # Learning parameters
        self.alpha = alpha      # Learning rate: how fast to update knowledge
        self.gamma = gamma      # Discount factor: value of future rewards
        self.epsilon = epsilon  # Exploration rate: chance of random action
        
        # Agent statistics for performance tracking
        self.states = states
        self.actions = actions
        self.learning_episodes = 0
        self.total_reward = 0
        
        print(f"Q-Learning Agent initialized:")
        print(f"  States: {states}, Actions: {actions}")
        print(f"  Learning rate (α): {alpha}")
        print(f"  Discount factor (γ): {gamma}")
        print(f"  Exploration rate (ε): {epsilon}")
        print(f"  Q-table shape: {self.q_table.shape}")
    
    def learn(self, state, action, reward, next_state):  
        """
        Update Q-values based on experience using the Q-Learning update rule.
        
        This is the core learning mechanism that implements the Q-Learning equation:
        Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        
        The agent learns by:
        1. Taking an action and observing the reward
        2. Estimating the future value of the next state
        3. Updating its knowledge based on the difference between expected and actual outcomes
        
        Args:
            state (int): Current state index
            action (int): Action taken index  
            reward (float): Immediate reward received
            next_state (int): Resulting state after action
        """
        print(f"\n📚 Learning from experience:")
        print(f"   State: {state} → Action: {action} → Reward: {reward} → Next State: {next_state}")
        
        # Current Q-value for this state-action pair
        current_q = self.q_table[state, action]
        print(f"   Current Q-value Q({state},{action}): {current_q:.4f}")
        
        # Find the maximum Q-value for the next state (best future action)
        max_future_q = np.max(self.q_table[next_state])
        print(f"   Best future Q-value Q({next_state},*): {max_future_q:.4f}")
        
        # Q-Learning update equation
        # New estimate = immediate reward + discounted future value
        target_value = reward + self.gamma * max_future_q
        print(f"   Target value: {reward} + {self.gamma} × {max_future_q:.4f} = {target_value:.4f}")
        
        # Blend old knowledge with new learning
        new_q = (1 - self.alpha) * current_q + self.alpha * target_value
        print(f"   Updated Q-value: {new_q:.4f} (change: {new_q - current_q:+.4f})")
        
        # Update the Q-table
        self.q_table[state, action] = new_q
        
        # Track learning progress
        self.learning_episodes += 1
        self.total_reward += reward
        
        return new_q
    
    def choose_action(self, state, explore=True):
        """
        Select an action using epsilon-greedy strategy.
        
        This balances exploration (trying new actions) with exploitation
        (using known good actions) - a key challenge in reinforcement learning.
        
        Args:
            state (int): Current state
            explore (bool): Whether to use exploration strategy
            
        Returns:
            int: Selected action index
        """
        if explore and np.random.random() < self.epsilon:
            # Exploration: choose random action
            action = np.random.randint(0, self.actions)
            print(f"🎲 Exploring: Random action {action} selected")
            return action
        else:
            # Exploitation: choose best known action
            action = np.argmax(self.q_table[state])
            best_q = self.q_table[state, action]
            print(f"🎯 Exploiting: Best action {action} selected (Q-value: {best_q:.4f})")
            return action
    
    def get_policy(self):
        """
        Extract the learned policy (best action for each state).
        
        Returns:
            numpy.array: Best action for each state
        """
        policy = np.argmax(self.q_table, axis=1)
        print(f"\n📋 Learned Policy (best action for each state):")
        for state in range(self.states):
            best_action = policy[state]
            q_value = self.q_table[state, best_action]
            print(f"   State {state}: Action {best_action} (Q-value: {q_value:.4f})")
        return policy
    
    def display_q_table(self):
        """Display the current Q-table for analysis."""
        print(f"\n📊 Current Q-Table:")
        print("     Actions:", end="")
        for a in range(self.actions):
            print(f"    {a:6}", end="")
        print()
        
        for s in range(self.states):
            print(f"State {s}:", end="")
            for a in range(self.actions):
                print(f" {self.q_table[s,a]:6.3f}", end="")
            print()
    
    def get_learning_stats(self):
        """Get statistics about the learning process."""
        avg_reward = self.total_reward / max(1, self.learning_episodes)
        return {
            'episodes': self.learning_episodes,
            'total_reward': self.total_reward,
            'average_reward': avg_reward
        }

# Demonstration and Testing
print("=== Learning Agent Simulation ===")
print("Q-Learning Reinforcement Learning Demo")
print("-" * 40)

# Initialize agent with 5 states and 4 actions
print("\n🤖 Creating Q-Learning Agent")
agent = QLearningAgent(states=5, actions=4, alpha=0.1, gamma=0.9, epsilon=0.2)

print("\n" + "="*60)

# Simulate learning episodes
print("\n📖 LEARNING PHASE: Agent gaining experience")
print("Simulating various state transitions and rewards...")

# Training scenarios: different experiences for the agent to learn from
training_data = [
    (1, 2, 10, 3),   # State 1, Action 2, Reward 10, Next State 3
    (3, 1, 5, 4),    # State 3, Action 1, Reward 5, Next State 4  
    (2, 0, -2, 1),   # State 2, Action 0, Reward -2, Next State 1
    (4, 3, 15, 0),   # State 4, Action 3, Reward 15, Next State 0
    (0, 2, 8, 2),    # State 0, Action 2, Reward 8, Next State 2
    (1, 1, 12, 4),   # State 1, Action 1, Reward 12, Next State 4
    (3, 0, 3, 1),    # State 3, Action 0, Reward 3, Next State 1
]

for episode, (state, action, reward, next_state) in enumerate(training_data):
    print(f"\n--- Episode {episode + 1} ---")
    agent.learn(state, action, reward, next_state)

print("\n" + "="*60)

# Display learning results
print("\n📈 LEARNING RESULTS:")
stats = agent.get_learning_stats()
print(f"Total learning episodes: {stats['episodes']}")
print(f"Total reward accumulated: {stats['total_reward']}")
print(f"Average reward per episode: {stats['average_reward']:.2f}")

# Show the learned Q-table
agent.display_q_table()

# Extract and display learned policy
learned_policy = agent.get_policy()

print("\n" + "="*60)

# Test decision making with learned knowledge
print("\n🧠 DECISION MAKING: Using learned knowledge")
for test_state in [0, 2, 4]:
    print(f"\nTesting decision making in State {test_state}:")
    
    # Show exploration vs exploitation
    print("  With exploration:")
    action_explore = agent.choose_action(test_state, explore=True)
    
    print("  Pure exploitation:")  
    action_exploit = agent.choose_action(test_state, explore=False)

print("\n=== Learning Agent Key Features ===")
print("🧠 Adaptive behavior through experience")
print("📚 Learns from trial and error interactions")
print("⚖️  Balances exploration of new actions vs exploitation of known good ones")
print("🎯 Improves performance over time without explicit programming")
print("📊 Builds knowledge representation (Q-table) from experience")
print("🔄 Handles delayed rewards and temporal dependencies")

print(f"\n=== Q-Learning Algorithm Benefits ===")
print("• Model-free: No need to know environment dynamics")
print("• Off-policy: Can learn from any experience data")
print("• Convergence: Guaranteed to find optimal policy with enough exploration")
print("• Flexibility: Works in various environments and problem domains")