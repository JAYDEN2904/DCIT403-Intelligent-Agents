"""
LAB 2: Perception and Environment Modeling
=========================================
Implements:
- A simulated disaster environment
- A SensorAgent that periodically monitors conditions
- Generation and logging of disaster events (percepts)
"""

import asyncio
import os
import random
import warnings
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

# Disable SSL certificate verification warnings for local development
warnings.filterwarnings('ignore', message='.*certificate.*')


# ---------- Simulated Disaster Environment ----------

@dataclass
class EnvironmentState:
    """
    Simple representation of a disaster environment state.
    You can extend this later (e.g., flood level, fire, blocked roads).
    """

    damage_severity: int  # 0–100
    water_level: float  # meters
    fire_risk: int  # 0–100
    is_accessible: bool  # whether roads/paths are accessible


class DisasterEnvironment:
    """
    A very simple stochastic environment that evolves over time.
    The sensor agent will "perceive" this environment.
    """

    def __init__(self):
        # Start in a safe-ish state
        self.state = EnvironmentState(
            damage_severity=0,
            water_level=0.0,
            fire_risk=0,
            is_accessible=True,
        )

    def step(self) -> EnvironmentState:
        """
        Advance the environment by one time step and return the new state.
        This method randomly perturbs the variables to simulate a disaster.
        """
        # Random increments / decrements
        delta_damage = random.randint(0, 15)
        delta_water = random.uniform(-0.1, 0.5)
        delta_fire = random.randint(-5, 20)

        self.state.damage_severity = min(
            100, self.state.damage_severity + delta_damage)
        self.state.water_level = max(0.0, self.state.water_level + delta_water)
        self.state.fire_risk = max(
            0, min(100, self.state.fire_risk + delta_fire))

        # Accessibility decreases as damage grows
        if self.state.damage_severity > 70 or self.state.water_level > 1.0:
            self.state.is_accessible = False

        return self.state


# ---------- Sensor Agent ----------

class SensorAgent(Agent):
    """
    SensorAgent that periodically monitors the DisasterEnvironment
    and logs percepts (environment snapshots).
    """

    class SenseEnvironmentBehaviour(CyclicBehaviour):
        def __init__(self, env: DisasterEnvironment, period: int = 3, max_steps: int = 15):
            super().__init__()
            self.env = env
            self.period = period
            self.max_steps = max_steps
            self.step_count = 0

            # Prepare logging directory / file
            os.makedirs("logs", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(
                "logs", f"sensor_events_{timestamp}.log")

        async def log_event(self, percept: Dict[str, Any]) -> None:
        
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{percept}\n")

        async def run(self):
            self.step_count += 1
            agent_name = str(self.agent.jid).split("@")[0]

            
            state = self.env.step()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            
            percept = {
                "timestamp": timestamp,
                "agent": agent_name,
                "state": asdict(state),
            }

            
            print(
                f"👁️  [{agent_name}] Percept #{self.step_count} at {timestamp}")
            print(
                f"   Damage: {state.damage_severity:3d} | "
                f"Water: {state.water_level:4.2f} m | "
                f"Fire risk: {state.fire_risk:3d} | "
                f"Accessible: {state.is_accessible}"
            )

            
            await self.log_event(percept)

         
            if self.step_count >= self.max_steps:
                print(
                    f"🛑 [{agent_name}] Reached {self.max_steps} percepts, stopping agent.")
                self.kill()
                await self.agent.stop()
                return

            
            await asyncio.sleep(self.period)

    async def setup(self):
        """
        Setup method called when the agent starts.
        Creates the simulated environment and perception behaviour.
        """
        print(f"\n{'=' * 60}")
        print("   SPADE SensorAgent - Lab 2: Perception & Environment Modeling")
        print(f"{'=' * 60}\n")

        env = DisasterEnvironment()

        # Period in seconds between perceptions; adjust as needed
        behaviour = self.SenseEnvironmentBehaviour(
            env=env, period=2, max_steps=20)
        self.add_behaviour(behaviour)


async def main():
    """
    Main entry point to run the SensorAgent.
    """
    jid = "sensor@localhost"
    password = "290405"

    print(f"🔌 Connecting SensorAgent: {jid}")
    agent = SensorAgent(jid, password)

    try:
        # Start the agent with auto_register to skip manual credential creation
        await agent.start(auto_register=True)

    
        while agent.is_alive():
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error starting SensorAgent: {e}")
        print("   Make sure the XMPP server is running and credentials are created!")
        print("   Run: ./scripts/create_agent.sh sensor 290405")
    finally:
        if agent.is_alive():
            await agent.stop()
        print("✅ SensorAgent stopped")


if __name__ == "__main__":
    import spade
    spade.run(main())
