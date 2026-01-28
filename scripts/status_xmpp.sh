#!/bin/bash
# Check XMPP server status

echo "📊 XMPP Server Status"
echo "====================="
sudo prosodyctl status
echo ""
echo "📋 Registered Users:"
sudo prosodyctl mod_listusers 2>/dev/null || echo "   (No users or module not loaded)"
