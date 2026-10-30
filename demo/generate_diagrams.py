import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("demo/assets", exist_ok=True)

# Set common style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['text.color'] = '#f8fafc'

# Helper for drawing cards with title, badge, and items
def draw_card(ax, x, y, w, h, title, subtitle, items, bg_color="#1e293b", border_color="#38bdf8", badge=""):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=2,
        zorder=2
    )
    ax.add_patch(rect)
    
    # Title & Badge
    ax.text(x + 0.02, y + h - 0.05, title, fontsize=12, fontweight='bold', color='#f8fafc', zorder=3)
    if badge:
        ax.text(x + w - 0.02, y + h - 0.05, badge, fontsize=9, fontweight='bold', color=border_color,
                ha='right', va='center', bbox=dict(boxstyle="round,pad=0.2", facecolor="#0f172a", edgecolor=border_color, lw=1), zorder=3)
    
    if subtitle:
        ax.text(x + 0.02, y + h - 0.10, subtitle, fontsize=9.5, color='#94a3b8', style='italic', zorder=3)
    
    # Items
    start_y = y + h - 0.16
    for i, item in enumerate(items):
        ax.text(x + 0.02, start_y - (i * 0.045), f"• {item}", fontsize=9, color='#cbd5e1', zorder=3)

# 1. System Architecture Diagram
def create_system_architecture():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Header
    ax.text(0.5, 0.95, "TaskBoard — Cloud-Native End-to-End Architecture", 
            fontsize=20, fontweight='bold', ha='center', color='#38bdf8')
    ax.text(0.5, 0.91, "React 18 SPA • FastAPI Async Core • PostgreSQL • Kubernetes & Ingress • Observability", 
            fontsize=11, ha='center', color='#94a3b8')

    # Outer Cluster Boundary
    k8s_box = patches.FancyBboxPatch(
        (0.24, 0.10), 0.73, 0.77,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor="#131d31",
        edgecolor="#6366f1",
        linewidth=2,
        linestyle='--',
        zorder=1
    )
    ax.add_patch(k8s_box)
    ax.text(0.26, 0.84, "Kubernetes Cluster / EKS (Namespace: taskboard)", fontsize=13, fontweight='bold', color="#818cf8")

    # Client Browser
    draw_card(ax, 0.03, 0.45, 0.17, 0.35, "Client User", "Web Browser", 
              ["Modern SaaS UI", "Vite + React 18", "State & Filter Hook", "LCP Optimized < 1.2s", "HTTP/2 / HTTPS"],
              bg_color="#1e293b", border_color="#38bdf8", badge="CLIENT")

    # Ingress Controller
    draw_card(ax, 0.27, 0.45, 0.17, 0.35, "Nginx Ingress", "Reverse Proxy & Routing",
              ["Path: / → Frontend", "Path: /api → Backend", "SSL / TLS Term", "CORS Headers", "Port 80 / 443"],
              bg_color="#1e293b", border_color="#ec4899", badge="INGRESS")

    # Frontend Pods
    draw_card(ax, 0.48, 0.53, 0.22, 0.27, "Frontend Service", "Multi-stage Nginx Pods",
              ["2 Replicas (HA)", "Non-root (nginx)", "Gzip Comp Level 6", "1-Year Static Cache"],
              bg_color="#1e293b", border_color="#22c55e", badge=":80")

    # Backend Pods
    draw_card(ax, 0.48, 0.18, 0.22, 0.31, "Backend Service", "FastAPI Python 3.12",
              ["2 Replicas (HPA autoscaled)", "Non-root (UID 10001)", "SQLAlchemy ORM + Alembic", "Liveness: /health", "Readiness: /ready"],
              bg_color="#1e293b", border_color="#eab308", badge=":8000")

    # PostgreSQL Database
    draw_card(ax, 0.74, 0.18, 0.21, 0.31, "PostgreSQL 16", "Relational Database",
              ["Stateful Storage", "Alembic Migrations", "Schema: tasks table", "Task Status / Priority", "Health: pg_isready"],
              bg_color="#1e293b", border_color="#06b6d4", badge=":5432")

    # Monitoring Stack
    draw_card(ax, 0.74, 0.53, 0.21, 0.27, "Prometheus & Grafana", "Cluster Observability",
              ["Scrapes /metrics", "ServiceMonitor CRD", "HTTP p95 Latency", "Request Rate & Memory"],
              bg_color="#1e293b", border_color="#f97316", badge=":9090 / :3000")

    # Arrows
    arrow_props = dict(arrowstyle="-|>", lw=2.5, color="#cbd5e1", mutation_scale=18)
    
    # Client -> Ingress
    ax.annotate("", xy=(0.27, 0.62), xytext=(0.20, 0.62), arrowprops=arrow_props)
    ax.text(0.235, 0.64, "HTTPS", fontsize=9, color="#cbd5e1", ha="center")

    # Ingress -> Frontend
    ax.annotate("", xy=(0.48, 0.67), xytext=(0.44, 0.67), arrowprops=arrow_props)
    ax.text(0.46, 0.69, "/", fontsize=9, color="#22c55e", ha="center", fontweight='bold')

    # Ingress -> Backend
    ax.annotate("", xy=(0.48, 0.35), xytext=(0.44, 0.50),
                arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#eab308", mutation_scale=18,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(0.44, 0.38, "/api", fontsize=9, color="#eab308", ha="center", fontweight='bold')

    # Backend -> PostgreSQL
    ax.annotate("", xy=(0.74, 0.33), xytext=(0.70, 0.33), arrowprops=arrow_props)
    ax.text(0.72, 0.35, "TCP 5432", fontsize=8.5, color="#06b6d4", ha="center")

    # Backend -> Prometheus
    ax.annotate("", xy=(0.78, 0.53), xytext=(0.65, 0.49),
                arrowprops=dict(arrowstyle="-|>", lw=2, color="#f97316", linestyle=":", mutation_scale=16))
    ax.text(0.73, 0.49, "metrics", fontsize=8.5, color="#f97316", ha="center")

    plt.tight_layout()
    plt.savefig("demo/assets/diagram_system_architecture.png", dpi=200, bbox_inches='tight')
    plt.close()

# 2. CI/CD DevSecOps Pipeline Diagram
def create_cicd_pipeline():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "TaskBoard — Automated CI/CD & DevSecOps Pipeline", 
            fontsize=20, fontweight='bold', ha='center', color='#38bdf8')
    ax.text(0.5, 0.91, "GitHub Actions • Pytest Gate • Docker Multi-stage • Trivy Vulnerability Scan • GHCR • Helm", 
            fontsize=11, ha='center', color='#94a3b8')

    stages = [
        ("1. Code Push", "Developer Workspace", ["git push origin main", "Commit SHA generated", "Webhook triggers CI"], "#3b82f6", 0.03),
        ("2. Test Gate", "Quality Assurance", ["pytest -v (9/9 pass)", "Isolated in-memory DB", "npm run build (Vite)", "Fails pipeline on error"], "#22c55e", 0.19),
        ("3. Containerize", "Multi-Stage Build", ["Docker BuildKit", "FastAPI Python slim", "Node 22 + Nginx alpine", "Non-root user security"], "#eab308", 0.35),
        ("4. Security Gate", "Trivy Vulnerability Scan", ["aquasecurity/trivy", "Scan backend & frontend", "Severity: HIGH,CRITICAL", "Exit-code: 1 on CVE"], "#ef4444", 0.51),
        ("5. GHCR Registry", "Artifact Publishing", ["ghcr.io/akshansh-sinha", "Tag: ${{ github.sha }}", "Immutable artifacts", "Container security badge"], "#a855f7", 0.67),
        ("6. CD Deploy", "Kubernetes GitOps", ["Kind / EKS cluster", "Helm upgrade --install", "Rolling zero-downtime", "Readiness check pass"], "#06b6d4", 0.83)
    ]

    for title, subtitle, items, color, x_pos in stages:
        draw_card(ax, x_pos, 0.28, 0.14, 0.52, title, subtitle, items,
                  bg_color="#1e293b", border_color=color, badge="PASS")
        
    # Connecting Arrows
    for i in range(len(stages) - 1):
        x1 = stages[i][4] + 0.14
        x2 = stages[i+1][4]
        ax.annotate("", xy=(x2, 0.54), xytext=(x1, 0.54),
                    arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#f8fafc", mutation_scale=16))

    # Bottom Highlights
    highlights = [
        ("Shift-Left Security", "Trivy inspects layers before registry push; no CVEs leak to production.", "#ef4444", 0.05, 0.10, 0.28),
        ("Traceability & Audit", "Every image tag maps directly to the exact Git commit SHA hash.", "#a855f7", 0.36, 0.10, 0.28),
        ("Automated Quality", "Strict Pytest & Vite build gates guarantee zero broken builds.", "#22c55e", 0.67, 0.10, 0.28)
    ]
    for h_title, h_desc, h_col, hx, hy, hw in highlights:
        rect = patches.FancyBboxPatch((hx, hy), hw, 0.13, boxstyle="round,pad=0.015,rounding_size=0.02",
                                      facecolor="#1e293b", edgecolor=h_col, lw=1.5)
        ax.add_patch(rect)
        ax.text(hx + 0.015, hy + 0.09, h_title, fontsize=10.5, fontweight='bold', color=h_col)
        ax.text(hx + 0.015, hy + 0.04, h_desc, fontsize=8.5, color="#cbd5e1")

    plt.tight_layout()
    plt.savefig("demo/assets/diagram_cicd_pipeline.png", dpi=200, bbox_inches='tight')
    plt.close()

# 3. AWS & Terraform Infrastructure Topology
def create_terraform_aws():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "TaskBoard — AWS Infrastructure as Code (Terraform)", 
            fontsize=20, fontweight='bold', ha='center', color='#38bdf8')
    ax.text(0.5, 0.91, "Modular HCL • VPC with Multi-AZ Subnets • AWS EKS v1.31 • Auto-scaling Managed Node Group", 
            fontsize=11, ha='center', color='#94a3b8')

    # AWS Cloud Outer Box
    aws_box = patches.FancyBboxPatch((0.05, 0.08), 0.90, 0.80, boxstyle="round,pad=0.02,rounding_size=0.03",
                                     facecolor="#111c30", edgecolor="#f59e0b", lw=2, linestyle="--")
    ax.add_patch(aws_box)
    ax.text(0.08, 0.84, "AWS Cloud (Region: us-east-1)", fontsize=13, fontweight='bold', color="#fbbf24")

    # VPC Box
    vpc_box = patches.FancyBboxPatch((0.08, 0.12), 0.84, 0.69, boxstyle="round,pad=0.02,rounding_size=0.03",
                                     facecolor="#16233b", edgecolor="#38bdf8", lw=1.8)
    ax.add_patch(vpc_box)
    ax.text(0.11, 0.77, "Virtual Private Cloud (VPC: 10.0.0.0/16)", fontsize=12, fontweight='bold', color="#38bdf8")

    # Internet Gateway
    draw_card(ax, 0.11, 0.52, 0.22, 0.20, "Internet Gateway", "Public Edge Routing",
              ["IGW connected to VPC", "Routes 0.0.0.0/0", "Public Subnets: AZ-a & AZ-b"],
              bg_color="#1e293b", border_color="#38bdf8", badge="IGW")

    # EKS Control Plane
    draw_card(ax, 0.38, 0.50, 0.26, 0.24, "AWS EKS Control Plane", "Managed Master Nodes",
              ["Kubernetes v1.31", "Multi-AZ High Availability", "Security Groups & IAM Roles", "OIDC Provider Integrated"],
              bg_color="#1e293b", border_color="#a855f7", badge="MANAGED")

    # Worker Node Group
    draw_card(ax, 0.68, 0.50, 0.22, 0.24, "EKS Node Group", "Managed EC2 Instances",
              ["Instance Type: t3.medium", "Min: 2, Max: 5, Desired: 2", "Auto Scaling Group", "Containerd Runtime"],
              bg_color="#1e293b", border_color="#22c55e", badge="WORKERS")

    # Subnets row
    draw_card(ax, 0.11, 0.17, 0.24, 0.28, "Public Subnets (2x)", "CIDRs: 10.0.1.0/24, 10.0.2.0/24",
              ["AZ: us-east-1a & us-east-1b", "LoadBalancer / Ingress placement", "Auto-assign public IP: true"],
              bg_color="#1e293b", border_color="#06b6d4", badge="PUBLIC")

    draw_card(ax, 0.38, 0.17, 0.26, 0.28, "Private Subnets (2x)", "CIDRs: 10.0.10.0/24, 10.0.20.0/24",
              ["NAT Gateway egress", "Internal pod communication", "Isolated database layer", "Zero direct public ingress"],
              bg_color="#1e293b", border_color="#6366f1", badge="PRIVATE")

    draw_card(ax, 0.68, 0.17, 0.22, 0.28, "Terraform State Life", "State & Plan Operations",
              ["terraform init (clean lock)", "terraform fmt & validate", "terraform plan (reproducible)", "terraform destroy (cost safety)"],
              bg_color="#1e293b", border_color="#f59e0b", badge="IAC")

    # Connectors
    ax.annotate("", xy=(0.38, 0.62), xytext=(0.33, 0.62),
                arrowprops=dict(arrowstyle="-|>", lw=2, color="#f8fafc", mutation_scale=15))
    ax.annotate("", xy=(0.68, 0.62), xytext=(0.64, 0.62),
                arrowprops=dict(arrowstyle="-|>", lw=2, color="#f8fafc", mutation_scale=15))

    plt.tight_layout()
    plt.savefig("demo/assets/diagram_aws_terraform.png", dpi=200, bbox_inches='tight')
    plt.close()

# 4. Kubernetes & Helm Architecture Diagram
def create_k8s_helm():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "TaskBoard — Kubernetes & Helm Deployment Architecture", 
            fontsize=20, fontweight='bold', ha='center', color='#38bdf8')
    ax.text(0.5, 0.91, "Helm Charts • Declarative Values • Ingress Controller • HPA Autoscaling • ServiceMonitor", 
            fontsize=11, ha='center', color='#94a3b8')

    # Namespace Frame
    ns_box = patches.FancyBboxPatch((0.04, 0.08), 0.92, 0.80, boxstyle="round,pad=0.02,rounding_size=0.03",
                                    facecolor="#121e33", edgecolor="#38bdf8", lw=2)
    ax.add_patch(ns_box)
    ax.text(0.07, 0.84, "Kubernetes Namespace: taskboard (managed via Helm)", fontsize=13, fontweight='bold', color="#38bdf8")

    # Helm Release Overview Card
    draw_card(ax, 0.07, 0.50, 0.26, 0.30, "Helm Chart Package", "helm/taskboard",
              ["Chart.yaml & _helpers.tpl", "values.yaml (Defaults)", "values-dev.yaml (1 replica)", "values-prod.yaml (HA + HPA)", "helm lint: 0 errors"],
              bg_color="#1e293b", border_color="#a855f7", badge="HELM 3")

    # Ingress Resource
    draw_card(ax, 0.37, 0.50, 0.26, 0.30, "Ingress Controller", "ingress.yaml",
              ["Host: taskboard.local", "Path: / → frontend-svc:80", "Path: /api → backend-svc:8000", "IngressClass: nginx"],
              bg_color="#1e293b", border_color="#ec4899", badge="INGRESS")

    # HPA Autoscaler
    draw_card(ax, 0.67, 0.50, 0.26, 0.30, "Horizontal Pod Autoscaler", "hpa.yaml",
              ["Target: backend deployment", "Min Replicas: 2, Max: 10", "CPU Target Utilization: 80%", "Auto-scales under load-test.sh"],
              bg_color="#1e293b", border_color="#eab308", badge="HPA")

    # Frontend Deploy & Service
    draw_card(ax, 0.07, 0.13, 0.26, 0.32, "Frontend Deployment", "frontend-deployment.yaml",
              ["Replicas: 2 pods", "Service: ClusterIP :80", "Probes: httpGet /", "RollingUpdate strategy: 25% maxUnavailable"],
              bg_color="#1e293b", border_color="#22c55e", badge="FRONTEND")

    # Backend Deploy & Service
    draw_card(ax, 0.37, 0.13, 0.26, 0.32, "Backend Deployment", "backend-deployment.yaml",
              ["Replicas: 2 pods", "Service: ClusterIP :8000", "Liveness: /health", "Readiness: /ready (DB check)", "Resources: CPU 100m, Mem 128Mi"],
              bg_color="#1e293b", border_color="#38bdf8", badge="BACKEND")

    # PostgreSQL Stateful Deployment
    draw_card(ax, 0.67, 0.13, 0.26, 0.32, "PostgreSQL Database", "postgres.yaml",
              ["Service: ClusterIP :5432", "PVC: 5Gi persistent volume", "Liveness probe: pg_isready", "Initialized via Alembic migrations"],
              bg_color="#1e293b", border_color="#06b6d4", badge="DATABASE")

    # Arrows
    arrow_props = dict(arrowstyle="-|>", lw=2, color="#cbd5e1", mutation_scale=15)
    ax.annotate("", xy=(0.20, 0.45), xytext=(0.40, 0.50), arrowprops=arrow_props)
    ax.annotate("", xy=(0.50, 0.45), xytext=(0.50, 0.50), arrowprops=arrow_props)
    ax.annotate("", xy=(0.67, 0.29), xytext=(0.63, 0.29), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig("demo/assets/diagram_k8s_helm.png", dpi=200, bbox_inches='tight')
    plt.close()

# 5. Observability & Troubleshooting
def create_observability_troubleshooting():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0f172a')
    ax.set_facecolor('#0f172a')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    ax.text(0.5, 0.95, "TaskBoard — Observability, Metrics & Troubleshooting", 
            fontsize=20, fontweight='bold', ha='center', color='#38bdf8')
    ax.text(0.5, 0.91, "Prometheus Scrapes • Grafana Dashboards • Proactive Probes • Live Chaos Triage", 
            fontsize=11, ha='center', color='#94a3b8')

    # Observability Side
    obs_box = patches.FancyBboxPatch((0.04, 0.08), 0.44, 0.80, boxstyle="round,pad=0.02,rounding_size=0.03",
                                     facecolor="#121e33", edgecolor="#f97316", lw=2)
    ax.add_patch(obs_box)
    ax.text(0.07, 0.84, "Observability & Metrics Architecture", fontsize=13, fontweight='bold', color="#fb923c")

    draw_card(ax, 0.07, 0.50, 0.38, 0.30, "FastAPI Instrumentator", "GET /metrics Endpoint",
              ["Automatic HTTP request instrumentation", "Tracks status codes (2xx, 4xx, 5xx)", "Latency histogram & p95 summary", "RSS memory & CPU usage metrics"],
              bg_color="#1e293b", border_color="#f97316", badge=":8000/metrics")

    draw_card(ax, 0.07, 0.13, 0.38, 0.33, "Prometheus & Grafana Stack", "ServiceMonitor + Prebuilt Dashboard",
              ["Prometheus Operator ServiceMonitor CRD", "Auto-scraping interval: 15s", "Grafana Dashboard (grafana-dashboard.json)", "Live panels: Requests/sec, Latency, Error Rate"],
              bg_color="#1e293b", border_color="#eab308", badge="DASHBOARD")

    # Troubleshooting Side
    ts_box = patches.FancyBboxPatch((0.52, 0.08), 0.44, 0.80, boxstyle="round,pad=0.02,rounding_size=0.03",
                                    facecolor="#121e33", edgecolor="#ef4444", lw=2)
    ax.add_patch(ts_box)
    ax.text(0.55, 0.84, "Troubleshooting & Failure Simulation", fontsize=13, fontweight='bold', color="#f87171")

    draw_card(ax, 0.55, 0.50, 0.38, 0.30, "Scenario 1: Broken Image", "troubleshooting/broken-image.yaml",
              ["Symptom: ImagePullBackOff / ErrImagePull", "Diagnosis: kubectl describe pod taskboard-broken", "Root Cause: non-existent image tag", "Resolution: fix image tag to valid GHCR SHA"],
              bg_color="#1e293b", border_color="#ef4444", badge="TRIAGE 1")

    draw_card(ax, 0.55, 0.13, 0.38, 0.33, "Scenario 2: Broken Service", "troubleshooting/broken-service.yaml",
              ["Symptom: 502 Bad Gateway / Connection Refused", "Diagnosis: kubectl get endpoints backend-broken", "Root Cause: selector label mismatch (app: wrong)", "Resolution: align selector labels with pod labels"],
              bg_color="#1e293b", border_color="#f43f5e", badge="TRIAGE 2")

    plt.tight_layout()
    plt.savefig("demo/assets/diagram_observability_troubleshooting.png", dpi=200, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating diagrams...")
    create_system_architecture()
    create_cicd_pipeline()
    create_terraform_aws()
    create_k8s_helm()
    create_observability_troubleshooting()
    print("Diagrams successfully generated in demo/assets/!")
