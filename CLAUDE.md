# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**cc-switch-web** - A Web-based model switcher for Claude Code, designed for headless environments like WSL2, remote servers, and terminals.

Reference: [cc-switch](https://github.com/farion1231/cc-switch)

## Architecture

- **Backend**: Python Flask with REST API
- **Frontend**: Vanilla HTML/CSS/JS (no frameworks)
- **Communication**: HTTP REST API
- **Target**: WSL2 headless environment with browser access

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask main program, API endpoints |
| `config.py` | Provider and model configuration |
| `cc_switch/switcher.py` | Claude Code config file read/write (uses `~/.claude/settings.json` with `env` structure) |
| `templates/index.html` | Web UI template |
| `static/style.css` | Styles |
| `static/app.js` | Frontend logic |

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Run with custom host/port
python app.py -H 0.0.0.0 -p 8080
```

## Claude Code Configuration

Claude Code stores configuration at `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "sk-..."
  }
}
```

## API Endpoints

- `GET /` - Web UI
- `GET /health` - Health check
- `GET /api/providers` - List available providers (excludes API keys)
- `GET /api/current` - Get current provider and model
- `POST /api/switch` - Switch model (body: `{"provider_id": "...", "model_id": "..."}`)
- `GET /api/config_status` - Config file status

## Implementation Notes

Proxy is configured in `~/.zshrc` to use `127.0.0.1:7897` for HTTP/HTTPS traffic.

This project was built with reference to cc-switch's architecture but simplified to a pure Python Flask implementation suitable for WSL2's headless environment.
