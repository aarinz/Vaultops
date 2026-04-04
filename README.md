# VaultOps 
### BA-Governed Financial Release Pipeline

> A DevOps pipeline where **Business Analysts own the deploy gate** — no release goes live without passing AI-powered business risk analysis.

**Live Demo:** [vaultops-sigma.vercel.app](https://vaultops-sigma.vercel.app)

---

## The Problem

In fintech, standard CI/CD pipelines only check if code *works technically*. They don't check:
- Will this release violate PCI-DSS or SOX compliance?
- What's the business risk of this change going live?
- Should a Business Analyst approve this before it touches production?

**VaultOps fixes that.** It adds a BA Governance Layer on top of DevOps — making business analysts a first-class actor in the deployment pipeline.

---

## Architecture

```
Developer submits release (React Dashboard)
          ↓
FastAPI Backend receives request
          ↓
Llama 3.1 8B (HuggingFace Router) analyzes:
  • Business Risk Score (0–100)
  • PCI-DSS / SOX Regulatory Flags
  • AI Reasoning & Recommendation
          ↓
BA reviews on dashboard → APPROVE or REJECT
          ↓
GitHub Actions Pipeline checks BA gate via API
  • APPROVED → pipeline continues
  • REJECTED → pipeline BLOCKS, deploy stops
          ↓
Terraform deploys release artifact to AWS
  • Artifact uploaded to S3
  • EC2 instance updated
  • RDS records deploy event
          ↓
Post-Deploy Metric Watcher
  • AI compares pre/post metrics
  • Auto-triggers rollback if thresholds breach
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React + Vite + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | PostgreSQL (AWS RDS) |
| AI Engine | Llama 3.1 8B via HuggingFace Router |
| Infrastructure | Terraform (AWS EC2 + S3 + RDS) |
| Pipeline | GitHub Actions |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |

---

## Key Features

### 🤖 AI Risk Engine
Llama 3.1 8B analyzes every release description and returns:
- **Risk Score** (0–100) with color-coded severity
- **Regulatory Flags** — PCI-DSS and SOX violation detection
- **Cost of Delay** — hourly revenue impact if release is blocked
- **Natural language reasoning** explaining the risk assessment

### 🏦 BA Approval Gate
The Business Analyst sees a purpose-built dashboard showing all risk data and makes an approve/reject decision with optional comments. No deploy happens without this decision.

### ⚙️ GitHub Actions Integration
The pipeline calls the BA Gate API before deploying:
```yaml
- name: Check BA approval status
  run: |
    APPROVED=$(curl -s "$API_URL/gate/$RELEASE_ID" | python3 -c "...")
    if [ "$APPROVED" != "true" ]; then
      echo "❌ DEPLOY BLOCKED — BA has not approved"
      exit 1
    fi
```

### 🏗️ Terraform Infrastructure
Real AWS infrastructure provisioned as code:
```hcl
resource "aws_s3_bucket" "vaultops_artifacts" { ... }
resource "aws_db_instance" "vaultops_db" { ... }
resource "aws_instance" "vaultops_backend" { ... }
```

### 📊 Post-Deploy Rollback Monitor
After deploy, AI compares business metrics (transaction success rate, revenue/min, error rate). If metrics breach thresholds, it recommends and triggers automatic rollback.

---

## Project Structure

```
VaultOps/
├── terraform/              # AWS infrastructure as code
│   ├── main.tf             # EC2, RDS, S3 resources
│   ├── variables.tf
│   └── outputs.tf
├── backend/                # FastAPI application
│   ├── main.py             # API routes
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── ai_engine.py        # HuggingFace LLM integration
│   ├── database.py         # SQLAlchemy setup
│   └── requirements.txt
├── frontend/               # React dashboard
│   └── src/
│       └── App.jsx         # Full dashboard UI
└── .github/
    └── workflows/
        └── pipeline.yml    # BA-gated CI/CD pipeline
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/releases/` | Create release + trigger AI analysis |
| GET | `/releases/` | List all releases |
| GET | `/releases/{id}` | Get release details |
| POST | `/releases/{id}/decision` | BA approve/reject |
| GET | `/gate/{id}` | Pipeline gate check |
| POST | `/releases/{id}/rollback-check` | Post-deploy metric analysis |

---

## Local Setup

**Prerequisites:** Python 3.11+, Node.js, Docker, Terraform CLI, AWS CLI

```bash
# Clone
git clone https://github.com/aarinz/Vaultops.git
cd Vaultops

# Backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Setup .env
DATABASE_URL=your_postgres_url
HF_TOKEN=your_huggingface_token
S3_BUCKET=your_s3_bucket

uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev

# Infrastructure
cd terraform
terraform init
terraform apply
```

---

## Why This Project Matters

Most DevOps projects demonstrate technical pipeline setup. VaultOps demonstrates **cross-functional thinking** — the insight that in regulated industries like fintech, the question isn't just "does the code work?" but "should this change go live at all?"

This maps directly to real enterprise fintech workflows at companies like Stripe, Mastercard, and Razorpay — where compliance, risk, and engineering must align before any production change.
