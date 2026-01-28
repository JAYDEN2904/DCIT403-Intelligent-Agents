#!/bin/bash
# Stop the Prosody XMPP server

echo "🛑 Stopping Prosody XMPP server..."

# Try service command
if command -v service &> /dev/null; then
    sudo service prosody stop 2>/dev/null
fi

# Kill any running Prosody processes
if pgrep -x prosody > /dev/null; then
    echo "   Stopping Prosody processes..."
    sudo pkill -x prosody
    sleep 1
fi

# Also try prosodyctl as fallback
sudo prosodyctl --force stop 2>/dev/null || true

echo "✅ XMPP server stopped."
