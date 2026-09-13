# SRE Study App

A deliberately simple Flask app built for practicing the SRE study plan:
Docker → Kubernetes → CI/CD → Observability.

## Endpoints

| Method | Path                | Purpose                                      |
|--------|---------------------|-----------------------------------------------|
| GET    | `/`                 | Basic info (version, environment)             |
| GET    | `/health`           | Liveness probe target                         |
| GET    | `/ready`            | Readiness probe target                        |
| POST   | `/admin/ready/on`\|`off` | Toggle readiness (for testing probes)    |
| GET    | `/metrics`          | Prometheus metrics                            |
| GET    | `/api/tasks`        | List tasks                                    |
| POST   | `/api/tasks`        | Create task `{"title": "..."}`                |
| GET    | `/api/tasks/<id>`   | Get one task                                  |
| DELETE | `/api/tasks/<id>`   | Delete a task                                 |
| GET    | `/api/fail`         | Always returns 500 (for alerting practice)    |

## Run locally (with uv)

This project uses [uv](https://docs.astral.sh/uv/) for dependency and
virtual environment management — no manual `venv` + `pip` steps needed.

Install uv (one-time, if you don't have it):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then:

```bash
uv sync            # creates .venv and installs deps (incl. dev group) from uv.lock
uv run python app.py
# app runs on http://localhost:5000
```

Run tests:

```bash
uv run pytest tests/ -v
```

Lint:

```bash
uv run flake8 app.py tests/ --max-line-length=100
```

`uv sync` installs both runtime and dev dependencies by default. For a
production-only install (no dev tools), use `uv sync --no-dev` — this is
what the Dockerfile does.

Add a new dependency:

```bash
uv add requests            # runtime dependency
uv add --dev mypy          # dev-only dependency
```

This updates `pyproject.toml` and `uv.lock` automatically — commit both.

## Run with Docker

The Dockerfile uses `uv` internally (via a static binary copied from
`ghcr.io/astral-sh/uv`) to install dependencies from `uv.lock` — this makes
builds faster and fully reproducible.

```bash
docker build -t sre-study-app:latest .
docker run -p 5000:5000 sre-study-app:latest
```

Or with docker-compose (includes a healthcheck using `/health`):

```bash
docker-compose up --build
```

## Deploy to Kubernetes (kind/minikube)

```bash
# Build the image and load it into your local cluster (kind example)
docker build -t sre-study-app:latest .
kind load docker-image sre-study-app:latest

kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods
kubectl port-forward svc/sre-study-app 8080:80
# visit http://localhost:8080
```

To practice readiness-probe behavior:

```bash
kubectl port-forward svc/sre-study-app 8080:80 &
curl -X POST http://localhost:8080/admin/ready/off
kubectl get pods   # watch it flip to NotReady after the next probe interval
```

## CI/CD (GitHub Actions)

The workflow at `.github/workflows/ci-cd.yml` runs on every push/PR to `main`:

1. **lint** — flake8
2. **test** — pytest
3. **build-and-push** — builds the Docker image and pushes it to
   `ghcr.io/<your-username>/<repo-name>` (only on push to `main`)
4. **deploy** — disabled by default (`if: false`). To enable: add a
   `KUBE_CONFIG` secret (base64-encoded kubeconfig) to your repo, then
   remove the `if: false` line.

### To use this in your own repo

```bash
git init
git add .
git commit -m "Initial commit: SRE study app"
gh repo create sre-study-app --public --source=. --push
# or push manually to a repo you created on github.com
```

No extra secrets are needed for lint/test/build-and-push — `GITHUB_TOKEN`
is provided automatically by GitHub Actions for pushing to GHCR (make sure
your repo's Actions settings allow "Read and write permissions" under
Settings → Actions → General → Workflow permissions).

## Observability

Once running, scrape metrics from `/metrics`. Two custom metrics of note:

- `app_requests_total{method, endpoint, http_status}` — request counts by outcome
- `app_request_latency_seconds{endpoint}` — request latency histogram
- `app_tasks_created_total` — business metric example

Good practice queries once you have Prometheus scraping this app (Week 3
of the study plan):

```promql
rate(app_requests_total{http_status="500"}[5m])
histogram_quantile(0.95, rate(app_request_latency_seconds_bucket[5m]))
```

Hit `/api/fail` a few times and watch the error-rate metric move — useful
for practicing Grafana alert rules.
