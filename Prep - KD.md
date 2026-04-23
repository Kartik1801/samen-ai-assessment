# Samen AI — Preparation Topics - KD

**Based on:** Original JD + Assessment Analysis + Website Research  
**For:** Kartik Dhawan | 11 days to May 4

---

> **Strategy:** JD says "ML from scratch, no API wrappers" — but assessment proved they care about **production correctness + systems thinking**. Cover both — JD topics for interviews/tasks, assessment gaps for day-1 delivery.

---

## 🔴 PRIORITY 1 — Python Fundamentals (Your Biggest Gap)

_You are a JS/TS developer. Python syntax jump is fast — do this first._

- [ ] Python vs JS — syntax differences (variables, functions, classes, modules)
- [ ] List comprehensions, generators, decorators
- [ ] `*args`, `**kwargs`, type hints
- [ ] Virtual environments — `venv`, `pip`, `requirements.txt`
- [ ] File I/O, JSON handling, environment variables
- [ ] Exception handling — `try/except/finally`, custom exceptions
- [ ] Dataclasses (`@dataclass`) — used directly in their assessment
- [ ] `collections` module — `defaultdict`, `Counter`, `deque`
- [ ] Context managers — `with` statement
- [ ] `itertools`, `functools` basics

---

## 🔴 PRIORITY 2 — Data Science Foundations

_JD says "strong data science expertise" — this is the base of everything_

### Mathematics & Statistics

- [ ] Linear algebra basics — vectors, matrices, dot product, transpose
- [ ] Probability — distributions, Bayes theorem, conditional probability
- [ ] Statistics — mean, median, variance, standard deviation, correlation
- [ ] Hypothesis testing — p-values, confidence intervals
- [ ] Gradient descent — intuition + math (core of all ML training)
- [ ] Chain rule, partial derivatives (for backpropagation understanding)

### Data Handling with Python

- [ ] NumPy — arrays, broadcasting, vectorized operations, reshaping
- [ ] Pandas — DataFrames, groupby, merge, pivot, apply, missing data
- [ ] Data cleaning — handling nulls, outliers (IQR method, z-score)
- [ ] Feature engineering — encoding (OHE, label), scaling (StandardScaler, MinMax)
- [ ] Train/validation/test split — why 3-way, stratification
- [ ] EDA — exploratory data analysis workflow

---

## 🔴 PRIORITY 3 — Machine Learning (Core JD Requirement)

_JD: "design, build, and train AI/ML models from scratch"_

### Supervised Learning

- [ ] Linear Regression — math, implementation, evaluation (MAE, MSE, R²)
- [ ] Logistic Regression — sigmoid, log loss, classification metrics
- [ ] Decision Trees — splitting criteria (Gini, entropy), overfitting
- [ ] Random Forest — bagging, feature importance
- [ ] Gradient Boosting — XGBoost, LightGBM — how boosting works
- [ ] SVM — hyperplane, kernel trick, margin
- [ ] k-NN — distance metrics, curse of dimensionality

### Unsupervised Learning

- [ ] K-Means clustering — centroid update, elbow method
- [ ] DBSCAN — density-based, noise handling
- [ ] PCA — dimensionality reduction, explained variance
- [ ] Anomaly detection — Isolation Forest, z-score, IQR

### Model Evaluation

- [ ] Classification — accuracy, precision, recall, F1, ROC-AUC, confusion matrix
- [ ] Regression — MAE, MSE, RMSE, R²
- [ ] Cross-validation — k-fold, stratified k-fold
- [ ] Overfitting vs underfitting — bias-variance tradeoff
- [ ] Regularization — L1 (Lasso), L2 (Ridge), ElasticNet

### Scikit-learn (Already have some — deepen)

- [ ] Pipeline — `sklearn.pipeline.Pipeline`
- [ ] GridSearchCV, RandomizedSearchCV — hyperparameter tuning
- [ ] ColumnTransformer — preprocessing different column types
- [ ] Custom transformers — `BaseEstimator`, `TransformerMixin`
- [ ] `joblib` — model serialization (save/load)

---

## 🔴 PRIORITY 4 — Reinforcement Learning

_JD explicitly mentions RL — and Task 4 tested it. Fix the Q-learning bug._

- [ ] MDP — Markov Decision Process (states, actions, rewards, transitions)
- [ ] Bellman equation — understand it deeply, not just memorize
- [ ] Q-Learning — correct update rule:
  ```
  Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a')) - Q(s,a)]
  ```
- [ ] Epsilon-greedy exploration — decay strategies, tie-breaking
- [ ] Policy vs Value function
- [ ] Temporal Difference learning
- [ ] Deep Q-Network (DQN) — basics only
- [ ] Grid world implementation — fix your Task 4 submission

---

## 🟠 PRIORITY 5 — Deep Learning

_JD mentions "advanced ML techniques" — deep learning is implied_

### Neural Network Fundamentals

- [ ] Perceptron → MLP — forward pass, activation functions (ReLU, sigmoid, tanh, softmax)
- [ ] Backpropagation — chain rule in practice
- [ ] Loss functions — cross entropy, MSE, when to use which
- [ ] Optimizers — SGD, Adam, RMSprop — intuition
- [ ] Batch normalization, dropout — regularization in NNs
- [ ] Learning rate scheduling

### PyTorch (Industry standard, Samen AI uses it)

- [ ] Tensors — creation, operations, GPU vs CPU
- [ ] `Dataset` and `DataLoader`
- [ ] `nn.Module` — building custom models
- [ ] Training loop — forward, loss, backward, optimizer step
- [ ] Saving/loading models — `torch.save`, `torch.load`
- [ ] Transfer learning — loading pretrained weights, freezing layers

### CNN (For Computer Vision — they use MediaPipe/YOLO)

- [ ] Convolution, pooling, feature maps — intuition
- [ ] Common architectures — ResNet, VGG (understand, not implement)
- [ ] Object detection basics — YOLO intuition

---

## 🟠 PRIORITY 6 — AI Architecture & System Design

_JD: "solid understanding of AI architecture" — Task 2 tested this_

- [ ] End-to-end ML pipeline architecture — data → features → model → serving
- [ ] API connector architecture — ingestion, normalization, retry, rate limiting at scale
- [ ] Model serving — REST API via FastAPI, batch vs real-time inference
- [ ] Feature stores — what they are, why they matter
- [ ] Model registry — versioning, staging, production promotion
- [ ] Data versioning — DVC basics
- [ ] Schema drift detection — how to detect and handle
- [ ] Sandboxing untrusted code — SSRF protection, private IP blocklisting
- [ ] Distributed rate limiting — across thousands of APIs
- [ ] Contract testing — mocked API response validation

---

## 🟠 PRIORITY 7 — Production Python & API Connectors

_This is what Task 3 tested — and likely core daily work_

- [ ] `requests` library — GET/POST, headers, auth, sessions
- [ ] Link header pagination — parsing `rel="next"` correctly
- [ ] Retry logic — `Retry-After` header, exponential backoff, max retries
- [ ] 429 vs 403 handling — rate limit vs permission denied (different!)
- [ ] OAuth2 in Python — token refresh flow
- [ ] `httpx` — async HTTP client (modern alternative to requests)
- [ ] FastAPI — routes, Pydantic models, dependency injection, middleware
- [ ] `pytest` — fixtures, parametrize, marks
- [ ] `unittest.mock` — `patch`, `MagicMock`, `side_effect`
- [ ] Mocking HTTP — `responses` library or `httpretty`

---

## 🟠 PRIORITY 8 — NLP & LLM (Applied)

_JD says "no API wrappers" — but Samen AI uses Claude/OpenAI. Know both._

### Traditional NLP (Know the concepts)

- [ ] Tokenization, stemming, lemmatization
- [ ] TF-IDF, Bag of Words
- [ ] Word embeddings — Word2Vec, GloVe intuition
- [ ] Named Entity Recognition, POS tagging

### LLM / Applied AI (Your actual strength — in Python)

- [ ] RAG — Retrieval Augmented Generation architecture
- [ ] Vector databases — Chroma, Pinecone, Weaviate — how embeddings are stored/queried
- [ ] `sentence-transformers` — generating embeddings in Python
- [ ] Claude API in Python — messages, system prompts, streaming
- [ ] OpenAI API in Python — same patterns
- [ ] Prompt engineering — few-shot, chain-of-thought, structured outputs
- [ ] LangChain basics — chains, agents, memory (awareness level)
- [ ] Local LLMs — Ollama setup, running Llama/Mistral locally

---

## 🟡 PRIORITY 9 — MLOps & Deployment

_JD: "production-ready AI solutions" — know the basics_

- [ ] Docker — Dockerfile, build, run, volumes, ports (you have some exposure)
- [ ] Docker Compose — multi-container setups
- [ ] MLflow — experiment tracking, model registry, artifact logging
- [ ] Model monitoring — data drift, concept drift, performance degradation
- [ ] CI/CD for ML — GitHub Actions basics
- [ ] GCP Cloud Run — deploying containerized ML APIs (you have EVCO experience)
- [ ] Logging & observability — structured logging, Prometheus basics

---

## 🟡 PRIORITY 10 — Computer Vision

_Samen AI has a Computer Vision practice — you mentioned MediaPipe in interview_

- [ ] MediaPipe — hands, face mesh, pose estimation pipelines
- [ ] OpenCV — image read/write, resize, color space, drawing
- [ ] YOLO (Ultralytics) — object detection, running inference, custom datasets
- [ ] Face detection — Haar cascades vs deep learning approaches
- [ ] Speaker diarization — pyannote.audio basics (you used this in proctoring)
- [ ] Edge AI — OpenVINO basics (Samen AI uses it)

---

## 📚 Recommended Resources (Fast Track)

| Topic              | Resource                                         | Time                |
| ------------------ | ------------------------------------------------ | ------------------- |
| Python for JS devs | YouTube: "Python for JavaScript developers"      | 3-4 hrs             |
| ML fundamentals    | fast.ai Practical Deep Learning (free, top-down) | Skim relevant parts |
| Scikit-learn       | Official docs + Kaggle learn                     | 2-3 days            |
| PyTorch            | official 60-min blitz tutorial                   | 1 day               |
| Q-Learning         | Sentdex RL series on YouTube                     | 2-3 hrs             |
| FastAPI            | tiangolo.com official docs                       | 1 day               |
| RAG                | LangChain docs + DeepLearning.AI short course    | 1 day               |
| Docker             | TechWorld with Nana — Docker tutorial            | 3-4 hrs             |

---

## ✅ Your Existing Strengths (Don't Waste Time Here)

| Skill                | Why Skip                                   |
| -------------------- | ------------------------------------------ |
| System Architecture  | Already strong — Palantir Foundry, EVCO    |
| LLM Concepts         | EVCO MCP server, Claude API, n8n pipelines |
| ETL Pipelines        | BigQuery ETL in production                 |
| API Design           | MCP server, REST APIs in production        |
| Node.js / TypeScript | Not needed for this role                   |

---

## 🗓️ Suggested 11-Day Sprint (Apr 23 — May 3)

| Day    | Focus                                                    |
| ------ | -------------------------------------------------------- |
| Day 1  | Python basics — syntax, classes, dataclasses, exceptions |
| Day 2  | NumPy + Pandas — data handling fundamentals              |
| Day 3  | Scikit-learn deep dive — pipelines, evaluation, tuning   |
| Day 4  | API connector in Python — pagination, retry, tests       |
| Day 5  | pytest + mocking — proper test suite                     |
| Day 6  | FastAPI — endpoints, Pydantic, middleware                |
| Day 7  | Deep Learning basics — PyTorch training loop             |
| Day 8  | Q-Learning fix + RL concepts                             |
| Day 9  | LLM in Python — Claude API, RAG, embeddings              |
| Day 10 | Ollama local LLM + Computer Vision (MediaPipe refresh)   |
| Day 11 | Buffer — revision, mock Q&A, system design practice      |

---

_Kartik Dhawan | Cyntexa | April 2026_
