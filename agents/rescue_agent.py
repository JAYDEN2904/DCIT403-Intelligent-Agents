"""
LAB 3: Goals, Events, and Reactive Behavior
=============================================
Implements:
- Rescue and response goals
- Event-triggered behavior from sensor reports
- Finite State Machine (FSM) reactive behavior

FSM States:
    IDLE → ALERT → RESPONDING → COMPLETED → IDLE
"""

import asyncio
import random
import warnings
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# Suppress SSL warnings
warnings.filterwarnings('ignore')


# ---------- Agent Goals ----------

class RescueGoals:
    """
    Simple goal definitions for the RescueAgent.
    Goals guide what the agent tries to achieve.
    """
    SAVE_LIVES = "save_lives"
    ASSESS_DAMAGE = "assess_damage"
    SECURE_AREA = "secure_area"
    DELIVER_AID = "deliver_aid"


# ---------- Simulated Disaster Events ----------

class DisasterEvent:
    """
    Represents a disaster event that triggers agent response.
    In a real system, these would come from SensorAgent.
    """
    
    TYPES = ["flood", "fire", "earthquake", "building_collapse"]
    SEVERITIES = ["low", "medium", "high", "critical"]
    
    def __init__(self):
        self.event_type = random.choice(self.TYPES)
        self.severity = random.choice(self.SEVERITIES)
        self.location = f"Zone-{random.randint(1, 5)}"
        self.timestamp = datetime.now().strftime("%H:%M:%S")
    
    def __str__(self):
        return f"{self.event_type.upper()} at {self.location} (Severity: {self.severity})"


# ---------- FSM States ----------

# State names
STATE_IDLE = "IDLE"
STATE_ALERT = "ALERT"
STATE_RESPONDING = "RESPONDING"
STATE_COMPLETED = "COMPLETED"


class IdleState(State):
    """
    IDLE State: Agent waits for disaster events.
    Transitions to ALERT when an event is detected.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        print(f"\n🟢 [{agent_name}] STATE: IDLE - Waiting for events...")
        
        # Simulate waiting for an event (random delay)
        await asyncio.sleep(random.randint(2, 4))
        
        # Check if we should stop (after max cycles)
        self.agent.cycle_count += 1
        if self.agent.cycle_count > self.agent.max_cycles:
            print(f"🛑 [{agent_name}] Reached max cycles, stopping...")
            self.set_next_state(None)  # End FSM
            return
        
        # Simulate receiving an event (in real system, would check messages)
        if random.random() > 0.3:  # 70% chance of event
            self.agent.current_event = DisasterEvent()
            print(f"⚡ [{agent_name}] Event detected: {self.agent.current_event}")
            self.set_next_state(STATE_ALERT)
        else:
            print(f"   [{agent_name}] No event detected, continuing patrol...")
            self.set_next_state(STATE_IDLE)


class AlertState(State):
    """
    ALERT State: Agent received a disaster event.
    Assesses the situation and decides on response.
    Transitions to RESPONDING.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        event = self.agent.current_event
        
        print(f"\n🟡 [{agent_name}] STATE: ALERT - Assessing situation...")
        print(f"   Event: {event}")
        
        # Determine goals based on event severity
        if event.severity in ["high", "critical"]:
            self.agent.active_goals = [RescueGoals.SAVE_LIVES, RescueGoals.ASSESS_DAMAGE]
            print(f"   Priority: HIGH - Goals: {self.agent.active_goals}")
        else:
            self.agent.active_goals = [RescueGoals.ASSESS_DAMAGE, RescueGoals.SECURE_AREA]
            print(f"   Priority: NORMAL - Goals: {self.agent.active_goals}")
        
        await asyncio.sleep(1)
        print(f"   [{agent_name}] Assessment complete, deploying response...")
        self.set_next_state(STATE_RESPONDING)


class RespondingState(State):
    """
    RESPONDING State: Agent is actively responding to the disaster.
    Executes rescue actions based on active goals.
    Transitions to COMPLETED.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        event = self.agent.current_event
        
        print(f"\n🔴 [{agent_name}] STATE: RESPONDING - Executing rescue operations...")
        print(f"   Location: {event.location}")
        
        # Execute each goal
        for goal in self.agent.active_goals:
            print(f"   → Executing goal: {goal}")
            await asyncio.sleep(1)  # Simulate work
        
        # Simulate rescue operation result
        success = random.random() > 0.2  # 80% success rate
        self.agent.last_result = "SUCCESS" if success else "PARTIAL"
        
        print(f"   [{agent_name}] Response result: {self.agent.last_result}")
        self.set_next_state(STATE_COMPLETED)


class CompletedState(State):
    """
    COMPLETED State: Response operation finished.
    Logs results and returns to IDLE.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        event = self.agent.current_event
        
        print(f"\n🟣 [{agent_name}] STATE: COMPLETED - Logging results...")
        
        # Log the execution trace
        trace = {
            "cycle": self.agent.cycle_count,
            "event": str(event),
            "goals": self.agent.active_goals,
            "result": self.agent.last_result,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.agent.execution_trace.append(trace)
        
        print(f"   Trace logged: Cycle {trace['cycle']}, Result: {trace['result']}")
        
        # Clear current event
        self.agent.current_event = None
        self.agent.active_goals = []
        
        await asyncio.sleep(1)
        print(f"   [{agent_name}] Returning to patrol...")
        self.set_next_state(STATE_IDLE)


# ---------- FSM Behavior ----------

class RescueFSMBehaviour(FSMBehaviour):
    """
    FSM Behavior that manages the RescueAgent's state transitions.
    """
    
    async def on_start(self):
        print(f"🚀 FSM Behaviour started")
    
    async def on_end(self):
        agent_name = str(self.agent.jid).split("@")[0]
        print(f"\n{'='*50}")
        print(f"📊 [{agent_name}] EXECUTION TRACE SUMMARY")
        print(f"{'='*50}")
        
        for trace in self.agent.execution_trace:
            print(f"  Cycle {trace['cycle']}: {trace['event'][:30]}... → {trace['result']}")
        
        print(f"{'='*50}")
        print(f"   Total responses: {len(self.agent.execution_trace)}")
        print(f"{'='*50}\n")
        
        await self.agent.stop()


# ---------- Rescue Agent ----------

class RescueAgent(Agent):
    """
    RescueAgent that uses FSM behavior to respond to disaster events.
    """
    
    def __init__(self, jid, password, max_cycles=5):
        super().__init__(jid, password)
        self.max_cycles = max_cycles
        self.cycle_count = 0
        self.current_event = None
        self.active_goals = []
        self.last_result = None
        self.execution_trace = []
    
    async def setup(self):
        print(f"\n{'='*60}")
        print("   SPADE RescueAgent - Lab 3: Goals, Events & FSM Behavior")
        print(f"{'='*60}\n")
        
        # Create FSM behaviour
        fsm = RescueFSMBehaviour()
        
        # Add states
        fsm.add_state(name=STATE_IDLE, state=IdleState(), initial=True)
        fsm.add_state(name=STATE_ALERT, state=AlertState())
        fsm.add_state(name=STATE_RESPONDING, state=RespondingState())
        fsm.add_state(name=STATE_COMPLETED, state=CompletedState())
        
        # Add transitions
        fsm.add_transition(source=STATE_IDLE, dest=STATE_IDLE)        # No event
        fsm.add_transition(source=STATE_IDLE, dest=STATE_ALERT)       # Event detected
        fsm.add_transition(source=STATE_ALERT, dest=STATE_RESPONDING) # Start response
        fsm.add_transition(source=STATE_RESPONDING, dest=STATE_COMPLETED)  # Done
        fsm.add_transition(source=STATE_COMPLETED, dest=STATE_IDLE)   # Return to patrol
        
        self.add_behaviour(fsm)
        
        print("📋 FSM Diagram:")
        print("   ┌────────────────────────────────────────────┐")
        print("   │  IDLE ──(event)──► ALERT ──► RESPONDING   │")
        print("   │   ▲                              │         │")
        print("   │   └───── COMPLETED ◄─────────────┘         │")
        print("   └────────────────────────────────────────────┘")
        print()


# ---------- Main ----------

async def main():
    jid = "rescue@localhost"
    password = "290405"
    
    print(f"🔌 Connecting RescueAgent: {jid}")
    agent = RescueAgent(jid, password, max_cycles=5)
    
    try:
        await agent.start(auto_register=True)
        
        while agent.is_alive():
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if agent.is_alive():
            await agent.stop()
        print("✅ RescueAgent stopped")


if __name__ == "__main__":
    import spade
    spade.run(main())

