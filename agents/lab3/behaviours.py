"""
LAB 3: FSM and Receive Behaviours for RescueAgent
"""

import json
import warnings

from spade.behaviour import FSMBehaviour, CyclicBehaviour
from spade.template import Template

from .fsm_states import (
    STATE_IDLE,
    STATE_ALERT,
    STATE_RESPONDING,
    STATE_COMPLETED,
    IdleState,
    AlertState,
    RespondingState,
    CompletedState,
)

warnings.filterwarnings('ignore')


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


class ReceiveSensorReportsBehaviour(CyclicBehaviour):
    """
    Receives percept messages from SensorAgent and queues them for the FSM.
    Events are thus triggered from sensor reports.
    """
    
    async def run(self):
        msg = await self.receive(timeout=3)
        if msg:
            try:
                percept = json.loads(msg.body)
                self.agent.pending_events.append(percept)
                agent_name = str(self.agent.jid).split("@")[0]
                print(f"   📥 [{agent_name}] Queued sensor report (pending: {len(self.agent.pending_events)})")
            except (json.JSONDecodeError, KeyError):
                pass


def create_fsm():
    """Create and configure the RescueAgent FSM."""
    fsm = RescueFSMBehaviour()
    
    fsm.add_state(name=STATE_IDLE, state=IdleState(), initial=True)
    fsm.add_state(name=STATE_ALERT, state=AlertState())
    fsm.add_state(name=STATE_RESPONDING, state=RespondingState())
    fsm.add_state(name=STATE_COMPLETED, state=CompletedState())
    
    fsm.add_transition(source=STATE_IDLE, dest=STATE_IDLE)
    fsm.add_transition(source=STATE_IDLE, dest=STATE_ALERT)
    fsm.add_transition(source=STATE_ALERT, dest=STATE_RESPONDING)
    fsm.add_transition(source=STATE_RESPONDING, dest=STATE_COMPLETED)
    fsm.add_transition(source=STATE_COMPLETED, dest=STATE_IDLE)
    
    return fsm


def get_sensor_report_template():
    """Template for receiving sensor INFORM messages."""
    template = Template()
    template.set_metadata("performative", "inform")
    template.set_metadata("ontology", "disaster-response")
    return template
