"""
LAB 4: Utility classes for FIPA-ACL communication
"""

from datetime import datetime
from typing import Tuple


def derive_disaster_info(reading: dict) -> Tuple[str, str]:
    """
    Derive disaster type and severity from sensor metrics.
    Returns (disaster_type, severity).
    """
    damage = reading.get("damage_severity", 0)
    water = reading.get("water_level", 0.0)
    fire = reading.get("fire_risk", 0)
    
    # Disaster type from dominant hazard
    if water > 0.5:
        disaster_type = "FLOOD"
    elif fire > 50:
        disaster_type = "FIRE"
    elif damage > 70:
        disaster_type = "BUILDING_COLLAPSE"
    else:
        disaster_type = "EMERGENCY"
    
    # Severity
    if damage > 70 or fire > 70:
        severity = "critical"
    elif damage > 50 or fire > 50:
        severity = "high"
    elif damage > 30:
        severity = "medium"
    else:
        severity = "low"
    
    return disaster_type, severity
from spade.message import Message


class Performative:
    """Standard FIPA-ACL performatives used in this system."""
    INFORM = "inform"       # Sharing information
    REQUEST = "request"     # Requesting an action
    AGREE = "agree"         # Agreeing to perform action
    REFUSE = "refuse"       # Refusing to perform action


class MessageLogger:
    """Simple logger for ACL messages."""
    
    @staticmethod
    def log(agent_name: str, direction: str, msg: Message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        perf = msg.get_metadata("performative") or "unknown"
        sender = str(msg.sender).split("@")[0] if msg.sender else "?"
        receiver = str(msg.to).split("@")[0] if msg.to else "?"
        
        if direction == "SENT":
            print(f"📤 [{timestamp}] {agent_name} → {receiver}")
        else:
            print(f"📥 [{timestamp}] {sender} → {agent_name}")
        
        print(f"   Performative: {perf.upper()}")
        print(f"   Content: {msg.body[:60]}..." if len(msg.body) > 60 else f"   Content: {msg.body}")


