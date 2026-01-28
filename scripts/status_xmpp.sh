#!/bin/bash
# Check XMPP server status

echo "📊 XMPP Server Status"
echo "====================="

# Try systemctl first
if command -v systemctl &> /dev/null && systemctl --version &> /dev/null; then
    sudo systemctl status prosody --no-pager 2>/dev/null || sudo prosodyctl status
else
    sudo prosodyctl status
fi

echo ""
echo "📋 Registered Users:"
sudo prosodyctl mod_listusers 2>/dev/null || echo "   (Run: sudo prosodyctl about to see registered users)"
