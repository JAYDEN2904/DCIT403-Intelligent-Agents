"""
LAB 1: Basic SPADE Agent
========================
A simple SPADE agent that demonstrates:
- Agent creation and connection
- Cyclic behavior implementation
- Agent lifecycle management
"""

import asyncio
import warnings
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from datetime import datetime

# Suppress SSL warnings for local development
warnings.filterwarnings('ignore')


class BasicAgent(Agent):
    """
    A simple SPADE agent that prints a message when it starts.
    """

    class StartupBehaviour(OneShotBehaviour):
        """
        A simple behavior that runs once when the agent starts.
        """

        async def run(self):
            agent_name = str(self.agent.jid).split('@')[0]
            print(f"✅ [{agent_name}] Agent is running!")
            print(f"   JID: {self.agent.jid}")
            print(f"   Started at: {datetime.now().strftime('%H:%M:%S')}")

    async def setup(self):
        """
        Setup method called when the agent starts.
        """
        print(f"\n{'='*50}")
        print(f"   SPADE Basic Agent - Lab 1")
        print(f"{'='*50}\n")

        # Add the startup behavior
        startup_behaviour = self.StartupBehaviour()
        self.add_behaviour(startup_behaviour)


async def main():
    """
    Main function to create and run the agent.
    """
    # Agent credentials - using embedded XMPP server, so any password works
    jid = "jayden@localhost"
    password = "290405"

    print(f"🔌 Connecting agent: {jid}")

    # Create the agent
    agent = BasicAgent(jid, password)

    try:
        # Start the agent with auto_register to skip manual credential creation
        await agent.start(auto_register=True)

        # Keep the agent running
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
    import spade
    # Use SPADE's embedded XMPP server to avoid certificate issues
    spade.run(main())
