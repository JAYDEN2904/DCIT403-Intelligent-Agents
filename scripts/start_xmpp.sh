#!/bin/bash
# Start the Prosody XMPP server

echo "🌐 Starting Prosody XMPP server..."

# Create log directory if it doesn't exist
sudo mkdir -p /var/log/prosody
sudo chown prosody:prosody /var/log/prosody 2>/dev/null || true

# Try systemctl first (for systemd-based systems like Codespaces)
if command -v systemctl &> /dev/null && systemctl --version &> /dev/null; then
    echo "   Using systemctl..."
    sudo systemctl start prosody
    sleep 2
    
    if sudo systemctl is-active --quiet prosody; then
        echo "✅ XMPP server is running!"
        echo "   - Client port: 5222"
        echo "   - Admin port: 5280"
        sudo systemctl status prosody --no-pager
        exit 0
    fi
fi

# Fallback: try prosodyctl with --force flag
echo "   Trying prosodyctl with --force..."
sudo prosodyctl --force start

sleep 2
if sudo prosodyctl status 2>/dev/null | grep -q "running"; then
    echo "✅ XMPP server is running!"
    echo "   - Client port: 5222"
    echo "   - Admin port: 5280"
else
    echo "❌ Failed to start XMPP server"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   1. Check logs: sudo cat /var/log/prosody/prosody.err"
    echo "   2. Try manual start: sudo prosody"
    echo "   3. Check config: sudo prosodyctl check"
    exit 1
fi
