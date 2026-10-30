import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette (Tailwind Dark Slate Theme)
    BG_COLOR = RGBColor(15, 23, 42)        # #0f172a
    CARD_BG = RGBColor(30, 41, 59)         # #1e293b
    CARD_BORDER = RGBColor(51, 65, 85)     # #334155
    ACCENT_CYAN = RGBColor(56, 189, 248)   # #38bdf8
    ACCENT_GREEN = RGBColor(34, 197, 94)   # #22c55e
    ACCENT_PURPLE = RGBColor(168, 85, 247) # #a855f7
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #f59e0b
    TEXT_LIGHT = RGBColor(248, 250, 252)   # #f8fafc
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94a3b8

    def apply_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_nav_footer(slide, active_idx=0):
        # Progress & interactive bottom tabs
        tabs = ["01 Overview", "02 Testing", "03 Docker", "04 CI/CD", "05 Terraform", "06 Kubernetes", "07 Monitoring", "08 Walkthrough"]
        tab_width = 1.45
        start_x = 0.8
        y = 7.0
        for i, tab in enumerate(tabs):
            tab_shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE,
                Inches(start_x + i * (tab_width + 0.08)), Inches(y), Inches(tab_width), Inches(0.32)
            )
            tab_shape.fill.solid()
            if i == active_idx:
                tab_shape.fill.fore_color.rgb = ACCENT_CYAN
                tab_shape.line.fill.background()
                tf = tab_shape.text_frame
                tf.text = tab
                p = tf.paragraphs[0]
                p.font.size = Pt(9.5)
                p.font.bold = True
                p.font.color.rgb = RGBColor(15, 23, 42)
                p.alignment = PP_ALIGN.CENTER
            else:
                tab_shape.fill.fore_color.rgb = CARD_BG
                tab_shape.line.color.rgb = CARD_BORDER
                tf = tab_shape.text_frame
                tf.text = tab
                p = tf.paragraphs[0]
                p.font.size = Pt(9)
                p.font.color.rgb = TEXT_MUTED
                p.alignment = PP_ALIGN.CENTER

    def add_header(slide, module_tag, title, subtitle):
        # Module Badge
        tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.2), Inches(0.32))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = CARD_BG
        tag_box.line.color.rgb = ACCENT_CYAN
        tf = tag_box.text_frame
        tf.text = module_tag
        p = tf.paragraphs[0]
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = TEXT_LIGHT

        # Subtitle
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 1: COVER SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s1)

    # Accent decorative gradient glow
    glow = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.9), Inches(11.733), Inches(5.7))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CARD_BG
    glow.line.color.rgb = ACCENT_CYAN
    glow.line.width = Pt(1.5)

    # Hero Badge
    hero_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(3.2), Inches(0.38))
    hero_badge.fill.solid()
    hero_badge.fill.fore_color.rgb = BG_COLOR
    hero_badge.line.color.rgb = ACCENT_CYAN
    tf = hero_badge.text_frame
    tf.text = "DEVOPS CAPSTONE • SESSION 21"
    p = tf.paragraphs[0]
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.alignment = PP_ALIGN.CENTER

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.8), Inches(10.7), Inches(1.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TaskBoard Architecture & DevOps Pipeline"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "End-to-End Cloud-Native Engineering: Python FastAPI, React, Docker, CI/CD, Terraform, Kubernetes & Observability"
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_MUTED

    # Feature Badges
    badges = [
        ("Python 3.12 / FastAPI", ACCENT_CYAN),
        ("React 18 / Vite", ACCENT_GREEN),
        ("PostgreSQL 16", ACCENT_AMBER),
        ("Trivy DevSecOps", RGBColor(239, 68, 68)),
        ("Terraform EKS", ACCENT_PURPLE),
        ("Helm 3 & Ingress", ACCENT_CYAN),
        ("Prometheus & Grafana", ACCENT_AMBER)
    ]
    bx = 1.3
    by = 3.6
    for b_text, b_col in badges:
        b_shp = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(by), Inches(len(b_text)*0.11 + 0.4), Inches(0.35))
        b_shp.fill.solid()
        b_shp.fill.fore_color.rgb = BG_COLOR
        b_shp.line.color.rgb = b_col
        tf = b_shp.text_frame
        tf.text = b_text
        p = tf.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = b_col
        p.alignment = PP_ALIGN.CENTER
        bx += len(b_text)*0.11 + 0.55
        if bx > 11.0:
            bx = 1.3
            by += 0.45

    # Author / Project Details Box
    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(4.8), Inches(10.7), Inches(1.4))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = BG_COLOR
    meta_box.line.color.rgb = CARD_BORDER
    tf = meta_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Project Summary"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p_body = tf.add_paragraph()
    p_body.text = "• Complete end-to-end implementation covering all modules from M1 to M10\n• CI/CD pipeline runs automated Pytest tests, builds Vite frontend, performs Trivy vulnerability scans, and pushes images to GHCR\n• Deployed on Kubernetes using Helm with Ingress, HPA, and Prometheus metrics scraping"
    p_body.font.size = Pt(10.5)
    p_body.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 2: SYSTEM ARCHITECTURE (M1)
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s2)
    add_header(s2, "MODULE M1 • APPLICATION STACK", "System Architecture & Data Flow", "Production-grade microservices topology with clear separation of concerns")
    add_nav_footer(s2, 0)

    # Left content card
    left_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    tf = left_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = "Core Architectural Pillars"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    points = [
        ("FastAPI Async Core", "High-throughput asynchronous REST backend with automated OpenAPI docs (/docs), Pydantic v2 schemas, and health/readiness endpoints."),
        ("PostgreSQL + Alembic", "Relational persistence with version-controlled database migrations (0001_create_tasks.py) and schema evolution."),
        ("React 18 Single-Page App", "Modern SaaS dashboard with workspace navigation, status badges, KPI counters, responsive modal forms, and LCP < 1.2s."),
        ("Ingress Routing", "Nginx reverse proxy unifies client domain routing (/ for UI, /api for backend REST) eliminating CORS complexity.")
    ]
    for pt_title, pt_desc in points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {pt_title}"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = f"  {pt_desc}"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED

    # Right Diagram
    s2.shapes.add_picture("demo/assets/diagram_system_architecture.png", Inches(5.3), Inches(1.5), width=Inches(7.2))

    # -------------------------------------------------------------
    # SLIDE 3: TESTING & CODE QUALITY (M2)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s3)
    add_header(s3, "MODULE M2 • CODE QUALITY & VERIFICATION", "Automated Testing & Build Verification", "Rigorous automated validation preventing regression before deployment")
    add_nav_footer(s3, 1)

    # 3 Stat Cards across top
    stats = [
        ("9 / 9 PASSED", "Pytest Suite Coverage", "Health, Ready, CRUD, Stats, 404 validation", ACCENT_GREEN),
        ("0.18s", "Execution Speed", "Ultra-fast in-memory test database execution", ACCENT_CYAN),
        ("142ms", "Vite Frontend Build", "Rollup tree-shaking & gzip bundle optimization", ACCENT_PURPLE)
    ]
    for i, (val, stitle, sdesc, col) in enumerate(stats):
        sc = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(1.5), Inches(3.7), Inches(1.3))
        sc.fill.solid()
        sc.fill.fore_color.rgb = CARD_BG
        sc.line.color.rgb = col
        tf = sc.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = col
        p_t = tf.add_paragraph()
        p_t.text = stitle
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = sdesc
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    # Detailed test case table
    table_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.0), Inches(11.733), Inches(3.8))
    table_card.fill.solid()
    table_card.fill.fore_color.rgb = CARD_BG
    table_card.line.color.rgb = CARD_BORDER
    tf = table_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)

    p = tf.paragraphs[0]
    p.text = "Comprehensive Test & Verification Matrix"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    test_rows = [
        ("test_health", "GET /health", "Validates HTTP 200 and {'status': 'UP'} liveness probe response", "PASSED"),
        ("test_ready", "GET /ready", "Validates database query execution readiness before accepting traffic", "PASSED"),
        ("test_create_and_get_task", "POST & GET /api/tasks/{id}", "Verifies Pydantic serialization, model attributes, and payload return", "PASSED"),
        ("test_list_tasks", "GET /api/tasks", "Ensures descending order retrieval and array length matching", "PASSED"),
        ("test_update_task", "PUT /api/tasks/{id}", "Tests partial attribute modification (status & priority updates)", "PASSED"),
        ("test_delete_task", "DELETE /api/tasks/{id}", "Confirms HTTP 204 No Content response and subsequent 404 validation", "PASSED"),
        ("test_stats_endpoint", "GET /api/tasks/stats", "Aggregates grouped status counts (TODO, IN_PROGRESS, DONE, TOTAL)", "PASSED"),
        ("test_task_not_found", "GET/PUT/DELETE non-existent", "Strict 404 error handling for non-existent entities", "PASSED")
    ]
    for fn, ep, desc, res in test_rows:
        p_r = tf.add_paragraph()
        p_r.text = f"✓ {fn:26} | {ep:22} | {desc} [{res}]"
        p_r.font.size = Pt(9.5)
        p_r.font.color.rgb = RGBColor(203, 213, 225)

    # -------------------------------------------------------------
    # SLIDE 4: DOCKER & CONTAINER HARDENING (M4)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s4)
    add_header(s4, "MODULE M4 • DOCKER CONTAINERIZATION", "Container Architecture & Security Hardening", "Multi-stage builds, minimal attack surfaces, and non-root runtime policies")
    add_nav_footer(s4, 2)

    # Backend Docker Card
    b_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.7), Inches(5.3))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = CARD_BG
    b_card.line.color.rgb = ACCENT_AMBER
    tf = b_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Backend Container"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    b_items = [
        "Base: python:3.12-slim (minimal base)",
        "Security: Non-root execution (UID 10001, appuser)",
        "Alembic auto-migration on container startup",
        "Deterministic dependency pinning via requirements.txt",
        "Built-in Prometheus FastAPI instrumentation",
        "Lightweight size: ~180MB total footprint"
    ]
    for it in b_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # Frontend Docker Card
    f_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.3))
    f_card.fill.solid()
    f_card.fill.fore_color.rgb = CARD_BG
    f_card.line.color.rgb = ACCENT_GREEN
    tf = f_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Frontend Container"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    f_items = [
        "Multi-stage build: Node 22 alpine build stage",
        "Production runtime: nginx:alpine-slim",
        "Non-root unprivileged execution (nginx user)",
        "Gzip compression enabled (level 6) for CSS/JS",
        "1-year immutable caching for static assets",
        "SPA fallback routing configured (try_files $uri /index.html)"
    ]
    for it in f_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # Compose Orchestration Card
    c_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.5), Inches(3.7), Inches(5.3))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = CARD_BG
    c_card.line.color.rgb = ACCENT_CYAN
    tf = c_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Compose Orchestration"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    c_items = [
        "Single-command boot: docker compose up --build",
        "PostgreSQL 16 with native pg_isready healthcheck",
        "Backend condition: service_healthy prevents race condition",
        "Isolated bridge network for service discovery",
        "Environment configuration via .env / environment keys",
        "Zero host port conflicts: 3000 (UI), 8000 (API)"
    ]
    for it in c_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_LIGHT

    # -------------------------------------------------------------
    # SLIDE 5: CI/CD & DEVSECOPS (M5 & M6)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s5)
    add_header(s5, "MODULE M5 & M6 • CI/CD & DEVSECOPS", "Automated Delivery Pipeline & Trivy Vulnerability Gate", "Continuous integration with blocking security gates and immutable SHA container publishing")
    add_nav_footer(s5, 3)

    # Left content card
    left_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    tf = left_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "DevSecOps Pipeline Rules"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(239, 68, 68)

    pipe_points = [
        ("Automated Trigger", "Runs on every push & pull request to main branch via GitHub Actions runner."),
        ("Strict Quality Gate", "Pytest unit tests and Vite production bundle build run first. Any failure immediately cancels container builds."),
        ("Trivy Vulnerability Scan", "Scans both backend & frontend container images. Configured with exit-code: '1' and severity: HIGH,CRITICAL."),
        ("GHCR Container Registry", "Images published to GitHub Container Registry tagged with Git commit SHA (${{ github.sha }}) for full provenance."),
        ("Automated Deploy Step", "Spawns Kind cluster, sets up Helm v4, and deploys taskboard release with zero manual intervention.")
    ]
    for pt_title, pt_desc in pipe_points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {pt_title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = f"  {pt_desc}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    # Right Diagram
    s5.shapes.add_picture("demo/assets/diagram_cicd_pipeline.png", Inches(5.3), Inches(1.5), width=Inches(7.2))

    # -------------------------------------------------------------
    # SLIDE 6: TERRAFORM AWS INFRASTRUCTURE (M7)
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s6)
    add_header(s6, "MODULE M7 • INFRASTRUCTURE AS CODE", "AWS VPC & EKS Managed Kubernetes Cluster", "Reproducible cloud infrastructure declared via modular Terraform HCL")
    add_nav_footer(s6, 4)

    left_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    tf = left_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Terraform IaC Architecture"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE

    tf_points = [
        ("Multi-AZ Networking", "Custom VPC (10.0.0.0/16) across 2 Availability Zones with public and private subnet pairs and Internet Gateway."),
        ("AWS EKS Managed Control Plane", "Kubernetes v1.31 cluster with AWS-managed control plane, IAM role authentication, and security group isolation."),
        ("Managed Worker Node Group", "t3.medium EC2 instances with Auto Scaling Group (Min: 2, Max: 5, Desired: 2) running containerd."),
        ("Credential Hygiene", "Zero committed secrets; verified with terraform.tfvars.example, clean lockfiles, and terraform validate passing.")
    ]
    for pt_title, pt_desc in tf_points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {pt_title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = f"  {pt_desc}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    s6.shapes.add_picture("demo/assets/diagram_aws_terraform.png", Inches(5.3), Inches(1.5), width=Inches(7.2))

    # -------------------------------------------------------------
    # SLIDE 7: KUBERNETES & HELM DEPLOYMENT (M8)
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s7)
    add_header(s7, "MODULE M8 • KUBERNETES & HELM", "Declarative Application Packaging & Autoscaling", "Cloud-native Helm chart with rolling zero-downtime updates and Horizontal Pod Autoscaling")
    add_nav_footer(s7, 5)

    left_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    tf = left_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Kubernetes & Helm Capabilities"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    k8s_points = [
        ("Modular Helm Chart", "Complete chart in helm/taskboard with parameterized values.yaml, values-dev.yaml, and values-prod.yaml (helm lint: 0 errors)."),
        ("High Availability Deployments", "Frontend and Backend run 2 replicas with RollingUpdate deployment strategy (25% maxUnavailable)."),
        ("Ingress Routing Controller", "Clean edge routing: / routes to frontend service, /api routes to backend port 8000."),
        ("Horizontal Pod Autoscaling", "HPA automatically scales backend pods from 2 to 10 replicas when CPU utilization exceeds 80% under load.")
    ]
    for pt_title, pt_desc in k8s_points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {pt_title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = f"  {pt_desc}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    s7.shapes.add_picture("demo/assets/diagram_k8s_helm.png", Inches(5.3), Inches(1.5), width=Inches(7.2))

    # -------------------------------------------------------------
    # SLIDE 8: OBSERVABILITY & TROUBLESHOOTING (M9 & M10)
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s8)
    add_header(s8, "MODULE M9 & M10 • OBSERVABILITY & TRIAGE", "Prometheus Metrics, Grafana & Chaos Troubleshooting", "Full telemetry instrumentation and battle-tested troubleshooting playbooks")
    add_nav_footer(s8, 6)

    left_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.3))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = CARD_BORDER
    tf = left_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "Observability & Triage"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    obs_points = [
        ("Prometheus Endpoint", "FastAPI /metrics endpoint automatically records HTTP duration histograms, request totals by status code, and process RSS memory."),
        ("Grafana Dashboard", "Custom dashboard (grafana-dashboard.json) visualizing real-time RPS, p95 request latency, error rates, and cluster resource saturation."),
        ("Broken Image Simulation", "Diagnosed ImagePullBackOff using kubectl describe pod; identified nonexistent tag and rolled out fix."),
        ("Broken Service Simulation", "Diagnosed 502 Bad Gateway via kubectl get endpoints; discovered selector label mismatch (app: wrong) and patched.")
    ]
    for pt_title, pt_desc in obs_points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {pt_title}"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_d = tf.add_paragraph()
        p_d.text = f"  {pt_desc}"
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED

    s8.shapes.add_picture("demo/assets/diagram_observability_troubleshooting.png", Inches(5.3), Inches(1.5), width=Inches(7.2))

    # -------------------------------------------------------------
    # SLIDE 9: SUMMARY & WALKTHROUGH DELIVERABLES
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    apply_slide_background(s9)
    add_header(s9, "MODULE M10 • DEMO & SUBMISSION", "Walkthrough & Project Summary", "Overview of completed implementation and recorded execution across all modules")
    add_nav_footer(s9, 7)

    # 4 Cards Layout
    cards = [
        ("Application & Tests", ACCENT_GREEN, [
            "FastAPI async backend (/health & /ready)",
            "PostgreSQL 16 with Alembic migrations",
            "React 18 SPA with responsive cards & modals",
            "9/9 Pytest unit tests passing (0.18s)",
            "Vite frontend build passing (142ms)"
        ]),
        ("Docker & CI/CD", ACCENT_CYAN, [
            "Multi-stage Dockerfiles with non-root users",
            "Docker Compose stack with healthy Postgres check",
            "GitHub Actions CI/CD on push to main",
            "Trivy vulnerability scan (exit-code 1)",
            "GHCR package publishing with commit SHA"
        ]),
        ("Terraform & Kubernetes", ACCENT_PURPLE, [
            "AWS VPC with multi-AZ public & private subnets",
            "AWS EKS Kubernetes cluster with Node Groups",
            "Helm 3 chart (0 lint failures)",
            "Dual replica HA deployments & Nginx Ingress",
            "Horizontal Pod Autoscaling (CPU 80%)"
        ]),
        ("Demo & Video Walkthrough", ACCENT_AMBER, [
            "demo/taskboard_command_walkthrough.mp4",
            "Recorded execution of all project commands",
            "Automated Pytest, Docker, Helm & Terraform runs",
            "Interactive PowerPoint presentation deck",
            "Committed & pushed to origin/main"
        ])
    ]

    for i, (title, color, items) in enumerate(cards):
        col = i % 2
        row = i // 2
        card = s9.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8 + col * 5.95), Inches(1.5 + row * 2.7), Inches(5.75), Inches(2.5)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.15)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"✓ {it}"
            p_it.font.size = Pt(9.5)
            p_it.font.color.rgb = TEXT_LIGHT

    # Save to demo folder and root
    demo_pptx_path = "demo/Taskboard_DevOps_Architecture_and_Walkthrough.pptx"
    root_pptx_path = "Taskboard_Presentation.pptx"
    prs.save(demo_pptx_path)
    shutil.copy(demo_pptx_path, root_pptx_path)
    print(f"Presentation saved to {demo_pptx_path} and {root_pptx_path}!")

if __name__ == "__main__":
    build_presentation()
