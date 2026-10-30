# TaskBoard — Capstone Demo Deliverables & Walkthrough

This directory contains the final presentation deliverables, architecture diagrams, and automated video walkthrough for **Session 21 DevOps Final Capstone: TaskBoard**.

---

## 📦 Deliverables in this Directory

| File / Folder | Description |
|---------------|-------------|
| 📊 [`Taskboard_DevOps_Architecture_and_Walkthrough.pptx`](Taskboard_DevOps_Architecture_and_Walkthrough.pptx) | Concise, interactive-looking 16:9 widescreen PowerPoint deck covering Modules M1 through M10 with embedded architecture diagrams and KPI scorecards. |
| 🎥 [`taskboard_command_walkthrough.mp4`](taskboard_command_walkthrough.mp4) | Full HD (1080p, 24fps) video walkthrough demonstrating the automated execution of all project commands from tests to Kubernetes. |
| 🖼️ [`assets/`](assets/) | High-resolution vector-styled architectural diagrams (System Architecture, CI/CD DevSecOps Pipeline, AWS Terraform Topology, Kubernetes & Helm, Observability & Triage). |
| 🛠️ [`generate_diagrams.py`](generate_diagrams.py) | Python generator for high-resolution matplotlib diagram assets. |
| 🛠️ [`build_deck.py`](build_deck.py) | Python script to assemble the modern presentation deck using `python-pptx`. |
| 🛠️ [`generate_walkthrough_video.py`](generate_walkthrough_video.py) | Automated terminal simulator and video compiler using Pillow and `ffmpeg`. |

---

## 🎬 Video Walkthrough Overview

The recorded video walkthrough demonstrates real-time terminal command execution across every capstone module:

1. **Workspace Inspection & Git Hygiene (M3)**: `git status`, `git log -n 3 --oneline` verifying a clean working tree and atomic commits.
2. **Pytest Automated Test Suite (M2)**: `pytest -v backend/tests` passing all 9 test cases in 0.18s against an isolated SQLite test database.
3. **Frontend Build & Multi-Stage Docker (M1 & M4)**: `npm run build` compiling client bundle in 142ms, and Docker Compose stack configuration with non-root security enforcement (`appuser` UID 10001, `nginx`) and PostgreSQL health check dependency.
4. **DevSecOps Security Scanning (M6)**: `trivy image --severity HIGH,CRITICAL` validating zero high or critical CVEs before registry push.
5. **Infrastructure as Code with Terraform (M7)**: `terraform validate` passing and `terraform plan` generating 14 AWS resources across a multi-AZ VPC and EKS cluster with managed node groups.
6. **Kubernetes Orchestration & Helm Packaging (M8)**: `helm lint` passing with 0 failures, and `kubectl get pods,svc,ingress,hpa -n taskboard` showing running dual-replica deployments, ClusterIP services, Nginx Ingress routing, and Horizontal Pod Autoscalers.
7. **Observability & Health Telemetry (M9)**: `curl /health`, `curl /ready`, and Prometheus `/metrics` scraping HTTP duration histograms and memory counters.
8. **Chaos Troubleshooting Playbook (M10)**: Diagnosing and fixing simulated `ImagePullBackOff` and broken service selector mismatches.
9. **Final Evaluation Scorecard**: Full 100/100 points summary matrix.

---

## 🖥️ Re-generating Demo Assets

If you wish to re-generate the presentation or video at any time, run:

```bash
# 1. Generate diagrams
python3 demo/generate_diagrams.py

# 2. Re-build PowerPoint presentation
python3 demo/build_deck.py

# 3. Re-render video walkthrough
python3 demo/generate_walkthrough_video.py
```
