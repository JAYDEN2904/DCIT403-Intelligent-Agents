#!/bin/bash
# Stop the Prosody XMPP server

echo "🛑 Stopping Prosody XMPP server..."

# Try systemctl first
if command -v systemctl &> /dev/null && systemctl --version &> /dev/null; then
    sudo systemctl stop prosody 2>/dev/null
fi

# Also try prosodyctl as fallback
sudo prosodyctl --force stop 2>/dev/null || true

echo "✅ XMPP server stopped."
