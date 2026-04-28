# Mock Interview — Mohit Saini

**Interviewer:** Kartik Dhawan | Cyntexa  
**Format:** Round 1 (Intro, 30–45 min) + Round 2 (4-hour task assessment)

---

## Round 1: Introduction & Project Deep-Dive

### Section A: Warm-Up & Background (5 min)

**Q1: Tell me about yourself and your journey as a developer.**

> **What to listen for:** Does he position himself as an AI/ML engineer? Does he lead with LLM/RAG experience (his strongest area)? Does he mention Claude, GCP, production AI systems?
>
> **Good answer:** "I'm a Senior Software Developer with 5+ years focused on building production AI systems — from RAG optimization and GenAI platforms on GCP Vertex AI, to ETL pipelines and automated sales funnels using Claude and n8n. I work primarily in Python with PyTorch, LangChain, and Scikit-learn."

**Q2: What excites you about working with a European AI company like Samen AI?**

> **What to listen for:** Same as Ayush — has he researched Samen AI? Bonus if he connects his RAG/connector work to their Intelligence OS vision.
>
> **Good answer mentions:** Dutch AI consultancy, Intelligence OS concept, enterprise data connectors feeding AI insights, EU AI Act compliance, production-grade AI.

---

### Section B: Resume Project Deep-Dive (15–20 min)

#### RAG Optimization & Evaluation System

**Q3: Walk me through your RAG Optimization system. What problem were you solving and how did you approach it?**

> **Expected answer:** Enterprise AI applications were getting poor retrieval quality → hallucinated or irrelevant LLM responses. Built an optimization framework to improve retrieval accuracy. Tested multiple chunking strategies (fixed-size, semantic, hierarchical), established evaluation benchmarks, added guardrails (PII detection, toxicity, hallucination reduction, prompt injection protection). Deployed on GCP (Vertex AI, BigQuery, Cloud Run).
>
> **Follow-up probes:**
>
> - "What chunking strategy worked best and why?" → Should have a nuanced answer: semantic chunking preserves context boundaries but is slower; fixed-size is fast but splits mid-sentence; hierarchical gives best of both with parent-child structure.
> - "How did you measure retrieval quality?" → Should mention metrics like MRR (Mean Reciprocal Rank), NDCG, recall@k, faithfulness score, answer relevancy.
> - "How does your hallucination reduction work?" → Should mention: grounding responses in retrieved context, citation checking, confidence thresholds, factual consistency scoring.

**Q4: What is prompt injection and how did you protect against it?**

> **Expected answer:** Prompt injection is when malicious user input manipulates the LLM to ignore its system prompt or perform unintended actions (e.g., "ignore previous instructions and..."). Protection: input sanitization, system prompt armoring, output filtering, separate system/user message boundaries, canary tokens, content moderation layer.
>
> **Red flag:** If he only says "we filtered bad words" — that's surface-level.

#### Vertex AI GenAI Platform

**Q5: You built MLOps workflows on Vertex AI. Walk me through the model lifecycle — from training to production.**

> **Expected answer:** Data ingestion (BigQuery/Dataflow) → feature engineering (Feature Store) → model training (Vertex AI Workbench/Training) → experiment tracking (Vertex AI Experiments) → model evaluation → Model Registry (versioning, staging) → deployment (Vertex AI Endpoints) → monitoring (prediction drift, feature drift) → retraining trigger.
>
> **Follow-up:** "How did you handle model versioning?" → Model Registry with staging/production labels, A/B testing with traffic splitting, rollback capability.

**Q6: How did you implement observability for your production AI systems?**

> **Expected answer:** Structured logging, metrics collection (latency, throughput, error rates), alerting on anomalies, prediction distribution monitoring, feature drift detection, dashboard visualization. Should mention specific tools or GCP services.
>
> **This maps directly to Samen AI's observability requirement in Task 2.**

#### AI Lead Generation & Outreach Automation

**Q7: This is interesting — you built scrapers, ETL, and AI qualification in one pipeline. Walk me through the architecture end-to-end.**

> **Expected answer:**
>
> 1. **Scraping:** Playwright scrapers on Depop/Vinted → extract seller profiles, listings, pricing, activity
> 2. **ETL:** Clean + normalize → BigQuery (dedup, format standardization)
> 3. **AI Qualification:** Claude scores leads against ideal customer profile (inventory volume, category, pricing tier, activity)
> 4. **Proposal Generation:** Claude + prompt engineering → personalized wholesale bundle proposals
> 5. **Orchestration:** n8n schedules daily runs, triggers workflows, manages webhooks
>
> **Follow-up probes:**
>
> - "How did you handle anti-bot measures?" → Should mention: rotating proxies, headless browser fingerprint randomization, rate limiting own requests, retry on blocks.
> - "How did you handle pagination in the scrapers?" → **Critical question** — tests if he understands pagination patterns before Task 3.
> - "What happens when a scrape fails mid-way?" → Should mention: checkpoint/resume logic, dead letter queue, alerting, idempotent processing.

**Q8: You used Claude for lead qualification. How did you structure the prompt to get consistent scoring?**

> **Expected answer:** System prompt with scoring rubric, structured output format (JSON), few-shot examples of good/bad leads with scores, temperature set low for consistency, validation of output schema before processing.
>
> **Bonus:** Mentions retry on malformed LLM output, fallback scoring logic.

#### Recommendation Engine

**Q9: Your recommendation engine was built "without relying on third-party AI APIs." Explain the algorithms you used.**

> **Expected answer:**
>
> - **Collaborative filtering:** User-item interaction matrix → find similar users (user-based) or similar items (item-based) → recommend based on neighbors. Uses matrix factorization (SVD, ALS) for scalability.
> - **Content-based:** Item feature vectors (category, price, description embeddings) → cosine similarity with user's liked items.
> - **Hybrid:** Weighted combination or cascade (content-based for cold-start, collaborative for established users).
>
> **Follow-up:** "What is matrix factorization and why is it better than raw similarity?" → Decomposes user-item matrix into latent factor matrices, handles sparsity, captures hidden patterns, much more scalable.

**Q10: How did you evaluate recommendation quality?**

> **Expected answer:** Precision@K, Recall@K, MAP (Mean Average Precision), NDCG, RMSE for rating prediction. Should mention offline vs online evaluation — offline on holdout set, online via A/B testing (click-through rate, conversion rate).

---

### Section C: Conceptual Questions (10–15 min)

**Q11: What is the difference between a 429 and a 403 HTTP response? How would you handle each in an API connector?**

> **Expected answer:**
>
> - **429:** Rate limited — too many requests. Handle: read `Retry-After` header, sleep, retry. Use `continue` to restart the request loop.
> - **403:** Forbidden — usually permission denied. BUT GitHub sometimes returns 403 for rate limiting too. Must check for `x-ratelimit-reset` or `Retry-After` headers to distinguish. If no rate limit headers → it's a real 403, don't retry.
>
> **This is the exact trap from Task 3.** If he gets this right conceptually, he'll likely handle it in code.

**Q12: Explain the Q-learning update rule. Write it out and explain each term.**

> Write the formula: `Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a')) - Q(s,a)]`
>
> **Expected answer:**
>
> - `Q(s,a)` = estimated value of taking action a in state s
> - `alpha` = learning rate
> - `r` = immediate reward received
> - `gamma` = discount factor (0 to 1, how much future matters)
> - `max_a'(Q(s',a'))` = best Q-value achievable from next state s'
> - The bracket `[r + gamma*max - Q(s,a)]` is the TD error — difference between what we expected and what we got
>
> **Critical:** Make sure he understands the parentheses grouping. The entire bracket is multiplied by alpha, then ADDED to old Q. Common error: `Q + (alpha * (r + gamma*max) - Q)` which drops the old Q-value.

**Q13: You have LangChain on your resume. When would you use LangChain vs direct API calls to Claude/OpenAI?**

> **Expected answer:**
>
> - **Direct API:** Simple use cases, maximum control, lower latency, fewer dependencies, production systems where you want minimal abstraction.
> - **LangChain:** Complex chains (multi-step reasoning), agent workflows, tool use, memory management, quick prototyping. But adds complexity and abstraction overhead.
> - **Good nuance:** "For production, I prefer direct API calls for reliability. LangChain is great for prototyping and complex agent workflows."

**Q14: What is the difference between fine-tuning and RAG? When would you choose each?**

> **Expected answer:**
>
> - **Fine-tuning:** Modify model weights on domain-specific data. Better for: learning new behaviors, style, specialized tasks. Expensive, needs data, model becomes static.
> - **RAG:** Keep model as-is, inject relevant context at query time. Better for: knowledge that changes frequently, factual grounding, no training cost, explainable (can cite sources).
> - **Choose RAG when:** Knowledge updates often, need citations, budget-constrained, want quick iteration.
> - **Choose fine-tuning when:** Need specialized behavior/format, RAG context window isn't enough, task is very domain-specific.

**Q15: If you were designing a system to connect to 100 different enterprise APIs (Salesforce, Jira, GitHub, SAP...), fetch their data, normalize it, and feed it to an AI model — how would you architect it?**

> **This is Task 2 in verbal form.** Listen for:
>
> - Connector layer with plugin/adapter pattern (not hardcoded per API)
> - Auth abstraction (OAuth2, API key, bearer token — configurable per connector)
> - Pagination abstraction (cursor, offset, link header — configurable)
> - Retry + backoff per connector (429, 5xx)
> - Normalization layer (raw API response → canonical schema)
> - Schema registry + versioning
> - Observability (logs, metrics, health checks)
>
> **Mohit prediction:** His ETL/pipeline background should make this strong. Watch if he mentions schema drift, contract testing, and safe execution for untrusted API specs — those are the 4/5 and 5/5 differentiators.

---

## Round 2: Task-Based Assessment (4 Hours)

> **Instructions to give Mohit:** "You have 4 tasks, 1 hour each. At the 60-minute mark, stop and submit whatever you have — even if incomplete. We evaluate correctness, completeness, and production thinking."

Use the **exact same 4 tasks** from the repo:

- [Task 01](../Task%2001/Task%2001.md) — Systems Debugging (C)
- [Task 02](../Task%2002/Task%2002.md) — Architecture Design
- [Task 03](../Task%2003/Task%2003.md) — GitHub Issues Connector (Python)
- [Task 04](../Task%2004/Task%2004.md) — Reinforcement Learning

### Evaluation Rubric Per Task

#### Task 1: Systems Debugging (C) — Expected Score: 1-2/5

| Criteria                                     | Points | What to Check                   |
| -------------------------------------------- | ------ | ------------------------------- |
| `while` around `pthread_cond_wait`           | 1      | Spurious wakeup fix             |
| Queue full check in `enqueue()`              | 1      | Ring buffer overflow prevention |
| Shutdown with `pthread_cond_broadcast`       | 1      | Workers can exit cleanly        |
| FD close on both success + error paths       | 1      | Resource leak prevention        |
| `malloc()` null check + `read()==0` handling | 1      | Edge cases                      |

> **Mohit prediction:** Same as Ayush — no C experience. May do slightly better if his systems thinking from pipeline architecture translates. Watch for the `while` vs `if` fix and whether he notices the missing shutdown broadcast.

#### Task 2: Architecture Design — Expected Score: 3-4/5

| Criteria                                  | Points | What to Check                              |
| ----------------------------------------- | ------ | ------------------------------------------ |
| Clear component separation                | 1      | Ingestion/normalization/runtime/validation |
| Auth, pagination, retry/backoff specifics | 1      | HOW, not just "handle it"                  |
| Schema drift + versioning strategy        | 1      | Real-world API challenges                  |
| Contract testing with mocked responses    | 1      | Testing strategy                           |
| Safe execution model for untrusted specs  | 1      | Security thinking                          |

> **Mohit prediction:** This should be his strongest task. His Vertex AI platform + ETL pipeline + n8n orchestration experience maps directly. Expect him to nail component separation and pipeline architecture. Watch for contract testing and untrusted spec handling — those separate 3/5 from 5/5.

#### Task 3: GitHub Issues Connector — Expected Score: 2-3/5

| Criteria                                                      | Points | What to Check     |
| ------------------------------------------------------------- | ------ | ----------------- |
| Correct pagination (Link header, URL update OUTSIDE for loop) | 1      | The #1 trap       |
| Correct retry (429/403 with `continue`, 5xx with backoff)     | 1      | Control flow      |
| 403 distinguished from rate limit                             | 0.5    | Edge case         |
| PR filtering (`"pull_request"` key check)                     | 0.5    | Completeness      |
| Tests (pagination, retry, normalization, PR filtering)        | 1      | pytest + mock     |
| Clean normalization to required schema                        | 1      | Attention to spec |

> **Mohit prediction:** His scraper + ETL background helps conceptually, but the specific patterns (Link header parsing, `continue` after retry sleep) may trip him. His Claude API usage means he's called APIs, but may not have implemented connector-grade retry logic. **Tests are the wildcard** — if he writes them, major advantage over Kartik's submission.

#### Task 4: Q-Learning — Expected Score: 2-3/5

| Criteria                                | Points | What to Check                     |
| --------------------------------------- | ------ | --------------------------------- |
| Correct update rule (right parentheses) | 1.5    | `Q + alpha * (r + gamma*max - Q)` |
| Epsilon-greedy with random tie-breaking | 0.5    | Not `index(max(...))`             |
| Epsilon decay                           | 0.5    | Exploration → exploitation        |
| Learned policy display                  | 0.5    | Visual path output                |
| Random baseline comparison              | 0.5    | Completeness                      |
| Agent converges                         | 0.5    | Correctness proof                 |

> **Mohit prediction:** No RL experience on resume, but his deep learning background (TensorFlow, PyTorch) means he understands optimization concepts. The update rule parentheses trap is still dangerous. Watch for biased argmax.

---

## Post-Assessment Debrief Questions (10 min)

1. "Which task did you find hardest and why?"
2. "If you had 30 more minutes on any task, which would you pick and what would you do?"
3. "How would your RAG evaluation framework apply to evaluating connector data quality?"
4. "What would you change about your GitHub connector if it needed to handle 1000 different APIs?" _(connects to his actual experience)_

---

## Overall Scoring Guide

| Score | Meaning                                              |
| ----- | ---------------------------------------------------- |
| 1/5   | Attempted but fundamentally incorrect                |
| 2/5   | Partial understanding, critical bugs remain          |
| 3/5   | Mostly correct, missing edge cases or requirements   |
| 4/5   | Solid implementation, minor issues only              |
| 5/5   | Production-quality, all requirements met, clean code |

**Minimum bar for Samen AI selection:** 2.25/5 average (Kartik's score). Mohit's LLM/RAG/GCP background gives him a significant advantage in actual day-to-day work relevance, which can compensate for lower assessment scores — similar to how Kartik's architectural thinking compensated.

---

## Mohit vs Ayush: Key Differentiators to Watch

| Dimension                 | Ayush                    | Mohit                                   |
| ------------------------- | ------------------------ | --------------------------------------- |
| ML model building         | ✅ Strong (classical ML) | ✅ Strong (classical + deep)            |
| LLM/RAG/GenAI             | ❌ Gap                   | ✅ Very strong                          |
| Production pipelines      | ✅ MLflow/Airflow/AWS    | ✅ Vertex AI/BigQuery/n8n               |
| Samen AI alignment        | ⚠️ Moderate              | ✅ High (Claude, n8n, GCP, RAG)         |
| Systems thinking (Task 1) | ❓ Unknown               | ❓ Unknown                              |
| API connector (Task 3)    | ❓ Unknown               | ⚠️ Slightly better (scraper experience) |
| RL (Task 4)               | ❓ Unknown               | ❓ Unknown                              |

**Bottom line:** If both score similarly on the assessment, **Mohit is the stronger hire** for Samen AI because his daily work experience (LLM/RAG/Claude/GCP/ETL) directly maps to what Samen AI builds. Ayush would need more ramp-up time on the LLM/GenAI stack.
