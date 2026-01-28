-- Prosody XMPP Server Configuration for SPADE Development
-- This configuration is optimized for local agent development

-- Admins
admins = { "admin@localhost" }

-- Modules
modules_enabled = {
    -- Core modules
    "roster";
    "saslauth";
    "tls";
    "dialback";
    "disco";
    "posix";
    "ping";
    "register";
    "admin_adhoc";
    
    -- Nice to have
    "version";
    "uptime";
    "time";
    "carbons";
    "blocklist";
}

modules_disabled = {}

-- Allow registration (for creating agent accounts)
allow_registration = true

-- Disable TLS requirement for local development
c2s_require_encryption = false
s2s_require_encryption = false
s2s_secure_auth = false

-- Authentication
authentication = "internal_plain"

-- Logging
log = {
    info = "/var/log/prosody/prosody.log";
    error = "/var/log/prosody/prosody.err";
    "*syslog";
}

-- Virtual host for localhost
VirtualHost "localhost"
    enabled = true

-- Component for multi-user chat (optional)
Component "conference.localhost" "muc"
    name = "SPADE Agent Chat Rooms"
    restrict_room_creation = false
