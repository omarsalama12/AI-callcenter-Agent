# Tech Stack Reference

## Layer Breakdown

### Voice — NVIDIA PersonaPlex
- **What it is:** Real-time, full-duplex speech-to-speech model
- **Why it matters:** Listens and speaks simultaneously — no "wait to speak" lag
- **Key feature:** Persona control via text role prompts + audio voice conditioning
- **Status:** Production (open-source, MIT license for code / NVIDIA Open Model License for weights)
- **Repo:** https://github.com/NVIDIA/personaplex

### Speech Safety — NVIDIA NeMo Guardrails
- **What it is:** Policy-based rails that sit between user input and the LLM
- **Why it matters:** Prevents off-topic responses, competitor mentions, compliance violations
- **Config language:** Colang (per-client config files)
- **Status:** Stable
- **Docs:** https://docs.nvidia.com/nemo-guardrails

### Telephony — Twilio / Vonage
- **What it is:** SIP trunk that routes inbound calls to PersonaPlex
- **Why it matters:** Production-grade call ingestion with number management
- **Protocol:** SIP over TLS + SRTP for media

### Orchestration — Agno
- **What it is:** Multi-agent orchestration framework
- **Why it matters:** Coordinates RAG Agent, Action Agent, and Escalation Agent per call
- **Key feature:** Session state management across multi-turn conversations

### LLM — Ollama + Nemotron
- **What it is:** Local LLM inference server
- **Why it matters:** Zero data egress — everything stays on the server
- **Recommended model:** `nemotron-mini:q4_k_m` (fast + high quality)
- **Fallback model:** `phi3.5:q4_k_m` (lighter for lower-spec hardware)

### Execution — OpenClaw + NemoClaw
- **OpenClaw:** The agent that operates the computer (CRM, ERP, databases)
- **NemoClaw:** The secure sandbox OpenClaw runs inside
- **Why both:** OpenClaw does the work, NemoClaw enforces what it's allowed to do
- **Status:** Alpha (do not use in production yet without testing)
- **Repo:** https://github.com/NVIDIA/NemoClaw

### Knowledge — Qdrant + LlamaIndex
- **Qdrant:** Vector database with namespace isolation per client
- **LlamaIndex:** Handles PDF/document ingestion and chunking
- **Why Qdrant:** Native namespace support = perfect for multi-tenant isolation

### Event Bus — Apache Kafka
- **What it is:** Distributed event streaming platform
- **Why it matters:** Every event (call start, action taken, error) flows through Kafka
- **Use cases:** Audit trail, replay, real-time analytics, sentiment pipeline

### Infrastructure — Docker + Kubernetes
- **Docker:** Each client runs in its own container group
- **Kubernetes:** Manages container lifecycle, auto-scaling, GPU allocation
- **Isolation:** NetworkPolicy ensures zero cross-client traffic

### Monitoring — Grafana + Prometheus
- **Prometheus:** Collects metrics from every service
- **Grafana:** Visualizes per-client dashboards, alerts, sentiment trends
- **Custom metrics:** Resolution rate, TTFT latency, guardrail trigger rate
