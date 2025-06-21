"""
Multi-Agent System Implementation - Warehouse Automation Example

This module demonstrates a Multi-Agent System (MAS) where multiple autonomous agents
coordinate, collaborate, and sometimes compete to achieve common objectives.

Key MAS Characteristics Demonstrated:
- Decentralization: Each agent makes independent decisions
- Collaboration: Agents work together toward shared goals
- Competition: Agents compete for limited resources (charging stations)
- Scalability: System can handle multiple agents dynamically
- Specialization: Different agent types with specific capabilities

This warehouse scenario shows how picker agents, transport agents, and a coordinator
agent work together to fulfill orders efficiently while managing resource constraints.
"""

import random
import time
from enum import Enum

class AgentState(Enum):
    """Enumeration of possible agent states for coordination."""
    IDLE = "idle"
    WORKING = "working"
    MOVING = "moving"
    CHARGING = "charging"
    WAITING = "waiting"

class Message:
    """Communication message between agents in the MAS."""
    
    def __init__(self, sender_id, receiver_id, message_type, content):
        """
        Initialize a message for inter-agent communication.
        
        Args:
            sender_id (str): ID of the sending agent
            receiver_id (str): ID of the receiving agent ('ALL' for broadcast)
            message_type (str): Type of message (REQUEST, RESPONSE, NOTIFY, etc.)
            content (dict): Message payload data
        """
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message_type = message_type
        self.content = content
        self.timestamp = time.time()

class BaseAgent:
    """
    Base class for all agents in the Multi-Agent System.
    
    Provides common functionality for communication, coordination,
    and basic agent lifecycle management.
    """
    
    def __init__(self, agent_id, agent_type, position=(0, 0)):
        """
        Initialize base agent with common properties.
        
        Args:
            agent_id (str): Unique identifier for this agent
            agent_type (str): Type/role of the agent
            position (tuple): Starting (x, y) position
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.position = position
        self.state = AgentState.IDLE
        self.battery_level = 100
        self.message_queue = []
        self.current_task = None
        self.performance_metrics = {
            'tasks_completed': 0,
            'messages_sent': 0,
            'messages_received': 0,
            'collaboration_count': 0
        }
        
        print(f"🤖 Agent {self.agent_id} ({self.agent_type}) initialized at position {self.position}")
    
    def send_message(self, mas_coordinator, receiver_id, message_type, content):
        """Send a message to another agent through the MAS coordinator."""
        message = Message(self.agent_id, receiver_id, message_type, content)
        mas_coordinator.route_message(message)
        self.performance_metrics['messages_sent'] += 1
        print(f"📤 {self.agent_id} sent {message_type} to {receiver_id}: {content}")
    
    def receive_message(self, message):
        """Receive and queue a message from another agent."""
        self.message_queue.append(message)
        self.performance_metrics['messages_received'] += 1
        print(f"📥 {self.agent_id} received {message.message_type} from {message.sender_id}")
    
    def process_messages(self):
        """Process all queued messages."""
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.handle_message(message)
    
    def handle_message(self, message):
        """Handle a specific message - to be overridden by subclasses."""
        print(f"💬 {self.agent_id} handling {message.message_type}: {message.content}")
    
    def update_battery(self, consumption=1):
        """Update battery level based on activity."""
        self.battery_level = max(0, self.battery_level - consumption)
        if self.battery_level < 20:
            print(f"🔋 {self.agent_id} battery low: {self.battery_level}%")

class PickerAgent(BaseAgent):
    """
    Specialized agent for picking items from warehouse shelves.
    
    Demonstrates specialization in MAS - focused on item retrieval tasks.
    """
    
    def __init__(self, agent_id, position=(0, 0)):
        super().__init__(agent_id, "Picker", position)
        self.carrying_capacity = 10
        self.current_load = 0
        self.picking_speed = 2  # items per time unit
    
    def handle_message(self, message):
        """Handle messages specific to picker operations."""
        if message.message_type == "PICK_REQUEST":
            self.handle_pick_request(message.content)
        elif message.message_type == "COLLABORATION_REQUEST":
            self.handle_collaboration_request(message.content)
    
    def handle_pick_request(self, request):
        """Process a request to pick specific items."""
        items_needed = request.get('items', [])
        location = request.get('location', (0, 0))
        
        print(f"🎯 {self.agent_id} received pick request: {len(items_needed)} items at {location}")
        
        if self.state == AgentState.IDLE and self.current_load + len(items_needed) <= self.carrying_capacity:
            self.state = AgentState.WORKING
            self.current_task = request
            self.move_to_location(location)
            self.pick_items(items_needed)
            self.performance_metrics['tasks_completed'] += 1
        else:
            print(f"❌ {self.agent_id} cannot handle request - busy or capacity exceeded")
    
    def handle_collaboration_request(self, request):
        """Handle requests for collaboration from other agents."""
        if self.state == AgentState.IDLE:
            print(f"🤝 {self.agent_id} accepting collaboration request")
            self.performance_metrics['collaboration_count'] += 1
            return True
        return False
    
    def move_to_location(self, target_location):
        """Move to a specific location in the warehouse."""
        self.state = AgentState.MOVING
        print(f"🚶 {self.agent_id} moving from {self.position} to {target_location}")
        self.position = target_location
        self.update_battery(2)
    
    def pick_items(self, items):
        """Pick items from the current location."""
        print(f"📦 {self.agent_id} picking {len(items)} items")
        self.current_load += len(items)
        self.update_battery(len(items))
        self.state = AgentState.IDLE

class TransportAgent(BaseAgent):
    """
    Specialized agent for transporting items between locations.
    
    Demonstrates specialization and collaboration in MAS.
    """
    
    def __init__(self, agent_id, position=(0, 0)):
        super().__init__(agent_id, "Transport", position)
        self.carrying_capacity = 50
        self.current_load = 0
        self.transport_speed = 5  # units per time
    
    def handle_message(self, message):
        """Handle messages specific to transport operations."""
        if message.message_type == "TRANSPORT_REQUEST":
            self.handle_transport_request(message.content)
        elif message.message_type == "PICKUP_READY":
            self.handle_pickup_ready(message.content)
    
    def handle_transport_request(self, request):
        """Process a request to transport items."""
        pickup_location = request.get('pickup_location', (0, 0))
        delivery_location = request.get('delivery_location', (10, 10))
        item_count = request.get('item_count', 0)
        
        print(f"🚛 {self.agent_id} received transport request: {item_count} items")
        
        if self.state == AgentState.IDLE and item_count <= self.carrying_capacity:
            self.state = AgentState.WORKING
            self.current_task = request
            self.execute_transport(pickup_location, delivery_location, item_count)
            self.performance_metrics['tasks_completed'] += 1
    
    def handle_pickup_ready(self, notification):
        """Handle notification that items are ready for pickup."""
        print(f"📬 {self.agent_id} notified that pickup is ready")
        # Coordinate with picker agents for efficient pickup
    
    def execute_transport(self, pickup_loc, delivery_loc, item_count):
        """Execute the complete transport operation."""
        print(f"🚚 {self.agent_id} executing transport mission")
        
        # Move to pickup location
        self.move_to_location(pickup_loc)
        
        # Load items
        self.current_load += item_count
        print(f"📦 {self.agent_id} loaded {item_count} items")
        
        # Move to delivery location
        self.move_to_location(delivery_loc)
        
        # Unload items
        self.current_load -= item_count
        print(f"📤 {self.agent_id} delivered {item_count} items")
        self.state = AgentState.IDLE

class CoordinatorAgent(BaseAgent):
    """
    Coordinator agent that manages task distribution and resource allocation.
    
    Demonstrates centralized coordination in a decentralized MAS.
    """
    
    def __init__(self, agent_id):
        super().__init__(agent_id, "Coordinator", (5, 5))
        self.pending_orders = []
        self.resource_status = {
            'charging_stations': 3,
            'available_stations': 3
        }
        self.agent_registry = {}
    
    def register_agent(self, agent):
        """Register an agent with the coordinator."""
        self.agent_registry[agent.agent_id] = agent
        print(f"📋 Coordinator registered agent {agent.agent_id}")
    
    def handle_message(self, message):
        """Handle coordination messages."""
        if message.message_type == "ORDER_REQUEST":
            self.handle_order_request(message.content)
        elif message.message_type == "RESOURCE_REQUEST":
            self.handle_resource_request(message.content)
        elif message.message_type == "STATUS_UPDATE":
            self.handle_status_update(message.content)
    
    def handle_order_request(self, order):
        """Process a new order and coordinate agent assignments."""
        print(f"📋 Coordinator processing order: {order}")
        self.pending_orders.append(order)
        self.allocate_tasks(order)
    
    def allocate_tasks(self, order):
        """Allocate tasks to appropriate agents based on specialization."""
        items_needed = order.get('items', [])
        
        # Find available picker agents
        available_pickers = [
            agent for agent in self.agent_registry.values()
            if isinstance(agent, PickerAgent) and agent.state == AgentState.IDLE
        ]
        
        # Find available transport agents
        available_transporters = [
            agent for agent in self.agent_registry.values()
            if isinstance(agent, TransportAgent) and agent.state == AgentState.IDLE
        ]
        
        if available_pickers and available_transporters:
            # Assign picking task
            picker = available_pickers[0]
            picker.handle_pick_request({
                'items': items_needed,
                'location': (random.randint(1, 10), random.randint(1, 10))
            })
            
            # Assign transport task
            transporter = available_transporters[0]
            transporter.handle_transport_request({
                'pickup_location': picker.position,
                'delivery_location': (random.randint(1, 10), random.randint(1, 10)),
                'item_count': len(items_needed)
            })
            
            print(f"✅ Coordinator assigned order to {picker.agent_id} and {transporter.agent_id}")
        else:
            print(f"⏳ Coordinator queuing order - insufficient available agents")
    
    def handle_resource_request(self, request):
        """Handle requests for shared resources (e.g., charging stations)."""
        resource_type = request.get('resource_type', '')
        requesting_agent = request.get('agent_id', '')
        
        if resource_type == 'charging_station':
            if self.resource_status['available_stations'] > 0:
                self.resource_status['available_stations'] -= 1
                print(f"🔌 Coordinator allocated charging station to {requesting_agent}")
                return True
            else:
                print(f"⚡ No charging stations available for {requesting_agent}")
                return False
    
    def handle_status_update(self, status):
        """Handle status updates from agents."""
        agent_id = status.get('agent_id', '')
        new_status = status.get('status', '')
        print(f"📊 Coordinator received status update from {agent_id}: {new_status}")

class MultiAgentSystem:
    """
    Main Multi-Agent System coordinator that manages all agents and communications.
    
    Demonstrates the overall MAS architecture with decentralized agents
    coordinating through a communication infrastructure.
    """
    
    def __init__(self):
        """Initialize the Multi-Agent System."""
        self.agents = {}
        self.coordinator = None
        self.message_log = []
        self.system_metrics = {
            'total_messages': 0,
            'orders_processed': 0,
            'collaboration_instances': 0
        }
        
        print("🏢 Multi-Agent System initialized")
    
    def add_agent(self, agent):
        """Add an agent to the MAS."""
        self.agents[agent.agent_id] = agent
        if isinstance(agent, CoordinatorAgent):
            self.coordinator = agent
        elif self.coordinator:
            self.coordinator.register_agent(agent)
        
        print(f"➕ Added {agent.agent_type} agent {agent.agent_id} to MAS")
    
    def route_message(self, message):
        """Route messages between agents."""
        self.message_log.append(message)
        self.system_metrics['total_messages'] += 1
        
        if message.receiver_id == 'ALL':
            # Broadcast message to all agents
            for agent in self.agents.values():
                if agent.agent_id != message.sender_id:
                    agent.receive_message(message)
        elif message.receiver_id in self.agents:
            # Send to specific agent
            self.agents[message.receiver_id].receive_message(message)
        else:
            print(f"❌ Message routing failed: Agent {message.receiver_id} not found")
    
    def process_order(self, order):
        """Process a new order through the MAS."""
        print(f"\n📦 NEW ORDER RECEIVED: {order}")
        self.system_metrics['orders_processed'] += 1
        
        if self.coordinator:
            self.coordinator.handle_order_request(order)
        else:
            print("❌ No coordinator available to process order")
    
    def simulate_step(self):
        """Execute one simulation step for all agents."""
        print(f"\n⏰ MAS Simulation Step")
        
        # Process messages for all agents
        for agent in self.agents.values():
            agent.process_messages()
        
        # Simulate resource competition
        self.simulate_resource_competition()
    
    def simulate_resource_competition(self):
        """Simulate competition for limited resources."""
        low_battery_agents = [
            agent for agent in self.agents.values()
            if agent.battery_level < 30 and not isinstance(agent, CoordinatorAgent)
        ]
        
        if low_battery_agents and self.coordinator:
            print(f"⚡ {len(low_battery_agents)} agents need charging - resource competition!")
            
            for agent in low_battery_agents:
                success = self.coordinator.handle_resource_request({
                    'resource_type': 'charging_station',
                    'agent_id': agent.agent_id
                })
                
                if success:
                    agent.state = AgentState.CHARGING
                    agent.battery_level = 100
                    print(f"🔋 {agent.agent_id} successfully charged")
                else:
                    print(f"⏳ {agent.agent_id} waiting for charging station")
    
    def get_system_status(self):
        """Get comprehensive system status and metrics."""
        print(f"\n📊 === MAS SYSTEM STATUS ===")
        print(f"Total Agents: {len(self.agents)}")
        print(f"Total Messages: {self.system_metrics['total_messages']}")
        print(f"Orders Processed: {self.system_metrics['orders_processed']}")
        
        print(f"\n🤖 Agent Status:")
        for agent in self.agents.values():
            print(f"  {agent.agent_id} ({agent.agent_type}): {agent.state.value} - Battery: {agent.battery_level}%")
            print(f"    Tasks: {agent.performance_metrics['tasks_completed']}, "
                  f"Messages: {agent.performance_metrics['messages_sent']}/{agent.performance_metrics['messages_received']}")

# Demonstration and Testing
def run_mas_simulation():
    """Run a complete Multi-Agent System simulation."""
    print("=== Multi-Agent System Simulation ===")
    print("Warehouse Automation with Collaborative Agents")
    print("-" * 50)
    
    # Initialize the MAS
    mas = MultiAgentSystem()
    
    # Create and add agents to the system
    coordinator = CoordinatorAgent("COORD_01")
    mas.add_agent(coordinator)
    
    # Add specialized picker agents
    picker1 = PickerAgent("PICKER_01", (2, 3))
    picker2 = PickerAgent("PICKER_02", (7, 8))
    mas.add_agent(picker1)
    mas.add_agent(picker2)
    
    # Add specialized transport agents
    transport1 = TransportAgent("TRANSPORT_01", (1, 1))
    transport2 = TransportAgent("TRANSPORT_02", (9, 9))
    mas.add_agent(transport1)
    mas.add_agent(transport2)
    
    print(f"\n🏗️  MAS Setup Complete - {len(mas.agents)} agents active")
    
    # Simulate order processing
    orders = [
        {'order_id': 'ORD_001', 'items': ['item1', 'item2', 'item3'], 'priority': 'high'},
        {'order_id': 'ORD_002', 'items': ['item4', 'item5'], 'priority': 'normal'},
        {'order_id': 'ORD_003', 'items': ['item6', 'item7', 'item8', 'item9'], 'priority': 'low'}
    ]
    
    # Process orders and simulate system operation
    for i, order in enumerate(orders):
        print(f"\n{'='*60}")
        print(f"PROCESSING ORDER {i+1}")
        mas.process_order(order)
        mas.simulate_step()
        
        # Simulate battery drain
        for agent in mas.agents.values():
            if not isinstance(agent, CoordinatorAgent):
                agent.update_battery(random.randint(5, 15))
    
    # Final system status
    print(f"\n{'='*60}")
    print("SIMULATION COMPLETE")
    mas.get_system_status()
    
    print(f"\n=== Multi-Agent System Key Features Demonstrated ===")
    print("🔄 Decentralization: Each agent makes independent decisions")
    print("🤝 Collaboration: Agents work together to fulfill orders")
    print("⚡ Competition: Agents compete for limited charging stations")
    print("📈 Scalability: System handles multiple agents and orders efficiently")
    print("🎯 Specialization: Different agent types with specific capabilities")
    print("📡 Communication: Agents coordinate through message passing")
    print("🧠 Coordination: Centralized coordination with decentralized execution")

if __name__ == "__main__":
    run_mas_simulation()
