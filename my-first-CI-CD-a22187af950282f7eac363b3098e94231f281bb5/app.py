"""Applicazione Flask con rate limiting, health check e version endpoint."""

import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configurazione rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
)
limiter.init_app(app)

def get_version() -> str:
    """Legge la versione dal file version.info."""
    version_file = Path(__file__).parent / "version.info"
    if version_file.exists():
        try:
            with version_file.open("r") as f:
                return f.read().strip()
        except OSError:
            return "unknown"
    return "dev"


def get_agent_name() -> str:
    """Ottiene il nome dell'agente dalle variabili d'ambiente."""
    return os.environ.get("AGENT_NAME", "DefaultAgent")


@app.route("/")
@limiter.limit("100 per minute")
def hello() -> dict:
    """Endpoint principale con rate limiting."""
    agent_name = get_agent_name()
    version = get_version()
    current_time = datetime.now(tz=timezone.utc).strftime("%H:%M")

    message = (
        f"Ciao, mi chiamo {agent_name}, versione {version}, "
        f"sono le ore {current_time}."
    )
    return jsonify({"message": message})


@app.route("/health")
def health_check() -> dict:
    """Health check endpoint - senza rate limiting per le probe Kubernetes."""
    return jsonify(
        {
            "status": "healthy",
            "version": get_version(),
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        },
    )


@app.route("/version")
@limiter.limit("100 per minute")
def version() -> dict:
    """Endpoint dedicato per la versione."""
    return jsonify(
        {
            "version": get_version(),
            "agent_name": get_agent_name(),
        },
    )


@app.errorhandler(429)
def ratelimit_handler(e: Exception) -> tuple[dict, int]:
    """Gestisce il superamento del rate limit."""
    return (
        {
            "error": "Rate limit exceeded",
            "description": str(getattr(e, "description", "")),
            "retry_after": getattr(e, "retry_after", None),
        },
        429,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    host = os.environ.get("HOST", "0.0.0.0")  # noqa: S104  # nosec B104

    # In ambiente container (Docker/K8s) puoi impostare HOST=0.0.0.0
    app.run(host=host, port=port, debug=False)
