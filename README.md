# cc-switch-web

A Web-based model switcher for Claude Code, designed for headless environments like WSL2, remote servers, and terminals.

## Background

[cc-switch](https://github.com/farion1231/cc-switch) is an excellent cross-platform GUI tool for switching Claude Code models. However, it requires a desktop environment, which makes it unsuitable for:

- **WSL2** without GUI support
- **Remote servers** accessed via SSH
- **Headless environments** without display

This project provides a Web interface that can run anywhere Python is available. Access it via browser or make API calls directly.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your API keys

# 3. Run
python app.py

# 4. Open browser
# http://localhost:5000
```

For remote access via SSH tunnel:

```bash
# On WSL2/Server: run with 0.0.0.0
python app.py -H 0.0.0.0

# On local machine: create SSH tunnel
ssh -L 5000:localhost:5000 user@server

# Then open browser at http://localhost:5000
```

## Configuration

Edit `config.py` or use environment variables in `.env`:

```bash
ANTHROPIC_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
MINIMAX_API_KEY=your_key
```

## Comparison with cc-switch

| Feature | cc-switch | cc-switch-web |
|---------|-----------|---------------|
| Interface | Desktop GUI | Web Browser |
| Dependency | Desktop environment | Python + Browser |
| Use Cases | Windows/macOS/Linux desktop | Servers, WSL2, headless |
| Installation | Download installer | pip + Python |
| Features | Full-featured (MCP, Skills, etc.) | Model switching only |

## Project Structure

```
cc-switch-web/
├── app.py              # Flask backend
├── config.py           # Provider configuration
├── cc_switch/
│   └── switcher.py     # Claude Code config handler
├── templates/
│   └── index.html     # Web UI
├── static/
│   ├── style.css
│   └── app.js
└── .env.example        # Environment template
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/providers` | GET | List providers |
| `/api/current` | GET | Get current model |
| `/api/switch` | POST | Switch model |

Example:

```bash
curl -X POST http://localhost:5000/api/switch \
  -H "Content-Type: application/json" \
  -d '{"provider_id": "minimax", "model_id": "MiniMax-M2.7"}'
```

## License

MIT

## Reference

- [cc-switch](https://github.com/farion1231/cc-switch) - The GUI inspiration for this project
- [ccm](https://github.com/foreveryh/claude-code-switch) - Another CLI alternative
