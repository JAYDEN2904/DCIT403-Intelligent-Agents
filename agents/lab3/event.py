"""
LAB 3: Disaster Event (parsed from sensor reports)
"""


class DisasterEvent:
    """
    Represents a disaster event parsed from SensorAgent percept messages.
    """
    
    def __init__(self, percept: dict):
        state = percept.get("state", {})
        self.damage_severity = state.get("damage_severity", 0)
        self.water_level = state.get("water_level", 0.0)
        self.fire_risk = state.get("fire_risk", 0)
        self.is_accessible = state.get("is_accessible", True)
        self.timestamp = percept.get("timestamp", "")
        
        # Derive event type from conditions
        if self.water_level > 0.5:
            self.event_type = "flood"
        elif self.fire_risk > 50:
            self.event_type = "fire"
        elif self.damage_severity > 70:
            self.event_type = "building_collapse"
        else:
            self.event_type = "emergency"
        
        # Derive severity from damage
        if self.damage_severity > 70 or self.fire_risk > 70:
            self.severity = "critical"
        elif self.damage_severity > 50 or self.fire_risk > 50:
            self.severity = "high"
        elif self.damage_severity > 30:
            self.severity = "medium"
        else:
            self.severity = "low"
        
        self.location = f"Zone-{hash(str(percept)) % 5 + 1}"
    
    def __str__(self):
        return f"{self.event_type.upper()} at {self.location} (Severity: {self.severity})"
