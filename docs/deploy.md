# Deploying MuseForge MCP behind Cloudflare Tunnel

This guide deploys the MuseForge MCP server on an existing Linux VPS (Ubuntu/Debian)
and fronts it with **Cloudflare Tunnel**. The result is:

- HTTPS automatically (Cloudflare-issued cert, no Let's Encrypt needed)
- No inbound ports open on the VPS (cloudflared is outbound-only)
- DDoS protection + WAF (Cloudflare free tier)
- Zero code changes vs. local — the same `museforge-mcp-http` you just smoke-tested.

```
Internet -> Cloudflare edge (HTTPS, WAF)
                 |
                 v (outbound tunnel)
         +---------------+
         |  cloudflared  |   <-- on the VPS, outbound TCP only
         +-------+-------+
                 |
                 v
       127.0.0.1:8000  museforge-mcp-http (uvicorn)
```

If you'd rather run on Fly.io or use Cloudflare **Workers** (requires a Durable-Object
rewrite of the token store), see `docs/roadmap.md`.

---

## Prerequisites

- A Linux VPS (Ubuntu 22.04+ recommended) you can `ssh` into.
- Python 3.12+.
- A domain managed in Cloudflare (free tier is enough).
- The OAuth credentials already in your local `.env` (see Phase 4 of the project brief).

## One-time setup on the server

### 1. Install Python 3.12 + venv

```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv git curl
sudo useradd --system --shell /usr/sbin/nologin --home /opt/museforge --create-home museforge || true
sudo -u museforge mkdir -p /opt/museforge
```

### 2. Clone + install

```bash
sudo -u museforge git clone https://github.com/Lunar-feedmob/museforge.git /opt/museforge
cd /opt/museforge
sudo -u museforge python3.12 -m venv .venv
sudo -u museforge ./venv/bin/pip install -U pip
sudo -u museforge ./venv/bin/pip install -e ".[mcp-http]"
```

### 3. Create the persistent data directory + .env

```bash
sudo -u museforge mkdir -p /opt/museforge/data
sudo cp deploy/.env.production.example /opt/museforge/.env
sudo chown museforge:museforge /opt/museforge/.env
sudo chmod 600 /opt/museforge/.env
# Edit /opt/museforge/.env and paste the real values from your local .env.
sudo -u museforge $EDITOR /opt/museforge/.env
```

Re-seed the knowledge base once:

```bash
sudo -u museforge /opt/museforge/.venv/bin/python /opt/museforge/scripts/seed_data.py
```

### 4. Install the systemd unit for `museforge-mcp-http`

```bash
sudo cp deploy/museforge-mcp-http.service /etc/systemd/system/museforge-mcp-http.service
sudo systemctl daemon-reload
sudo systemctl enable --now museforge-mcp-http
sudo systemctl status museforge-mcp-http   # should be active (running)
sudo journalctl -u museforge-mcp-http -f   # tail logs
```

Smoke test on the VPS:

```bash
curl -s http://127.0.0.1:8000/.well-known/oauth-authorization-server | python -m json.tool
```

## Set up Cloudflare Tunnel

### 5. Install cloudflared

```bash
# Add the Cloudflare package repo and install (Ubuntu/Debian).
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
  | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update
sudo apt install -y cloudflared
cloudflared --version
```

### 6. Authenticate + create the tunnel

```bash
# 6a. One-time login (opens a browser; you sign in to Cloudflare and pick the zone).
cloudflared login

# 6b. Create the tunnel (note the printed UUID — you'll need it below).
cloudflared tunnel create museforge
# => Tunnel credentials written to /root/.cloudflared/<UUID>.json (or ~/.cloudflared/... for your user).

# 6c. Copy credentials to a stable location cloudflared can read as the nobody user.
sudo mkdir -p /etc/cloudflared
sudo cp ~/.cloudflared/<UUID>.json /etc/cloudflared/<UUID>.json
sudo chmod 600 /etc/cloudflared/<UUID>.json

# 6d. Drop in the tunnel config (replace REPLACE_WITH_TUNNEL_UUID + hostname).
sudo cp deploy/cloudflared-config.yml /etc/cloudflared/config.yml
sudo sed -i "s/REPLACE_WITH_TUNNEL_UUID/<UUID>/g" /etc/cloudflared/config.yml
sudo sed -i "s|museforge.yourdomain.com|museforge.YOUR-REAL-DOMAIN|g" /etc/cloudflared/config.yml
sudo systemctl edit cloudflared   # (optional — install the dedicated service below)
```

### 7. Install the systemd unit for cloudflared + create the DNS route

```bash
sudo cp deploy/cloudflared.service /etc/systemd/system/cloudflared.service
sudo systemctl daemon-reload

# Create the DNS route (do this AFTER the config.yml is in place).
cloudflared tunnel route dns <UUID> museforge.YOUR-REAL-DOMAIN

# Start it.
sudo systemctl enable --now cloudflared
sudo systemctl status cloudflared   # should be active (running), connected to <region>
sudo journalctl -u cloudflared -f
```

## Update Google Cloud Console

The production redirect URI **must** be registered on your OAuth client.

1. https://console.cloud.google.com → APIs & Services → Credentials
2. Open the MuseForge MCP OAuth client.
3. Authorized redirect URIs — add the production URL:
   ```
   https://museforge.YOUR-REAL-DOMAIN/callback
   ```
   (keep `http://localhost:8000/callback` if you also develop locally).

## Verify end-to-end

```bash
PUBLIC=https://museforge.YOUR-REAL-DOMAIN

# Discovery endpoints (no auth)
curl -s "$PUBLIC/.well-known/oauth-authorization-server" | python -m json.tool

# Should NOT be 502/521 — Cloudflare is proxying through.
```

Then run `python scripts/e2e_oauth_smoke.py "$PUBLIC"` from your laptop. The browser
portion still needs your `@feedmob.com` sign-in, but everything else runs end-to-end through
the public URL.

## Operations

```bash
sudo systemctl status museforge-mcp-http cloudflared
sudo journalctl -u museforge-mcp-http -f
sudo journalctl -u cloudflared -f

# Restart after code updates:
cd /opt/museforge && sudo -u museforge git pull
sudo -u museforge /opt/museforge/.venv/bin/pip install -e ".[mcp-http]"
sudo systemctl restart museforge-mcp-http

# Update seed knowledge (after editing scripts/seed_data.py):
sudo systemctl stop museforge-mcp-http
sudo -u museforge /opt/museforge/.venv/bin/python /opt/museforge/scripts/seed_data.py
sudo systemctl start museforge-mcp-http
```

## Production notes / known V0 limitations

- **In-memory token store.** `InMemoryAuthStore` does not survive restarts and is not
  shared across multiple `museforge-mcp-http` instances. Run a **single** process for V0.
  For multi-instance or persistent tokens, replace `InMemoryAuthStore` with a Redis-backed
  implementation (the `museforge.auth.store` interface is designed for this).
- **Backup `/opt/museforge/data`.** It's the only stateful part (besides the in-memory
  tokens). `tar` it and copy off-host.
- **Watch the journal.** `cloudflared` will reconnect automatically if the tunnel drops;
  `museforge-mcp-http` restarts on failure (5s delay). For alerts, hook
  `systemctl is-active museforge-mcp-http cloudflared` into your monitor of choice.

## Alternative: direct HTTPS on the VPS (no Cloudflare)

If you'd rather not use Cloudflare, a Caddyfile is in `deploy/Caddyfile`. With Caddy:

```bash
sudo apt install -y caddy
# Point your domain's DNS A record to the VPS's public IP, then:
sudo cp deploy/Caddyfile /etc/caddy/Caddyfile
sudo sed -i "s/museforge.example.com/museforge.YOUR-DOMAIN/g" /etc/caddy/Caddyfile
sudo systemctl reload caddy
# Caddy auto-issues Let's Encrypt certs.
```

The trade-off vs. Cloudflare Tunnel: you open ports 80/443 on the VPS and own TLS/HTTPS
yourself. Cloudflare Tunnel is the simpler, more secure default for V0.
