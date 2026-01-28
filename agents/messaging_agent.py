"""
LAB 1 (Extended): Messaging Between SPADE Agents
=================================================
Demonstrates agent-to-agent communication using XMPP messages.

Before running:
1. Start the XMPP server: ./scripts/start_xmpp.sh
2. Create credentials:
   ./scripts/create_agent.sh sender secret123
   ./scripts/create_agent.sh receiver secret123
"""

import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
from datetime import datetime


def get_agent_name(agent):
    """Helper to extract username from JID"""
    return str(agent.jid).split('@')[0]


class SenderAgent(Agent):
    """
    An agent that sends messages to another agent.
    """

    class SendBehaviour(OneShotBehaviour):
        """
        Sends a series of messages to the receiver agent.
        """

        def __init__(self, receiver_jid: str):
            super().__init__()
            self.receiver_jid = receiver_jid

        async def run(self):
            agent_name = get_agent_name(self.agent)
            print(f"📤 [{agent_name}] Starting to send messages...")
            
            messages = [
                "Hello from the sender agent!",
                "This is message number 2",
                "And here's the third message",
                "STOP"  # Signal to stop
            ]
            
            for i, content in enumerate(messages, 1):
                msg = Message(to=self.receiver_jid)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("message_id", str(i))
                msg.body = content
                
                await self.send(msg)
                print(f"   → Sent message {i}: '{content}'")
                await asyncio.sleep(1)
            
            print(f"📤 [{agent_name}] All messages sent!")
            await asyncio.sleep(2)
            await self.agent.stop()

    async def setup(self):
        agent_name = get_agent_name(self)
        print(f"🚀 [{agent_name}] Sender agent started")
        behaviour = self.SendBehaviour("receiver@localhost")
        self.add_behaviour(behaviour)


class ReceiverAgent(Agent):
    """
    An agent that receives and processes messages.
    """

    class ReceiveBehaviour(CyclicBehaviour):
        """
        Listens for incoming messages and processes them.
        """

        async def run(self):
            agent_name = get_agent_name(self.agent)
            
            # Wait for a message (timeout after 10 seconds)
            msg = await self.receive(timeout=10)
            
            if msg:
                sender = str(msg.sender)
                content = msg.body
                msg_id = msg.get_metadata("message_id")
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"📥 [{agent_name}] Received at {timestamp}:")
                print(f"   From: {sender}")
                print(f"   Message #{msg_id}: '{content}'")
                
                # Check for stop signal
                if content == "STOP":
                    print(f"🛑 [{agent_name}] Received stop signal")
                    self.kill()
                    await self.agent.stop()
            else:
                print(f"⏳ [{agent_name}] No message received (timeout)")

    async def setup(self):
        agent_name = get_agent_name(self)
        print(f"🚀 [{agent_name}] Receiver agent started, waiting for messages...")
        
        # Create a template to filter messages
        template = Template()
        template.set_metadata("performative", "inform")
        
        behaviour = self.ReceiveBehaviour()
        self.add_behaviour(behaviour, template)


async def main():
    """
    Run both sender and receiver agents.
    """
    print(f"\n{'='*50}")
    print(f"   SPADE Messaging Demo - Lab 1")
    print(f"{'='*50}\n")

    # Create agents
    receiver = ReceiverAgent("receiver@localhost", "secret123")
    sender = SenderAgent("sender@localhost", "secret123")

    try:
        # Start receiver first (so it's ready to receive)
        # verify_security=False for self-signed certs in dev environment
        await receiver.start(verify_security=False)
        await asyncio.sleep(1)
        
        # Start sender
        await sender.start(verify_security=False)
        
        # Wait for both agents to complete
        while receiver.is_alive() or sender.is_alive():
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the XMPP server is running and credentials are created!")
        print("   Run: ./scripts/create_agent.sh sender secret123")
        print("   Run: ./scripts/create_agent.sh receiver secret123")
    finally:
        if receiver.is_alive():
            await receiver.stop()
        if sender.is_alive():
            await sender.stop()
        print("\n✅ All agents stopped")


if __name__ == "__main__":
    asyncio.run(main())
