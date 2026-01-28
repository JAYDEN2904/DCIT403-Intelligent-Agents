#!/bin/bash
# Create agent credentials on the XMPP server

if [ $# -lt 2 ]; then
    echo "Usage: ./create_agent.sh <username> <password>"
    echo "Example: ./create_agent.sh agent1 secret123"
    exit 1
fi

USERNAME=$1
PASSWORD=$2
DOMAIN="localhost"

echo "👤 Creating agent: ${USERNAME}@${DOMAIN}"

# Register the user with Prosody
sudo prosodyctl register "$USERNAME" "$DOMAIN" "$PASSWORD"

if [ $? -eq 0 ]; then
    echo "✅ Agent credentials created successfully!"
    echo "   JID: ${USERNAME}@${DOMAIN}"
    echo "   Password: ${PASSWORD}"
else
    echo "❌ Failed to create agent credentials"
    echo "   The user might already exist or the server is not running"
fi
