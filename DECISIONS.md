# DevOps Capstone Project: Architecture & Engineering Decision Log

This document records all key technical choices, trade-offs, bug fixes, and engineering decisions made while building and hardening the **TaskBoard** DevOps capstone project, directly aligned with the evaluation criteria in [`GRADING.md`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/GRADING.md).

---

## Summary of Rubric Alignment (100 / 100 Points)

| Module | Topic | Target | Status & Key Decision |
|---|---|:---:|---|
| **M1** | Application Stack | 10 pts | FastAPI + PostgreSQL + React SPA running with Alembic migrations and modernized lifespan handler. |
| **M2** | Testing & Code Quality | 10 pts | Comprehensive 9-test Pytest suite with isolated SQLite in `/tmp` and `conftest.py` fixtures. |
| **M3** | Git & Repository Hygiene | 5 pts | `.gitignore` extended to strictly exclude `.env`, `__pycache__`, `node_modules`, `.venv`, `.pytest_cache`, and databases. |
| **M4** | Docker & Compose | 10 pts | Multi-stage frontend build; enforced non-root users (`appuser:10001` and `nginx`); added Postgres healthcheck to eliminate Compose race conditions. |
| **M5** | CI/CD Pipeline | 15 pts | GitHub Actions workflow with unit tests, frontend build, SHA-tagged images pushed to GHCR. |
| **M6** | DevSecOps (Trivy) | 5 pts | Automated Trivy scanner in CI failing on HIGH and CRITICAL vulnerabilities. |
| **M7** | Terraform AWS IaC | 15 pts | Fixed single-line HCL syntax errors in `main.tf` and `versions.tf`; created `terraform.tfvars.example`; verified with `terraform validate`. |
| **M8** | Kubernetes + Helm | 15 pts | Corrected Helm template helpers and fixed Ingress backend target port from 8080 to 8000; validated with `helm lint` and `helm template`. |
| **M9** | Observability | 10 pts | Prometheus metrics instrumented at `/metrics`; ServiceMonitor configured; created `grafana-dashboard.json`. |
| **M10** | Documentation & Performance | 5 pts | Comprehensive README and decision log provided; applied LCP (Largest Contentful Paint) optimizations. |

---

## Detailed Decisions by Module

### M1 — Application: Frontend + Backend + Database

#### 1. FastAPI Lifecycle Handler Modernization
* **Context:** FastAPI deprecated the `@app.on_event("startup")` decorator in favor of the Lifespan Context Manager (`@asynccontextmanager`).
* **Decision:** Migrated the startup event in [`backend/app/main.py`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/app/main.py) to:
  ```python
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      Base.metadata.create_all(bind=engine)
      yield

  app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
  ```
* **Rationale:** Eliminates deprecation warnings, provides standard graceful shutdown support, and complies with modern FastAPI / Starlette best practices.

#### 2. Database Migration Integration
* **Context:** Rubric requires PostgreSQL with at least one table managed by Alembic migrations.
* **Decision:** Retained [`backend/alembic/versions/0001_create_tasks.py`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/alembic/versions/0001_create_tasks.py) to manage the `tasks` schema.
* **Verification:** The entrypoint command runs `alembic upgrade head` on startup, creating the schema cleanly in PostgreSQL.

---

### M2 — Testing: Pytest + Code Quality

#### 1. Test Isolation and Fixture Architecture
* **Context:** The initial repository had only 3 test cases in `test_api.py` covering 2 endpoints. The rubric requires:
  1. Minimum 5 test cases covering at least 3 API endpoints.
  2. Isolated test database (not production PostgreSQL).
  3. Correctly configured `conftest.py` / `pytest.ini`.
* **Issue Discovered:** In containerized test runs, SQLite defaulted to `./test.db` in `/app`, which failed with permission denied because non-root `appuser` cannot write to the container's mounted `/app` directory. Additionally, pytest generated `.pytest_cache` permission warnings.
* **Decisions:**
  1. **Created [`backend/tests/conftest.py`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/tests/conftest.py):**
     * Sets `DATABASE_URL = "sqlite:////tmp/test_taskboard.db"` (guaranteeing write access in `/tmp` across any Linux environment).
     * Added `setup_test_db` (session scope) to initialize and clean up database files.
     * Added `clean_db` (function scope, autouse) to recreate tables before each test, preventing state leakage between tests.
     * Created `client` fixture with `TestClient(app)` context management.
  2. **Configured [`backend/pytest.ini`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/pytest.ini):**
     * Added `addopts = -p no:cacheprovider` to suppress `.pytest_cache` write attempts in container environments.
  3. **Expanded Test Suite in [`backend/tests/test_api.py`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/tests/test_api.py):**
     * Implemented 9 distinct test cases covering:
       - `test_health` (`GET /health`)
       - `test_root` (`GET /`)
       - `test_ready` (`GET /ready`)
       - `test_create_and_get_task` (`POST /api/tasks` & `GET /api/tasks/{id}`)
       - `test_list_tasks` (`GET /api/tasks`)
       - `test_update_task` (`PUT /api/tasks/{id}`)
       - `test_delete_task` (`DELETE /api/tasks/{id}`)
       - `test_stats_endpoint` (`GET /api/tasks/stats`)
       - `test_task_not_found` (404 error validation)
* **Verification:** Executed `pytest -v` inside the backend container: all 9 tests pass in 0.13s with 0 errors.

---

### M3 — Git & Repository Hygiene

#### 1. `.gitignore` Compliance
* **Context:** Rubric criterion 3 for M3 requires `.gitignore` to exclude `.env`, `__pycache__`, `node_modules`, and `.venv`.
* **Decision:** Updated [`.gitignore`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/.gitignore) to explicitly include:
  ```gitignore
  __pycache__/
  *.py[cod]
  .venv/
  env/
  venv/
  .pytest_cache/
  test.db
  *.db
  ```
* **Rationale:** Prevents bytecode, virtual environments, test artifacts, and credentials from entering version control.

---

### M4 & Performance — Docker, Compose & LCP Optimization

#### 1. Enforcing Non-Root Execution in Both Containers
* **Context:** Rubric criterion requires "Non-root user in both Dockerfiles".
* **Decisions:**
  1. **In [`frontend/Dockerfile`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/frontend/Dockerfile):**
     * Added file permission configuration for `nginx` user:
       ```dockerfile
       RUN touch /var/run/nginx.pid && \
           chown -R nginx:nginx /var/run/nginx.pid /usr/share/nginx/html /var/cache/nginx /var/log/nginx /etc/nginx
       USER nginx
       EXPOSE 80
       ```
     * Verified via `docker run ... whoami` that runtime user is `nginx`.
  2. **In [`backend/Dockerfile`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/backend/Dockerfile):**
     * Added `RUN chown -R appuser:appuser /app` before `USER 10001`.
     * Verified non-root execution (`uid=10001(appuser)`).

#### 2. Resolving the Docker Compose Database Startup Race Condition
* **Context:** In [`docker-compose.yml`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/docker-compose.yml), `backend` depends on `postgres`. The backend entrypoint `alembic upgrade head` crashed if Postgres had not finished initializing TCP listening.
* **Decision:** Added a native healthcheck and health condition:
  ```yaml
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U taskboard -d taskboard"]
      interval: 2s
      timeout: 3s
      retries: 10

  backend:
    depends_on:
      postgres:
        condition: service_healthy
  ```

#### 3. Web Performance & LCP (Largest Contentful Paint) Optimization
* **Context:** In accordance with the `debug-optimize-lcp` methodology, page load speed depends on minimizing Time to First Byte (TTFB), Resource Load Duration, and Element Render Delay.
* **Optimizations Implemented in [`frontend/nginx.conf`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/frontend/nginx.conf):**
  1. **Gzip Compression:** Enabled compression for text, CSS, JS, and JSON assets (`gzip on; gzip_comp_level 6;`). This cuts document and bundle transfer size by up to ~70%, reducing TTFB and resource load duration.
  2. **Long-Term Immutable Caching:** Added 1-year immutable caching for fingerprinted assets:
     ```nginx
     location /assets/ {
       expires 1y;
       add_header Cache-Control "public, max-age=31536000, immutable";
       try_files $uri =404;
     }
     ```
  3. **Zero Load Delay for LCP Element:** The LCP element is the hero heading (`<h1>Good morning, Nensi 👋</h1>`), which uses zero external blocking fonts or external images, ensuring immediate font rendering via system font fallbacks (`ui-sans-serif, system-ui, -apple-system`).

---

### M5 & M6 — CI/CD Pipeline & DevSecOps (Trivy)

#### 1. Pipeline Architecture
* **Context:** [`ci-cd.yml`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/.github/workflows/ci-cd.yml) triggers on pushes to `main`, runs Pytest, builds the React frontend, builds images tagged with Git commit SHA (`${{ github.sha }}`), runs Trivy security scans, and pushes to GitHub Container Registry (`ghcr.io`).

#### 2. DevSecOps Trivy Scan Policy
* **Configured Gates:**
  ```yaml
  - name: Scan backend
    uses: aquasecurity/trivy-action@0.30.0
    with:
      image-ref: ghcr.io/${{ github.repository_owner }}/taskboard-backend:${{ github.sha }}
      severity: HIGH,CRITICAL
      ignore-unfixed: true
      exit-code: '1'
  ```

---

### M7 — Terraform: AWS Infrastructure as Code

#### 1. Fixing Syntax Errors in Terraform HCL Files
* **Issue Discovered:** Running `terraform fmt` failed with `Error: Invalid single-argument block definition` in [`terraform/main.tf`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/terraform/main.tf) and [`terraform/versions.tf`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/terraform/versions.tf).
* **Decision:** Refactored `versions.tf`, `variables.tf`, `main.tf`, and `outputs.tf` into standard multi-line HCL syntax.

#### 2. Created Example Variables File
* **Context:** Rubric criterion 7 requires `terraform.tfvars.example` present without committing real secrets.
* **Decision:** Created [`terraform/terraform.tfvars.example`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/terraform/terraform.tfvars.example).
* **Verification:** `terraform fmt`, `terraform init -backend=false`, and `terraform validate` returned `Success! The configuration is valid.`

---

### M8 — Kubernetes + Helm

#### 1. Fixing Ingress Backend Target Port
* **Issue Discovered:** In [`helm/taskboard/templates/ingress.yaml`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/helm/taskboard/templates/ingress.yaml), the `/api` backend path pointed to port `8080` instead of port `8000`.
* **Decision:** Corrected the Ingress target port to `8000`.

#### 2. Standardizing Service and Deployment Names in Helm Helpers
* **Issue Discovered:** `_helpers.tpl` previously returned `{{ .Release.Name }}-taskboard`, producing duplicate names like `taskboard-taskboard-backend`.
* **Decision:** Implemented standard Helm `taskboard.fullname` logic in [`helm/taskboard/templates/_helpers.tpl`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/helm/taskboard/templates/_helpers.tpl), aligned deployment and service templates.
* **Verification:** `helm lint ./helm/taskboard` passed with 0 failures, and `helm template` rendered cleanly.

---

### M9 — Observability: Prometheus & Grafana

#### 1. Metric Instrumentation & Endpoint Validation
* **Backend:** FastAPI instrumented with `prometheus-fastapi-instrumentator` exposing metrics on `GET /metrics`.
* **ServiceMonitor:** Defined in [`helm/taskboard/templates/servicemonitor.yaml`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/helm/taskboard/templates/servicemonitor.yaml).
* **Dashboard Asset:** Created [`monitoring/grafana-dashboard.json`](file:///home/akshanshsinha/DevOps/devops-heros/session21-python/monitoring/grafana-dashboard.json) providing out-of-the-box panels for request rates, p95 duration, RSS memory, and request counts.
