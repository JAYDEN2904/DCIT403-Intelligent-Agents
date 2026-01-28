#!/bin/bash
# Check XMPP server status

echo "📊 XMPP Server Status"
echo "====================="

# Check if Prosody process is running
if pgrep -x prosody > /dev/null; then
    echo "✅ Prosody is running"
    echo "   PID: $(pgrep -x prosody)"
else
    echo "❌ Prosody is not running"
fi

echo ""

# Try service status
if command -v service &> /dev/null; then
    echo "Service status:"
    sudo service prosody status 2>/dev/null || echo "   (service command not available)"
fi

echo ""

# Try prosodyctl status
echo "Prosodyctl status:"
sudo prosodyctl status 2>/dev/null || echo "   (prosodyctl check failed)"

echo ""
echo "📋 Registered Users:"
sudo prosodyctl listusers localhost 2>/dev/null || echo "   (Run: sudo prosodyctl listusers localhost)"
