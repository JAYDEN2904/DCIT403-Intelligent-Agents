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
sudo mkdir -p /var/lib/prosody
sudo mkdir -p /var/log/prosody
sudo chown -R prosody:prosody /var/lib/prosody /var/log/prosody 2>/dev/null || true

# Run Prosody in foreground
echo "✅ Starting Prosody..."
sudo prosody
