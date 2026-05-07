# AI-Native BPO Platform — Full Project Plan

> An enterprise-grade, multi-tenant AI call center platform where autonomous agents handle customer calls, understand intent, and execute real tasks on company systems — with natural voice and zero perceptible latency.

---

## 1. Full Tech Stack

| Layer | Technology | Status | Role |
|---|---|---|---|
| Voice | NVIDIA PersonaPlex | Production | Full-duplex speech — listens and speaks simultaneously |
| Speech Safety | NeMo Guardrails | Stable | Blocks wrong responses and off-topic behavior |
| Telephony | Twilio / Vonage | Production | SIP Trunk — call ingestion and routing |
| Orchestrator | Agno | Stable | Coordinates the agent team and manages sessions |
| Brain | Ollama + Nemotron | Production | Local LLM — zero data egress to the internet |
| Hands | OpenClaw + NemoClaw | Alpha | Secure execution on client systems inside a sandbox |
| Memory | Qdrant + LlamaIndex | Stable | RAG — isolated knowledge base per client |
| Event Bus | Apache Kafka | Production | Streams and logs every system event |
| Infrastructure | Docker + Kubernetes | Production | Each client isolated in its own container group |
| Monitoring | Grafana + Prometheus | Production | Live dashboards and real-time sentiment analysis |

---

## 2. Hardware Requirements

### Production Server

| Component | Minimum | Recommended | Role |
|---|---|---|---|
| CPU | 2x Intel Xeon 32-core | 2x AMD EPYC 9354 (32-core) | Request processing, Kafka, Kubernetes control plane |
| RAM | 256 GB DDR5 | 512 GB — 1 TB DDR5 | Model loading, vector store, concurrent sessions |
| GPU | 2x NVIDIA A100 40GB | 4x NVIDIA A100 80GB / H100 | PersonaPlex, LLM inference, embeddings |
| Storage | 4x 2TB NVMe SSD | 4x 4TB NVMe (RAID 10) | Call recordings, LLM models, Kafka logs |
| Network | 1x 10Gbps NIC | 2x 25Gbps NIC | Concurrent calls without bottleneck |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS | Full NVIDIA Container Runtime support |

### GPU Allocation Strategy

```
GPU 0 + GPU 1  →  PersonaPlex (Voice)     Highest priority — any lag affects every call
GPU 2          →  Ollama LLM              Shared across clients via fair time-slicing
GPU 3          →  Reserved                Overflow handling + new model loading
```

### Development Machine

| Component | Minimum | Recommended |
|---|---|---|
| CPU | Intel i7 / AMD Ryzen 7 | Intel i9 / AMD Ryzen 9 |
| RAM | 32 GB | 64 GB |
| GPU | NVIDIA RTX 3090 | NVIDIA RTX 4090 24GB |
| Storage | 1TB NVMe | 2TB NVMe |

---

## 3. Build Plan — 4 Phases over 9 Months

```
Month:  1    2    3    4    5    6    7    8    9
        ████ ████                                   Phase 1: Foundation
                  ████ ████                         Phase 2: Integration
                            ████ ████ ████          Phase 3: Multi-Tenant Scale
                                         ████ ████  Phase 4: Production Launch
```

---

### Phase 1: Foundation (Month 1–2)
**Goal: Get the first real call working end-to-end with one client**

| Task | Owner | Duration | Dependencies |
|---|---|---|---|
| Provision server and install OS | DevOps | 3 days | Hardware purchased |
| Install NVIDIA drivers + CUDA + Docker | DevOps | 2 days | Server ready |
| Install and run PersonaPlex | AI Engineer | 3 days | NVIDIA drivers |
| Install Ollama + pull Nemotron model | AI Engineer | 1 day | GPU ready |
| Connect PersonaPlex to Ollama | AI Engineer | 4 days | Both running |
| Install Qdrant + LlamaIndex | AI Engineer | 2 days | — |
| Build initial RAG pipeline | AI Engineer | 5 days | Qdrant ready |
| Connect Twilio as SIP trunk | Backend | 3 days | Twilio account |
| End-to-end voice call test | Team | 3 days | Everything running |
| Bug fixes and latency tuning | Team | 5 days | Test passed |

---

### Phase 2: Integration (Month 3–4)
**Goal: Full stack wired together — voice, reasoning, and real actions**

| Task | Owner | Duration | Dependencies |
|---|---|---|---|
| Install NemoClaw + onboard first sandbox | AI Engineer | 4 days | NemoClaw CLI |
| Build MCP tools for client CRM | Backend | 1 week | CRM API docs |
| Integrate OpenClaw with NemoClaw sandbox | AI Engineer | 5 days | Both ready |
| Configure NeMo Guardrails for first client | AI Engineer | 3 days | Colang config |
| Build Agno orchestration layer | AI Engineer | 1 week | All agents ready |
| Test full action execution (cancel, refund) | Team | 4 days | Agno + NemoClaw |
| Add call recording + transcript pipeline | Backend | 3 days | Storage ready |
| Build initial sentiment analysis | AI Engineer | 3 days | Transcripts available |
| UAT with real client (paid pilot) | Team | 2 weeks | Full phase complete |

---

### Phase 3: Multi-Tenant Scale (Month 5–7)
**Goal: Multiple companies running isolated on the same server**

| Task | Owner | Duration | Dependencies |
|---|---|---|---|
| Convert setup into a repeatable template | DevOps | 1 week | Phase 2 complete |
| Build client onboarding automation script | DevOps | 4 days | Template ready |
| Kubernetes setup + namespace per client | DevOps | 1 week | K8s installed |
| Enforce cross-client NetworkPolicy isolation | DevOps | 3 days | K8s ready |
| Per-client Qdrant namespaces | AI Engineer | 2 days | Qdrant ready |
| GPU resource limits per namespace | DevOps | 3 days | K8s + GPU operator |
| Install Kafka + define initial topics | Backend | 4 days | Kafka server |
| Wire all system events through Kafka | Backend | 1 week | Kafka ready |
| Onboard second client (isolation test) | Team | 4 days | Template + K8s |
| Load test — 50+ concurrent calls | Team | 3 days | Two clients live |

---

### Phase 4: Production Launch (Month 8–9)
**Goal: Full scale, full observability, official launch**

| Task | Owner | Duration | Dependencies |
|---|---|---|---|
| Grafana dashboards per client | DevOps | 4 days | Prometheus |
| Live sentiment analysis dashboard | AI Engineer | 4 days | Grafana ready |
| Kubernetes auto-scaling rules | DevOps | 3 days | K8s + Prometheus |
| GPU time-slicing optimization | AI Engineer | 3 days | Benchmarks complete |
| Full security audit | Security | 1 week | Entire stack |
| Penetration testing on NemoClaw sandboxes | Security | 4 days | Audit complete |
| Disaster recovery + backup strategy | DevOps | 3 days | Production ready |
| Documentation + operational runbooks | Team | 4 days | Everything done |
| Soft launch (3 clients) | Team | 2 weeks | All phases complete |
| Full production launch | Team | 1 week | Soft launch successful |

---

## 4. Team

| Role | Headcount | Start | Core Responsibilities |
|---|---|---|---|
| Principal AI Engineer | 1 | Day 1 | PersonaPlex, Ollama, Agno, NemoClaw, RAG |
| Backend Engineer | 1 | Day 1 | Telephony, APIs, MCP tools, Kafka |
| DevOps / Platform Engineer | 1 | Day 1 | Docker, Kubernetes, GPU allocation, Monitoring |
| Security Engineer | 1 | Month 4 | NemoClaw audit, penetration testing, compliance |
| QA Engineer | 1 | Month 2 | Call testing, load testing, regression |

---

## 5. Budget Estimate

### Hardware (One-time)

| Item | Cost (USD) | Notes |
|---|---|---|
| 4x NVIDIA A100 80GB | $120,000 — $160,000 | Secondary market or direct from NVIDIA |
| 2x AMD EPYC Server CPU | $8,000 — $12,000 | Or Intel Xeon equivalent |
| 512 GB DDR5 ECC RAM | $3,000 — $5,000 | Registered ECC |
| 4x 4TB NVMe SSD | $2,000 — $3,000 | Samsung / WD Enterprise |
| Server chassis + PSU | $3,000 — $5,000 | Supermicro / Dell |
| Networking + KVM + UPS | $2,000 — $3,000 | — |
| **Total** | **$138,000 — $188,000** | |

### Monthly Operating Costs

| Item | Cost (USD/month) | Notes |
|---|---|---|
| Twilio SIP Trunk + minutes | $500 — $2,000 | Scales with call volume |
| Colocation / data center | $1,000 — $3,000 | Or on-premise if space available |
| Monitoring tools | $200 — $500 | Grafana Cloud or self-hosted |
| Offsite backup storage | $200 — $500 | AWS S3 or Wasabi |
| **Total** | **$1,900 — $6,000 / month** | |

### Team Cost (MENA Market Estimate)

| Role | Cost (USD/month) |
|---|---|
| Principal AI Engineer | $3,000 — $5,000 |
| Backend Engineer | $2,000 — $3,500 |
| DevOps Engineer | $2,000 — $3,500 |
| Security + QA | $1,500 — $3,000 |
| **Total** | **$8,500 — $15,000 / month** |

---

## 6. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| NemoClaw is in Alpha — APIs may change | High | Medium | Build an abstraction layer on top so it can be swapped |
| GPU cost is high upfront | High | High | Start with 2 GPUs, expand as clients are signed |
| PersonaPlex latency under high concurrent load | Medium | High | Speculative RAG prefetch + sentence-level streaming |
| Client data leakage between companies | Low | Critical | 4 isolation layers + regular security audits |
| LLM has no knowledge of client policies | Medium | Medium | Per-client RAG + optional fine-tuning later |
| Team unfamiliar with this specific stack | Medium | Medium | Start with a simple prototype and learn by building |

---

## 7. Success Metrics

| Metric | Minimum Target | Ideal Target | How to Measure |
|---|---|---|---|
| Response Latency (TTFT) | < 500ms | < 250ms | Grafana P95 latency |
| Resolution Rate | > 80% | > 95% | Kafka events — resolved vs escalated |
| Concurrent Calls per GPU | 50 calls | 100+ calls | Kubernetes resource metrics |
| Client Data Isolation | 100% | 100% | Security audit — zero cross-leak |
| Guardrails Accuracy | > 95% | > 99% | Manual review sample + Grafana |
| System Uptime | 99% | 99.9% | Prometheus uptime monitor |

---

## Next Step

> Sign the first paying pilot client and buy the hardware — before writing a single line of code.
