# NarrativeNexus - Azure Deployment Plan

**Status:** Planning Phase

## Phase 1: Planning

### Step 1: Workspace Analysis
- Mode: MODIFY (existing Streamlit app)
- Project Type: Python Streamlit Web Application
- Current State: Local development with NLP utilities

### Step 2: Requirements Gathering
- Classification: Web Application (AI/ML)
- Scale: Single-tier web app
- Budget: Standard tier preferred
- Hosting: Container-based (recommended for Streamlit)

### Step 3: Codebase Scan
- Framework: Streamlit
- Language: Python 3.x
- Key Dependencies: streamlit, pandas, scikit-learn, gensim, transformers, nltk, spacy
- UI Assets: Custom CSS, JavaScript libraries (tom-select, vis-network)
- Data: Sample uploaded_files directory
- Entry Point: app.py

### Step 4: Recipe Selection
- **Selected:** AZD + Terraform
- Rationale: Streamlit apps work best in Container Apps for scalability and portability

### Step 5: Architecture Planning
- **Service:** Azure Container Apps
- **Container Registry:** Azure Container Registry (ACR)
- **Components:**
  - Streamlit Frontend (containerized)
  - Environment variables for configuration
  - File upload storage (Azure Blob Storage)

### Step 6: Deployment Decisions
- **Deployment Type:** Docker container via Azure Container Apps
- **Database:** None (stateless app with optional blob storage)
- **Authentication:** Public access
- **Monitoring:** Basic Application Insights

---

## Phase 2: Execution (Pending Approval)

### Step 1: Research Components
- [ ] Load Azure Container Apps references
- [ ] Review Docker containerization patterns
- [ ] Load Terraform references

### Step 2: Confirm Azure Context
- [ ] Check subscription and location
- [ ] Verify resource limits

### Step 3: Generate Artifacts
- [ ] Create Dockerfile for Python/Streamlit
- [ ] Create Terraform configuration for:
  - Resource group
  - Azure Container Registry (ACR)
  - Container App environment
  - Container App (Streamlit frontend)
  - Log Analytics workspace
- [ ] Create .dockerignore
- [ ] Create .streamlit/config.toml for production

### Step 4: Security Hardening
- [ ] Configure environment variables for Streamlit
- [ ] Set appropriate resource limits (2 CPU, 4Gi memory)
- [ ] Configure logging and monitoring

### Step 5: Functional Verification
- [ ] Build Docker image locally
- [ ] Test container locally with `docker run`
- [ ] Verify Streamlit interface loads correctly

### Step 6: Update Plan Status
- [ ] Mark as "Ready for Validation"

### Step 7: Hand Off to azure-validate
- [ ] Invoke azure-validate skill

---

## Technical Specifications

- **Container Image:** NarrativeNexus Python Streamlit app
- **Base Image:** python:3.11-slim
- **Port:** 8501 (Streamlit default)
- **CPU:** 2 cores
- **Memory:** 4 GB
- **Auto-scaling:** Enabled (min 1, max 3 replicas)
- **Registry:** Azure Container Registry (for image storage)

## Expected Outcomes

- **Deployed URL:** Azure Container Apps public FQDN (e.g., `narrativenexus-[RANDOM].eastus.azurecontainerapps.io`)
- **Access:** Public Streamlit web interface (no authentication)
- **Scalability:** Auto-scaling based on CPU/memory metrics
- **Cost Estimate:** ~$50-100/month (depending on usage)

