#!/bin/bash
# Run Prosody XMPP server directly in foreground (for containers without systemd)

echo "🌐 Starting Prosody XMPP server directly..."
echo "   (Press Ctrl+C to stop)"
echo ""

# Check if Prosody is already running
if pgrep -x prosody > /dev/null; then
    echo "⚠️  Prosody is already running!"
    echo "   PID: $(pgrep -x prosody)"
    exit 1
fi

# Create necessary directories
mkdir -p /tmp/prosody-data
mkdir -p /tmp/prosody-logs

# Check if prosody user exists, if not run as current user
if id "prosody" &>/dev/null; then
    echo "✅ Starting Prosody as prosody user..."
    sudo -u prosody prosody 2>/dev/null || prosody
else
    echo "✅ Starting Prosody as current user..."
    prosody
fi
