#!/bin/bash
# Stop the Prosody XMPP server

echo "🛑 Stopping Prosody XMPP server..."
sudo prosodyctl stop
echo "✅ XMPP server stopped."
