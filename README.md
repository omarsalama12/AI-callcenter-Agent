# AI-callcenter-Agent
Next-Gen AI BPO Platform powered by PersonaPlex, NemoClaw and OpenClaw
# 🤖 AI-Native BPO Platform

> An enterprise-grade, multi-tenant AI call center platform where autonomous agents replace traditional human BPO operations — with full voice interaction, secure task execution, and zero data leakage between clients.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Infrastructure](#infrastructure)
- [Security & Isolation](#security--isolation)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Roadmap](#roadmap)

---

## Overview

Traditional BPO operations rely on massive human headcounts, leading to inconsistent service quality, high turnover, and scaling bottlenecks. This platform replaces that model entirely with AI-native autonomous agents that:

- **Listen and speak** naturally with customers via full-duplex voice
- **Think and reason** using local LLMs with company-specific knowledge
- **Act** on real systems — CRM, ERP, databases — securely and autonomously
- **Scale instantly** from 10 to 10,000 concurrent calls without hiring ramps
- **Stay isolated** — every client lives in its own sandboxed environment

---

## Architecture

```
CUSTOMER CALL
      │
      ▼
┌─────────────────────────────────────────────────┐
│           TELEPHONY GATEWAY                     │
│         Twilio / Vonage SIP Trunk               │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              SHARED LAYER                       │
│                                                 │
│  PersonaPlex     Kafka        Grafana           │
│  (Voice I/O)     (Event Bus)  (Monitoring)      │
│                                                 │
│  Qdrant          Call Recorder                  │
│  (Vector DB)     (Audio + Transcript)           │
└─────────────────────┬───────────────────────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  CLIENT A    │ │  CLIENT B    │ │  CLIENT C    │
│  Container   │ │  Container   │ │  Container   │
│  Group       │ │  Group       │ │  Group       │
│              │ │              │ │              │
│ NeMo Guards  │ │ NeMo Guards  │ │ NeMo Guards  │
│ Agno         │ │ Agno         │ │ Agno         │
│ Local LLM    │ │ Local LLM    │ │ Local LLM    │
│ RAG (ns: A)  │ │ RAG (ns: B)  │ │ RAG (ns: C)  │
│ OpenClaw     │ │ OpenClaw     │ │ OpenClaw     │
│ NemoClaw     │ │ NemoClaw     │ │ NemoClaw     │
│ MCP Tools    │ │ MCP Tools    │ │ MCP Tools    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
  Client A CRM     Client B ERP    Client C DB
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Voice** | NVIDIA PersonaPlex | Full-duplex speech-to-speech, persona control |
| **Safety** | NVIDIA NeMo Guardrails | Input/output rails, topical boundaries, compliance |
| **Telephony** | Twilio / Vonage | SIP trunk, call routing, WebRTC |
| **Orchestration** | Agno | Multi-agent OS, session management, agent routing |
| **LLM** | Ollama + Nemotron | Local inference, zero data egress |
| **Execution** | NVIDIA OpenClaw | Autonomous computer use, system actions |
| **Sandbox** | NVIDIA NemoClaw | Secure agent execution, policy enforcement |
| **Tools** | MCP Tools | CRM/ERP integrations, API connectors |
| **Knowledge** | Qdrant + LlamaIndex | Per-client vector namespaces, RAG pipeline |
| **Messaging** | Apache Kafka | Event streaming, audit trail, scale |
| **Infra** | Docker + Kubernetes | Container orchestration, auto-scaling |
| **Monitoring** | Grafana + Prometheus | Real-time dashboards, sentiment analysis |

---

## How It Works

### A Single Call — Step by Step

```
1. Customer dials the number
   └── Twilio/Vonage receives the call via SIP trunk

2. PersonaPlex activates
   └── Full-duplex listening begins immediately
   └── Identifies which client (company) this number belongs to
   └── Loads the correct voice persona for that brand

3. Speculative processing starts
   └── While customer is still speaking, RAG prefetch begins
   └── Partial transcript triggers knowledge retrieval

4. NeMo Guardrails (Input)
   └── Is this topic allowed for this client?
   └── Regex rules → Embedding similarity → LLM check (escalating)

5. Agno orchestrates
   └── Decides: need information? need action? need both?
   └── Dispatches to RAG Agent and/or Action Agent

6. RAG Agent
   └── Retrieves relevant company policies, pricing, FAQs
   └── Scoped to client's Qdrant namespace only

7. Action Agent (if needed)
   └── OpenClaw receives the task
   └── NemoClaw sandbox enforces execution boundaries
   └── MCP tools connect to actual client systems
   └── Action executes, result returned

8. Agno assembles response
   └── Combines knowledge + action results into natural reply

9. NeMo Guardrails (Output)
   └── Response safe to send? Correct format? On brand?

10. PersonaPlex speaks
    └── Streams response sentence by sentence — no waiting
    └── Customer hears reply in ~200-400ms

11. Kafka logs everything
    └── Call started, actions taken, topics discussed, outcome

12. Call Recorder saves
    └── Audio file + full text transcript per client storage
```

---

## Project Structure

```
ai-bpo-platform/
│
├── shared/                         # مشترك بين كل الشركات
│   ├── personaplex/
│   │   ├── server.py               # PersonaPlex WebSocket bridge
│   │   ├── persona_loader.py       # تحميل persona كل شركة
│   │   └── stream_handler.py       # Token streaming لـ zero lag
│   │
│   ├── telephony/
│   │   ├── twilio_gateway.py       # SIP trunk handler
│   │   ├── call_router.py          # توجيه المكالمة للشركة الصح
│   │   └── session_manager.py      # إدارة جلسات المكالمات
│   │
│   ├── kafka/
│   │   ├── producer.py             # نشر الأحداث
│   │   ├── consumer.py             # استقبال الأحداث
│   │   └── topics.py               # تعريف الـ topics
│   │
│   ├── recorder/
│   │   ├── audio_recorder.py       # تسجيل الصوت
│   │   ├── transcript_saver.py     # حفظ النصوص
│   │   └── sentiment_analyzer.py  # تحليل مشاعر العميل
│   │
│   └── monitoring/
│       ├── grafana/
│       │   └── dashboards/         # JSON dashboards
│       └── prometheus/
│           └── metrics.py          # Custom metrics
│
├── client_template/                # Template لكل شركة جديدة
│   │
│   ├── guardrails/
│   │   ├── config.yml              # LLM backend config
│   │   ├── rails/
│   │   │   ├── input.co            # Input rails (Colang)
│   │   │   ├── output.co           # Output rails
│   │   │   └── topics.co           # Topical boundaries
│   │   └── kb/                     # Knowledge للـ guardrails
│   │
│   ├── agno/
│   │   ├── orchestrator.py         # Main Agno agent team
│   │   ├── agents/
│   │   │   ├── rag_agent.py        # Knowledge retrieval agent
│   │   │   ├── action_agent.py     # Execution agent
│   │   │   └── escalation_agent.py # Human handoff agent
│   │   └── session.py              # Session state management
│   │
│   ├── llm/
│   │   ├── ollama_client.py        # Optimized Ollama client
│   │   ├── system_prompt.txt       # Client-specific persona
│   │   └── model_config.yml        # Model + quantization settings
│   │
│   ├── rag/
│   │   ├── ingestion/
│   │   │   ├── pdf_loader.py       # تحميل ملفات الشركة
│   │   │   ├── api_loader.py       # تحميل من API
│   │   │   └── chunker.py          # تقطيع المعلومات
│   │   ├── retrieval/
│   │   │   ├── qdrant_client.py    # Namespace-scoped queries
│   │   │   └── reranker.py         # ترتيب النتائج
│   │   └── speculative.py          # Prefetch أثناء الكلام
│   │
│   ├── execution/
│   │   ├── openclaw_manager.py     # OpenClaw task dispatcher
│   │   ├── nemoclaw_sandbox.py     # Sandbox lifecycle
│   │   ├── mcp_tools/
│   │   │   ├── crm_tool.py         # CRM connector
│   │   │   ├── erp_tool.py         # ERP connector
│   │   │   └── email_tool.py       # Email sender
│   │   └── action_registry.py     # Allowed actions per client
│   │
│   └── config/
│       ├── client.yml              # Client settings
│       ├── permissions.yml         # What this client can do
│       └── voices/                 # Brand voice assets
│
├── clients/                        # Instance لكل شركة
│   ├── client_telecom_egypt/       # نسخة من client_template
│   ├── client_insurance_ksa/
│   └── client_bank_uae/
│
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml      # Local development
│   │   └── Dockerfiles/
│   │       ├── Dockerfile.shared
│   │       └── Dockerfile.client
│   │
│   └── kubernetes/
│       ├── namespaces/             # Namespace per client
│       ├── shared/                 # Shared services
│       ├── client-template/        # K8s template per client
│       └── gpu-allocation/         # GPU resource limits
│
└── scripts/
    ├── onboard_client.sh           # إضافة شركة جديدة
    ├── ingest_knowledge.sh         # رفع معلومات الشركة
    └── health_check.sh             # فحص حالة النظام
```

---

## Infrastructure

### Physical Server Requirements

```
Component     Minimum              Recommended
─────────────────────────────────────────────
CPU           2x 32-core Xeon      2x AMD EPYC 64-core
RAM           256 GB               512 GB - 1 TB
GPU           2x A100 40GB         4x A100 80GB / H100
Storage       4x 2TB NVMe          4x 4TB NVMe (RAID 10)
Network       10 Gbps              2x 25 Gbps NIC
```

### GPU Allocation Strategy

```
GPU 0 + GPU 1  →  PersonaPlex (real-time voice — highest priority)
GPU 2          →  Ollama LLM  (shared across clients, time-sliced)
GPU 3          →  Reserved    (overflow + model loading)
```

### Kubernetes Namespaces

```
k8s namespaces:
├── shared-services     # PersonaPlex, Kafka, Grafana, Qdrant
├── client-a            # All containers for Client A
├── client-b            # All containers for Client B
└── client-c            # All containers for Client C

Network policy:
- shared-services → can receive from all client namespaces
- client-a        → CANNOT reach client-b or client-c
- client-b        → CANNOT reach client-a or client-c
```

---

## Security & Isolation

### Four Layers of Isolation

```
Layer 1 — Kubernetes Namespaces
  Each client in a separate namespace
  NetworkPolicy blocks cross-client traffic

Layer 2 — NemoClaw Sandbox
  OpenClaw agent runs inside OpenShell container
  Cannot access host filesystem
  Cannot reach other client systems
  Egress limited to allowed endpoints only

Layer 3 — Qdrant Namespaces
  Client A's knowledge invisible to Client B's agents
  Enforced at query level, not just application level

Layer 4 — Encrypted Storage
  Call recordings encrypted with per-client key
  Keys stored in separate secrets manager
  Anthropic-style zero-trust key access
```

---

## Getting Started

### Prerequisites

```bash
# Required on host
- Docker 28+
- Kubernetes (k3s or full K8s)
- NVIDIA Container Runtime
- CUDA 12.x
- Ollama
- NemoClaw CLI
```

### Install NemoClaw

```bash
curl -fsSL https://www.nvidia.com/nemoclaw.sh | bash
```

### Pull Required Models

```bash
# Main reasoning model
ollama pull nemotron-mini:q4_k_m

# Fallback / lighter model
ollama pull phi3.5:q4_k_m
```

### Start Shared Services

```bash
docker-compose -f infra/docker/docker-compose.yml up -d
```

### Onboard a New Client

```bash
./scripts/onboard_client.sh \
  --name "telecom_egypt" \
  --voice NATM1 \
  --language ar-EG \
  --crm-url https://crm.client.com/api \
  --knowledge-dir ./docs/telecom_egypt/
```

### Ingest Client Knowledge

```bash
./scripts/ingest_knowledge.sh \
  --client telecom_egypt \
  --source ./docs/telecom_egypt/policies.pdf \
  --source ./docs/telecom_egypt/pricing.pdf \
  --source ./docs/telecom_egypt/faqs.pdf
```

---

## Configuration

### Client Configuration (`client.yml`)

```yaml
client:
  id: telecom_egypt
  name: "Telecom Egypt Services"
  language: ar-EG
  dialect: egyptian

voice:
  persona: NATM1
  role_prompt: |
    إنت خالد، موظف خدمة عملاء محترف في شركة X للاتصالات.
    بتتكلم باللهجة المصرية، هادي، ومحترم في كل الأوقات.

llm:
  model: nemotron-mini:q4_k_m
  temperature: 0.3
  max_tokens: 200
  context_window: 2048

guardrails:
  blocked_topics:
    - competitors
    - internal_pricing
    - employee_names
  escalate_to_human_if:
    - customer_anger_score > 0.8
    - topic = legal_complaint
    - action = refund > 5000

permissions:
  allowed_actions:
    - get_account_info
    - check_balance
    - cancel_service
    - create_ticket
    - send_confirmation_email
  denied_actions:
    - delete_account
    - modify_billing_cycle
    - access_payment_card
```

---

## Monitoring

### Grafana Dashboards

Every client gets a real-time dashboard showing:

```
┌─────────────────────────────────────────────────┐
│  CLIENT A — Live Dashboard                      │
│                                                 │
│  Active Calls: 47      Avg Handle Time: 3:24   │
│  Resolution Rate: 94%  Escalations: 3          │
│                                                 │
│  Sentiment Trend ────────────────────           │
│  😊 Positive  ████████████████  72%            │
│  😐 Neutral   ████████         28%             │
│  😠 Negative  ██                6%             │
│                                                 │
│  Top Actions Executed Today:                    │
│  create_ticket        ████████████  847         │
│  get_account_info     ████████      612         │
│  cancel_service       ████          289         │
│                                                 │
│  LLM Latency P95: 380ms  RAG Latency P95: 45ms │
└─────────────────────────────────────────────────┘
```

### Key Metrics Tracked

```
Call metrics:     volume, duration, resolution rate, escalation rate
Voice metrics:    PersonaPlex latency, interruption count
LLM metrics:      TTFT (time to first token), full response time
Action metrics:   execution success rate, action types, failures
Safety metrics:   guardrail triggers, blocked topics, policy violations
System metrics:   GPU utilization, memory, Kafka lag, error rates
```

---

## Roadmap

```
Phase 1 — Foundation          (Month 1-2)
  ✅ Core stack integration
  ✅ Single client pilot
  ✅ Arabic dialect support (Egyptian)

Phase 2 — Multi-Tenant        (Month 3-4)
  ⬜ Multi-client isolation
  ⬜ Client onboarding automation
  ⬜ PersonaPlex multi-persona management

Phase 3 — Scale               (Month 5-6)
  ⬜ Kafka full integration
  ⬜ Kubernetes auto-scaling
  ⬜ GPU time-slicing optimization

Phase 4 — Expansion           (Month 7+)
  ⬜ KSA dialect support
  ⬜ UAE dialect support
  ⬜ PDPL (Saudi) compliance module
  ⬜ Advanced sentiment & QA scoring
```

---

## License

Proprietary — All rights reserved.

---

> Built with NVIDIA PersonaPlex · OpenClaw · NemoClaw · NeMo Guardrails · Agno · Ollama · Qdrant · Apache Kafka · Kubernetes
