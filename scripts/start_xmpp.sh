#!/bin/bash
# Start the Prosody XMPP server

echo "🌐 Starting Prosody XMPP server..."

# Create log directory if it doesn't exist
sudo mkdir -p /var/log/prosody
sudo chown prosody:prosody /var/log/prosody 2>/dev/null || true

# Try service command (for containers without systemd)
if command -v service &> /dev/null; then
    echo "   Using service command..."
    sudo service prosody start
    sleep 2
    
    if sudo service prosody status | grep -q "running\|active"; then
        echo "✅ XMPP server is running!"
        echo "   - Client port: 5222"
        echo "   - Admin port: 5280"
        exit 0
    fi
fi

# Fallback: try prosodyctl with --force flag
echo "   Trying prosodyctl with --force..."
sudo prosodyctl --force start

sleep 2

# Check if Prosody is running
if pgrep -x prosody > /dev/null || sudo prosodyctl status 2>/dev/null | grep -q "running"; then
    echo "✅ XMPP server is running!"
    echo "   - Client port: 5222"
    echo "   - Admin port: 5280"
else
    echo "⚠️  Prosody may not be running as a service"
    echo "   Trying to run Prosody directly..."
    echo ""
    echo "   Run this in a separate terminal:"
    echo "   sudo prosody"
    echo ""
    echo "   Or check status with:"
    echo "   sudo prosodyctl status"
    echo "   ps aux | grep prosody"
fi
