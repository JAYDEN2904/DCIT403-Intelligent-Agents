#!/bin/bash
# Start the Prosody XMPP server

echo "🌐 Starting Prosody XMPP server..."

# Create log directory if it doesn't exist
sudo mkdir -p /var/log/prosody
sudo chown prosody:prosody /var/log/prosody

# Start Prosody
sudo prosodyctl start

# Check status
sleep 2
if sudo prosodyctl status | grep -q "running"; then
    echo "✅ XMPP server is running!"
    echo "   - Client port: 5222"
    echo "   - Admin port: 5280"
else
    echo "❌ Failed to start XMPP server"
    echo "   Check logs: /var/log/prosody/prosody.err"
    exit 1
fi
