#!/bin/bash
set -e

echo "🚀 Setting up SPADE Agent Development Environment..."

# Update package lists
sudo apt-get update

# Install Prosody XMPP server
echo "📦 Installing Prosody XMPP server..."
sudo apt-get install -y prosody lua-sec

# Configure Prosody for local development
echo "⚙️ Configuring Prosody XMPP server..."
sudo cp .devcontainer/prosody.cfg.lua /etc/prosody/prosody.cfg.lua

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory for Prosody
sudo mkdir -p /var/lib/prosody
sudo chown -R prosody:prosody /var/lib/prosody

echo "✅ Environment setup complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Start XMPP server: ./scripts/start_xmpp.sh"
echo "  2. Create agent credentials: ./scripts/create_agent.sh <username> <password>"
echo "  3. Run the example agent: python agents/basic_agent.py"
