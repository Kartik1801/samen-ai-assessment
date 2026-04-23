# SAMEN AI — Client Briefing Document

**Prepared by:** Kartik Dhawan | Cyntexa | April 2026  
**Confidential:** Internal use only

---

> ⚠️ **Transparency Note:** This document combines verified information (from samen.ai website + GitHub assessment repo) with inferred conclusions (from assessment task analysis + interview recap shared by Kartik). Each section is marked with its confidence level.

---

## 1. Who Is Samen AI?

**Source: ✅ Verified — samen.ai website**

Samen AI (samen.ai) is a Dutch AI consultancy and product company based in the Netherlands. They describe themselves as "human-centred AI" — not a traditional consultancy but a flexible team-assembly model where they bring together their own people and network specialists around a client's problem.

| Field          | Detail                                                   |
| -------------- | -------------------------------------------------------- |
| Company Name   | SAMEN.ai                                                 |
| Location       | Netherlands                                              |
| Type           | AI Consultancy + Product Company                         |
| Website        | samen.ai                                                 |
| Delivery Model | Sprint-based — intake to live in 2–6 weeks               |
| Team Model     | Flexible — own people + network specialists              |
| Compliance     | EU GDPR & AI Act compliant by design                     |
| Our Engagement | Staff augmentation — Cyntexa team working under Samen AI |

---

## 2. What Samen AI Does — Service Portfolio

**Source: ✅ Verified — samen.ai website**

### 2.1 Core Practice Areas

| Practice Area       | What It Covers                                               | Technologies                                  |
| ------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| LLM & Agents        | Copilots, RAG pipelines, secure enterprise knowledge flows   | OpenAI, Claude, Mistral, Gemini, Groq, Cohere |
| Computer Vision     | MediaPipe pipelines + AI copilots for QA, safety, proctoring | MediaPipe, Ultralytics YOLO, OpenVINO         |
| Pattern Recognition | Fraud detection, churn prediction, anomaly detection         | Scikit-learn, PyTorch, TensorFlow             |

### 2.2 Department-Level Solutions

| Department | What They Build                                                  |
| ---------- | ---------------------------------------------------------------- |
| HR         | Time-to-hire reduction, mobility matching, policy Q&A bots       |
| Marketing  | SEO automation, content factory, brand consistency AI            |
| Sales      | Lead scoring, call summarization, AI-generated proposals         |
| Operations | Demand forecasting, route optimization, document flow automation |
| Finance    | AP automation, anomaly detection, financial forecasting          |
| IT         | Ticket triage, RAG knowledge bases, AI governance tools          |

### 2.3 Full Technology Stack

| Category          | Technologies                                                               |
| ----------------- | -------------------------------------------------------------------------- |
| LLM / AI APIs     | OpenAI, Anthropic Claude, Mistral AI, Meta AI, Google Gemini, Groq, Cohere |
| Computer Vision   | Google MediaPipe, Ultralytics YOLO, OpenVINO                               |
| ML / Data Science | Scikit-learn, PyTorch, TensorFlow, NumPy, Pandas                           |
| Cloud             | Microsoft Azure, AWS, Google Cloud Platform                                |
| Backend           | Python (FastAPI / Flask / Django)                                          |
| Compliance        | EU GDPR, EU AI Act, Dutch data regulations                                 |

---

## 3. Their Flagship Vision — The Intelligence OS

**Source: ⚠️ Inferred — from interview recap shared by Kartik + assessment task design**  
_Not publicly documented on their website_

Beyond client delivery, Samen AI is building a proprietary platform called the **Intelligence OS** — their long-term product, similar in concept to Palantir Foundry but AI-first.

**What it is (as described in interview):**

- Connects to enterprise data sources via custom connectors
- ETL pipelines that normalize and ingest data (GitHub, Jira, Salesforce, SAP, etc.)
- AI layer that monitors, observes, and analyzes enterprise data
- Generates business insights — predictions, suggestions, anomaly alerts

### Architecture Inferred From Assessment Tasks

| Layer               | What It Does                                                       | Assessment Task That Tested It         |
| ------------------- | ------------------------------------------------------------------ | -------------------------------------- |
| Connector Layer     | Connects to external APIs — auth, pagination, rate limits, retries | Task 3: GitHub Issues Connector        |
| Normalization Layer | Standardizes data into canonical schema                            | Task 3: NormalizedRecord dataclass     |
| Orchestration Layer | Concurrent workers, queues, resource lifecycle management          | Task 1: C threading/mutex/shutdown     |
| Intelligence Layer  | ML models that learn from enterprise data patterns                 | Task 4: Q-Learning agent               |
| Architecture Layer  | Scalable system design for thousands of APIs                       | Task 2: Universal API Connector design |

---

## 4. What Work They Will Likely Expect From Our Team

**Source: ⚠️ Inferred — from assessment tasks + website + interview recap**  
_This is our best analysis, not a stated job description_

### 4.1 High Probability (70%+)

- **Python API Connectors** — connecting to enterprise REST APIs, Link header pagination, retry strategies (429 with Retry-After, 5xx exponential backoff), auth handling, data normalization
- **ETL / Data Pipelines** — ingesting enterprise data, schema drift detection, continuous pipeline updates
- **LLM Integration** — RAG on enterprise data, Claude/OpenAI/Mistral API in Python, prompt engineering for business insights, vector embeddings + semantic search
- **Testing & Code Quality** — pytest unit tests, unittest.mock for HTTP mocking, edge case coverage
- **FastAPI Endpoints** — exposing connector data, health checks, schema validation

### 4.2 Medium Probability (40–60%)

- Local LLM inference — Ollama, llama.cpp (explains "good laptop for compute AI" requirement)
- Computer Vision — MediaPipe or YOLO for proctoring, QA, safety monitoring
- Docker & containerization — packaging connectors and services
- Observability — logging, metrics, alerts for connector health
- Full-stack development — React/Node.js dashboards for Intelligence OS

### 4.3 Lower Probability (20%)

- Training ML models from scratch — more likely fine-tuning pre-trained models
- Heavy ML research / mathematics — more applied than theoretical
- C/systems programming — used as a screening signal in assessment, unlikely daily
- Reinforcement Learning in production — conceptual understanding useful, not daily work

---

## 5. Client Project Types Mentioned in Interview

**Source: ⚠️ Inferred — from interview recap shared by Kartik**

| Project                | Description                                                        | Technologies Implied                                           |
| ---------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------- |
| AI Proctoring System   | Educational institute — monitors exam sessions, detects violations | MediaPipe, face detection, speaker diarization, audio analysis |
| Automated Driving Test | AI evaluates driving behavior, pass/fail determination             | Computer vision, behavioral pattern recognition                |
| Intelligence OS        | Internal product — enterprise data connectors + AI insights        | Python, ETL, LLM, RAG, FastAPI                                 |
| HR Automation          | Time-to-hire, candidate matching, policy Q&A                       | LLM, RAG, vector search                                        |
| Finance Automation     | AP automation, anomaly detection, forecasting                      | ML models, time-series forecasting                             |

> 💡 **Note:** Kartik mentioned the MediaPipe-based proctoring solution (face detection + speaker diarization) in the interview and Samen AI responded positively. This project story should be used in fresher interviews too.

---

## 6. Assessment Summary

**Source: ✅ Verified — GitHub repo (Kartik1801/samen-ai-assessment) + failure_analysis.md**

### Tasks & Scores

| Task        | Topic                                               | Score      | Key Failure Reason                                                                         |
| ----------- | --------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------ |
| Task 1      | Systems Debugging (C) — thread sync, resource leaks | 2/5        | Missed full queue overflow bug, incomplete shutdown logic, partial FD management           |
| Task 2      | Architecture Design — Universal API Connector       | 3/5        | Surface-level design, missing failure scaling, no contract testing                         |
| Task 3      | GitHub Issues Connector (Python)                    | 2/5        | Pagination logic broken (return inside for loop), retry didn't use continue, missing tests |
| Task 4      | Reinforcement Learning — Q-Learning                 | 2/5        | Wrong update rule (parentheses error), biased argmax, no baseline comparison               |
| **Overall** |                                                     | **2.25/5** | Implementation quality + edge cases + completeness                                         |

### What The Assessment Was Really Testing

The assessment was NOT testing ML theory. It was testing:

- **Production code correctness** — does your code work in edge cases?
- **Control flow discipline** — do you know when to use `continue`, `return`, `break`?
- **Systems thinking** — can you reason about concurrency, resource leaks, shutdown?
- **Mathematical translation** — can you accurately convert a formula into code?
- **Completeness** — do you deliver everything asked, or cut corners?

### Why Selected Despite 2.25/5

Feedback specifically noted: _"decent architectural intuition"_ and the architecture test (Task 2) was the highest score. They selected based on potential and architectural thinking — not implementation perfection.

---

## 7. Our Team & Role Alignment

**Source: ⚠️ Inferred — based on Kartik's actual skills + fresher training context**

### 7.1 Kartik Dhawan — Senior (May 4 Onboarding)

| Samen AI Need           | Kartik's Equivalent                                 | Gap                       |
| ----------------------- | --------------------------------------------------- | ------------------------- |
| API Connectors (Python) | EVCO MCP Server — OAuth2, RBAC, GCP Cloud Run       | Language only (JS→Python) |
| ETL Pipelines           | BigQuery ETL from Salesforce + Employee Navigator   | Python syntax             |
| LLM Integration         | Claude API — n8n multi-agent pipelines, MCP servers | Python vs JS, minimal     |
| System Architecture     | Palantir Foundry — same concept as Intelligence OS  | None — strongest area     |
| Computer Vision         | MediaPipe proctoring system (previous org)          | Needs refresh             |
| ML / Python             | No direct production experience                     | Primary gap to close      |

> 🟢 **Strongest Angle:** EVCO MCP Server is a production Intelligence OS — enterprise data → BigQuery ETL → Claude-powered NL querying with OAuth2 + RBAC. This IS their Intelligence OS vision, already built.

### 7.2 Fresher Team — Interview Stage

| Name  | Available From           | Strengths                                                     | Primary Gap                                             |
| ----- | ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------- |
| Mohit | Now (Apr 23)             | Python, PySpark, SQL, Scikit-learn, Regression/Classification | API connectors, LLM integration, testing, system design |
| Ayush | Apr 27                   | Python, PySpark, SQL, Scikit-learn, Regression/Classification | API connectors, LLM integration, testing, system design |
| Yash  | May 9 (exams till May 8) | Python, PySpark, SQL, some ML                                 | API connectors, LLM integration, testing, system design |

---

## 8. Engagement Terms & Requirements

**Source: ✅ Verified — shared by Samen AI via Cyntexa Slack**

| Requirement   | Detail                                                            |
| ------------- | ----------------------------------------------------------------- |
| Working Hours | 1:30 PM to 10:30 PM IST (Dutch business hours)                    |
| Internet      | Fast, stable connection required                                  |
| Hardware      | Good laptop/desktop for local AI compute (Ollama, local LLMs)     |
| Audio         | Clear microphone and earphones — client flagged audio quality     |
| Legal         | NDA + IP ownership — all code is Samen AI's intellectual property |
| Contract      | To be handled by Cyntexa (VJ/Neha)                                |

> ⚠️ **Action Required:** Kartik must have clear mic + earphones before May 4. Client specifically mentioned audio difficulty. Budget ~₹1500–3000 (Boult, Noise, Sony).

---

## 9. Preparation Strategy

### 9.1 Kartik — 11 Days to May 4

| Priority    | Topic                      | Why                                | Days      |
| ----------- | -------------------------- | ---------------------------------- | --------- |
| 🔴 Critical | Python production patterns | Root cause of assessment failures  | Day 1–3   |
| 🔴 Critical | API connector in Python    | Core daily work                    | Day 3–5   |
| 🔴 Critical | pytest + mocking           | Assessment specifically checked    | Day 5–6   |
| 🟠 High     | FastAPI                    | Likely daily work                  | Day 6–7   |
| 🟠 High     | LLM API in Python          | Strongest skill — port to Python   | Day 7–9   |
| 🟡 Medium   | Q-learning fix             | Complete the deliverable           | Day 9–10  |
| 🟡 Medium   | Ollama / local LLM         | Client wants compute AI capability | Day 10–11 |

### 9.2 Freshers — Interview Prep Track

| Phase    | Focus                                                              | Deliverable                                |
| -------- | ------------------------------------------------------------------ | ------------------------------------------ |
| Week 1   | Python API connectors — requests, pagination, retry, normalization | Working connector with tests               |
| Week 1   | System design — Intelligence OS architecture                       | Can explain connector-ETL-AI stack clearly |
| Week 2   | LLM integration — Claude/OpenAI API in Python                      | Simple RAG demo or LLM data analysis       |
| Week 2   | Interview prep — resume projects, profile confidence               | Speak to all projects fluently             |
| Week 2–3 | Mock interviews — Samen AI style simulation                        | 4-task mock completed with review          |

---

## 10. Key Takeaways

**What Samen AI really is:**  
A Dutch AI consultancy building enterprise AI solutions (LLM, Computer Vision, Pattern Recognition) for clients AND developing an Intelligence OS product internally. They prioritize production-grade implementation quality over theoretical AI knowledge.

**What they will actually expect from us:**  
Production Python code — API connectors, ETL pipelines, LLM integration, proper error handling, testable code. Not ML research. Builder mindset with attention to correctness and edge cases.

**Our strongest positioning:**  
Kartik's EVCO project is the perfect proof point — it IS their Intelligence OS architecture in production. Lead every conversation with that. Freshers bring Palantir + Python + ML foundations — position them as builders under senior guidance.

---

## Sources & Confidence Levels

| Section                      | Source                                           | Confidence |
| ---------------------------- | ------------------------------------------------ | ---------- |
| Company overview             | samen.ai website (fetched directly)              | ✅ High    |
| Service portfolio            | samen.ai website (fetched directly)              | ✅ High    |
| Technology stack             | samen.ai website (fetched directly)              | ✅ High    |
| Engagement terms             | Cyntexa Slack (shared by Kartik)                 | ✅ High    |
| Assessment tasks & scores    | GitHub repo — Kartik1801/samen-ai-assessment     | ✅ High    |
| Intelligence OS architecture | Interview recap + assessment inference           | ⚠️ Medium  |
| Expected daily work          | Assessment analysis + website inference          | ⚠️ Medium  |
| Client project types         | Interview recap shared by Kartik                 | ⚠️ Medium  |
| Team gap analysis            | Kartik's self-reported skills + training context | ⚠️ Medium  |

---

_Prepared by Kartik Dhawan | Cyntexa | April 2026_
