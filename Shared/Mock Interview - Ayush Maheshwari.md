# Mock Interview — Ayush Maheshwari

**Interviewer:** Kartik Dhawan | Cyntexa  
**Format:** Round 1 (Intro, 30–45 min) + Round 2 (4-hour task assessment)

---

## Round 1: Introduction & Project Deep-Dive

### Section A: Warm-Up & Background (5 min)

**Q1: Tell me about yourself and your journey as a developer.**

> **What to listen for:** Confidence, clarity, does he position himself as an AI/ML engineer (not just "developer")? Does he mention Python, ML, model building — not just generic web dev?
>
> **Good answer:** "I'm a Senior Software Developer with 4+ years of experience focused on ML engineering — building production ML pipelines, training models for churn prediction, fraud detection, and recommendation systems. I work primarily in Python with PyTorch, Scikit-learn, and deploy on AWS using SageMaker and Docker."

**Q2: What excites you about working with a European AI company like Samen AI?**

> **What to listen for:** Has he read about Samen AI? Does he mention their Intelligence OS, EU compliance, or AI consultancy model? Or is it a generic "I want international exposure" answer?
>
> **Good answer mentions:** Dutch AI company, enterprise AI solutions, EU AI Act compliance, working on production AI systems for clients, Intelligence OS concept.

---

### Section B: Resume Project Deep-Dive (15–20 min)

#### Churn Prediction Project

**Q3: Walk me through your Customer Churn Analytics Platform. What was the business problem and how did you solve it?**

> **Expected answer:** Telecom client, customers churning, needed proactive retention. Built XGBoost/Random Forest classifiers on customer usage/billing data. Deployed as REST APIs via Django. MLflow for versioning, Airflow for pipeline orchestration.
>
> **Follow-up probes:**
>
> - "What features had the highest importance?" → Should mention usage patterns, billing frequency, support calls, contract length
> - "How did you handle class imbalance?" → Should mention SMOTE, class weights, or stratified sampling
> - "What was your precision vs recall tradeoff?" → Should explain: high recall = catch more churners but more false alarms; high precision = fewer false alarms but miss some churners. For retention campaigns, recall is usually prioritized.

**Q4: How did you detect model drift in production? What triggered retraining?**

> **Expected answer:** Monitored prediction distribution shift, feature distribution drift (PSI or KL divergence), accuracy degradation on holdout set. Retraining triggered when metrics dropped below threshold.
>
> **Red flag:** If he says "we retrained on a schedule" without mentioning drift detection — that's surface-level.

#### Fraud Detection Project

**Q5: In your Fraud Detection system, you used Isolation Forest and Neural Networks. When would you use Isolation Forest vs a Neural Network for anomaly detection?**

> **Expected answer:**
>
> - **Isolation Forest:** Unsupervised, works well when you have very few labeled fraud cases, fast training, good for initial detection. Isolates anomalies by random partitioning — anomalies need fewer splits.
> - **Neural Network:** Supervised (needs labeled data), better accuracy when you have enough fraud examples, can capture complex nonlinear patterns, but needs more data and compute.
> - **In practice:** Often use Isolation Forest for initial flagging, then Neural Network for confirmation/scoring.

**Q6: How did you handle the extreme class imbalance in fraud detection? (Fraud is typically <1% of transactions)**

> **Expected answer:** Should mention at least 2-3 of: SMOTE/ADASYN for oversampling, undersampling majority class, class_weight='balanced', focal loss, precision-recall as primary metric (not accuracy), stratified k-fold.
>
> **Red flag:** If he only mentions accuracy as evaluation metric — that's a major gap.

#### Recommendation Engine

**Q7: Explain the difference between collaborative filtering and content-based filtering. Which did you use and why?**

> **Expected answer:**
>
> - **Collaborative filtering:** "Users who liked X also liked Y" — based on user-item interaction matrix. Doesn't need item features.
> - **Content-based:** "This item is similar to what you liked before" — based on item features (category, price, description).
> - **Hybrid:** Combines both to handle cold-start and improve coverage.
>
> **Follow-up:** "What is the cold-start problem and how did you handle it?" → New users/items with no interaction history. Solution: content-based fallback, popularity-based, or ask for preferences.

**Q8: What similarity metric did you use and why?**

> **Expected answer:** Cosine similarity (direction-based, works well for sparse vectors), or Pearson correlation. Should explain WHY cosine — it normalizes for user rating scale differences.

#### Demand Forecasting

**Q9: You used ARIMA, Prophet, and LSTM for demand forecasting. When would you pick each one?**

> **Expected answer:**
>
> - **ARIMA:** Good for stationary time series, simple, interpretable, fast. Needs manual parameter tuning (p,d,q).
> - **Prophet:** Handles seasonality, holidays, missing data well. Good for business users. Less flexible for complex patterns.
> - **LSTM:** Best for complex nonlinear patterns, long-term dependencies. Needs more data, harder to train, less interpretable.
>
> **Follow-up:** "How do you split time-series data for training/testing?" → **NEVER shuffle.** Use chronological split — train on past, test on future. Walk-forward validation.

---

### Section C: Conceptual Questions (10–15 min)

**Q10: What is overfitting? How do you detect and prevent it?**

> **Expected answer:**
>
> - **Detection:** Training accuracy >> validation accuracy, large gap in learning curves
> - **Prevention:** Regularization (L1/L2), dropout, early stopping, cross-validation, more data, simpler model, data augmentation
>
> **Red flag:** Only mentions "more data" without regularization techniques.

**Q11: Explain gradient descent in simple terms. What is the learning rate and why does it matter?**

> **Expected answer:** Optimization algorithm that iteratively adjusts model parameters in the direction of steepest descent of the loss function. Learning rate controls step size — too large = overshoot minimum, too small = slow convergence, may get stuck in local minimum.
>
> **Bonus:** Mentions Adam optimizer as adaptive learning rate.

**Q12: What is a REST API? If I asked you to build an API connector that fetches data from GitHub, what would you need to handle?**

> **Expected answer should cover:**
>
> - Authentication (Bearer token)
> - Pagination (Link header or cursor-based)
> - Rate limiting (429 status, Retry-After header)
> - Error handling (5xx retry with backoff, 4xx client errors)
> - Data normalization
>
> **This is a setup question for Task 3.** If he can't answer this conceptually, Task 3 will be very hard.

**Q13: What is RAG (Retrieval Augmented Generation)?**

> **Expected answer:** Technique that enhances LLM responses by first retrieving relevant documents from a knowledge base (using embeddings + vector search), then passing them as context to the LLM for generation. Solves hallucination and knowledge cutoff problems.
>
> **Note:** Ayush's resume doesn't show RAG experience, so this tests awareness. A good answer shows he's learning; inability to answer is a gap to note.

**Q14: You've deployed models on AWS SageMaker. Walk me through the deployment flow.**

> **Expected answer:** Train model → save artifacts (model.pkl or model.tar.gz) → create SageMaker model (specify container + model data) → create endpoint configuration → deploy endpoint → invoke endpoint via API. Should mention: instance types, auto-scaling, A/B testing with production variants.

**Q15: What is the Q-learning update rule? Can you explain what each term means?**

> **Setup for Task 4.** Write the formula on screen:
> `Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a')) - Q(s,a)]`
>
> **Expected answer:**
>
> - `Q(s,a)` = current Q-value for state s, action a
> - `alpha` = learning rate (how much to update)
> - `r` = immediate reward
> - `gamma` = discount factor (how much future rewards matter)
> - `max_a'(Q(s',a'))` = best possible Q-value from next state
> - `[r + gamma * max - Q(s,a)]` = temporal difference error
>
> **Note:** If he can explain this, Task 4 will go well. If not, flag it as a prep topic.

---

## Round 2: Task-Based Assessment (4 Hours)

> **Instructions to give Ayush:** "You have 4 tasks, 1 hour each. At the 60-minute mark, stop and submit whatever you have — even if incomplete. We evaluate correctness, completeness, and production thinking."

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

> **Ayush prediction:** Likely struggles here — no C/systems experience on resume. May get partial credit for identifying the `if` → `while` fix if he understands concurrency conceptually.

#### Task 2: Architecture Design — Expected Score: 2-3/5

| Criteria                                                                | Points | What to Check                  |
| ----------------------------------------------------------------------- | ------ | ------------------------------ |
| Clear component separation (ingestion/normalization/runtime/validation) | 1      | Modularity                     |
| Auth, pagination, retry/backoff specifics                               | 1      | Not just "handle errors" — HOW |
| Schema drift + versioning strategy                                      | 1      | Real-world API challenges      |
| Contract testing with mocked responses                                  | 1      | Testing strategy               |
| Safe execution model for untrusted specs                                | 1      | Security thinking              |

> **Ayush prediction:** His MLOps background should help with pipeline thinking, but may lack API connector architecture specifics. Watch if he mentions schema drift and contract testing — these are the differentiators.

#### Task 3: GitHub Issues Connector — Expected Score: 2-3/5

| Criteria                                                                    | Points | What to Check            |
| --------------------------------------------------------------------------- | ------ | ------------------------ |
| Correct pagination (Link header, `while` loop, URL update OUTSIDE for loop) | 1      | The #1 trap              |
| Correct retry (429/403 with `continue`, 5xx with backoff)                   | 1      | Control flow discipline  |
| 403 distinguished from rate limit (check headers)                           | 0.5    | Edge case awareness      |
| PR filtering (`"pull_request"` key check)                                   | 0.5    | Requirement completeness |
| Tests (pagination, retry, normalization, PR filtering)                      | 1      | pytest + mock            |
| Clean normalization to required schema                                      | 1      | Attention to spec        |

> **Ayush prediction:** Python is strong, but API connector patterns are a gap. Watch for the pagination trap (return inside for loop) and retry trap (no continue after sleep). Missing tests = major deduction.

#### Task 4: Q-Learning — Expected Score: 2-3/5

| Criteria                                        | Points | What to Check                                                             |
| ----------------------------------------------- | ------ | ------------------------------------------------------------------------- |
| Correct update rule (parentheses must be right) | 1.5    | `Q + alpha * (r + gamma*max - Q)` not `Q + (alpha * (r + gamma*max) - Q)` |
| Epsilon-greedy with random tie-breaking         | 0.5    | Not biased argmax                                                         |
| Epsilon decay                                   | 0.5    | Exploration → exploitation                                                |
| Learned policy display (visual path)            | 0.5    | Requirement completeness                                                  |
| Random baseline comparison                      | 0.5    | Requirement completeness                                                  |
| Agent converges (reaches goal consistently)     | 0.5    | Correctness proof                                                         |

> **Ayush prediction:** Has ML background but no RL. The update rule parentheses error is the biggest trap. If he gets the formula right, everything else follows. Watch for biased argmax.

---

## Post-Assessment Debrief Questions (10 min)

After the 4-hour assessment, ask these to gauge self-awareness:

1. "Which task did you find hardest and why?"
2. "If you had 30 more minutes on any task, which would you pick and what would you do?"
3. "What would you change about your GitHub connector if it needed to handle 1000 different APIs?"

---

## Overall Scoring Guide

| Score | Meaning                                              |
| ----- | ---------------------------------------------------- |
| 1/5   | Attempted but fundamentally incorrect                |
| 2/5   | Partial understanding, critical bugs remain          |
| 3/5   | Mostly correct, missing edge cases or requirements   |
| 4/5   | Solid implementation, minor issues only              |
| 5/5   | Production-quality, all requirements met, clean code |

**Minimum bar for Samen AI selection:** 2.25/5 average (Kartik's score), but higher is obviously better. Architectural thinking and potential weigh heavily.
