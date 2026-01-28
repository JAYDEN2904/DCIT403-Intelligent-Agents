"""
LAB 1: Basic SPADE Agent
========================
A simple SPADE agent that demonstrates:
- Agent creation and connection
- Cyclic behavior implementation
- Agent lifecycle management

Before running this agent:
1. Start the XMPP server: ./scripts/start_xmpp.sh
2. Create credentials: ./scripts/create_agent.sh jayden 290405
"""

import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from datetime import datetime


class BasicAgent(Agent):
    """
    A basic SPADE agent with demonstration behaviors.
    """

    class HelloBehaviour(OneShotBehaviour):
        """
        A one-shot behavior that runs once when the agent starts.
        """

        async def run(self):
            agent_name = str(self.agent.jid).split('@')[0]
            print(f"🚀 [{agent_name}] Agent started at {datetime.now().strftime('%H:%M:%S')}")
            print(f"   JID: {self.agent.jid}")
            print(f"   Available: {self.agent.is_alive()}")

    class HeartbeatBehaviour(CyclicBehaviour):
        """
        A cyclic behavior that runs repeatedly.
        Demonstrates continuous agent activity.
        """

        def __init__(self, period: int = 5):
            super().__init__()
            self.period = period
            self.counter = 0

        async def run(self):
            self.counter += 1
            agent_name = str(self.agent.jid).split('@')[0]
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"💓 [{agent_name}] Heartbeat #{self.counter} at {timestamp}")
            
            # Stop after 5 heartbeats for demonstration
            if self.counter >= 5:
                print(f"🛑 [{agent_name}] Stopping after {self.counter} heartbeats")
                self.kill()
                await self.agent.stop()
            
            await asyncio.sleep(self.period)

        async def on_end(self):
            agent_name = str(self.agent.jid).split('@')[0]
            print(f"👋 [{agent_name}] Heartbeat behavior ended")

    async def setup(self):
        """
        Setup method called when the agent starts.
        Add behaviors here.
        """
        print(f"\n{'='*50}")
        print(f"   SPADE Basic Agent - Lab 1")
        print(f"{'='*50}\n")

        # Add the hello behavior (runs once)
        hello_behaviour = self.HelloBehaviour()
        self.add_behaviour(hello_behaviour)

        # Add the heartbeat behavior (runs continuously)
        heartbeat_behaviour = self.HeartbeatBehaviour(period=2)
        self.add_behaviour(heartbeat_behaviour)


async def main():
    """
    Main function to create and run the agent.
    """
    # Agent credentials (create these first with ./scripts/create_agent.sh)
    jid = "jayden@localhost"
    password = "290405"

    print(f"🔌 Connecting agent: {jid}")
    
    # Create the agent
    agent = BasicAgent(jid, password)

    try:
        # Start the agent (verify_security=False for self-signed certs in dev)
        await agent.start(verify_security=False)
        
        # Wait for agent to complete its behaviors
        while agent.is_alive():
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the XMPP server is running and credentials are created!")
    finally:
        if agent.is_alive():
            await agent.stop()
        print("✅ Agent stopped")


if __name__ == "__main__":
    asyncio.run(main())
