"""
SRE Study App
A deliberately simple Flask application used to practice:
  - Containerization (Docker)
  - Orchestration (Kubernetes: liveness/readiness probes, ConfigMaps)
  - CI/CD (GitHub Actions)
  - Observability (Prometheus metrics, structured logging)

Endpoints:
  GET  /              -> basic info
  GET  /health         -> liveness probe target
  GET  /ready           -> readiness probe target (can be toggled "not ready")
  GET  /metrics        -> Prometheus metrics
  GET  /api/tasks      -> list tasks
  POST /api/tasks       -> create a task {"title": "..."}
  GET  /api/tasks/<id>  -> get single task
  DELETE /api/tasks/<id> -> delete a task
  GET  /api/fail        -> intentionally returns 500, for practicing alerting
"""

import logging
import os
import time
import uuid

from flask import Flask, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "0.1.0")
APP_ENV = os.environ.get("APP_ENV", "development")

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger("sre-study-app")

# In-memory "database" — resets on restart, intentionally simple.
TASKS = {}

# Readiness can be flipped off to simulate a pod that's alive but not ready
# (useful for practicing readiness-probe behavior in Kubernetes).
READY = {"value": True}

# ---------------------------------------------------------------------------
# Prometheus metrics
# ---------------------------------------------------------------------------

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    ["endpoint"],
)

TASKS_CREATED = Counter(
    "app_tasks_created_total",
    "Total number of tasks created",
)


@app.before_request
def start_timer():
    request.start_time = time.time()


@app.after_request
def record_metrics(response):
    latency = time.time() - getattr(request, "start_time", time.time())
    endpoint = request.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(
        method=request.method, endpoint=endpoint, http_status=response.status_code
    ).inc()
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    return jsonify(
        {
            "message": "SRE Study App",
            "version": APP_VERSION,
            "environment": APP_ENV,
        }
    )


@app.route("/health")
def health():
    """Liveness probe: should only fail if the process itself is broken."""
    return jsonify({"status": "ok"}), 200


@app.route("/ready")
def ready():
    """Readiness probe: can be toggled to simulate 'not ready' states."""
    if READY["value"]:
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not ready"}), 503


@app.route("/admin/ready/<mode>", methods=["POST"])
def set_ready(mode):
    """
    Toggle readiness for testing probe behavior.
    POST /admin/ready/on  or /admin/ready/off
    """
    if mode not in ("on", "off"):
        return jsonify({"error": "mode must be 'on' or 'off'"}), 400
    READY["value"] = mode == "on"
    logger.info(f"Readiness set to {READY['value']}")
    return jsonify({"ready": READY["value"]})


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify(list(TASKS.values()))


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    task_id = str(uuid.uuid4())
    task = {"id": task_id, "title": title, "done": False}
    TASKS[task_id] = task
    TASKS_CREATED.inc()
    logger.info(f"Created task {task_id}")
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": "not found"}), 404
    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in TASKS:
        return jsonify({"error": "not found"}), 404
    del TASKS[task_id]
    return "", 204


@app.route("/api/fail")
def fail():
    """Intentionally broken endpoint for practicing alerting on error rates."""
    logger.error("Simulated failure triggered on /api/fail")
    raise RuntimeError("Simulated failure for alerting practice")


@app.errorhandler(RuntimeError)
def handle_runtime_error(e):
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
