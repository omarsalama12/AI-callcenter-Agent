# System Architecture

## High-Level Overview

```
CUSTOMER CALL
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  TELEPHONY GATEWAY                          │
│               Twilio / Vonage SIP Trunk                     │
│         Receives call → identifies client → routes          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SHARED LAYER                             │
│                                                             │
│   PersonaPlex          Kafka            Grafana             │
│   (Voice I/O)          (Event Bus)      (Monitoring)        │
│                                                             │
│   Qdrant               Call Recorder                        │
│   (Vector DB)          (Audio + Transcript)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│   CLIENT A     │ │   CLIENT B     │ │   CLIENT C     │
│   Container    │ │   Container    │ │   Container    │
│                │ │                │ │                │
│ NeMo Guards    │ │ NeMo Guards    │ │ NeMo Guards    │
│ Agno           │ │ Agno           │ │ Agno           │
│ Ollama LLM     │ │ Ollama LLM     │ │ Ollama LLM     │
│ RAG (ns:A)     │ │ RAG (ns:B)     │ │ RAG (ns:C)     │
│ OpenClaw       │ │ OpenClaw       │ │ OpenClaw       │
│ NemoClaw       │ │ NemoClaw       │ │ NemoClaw       │
│ MCP Tools      │ │ MCP Tools      │ │ MCP Tools      │
└───────┬────────┘ └───────┬────────┘ └───────┬────────┘
        │                  │                  │
        ▼                  ▼                  ▼
   Client A CRM      Client B ERP      Client C DB
```

---

## Single Call — Step by Step

```
1. Customer dials
   └── Twilio/Vonage receives via SIP

2. PersonaPlex activates
   └── Full-duplex listening starts immediately
   └── Identifies the client this number belongs to
   └── Loads the correct brand voice persona

3. Speculative processing starts in parallel
   └── While customer is still speaking →
       RAG prefetch begins on partial transcript

4. NeMo Guardrails — Input check
   └── Regex rules (0ms) →
       Embedding similarity (~20ms) →
       LLM check only if suspicious (~150ms)

5. Agno orchestrates
   └── Decides: need knowledge? need action? both?
   └── Dispatches to RAG Agent and/or Action Agent

6. RAG Agent
   └── Retrieves from client's Qdrant namespace only
   └── Returns top-3 relevant chunks

7. Action Agent (if needed)
   └── OpenClaw receives the task
   └── NemoClaw sandbox enforces execution boundaries
   └── MCP tools connect to actual client systems
   └── Returns result

8. Agno assembles final response

9. NeMo Guardrails — Output check
   └── Safe to send? Correct format? On brand?

10. PersonaPlex streams response
    └── Sentence by sentence — customer hears in ~200-400ms

11. Kafka logs everything
    └── Call start, actions taken, topics, outcome, sentiment

12. Call Recorder saves
    └── Audio + full transcript per client storage
```

---

## Isolation Layers (Security)

```
Layer 1 — Kubernetes Namespaces
          Each client in a separate namespace.
          NetworkPolicy blocks all cross-client traffic.

Layer 2 — NemoClaw Sandbox
          OpenClaw runs inside an OpenShell container.
          Cannot reach host filesystem.
          Cannot reach other client systems.
          Egress limited to approved endpoints only.

Layer 3 — Qdrant Namespaces
          Client A knowledge is invisible to Client B agents.
          Enforced at the query level.

Layer 4 — Encrypted Storage
          Call recordings encrypted with a per-client key.
          Keys stored in a separate secrets manager.
```

---

## GPU Allocation

```
GPU 0 + GPU 1  →  PersonaPlex      Highest priority — real-time voice
GPU 2          →  Ollama LLM       Shared via time-slicing across clients
GPU 3          →  Reserved         Overflow + new model loading
```

---

## Latency Strategy

The system targets **< 300ms perceived response time** through:

- **Speculative RAG** — prefetching context while the customer is still speaking
- **Sentence streaming** — PersonaPlex starts speaking after the first sentence, not the full response
- **Guardrails tiering** — regex first, LLM rails only when needed
- **Quantized models** — `q4_k_m` quantization for 2-3x faster inference
- **Connection pooling** — persistent HTTP clients, no new connections per call
