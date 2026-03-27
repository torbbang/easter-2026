# 🐰 Easter Telnet Animation

![Demo](demo.gif)

ASCII art Easter animation served over telnet. A decorated egg cracks open, a bunny emerges, hops across a field of flowers and mini eggs, and finishes with a "Happy Easter! / God påske!" finale — all in 80×24 characters with ANSI color.

## Quick Start

```bash
python3 easter.py
```

## Run as a Telnet Server (Docker/Podman)

```bash
podman build -t easter .
podman run -p 2323:23 easter
```

Then connect:

```bash
telnet localhost 2323
```

Each connection gets its own animation. When it finishes, the connection closes.

## Requirements

- **Local:** Python 3.6+ (stdlib only, zero dependencies)
- **Container:** Alpine + ucspi-tcp6 (handled by the Dockerfile)
