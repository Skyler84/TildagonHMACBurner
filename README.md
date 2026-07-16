# Tildagon HMAC Burner

## Getting Started

### Client

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install .[client-remote]
export API_TOKEN=<insert API Token>
python3 tildagon_hmac_burner/client --loop --port-filter="/dev/tty(ACM|USB)xxx" --remote="https://<your-server>/"
```

### Server

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install .[server]
export MASTER_SECRET=<insert tildagon HMAC secret here>
python3 tildagon_hmac_burner/server
```