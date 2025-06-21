"""
Hierarchical Agent System Implementation - Smart Home Example

This module demonstrates a Hierarchical Agent Architecture where agents are organized
in layers with clear supervisor-subordinate relationships. Key characteristics:

- Hierarchical Structure: Agents organized in levels (supervisor → subagents)
- Task Decomposition: Complex tasks broken down into specialized subtasks  
- Coordination: Higher-level agents coordinate and delegate to lower-level agents
- Specialization: Each agent focuses on specific domain expertise

This smart home system shows how a supervisor agent coordinates specialized
security and climate control subagents based on sensor inputs.
"""

class SupervisorAgent:  
    """
    Top-level coordinator agent in the hierarchical system.
    
    The SupervisorAgent demonstrates key hierarchical agent principles:
    - Delegation: Assigns tasks to appropriate specialized subagents
    - Coordination: Manages overall system behavior and priorities
    - Abstraction: Handles high-level decision making while subagents handle details
    """
    
    def __init__(self):  
        """
        Initialize the supervisor with specialized subagent instances.
        
        The supervisor creates and manages a collection of specialized agents,
        each responsible for different aspects of the smart home system.
        """
        # Create specialized subagents for different domains
        self.subagents = {  
            "security": SecurityAgent(),    # Handles intrusion detection and response
            "climate": ClimateAgent()       # Manages temperature and HVAC systems
        }  
        print("SupervisorAgent initialized with subagents:", list(self.subagents.keys()))
    
    def coordinate(self, sensor_data):  
        """
        Main coordination logic - analyzes sensor data and delegates to subagents.
        
        This method demonstrates the hierarchical decision-making process:
        1. Analyze incoming sensor data
        2. Determine priority and appropriate subagent
        3. Delegate specific tasks to specialized agents
        
        Args:
            sensor_data (dict): Dictionary containing various sensor readings
                              Expected keys: "intruder" (bool), "temp" (int)
        """
        print(f"\nSupervisorAgent processing sensor data: {sensor_data}")
        
        # Priority-based decision making: Security takes precedence over comfort
        if sensor_data.get("intruder", False):  
            print("🚨 PRIORITY ALERT: Intruder detected!")
            print("Delegating to SecurityAgent...")
            self.subagents["security"].activate()  
        else:  
            print("✅ No security threats detected")
            print("Delegating to ClimateAgent for comfort management...")
            self.subagents["climate"].adjust(sensor_data.get("temp", 70))  

class SecurityAgent:  
    """
    Specialized agent responsible for home security operations.
    
    This subagent demonstrates domain-specific expertise within
    the hierarchical system. It handles all security-related tasks
    when activated by the supervisor.
    """
    
    def activate(self):  
        """
        Execute security protocols when threat is detected.
        
        In a real system, this might include:
        - Activating alarms and notifications
        - Locking doors and windows
        - Contacting security services
        - Recording security footage
        """
        print("🔒 SecurityAgent: Engaging security protocols")
        print("   - Activating alarm system")
        print("   - Securing all entry points") 
        print("   - Notifying authorities")
        print("   - Starting security recording")

class ClimateAgent:  
    """
    Specialized agent responsible for climate control and comfort.
    
    This subagent manages all temperature-related decisions and actions,
    demonstrating how specialized agents can focus on their domain expertise.
    """
    
    def adjust(self, current_temp):  
        """
        Adjust climate system based on current temperature reading.
        
        Args:
            current_temp (int): Current temperature in Fahrenheit
        """
        # Define comfortable temperature range
        target_temp = 72
        tolerance = 2
        
        print(f"🌡️  ClimateAgent: Current temperature is {current_temp}°F")
        
        if current_temp > target_temp + tolerance:  
            action = "Cool"
            print(f"   - Temperature too high, activating cooling system")
        elif current_temp < target_temp - tolerance:  
            action = "Heat"  
            print(f"   - Temperature too low, activating heating system")
        else:
            action = "Maintain"
            print(f"   - Temperature within comfort range, maintaining current settings")
            
        print(f"   - Climate system action: {action}")

# System Demonstration and Testing
print("=== Hierarchical Agent System Simulation ===")
print("Smart Home Management System")
print("-" * 40)

# Initialize the hierarchical system
smart_home = SupervisorAgent()  

# Test Scenario 1: Security threat detected
print("\n📋 SCENARIO 1: Security Breach")
print("Sensor input: Intruder detected, temperature normal")
smart_home.coordinate({"intruder": True, "temp": 68})

print("\n" + "="*50)

# Test Scenario 2: Normal operation - temperature management
print("\n📋 SCENARIO 2: Normal Operation")
print("Sensor input: No intruder, temperature too hot")
smart_home.coordinate({"intruder": False, "temp": 78})

print("\n" + "="*50)

# Test Scenario 3: Cold temperature management
print("\n📋 SCENARIO 3: Cold Weather")
print("Sensor input: No intruder, temperature too cold")
smart_home.coordinate({"intruder": False, "temp": 65})

print("\n=== Hierarchical Agent Architecture Benefits ===")
print("✅ Clear separation of concerns and responsibilities")
print("✅ Scalable - easy to add new specialized agents")
print("✅ Maintainable - each agent focuses on specific domain")
print("✅ Priority-based coordination and task delegation")
print("✅ Modular design allows independent agent development")