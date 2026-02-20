"""
LAB 3: Rescue Agent
Uses FSM behavior to respond to disaster events from SensorAgent.
"""

import warnings

from spade.agent import Agent

from .behaviours import (
    RescueFSMBehaviour,
    ReceiveSensorReportsBehaviour,
    create_fsm,
    get_sensor_report_template,
)

warnings.filterwarnings('ignore')


class RescueAgent(Agent):
    """
    RescueAgent that uses FSM behavior to respond to disaster events.
    Events are triggered by sensor reports from sensor_agent.py
    """
    
    def __init__(self, jid, password, max_cycles=5):
        super().__init__(jid, password)
        self.max_cycles = max_cycles
        self.cycle_count = 0
        self.current_event = None
        self.active_goals = []
        self.last_result = None
        self.execution_trace = []
        self.pending_events = []
    
    async def setup(self):
        print(f"\n{'='*60}")
        print("   SPADE RescueAgent - Lab 3: Goals, Events & FSM Behavior")
        print(f"{'='*60}\n")
        
        fsm = create_fsm()
        self.add_behaviour(fsm)
        
        self.add_behaviour(
            ReceiveSensorReportsBehaviour(),
            get_sensor_report_template()
        )
        
        print("📋 FSM Diagram:")
        print("   ┌────────────────────────────────────────────┐")
        print("   │  IDLE ──(event)──► ALERT ──► RESPONDING   │")
        print("   │   ▲                              │         │")
        print("   │   └───── COMPLETED ◄─────────────┘         │")
        print("   └────────────────────────────────────────────┘")
        print()
