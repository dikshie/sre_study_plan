# 30-Day SRE Study Plan (2 hrs/day)

**Starting point:** Strong in FreeBSD, Linux, shell scripting, Python.
**Goal:** Build working knowledge of containers, Kubernetes, CI/CD, IaC, and observability — enough to speak confidently in interviews and demonstrate hands-on projects.

**Total time budget:** ~60 hours over 30 days. Scope is trimmed to prioritize depth on Kubernetes, CI/CD, and observability since those are the biggest gaps from your background. Terraform and Go get lighter, "functional" coverage.

---

## Week 1: Docker + Kubernetes Foundations

### Day 1 (2h) — Docker Fundamentals
- **Study (45 min):** Docker Curriculum — https://docker-curriculum.com/
- **Hands-on (75 min):**
  - Install Docker: https://docs.docker.com/engine/install/
  - Take one of your existing Python scripts and containerize it
  - Write a Dockerfile using multi-stage build
  - Reference: https://docs.docker.com/build/building/multi-stage/

### Day 2 (2h) — Docker Networking & Compose
- **Study (30 min):** https://docs.docker.com/compose/gettingstarted/
- **Hands-on (90 min):**
  - Build a docker-compose.yml with 2 services (e.g., a Python Flask app + Redis or Postgres)
  - Practice: `docker network`, `docker volume`, inspect containers with `docker inspect`
  - Tutorial repo to follow: https://github.com/docker/awesome-compose (pick the flask-redis or python-postgres example)

### Day 3 (2h) — Kubernetes Concepts (Theory)
- **Study (2h):** Kubernetes official concepts docs, read (don't skip) these pages:
  - https://kubernetes.io/docs/concepts/overview/
  - https://kubernetes.io/docs/concepts/workloads/pods/
  - https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Take notes on: Pod, ReplicaSet, Deployment, Service, Namespace

### Day 4 (2h) — Local Cluster Setup + First Deployment
- **Hands-on (2h):**
  - Install `kind`: https://kind.sigs.k8s.io/docs/user/quick-start/
  - Install `kubectl`: https://kubernetes.io/docs/tasks/tools/
  - Create a cluster, deploy your Day 1 containerized app as a Deployment + Service
  - Best guide to follow step-by-step: https://kubernetes.io/docs/tutorials/kubernetes-basics/

### Day 5 (2h) — Kubernetes ConfigMaps, Secrets, Probes
- **Study + Hands-on (2h):**
  - https://kubernetes.io/docs/concepts/configuration/configmap/
  - https://kubernetes.io/docs/concepts/configuration/secret/
  - https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
  - Add a ConfigMap + liveness/readiness probe to your Day 4 deployment

### Day 6 (2h) — Ingress + Resource Limits
- **Hands-on (2h):**
  - Install an ingress controller in kind: https://kind.sigs.k8s.io/docs/user/ingress/
  - Add resource requests/limits to your deployment
  - Reference: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

### Day 7 (2h) — Helm Basics
- **Study (30 min):** https://helm.sh/docs/intro/quickstart/
- **Hands-on (90 min):**
  - Install Helm, convert your app's manifests into a basic Helm chart
  - Guide: https://helm.sh/docs/chart_template_guide/getting_started/
  - Deploy via `helm install`, practice `helm upgrade` and `helm rollback`

**Week 1 checkpoint:** You should be able to containerize an app, deploy it to a local k8s cluster with a Helm chart, and explain Pods/Deployments/Services/ConfigMaps/Secrets confidently.

---

## Week 2: CI/CD Pipelines

### Day 8 (2h) — GitHub Actions Basics
- **Study (30 min):** https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
- **Hands-on (90 min):**
  - Create a repo with your Python app
  - Write a workflow: lint (flake8/black) → run tests (pytest)
  - Follow: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

### Day 9 (2h) — Build & Push Docker Images in CI
- **Hands-on (2h):**
  - Extend your workflow: build Docker image, push to Docker Hub or GHCR
  - Guide: https://docs.github.com/en/actions/publishing-packages/publishing-docker-images
  - Use GitHub Secrets for registry credentials: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

### Day 10 (2h) — CD to Kubernetes
- **Hands-on (2h):**
  - Add a deploy step that runs `kubectl apply` or `helm upgrade` against your kind cluster (or use a self-hosted runner concept — for local practice, simulate with a script step)
  - Alternative real-world pattern to study: GitOps with ArgoCD — https://argo-cd.readthedocs.io/en/stable/getting_started/ (read only, hands-on optional if time allows on Day 14)

### Day 11 (2h) — Pipeline Patterns
- **Study + practice (2h):**
  - Environment promotion (dev/staging/prod), branch-based triggers
  - Read: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
  - Add a manual approval gate for a "production" environment in your workflow

### Day 12 (2h) — Secrets, Caching, Matrix Builds
- **Study + practice (2h):**
  - https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
  - Add dependency caching to your pipeline
  - Read about matrix builds: https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs

### Day 13 (2h) — Rollback Strategies (Theory + Light Practice)
- **Study (60 min):** Blue-green, canary, rolling deployments
  - https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/
- **Hands-on (60 min):** Practice `kubectl rollout undo` and `helm rollback` on your app

### Day 14 (2h) — Catch-up / GitOps intro
- Use this day to finish anything from Days 8–13
- If ahead: skim ArgoCD getting started guide above for conceptual exposure (very commonly asked about in SRE interviews)

**Week 2 checkpoint:** You should have a working CI/CD pipeline: push code → lint/test → build image → push to registry → deploy to k8s, and be able to explain rollback strategies.

---

## Week 3: Infrastructure as Code + Observability

### Day 15 (2h) — Terraform Basics
- **Study (30 min):** https://developer.hashicorp.com/terraform/intro
- **Hands-on (90 min):** Official interactive tutorial: https://developer.hashicorp.com/terraform/tutorials/aws-get-started (use AWS free tier, or LocalStack if avoiding cloud costs: https://docs.localstack.cloud/getting-started/)

### Day 16 (2h) — Terraform State, Variables, Modules
- **Study + practice (2h):**
  - https://developer.hashicorp.com/terraform/language/state
  - https://developer.hashicorp.com/terraform/language/values/variables
  - Refactor your Day 15 config to use variables and outputs

### Day 17 (2h) — Provision a Kubernetes Cluster with Terraform
- **Hands-on (2h):**
  - AWS EKS: https://developer.hashicorp.com/terraform/tutorials/kubernetes/eks
  - (This is a stretch on 2 hrs — if it runs long, just read through carefully and run partial steps; understanding the pattern matters more than finishing)

### Day 18 (2h) — Prometheus Basics
- **Study (30 min):** https://prometheus.io/docs/introduction/overview/
- **Hands-on (90 min):**
  - Install Prometheus in your kind cluster via Helm: https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack
  - Explore default dashboards/metrics

### Day 19 (2h) — Instrument Your App + PromQL
- **Hands-on (2h):**
  - Add the `prometheus_client` Python library to your app: https://github.com/prometheus/client_python
  - Expose a `/metrics` endpoint, scrape it from Prometheus
  - Practice basic PromQL queries: https://prometheus.io/docs/prometheus/latest/querying/basics/

### Day 20 (2h) — Grafana Dashboards + Alerting
- **Hands-on (2h):**
  - Grafana comes with kube-prometheus-stack — access it, build a dashboard for your app's metrics
  - Guide: https://grafana.com/tutorials/grafana-fundamentals/
  - Set up one alert rule (e.g., high error rate or pod restart count)

### Day 21 (2h) — Logging with Loki
- **Study + hands-on (2h):**
  - https://grafana.com/docs/loki/latest/get-started/
  - Install Loki + Promtail via Helm, view your app's logs in Grafana
  - Chart: https://github.com/grafana/helm-charts/tree/main/charts/loki-stack

**Week 3 checkpoint:** You should be able to explain and demo metrics collection (Prometheus), dashboards/alerts (Grafana), and log aggregation (Loki) for a running app.

---

## Week 4: SRE Concepts, Capstone Project, Interview Prep

### Day 22 (2h) — SRE Core Concepts
- **Study (2h):** Google's SRE Book (free) — read these chapters:
  - Ch. 4 (Service Level Objectives): https://sre.google/sre-book/service-level-objectives/
  - Ch. 5 (Eliminating Toil): https://sre.google/sre-book/eliminating-toil/
  - Take notes on SLI vs SLO vs SLA, error budgets

### Day 23 (2h) — Incident Response & Postmortems
- **Study (2h):**
  - https://sre.google/sre-book/postmortem-culture/
  - https://sre.google/workbook/incident-response/
  - Write a mock postmortem for a fictional outage (great interview prep artifact)

### Day 24 (2h) — Capstone Project: Wire It Together (Part 1)
- **Hands-on (2h):** Combine everything into one project:
  - App containerized (Docker) ✅ already done
  - Deployed via Helm to k8s ✅ already done
  - CI/CD auto-deploys on push ✅ already done
  - Add: Terraform-provisioned namespace/resources (even locally scoped) if time allows
  - Document architecture in a README

### Day 25 (2h) — Capstone Project (Part 2)
- **Hands-on (2h):**
  - Ensure Prometheus + Grafana + Loki are all monitoring this same app
  - Add a Grafana dashboard link + a sample alert to your README
  - Push everything to a public GitHub repo — this becomes your portfolio piece

### Day 26 (2h) — Go Fundamentals (Reading Level)
- **Study + light hands-on (2h):**
  - Tour of Go: https://go.dev/tour/welcome/1
  - Goal: read and understand simple Go programs (many SRE tools like kubectl, Prometheus, Terraform are written in Go) — not fluency, just comfort reading it
  - Write one simple CLI tool (e.g., a basic health-check pinger)

### Day 27 (2h) — Ansible Basics (Light Coverage)
- **Study + hands-on (2h):**
  - https://docs.ansible.com/ansible/latest/getting_started/index.html
  - Write a simple playbook (e.g., install a package, copy a config file) — gives you IaC breadth beyond Terraform

### Day 28 (2h) — Review Kubernetes + Docker Interview Questions
- **Study (2h):**
  - Review your own project — be ready to explain every design decision
  - Common questions: difference between Deployment/StatefulSet, how a Service routes traffic, what happens on `kubectl apply`, image layer caching

### Day 29 (2h) — Review CI/CD + Observability Interview Questions
- **Study (2h):**
  - Be ready to explain: your pipeline stages, how you'd add canary deployment, what SLIs you'd track for your capstone app, how you'd debug a pod that's crash-looping

### Day 30 (2h) — Mock Interview + Final Polish
- **Practice (2h):**
  - Write out a 2-minute verbal walkthrough of your capstone project (many interviews start with "walk me through a project you built")
  - Review your README, clean up the repo, make sure it's presentable
  - Optional: record yourself explaining it, listen back

---

## Key Resources Summary (Bookmark These)

| Area | Resource |
|---|---|
| Docker | https://docs.docker.com/get-started/ |
| Kubernetes | https://kubernetes.io/docs/tutorials/kubernetes-basics/ |
| Helm | https://helm.sh/docs/ |
| GitHub Actions | https://docs.github.com/en/actions |
| Terraform | https://developer.hashicorp.com/terraform/tutorials |
| Prometheus | https://prometheus.io/docs/ |
| Grafana | https://grafana.com/tutorials/ |
| Loki | https://grafana.com/docs/loki/latest/ |
| SRE Book (free) | https://sre.google/books/ |
| Go Tour | https://go.dev/tour/ |
| Ansible | https://docs.ansible.com/ansible/latest/getting_started/ |

## Notes on Pace
- If a day's hands-on runs over 2 hours, stop and continue the next day rather than skipping the concept study — understanding beats finishing.
- The capstone project (Days 24–25) is the single most valuable thing you'll produce — it's concrete proof of skills for interviews, more convincing than any certificate.
- If you have to cut something for time, cut Ansible (Day 27) or deep Terraform (Day 17) before cutting Kubernetes or observability — those two are what SRE interviews probe hardest.
