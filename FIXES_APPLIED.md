# Fixes Applied to SPADE Agent Issues

## Problems Solved

### 1. **XMPP Server Not Running**

- **Error**: "Error during the connection with the server"
- **Cause**: Prosody XMPP server was not started
- **Fix**: Started Prosody service with `sudo service prosody start`

### 2. **Invalid Certificate Trust Chain**

- **Error**: "CERT: Invalid certificate trust chain"
- **Cause**: Self-signed certificate issues with localhost
- **Fixes Applied**:
  - Created proper self-signed SSL certificates for localhost
  - Configured Prosody to use the certificates
  - Set `c2s_require_encryption = false` to not require TLS for client connections
  - Added certificate paths to Prosody configuration

### 3. **Missing Prosody Configuration**

- **Error**: "There is no 'pidfile' option in the configuration file"
- **Cause**: Incomplete Prosody configuration
- **Fixes Applied**:
  - Added `pidfile = "/var/run/prosody/prosody.pid"` to prosody.cfg.lua
  - Created necessary directories `/var/run/prosody` and `/var/log/prosody`
  - Set proper ownership to prosody user

### 4. **Invalid Agent.start() Parameters**

- **Error**: "Agent.start() got an unexpected keyword argument 'verify_security'"
- **Cause**: Invalid `verify_security` parameter in sensor_agent.py and messaging_agent.py
- **Fixes Applied**:
  - Removed `verify_security=False` from all agent.start() calls
  - Replaced with correct `auto_register=True` parameter
  - Added SSL warning suppression for certificate messages

## Files Modified

### 1. `.devcontainer/prosody.cfg.lua`

- Added pidfile configuration
- Added SSL certificate paths
- Disabled encryption requirement for local development

### 2. `agents/basic_agent.py`

- Added SSL warning suppression for development
- Cleaned up connection setup
- Added `auto_register=True` parameter

### 3. `agents/sensor_agent.py`

- Removed invalid `verify_security=False` parameter
- Added SSL warning suppression
- Changed to `auto_register=True`

### 4. `agents/messaging_agent.py`

- Removed invalid `verify_security=False` parameter from both receiver and sender
- Added SSL warning suppression
- Changed to `auto_register=True`

## How to Run

### Step 1: Ensure Prosody is Running

```bash
sudo service prosody start
# or check status
sudo service prosody status
```

### Step 2: Run Any Agent

```bash
# Basic Agent (Lab 1)
python agents/basic_agent.py

# Messaging Agent (Lab 1 Extended)
python agents/messaging_agent.py

# Sensor Agent (Lab 2)
python agents/sensor_agent.py
```

## Verification

### Basic Agent

```
🔌 Connecting agent: jayden@localhost
🚀 [jayden] Agent started at HH:MM:SS
   JID: jayden@localhost
   Available: True
💓 [jayden] Heartbeat #1 at HH:MM:SS
...
✅ Agent stopped
```

### Sensor Agent

```
🔌 Connecting SensorAgent: sensor@localhost
👁️  [sensor] Percept #1 at 2026-01-28 HH:MM:SS
   Damage:   4 | Water: 0.00 m | Fire risk:  18 | Accessible: True
...
✅ SensorAgent stopped
```

### Messaging Agent

```
🚀 [receiver] Receiver agent started, waiting for messages...
🚀 [sender] Sender agent started
📤 [sender] Starting to send messages...
📥 [receiver] Received at HH:MM:SS
...
✅ All agents stopped
```

## Notes for Future Development

- The Prosody XMPP server runs in the background
- It's configured for local development with encryption disabled
- Self-signed certificates are used for localhost
- The `auto_register=True` parameter allows agents to auto-register without manual credential creation
- For production use, you should use proper SSL certificates and enable encryption

## Troubleshooting

If issues persist:

1. **Check if Prosody is running**:

   ```bash
   ps aux | grep prosody
   ```

2. **Restart Prosody**:

   ```bash
   sudo killall lua5.4
   sleep 1
   sudo service prosody start
   ```

3. **Check logs**:

   ```bash
   sudo tail -f /var/log/prosody/prosody.log
   ```

4. **Verify certificates exist**:
   ```bash
   ls -la /etc/prosody/certs/
   ```
