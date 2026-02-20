"""
LAB 3: Main Entry Point
Runs SensorAgent and RescueAgent together.
Events are triggered from sensor reports (sensor_agent.py).

Usage:
    python agents/lab3/main.py
    OR
    python -m agents.lab3.main (from project root)
"""

import asyncio
import sys
import os
import warnings

import spade

# Import SensorAgent from Lab 2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sensor_agent import SensorAgent

from .rescue_agent import RescueAgent

warnings.filterwarnings('ignore')


async def main():
    password = "290405"
    
    rescue = RescueAgent("rescue@localhost", password, max_cycles=5)
    sensor = SensorAgent("sensor@localhost", password, rescue_jid="rescue@localhost")
    
    print(f"\n🔌 Lab 3: SensorAgent sends reports → RescueAgent FSM reacts")
    
    try:
        await rescue.start(auto_register=True)
        await asyncio.sleep(0.5)
        
        await sensor.start(auto_register=True)
        
        while rescue.is_alive() or sensor.is_alive():
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if rescue.is_alive():
            await rescue.stop()
        if sensor.is_alive():
            await sensor.stop()
        print("✅ Lab 3 agents stopped")


if __name__ == "__main__":
    spade.run(main())
