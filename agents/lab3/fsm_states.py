"""
LAB 3: FSM States for RescueAgent
IDLE → ALERT → RESPONDING → COMPLETED → IDLE
"""

import asyncio
import random
from datetime import datetime

from spade.behaviour import State

from .event import DisasterEvent
from .goals import RescueGoals

# State names
STATE_IDLE = "IDLE"
STATE_ALERT = "ALERT"
STATE_RESPONDING = "RESPONDING"
STATE_COMPLETED = "COMPLETED"


class IdleState(State):
    """
    IDLE State: Agent waits for disaster events from SensorAgent.
    Transitions to ALERT when a sensor report is received.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        print(f"\n🟢 [{agent_name}] STATE: IDLE - Waiting for sensor reports...")
        
        await asyncio.sleep(2)
        
        self.agent.cycle_count += 1
        if self.agent.cycle_count > self.agent.max_cycles:
            print(f"🛑 [{agent_name}] Reached max cycles, stopping...")
            self.set_next_state(None)
            return
        
        if self.agent.pending_events:
            percept = self.agent.pending_events.pop(0)
            self.agent.current_event = DisasterEvent(percept)
            print(f"⚡ [{agent_name}] Event from sensor: {self.agent.current_event}")
            self.set_next_state(STATE_ALERT)
        else:
            print(f"   [{agent_name}] No sensor report yet, continuing patrol...")
            self.set_next_state(STATE_IDLE)


class AlertState(State):
    """
    ALERT State: Agent received a disaster event.
    Assesses the situation and decides on response.
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        event = self.agent.current_event
        
        print(f"\n🟡 [{agent_name}] STATE: ALERT - Assessing situation...")
        print(f"   Event: {event}")
        
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
    """
    
    async def run(self):
        agent_name = str(self.agent.jid).split("@")[0]
        event = self.agent.current_event
        
        print(f"\n🔴 [{agent_name}] STATE: RESPONDING - Executing rescue operations...")
        print(f"   Location: {event.location}")
        
        for goal in self.agent.active_goals:
            print(f"   → Executing goal: {goal}")
            await asyncio.sleep(1)
        
        success = random.random() > 0.2
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
        
        trace = {
            "cycle": self.agent.cycle_count,
            "event": str(event),
            "goals": self.agent.active_goals,
            "result": self.agent.last_result,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.agent.execution_trace.append(trace)
        
        print(f"   Trace logged: Cycle {trace['cycle']}, Result: {trace['result']}")
        
        self.agent.current_event = None
        self.agent.active_goals = []
        
        await asyncio.sleep(1)
        print(f"   [{agent_name}] Returning to patrol...")
        self.set_next_state(STATE_IDLE)
