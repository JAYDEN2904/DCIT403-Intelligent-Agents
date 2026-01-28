# LAB 1: SPADE Agent Development Environment

## 🎯 Objective

Configure the Python agent development environment and deploy a basic SPADE agent.

## 📚 Background

The **Smart Python Agent Development Environment (SPADE)** enables the creation of intelligent agents using:
- Asynchronous behaviors
- Message-based interaction over XMPP (Extensible Messaging and Presence Protocol)

## 🚀 Quick Start

### 1. Launch GitHub Codespaces

Click the green "Code" button on GitHub and select "Create codespace on main". The environment will automatically set up with:
- Python 3.11
- Prosody XMPP server
- SPADE and dependencies

### 2. Verify Installation

```bash
# Check Python version
python --version

# Verify SPADE installation
python -c "import spade; print(f'SPADE version: {spade.__version__}')"
```

### 3. Start the XMPP Server

```bash
./scripts/start_xmpp.sh
```

### 4. Create Agent Credentials

```bash
# Create a basic agent
./scripts/create_agent.sh agent1 secret123

# For messaging demo, create two agents
./scripts/create_agent.sh sender secret123
./scripts/create_agent.sh receiver secret123
```

### 5. Run Your First Agent

```bash
python agents/basic_agent.py
```

## 📁 Project Structure

```
.
├── .devcontainer/
│   ├── devcontainer.json    # Codespaces configuration
│   ├── setup.sh             # Post-create setup script
│   └── prosody.cfg.lua      # XMPP server configuration
├── agents/
│   ├── basic_agent.py       # Simple agent with behaviors
│   └── messaging_agent.py   # Agent-to-agent communication
├── scripts/
│   ├── start_xmpp.sh        # Start XMPP server
│   ├── stop_xmpp.sh         # Stop XMPP server
│   ├── create_agent.sh      # Create agent credentials
│   └── status_xmpp.sh       # Check server status
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Available Scripts

| Script | Description |
|--------|-------------|
| `./scripts/start_xmpp.sh` | Start the Prosody XMPP server |
| `./scripts/stop_xmpp.sh` | Stop the XMPP server |
| `./scripts/create_agent.sh <user> <pass>` | Create agent credentials |
| `./scripts/status_xmpp.sh` | Check server status |

## 📝 Lab Tasks

### Task 1: Basic Agent

The `basic_agent.py` demonstrates:
- Agent creation and connection
- **OneShotBehaviour**: Runs once when agent starts
- **CyclicBehaviour**: Runs repeatedly (heartbeat)
- Agent lifecycle management

### Task 2: Agent Communication

The `messaging_agent.py` demonstrates:
- Two agents communicating via XMPP
- Message sending with metadata
- Message receiving with templates
- Coordinated agent behavior

## 🐛 Troubleshooting

### XMPP Connection Failed
```bash
# Check if server is running
./scripts/status_xmpp.sh

# Restart the server
./scripts/stop_xmpp.sh
./scripts/start_xmpp.sh
```

### Agent Already Exists
```bash
# This is fine - the agent credentials already exist
# You can proceed with running your agent
```

### Permission Denied on Scripts
```bash
chmod +x scripts/*.sh
```

## 📖 SPADE Documentation

- [SPADE Documentation](https://spade-mas.readthedocs.io/)
- [SPADE GitHub Repository](https://github.com/javipalanca/spade)
- [XMPP Protocol](https://xmpp.org/)

## 🎓 Learning Resources

- **Behaviors**: Learn about different behavior types (OneShotBehaviour, CyclicBehaviour, PeriodicBehaviour, FSMBehaviour)
- **Messages**: Understand FIPA-ACL message structure and performatives
- **Templates**: Use templates to filter incoming messages

---

*Happy Agent Development! 🤖*
