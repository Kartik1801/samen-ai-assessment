# Samen AI - Fresher Interview Prep Topics

## Topics to cover before following this guide

| Skill                      |
| -------------------------- |
| Python basics              |
| PySpark                    |
| SQL                        |
| Linear/Logistic Regression |
| Classification models      |
| Scikit-learn basics        |

**Start from where you left off - don't redo basics.**

---

## Fix Python Weak Spots

_Freshers often know syntax but miss production patterns. These are the exact things Samen AI checked._

- [ ] **Control flow discipline** - know exactly when to use `return`, `break`, `continue` inside loops. This was the #1 failure in Kartik's assessment
- [ ] **Exception handling** - `try/except/else/finally`, raising custom exceptions, not swallowing errors silently
- [ ] **Dataclasses** - `@dataclass` decorator, frozen dataclasses, `field()`
- [ ] **Type hints** - `def func(x: int) -> str:`, `List`, `Dict`, `Optional` from `typing`
- [ ] **f-strings** - proper string formatting
- [ ] **`enumerate`, `zip`, `map`, `filter`** - Pythonic patterns
- [ ] **List/dict/set comprehensions** - write clean one-liners
- [ ] **`defaultdict`, `Counter`** from `collections`
- [ ] **Reading from environment variables** - `os.environ.get()`
- [ ] **`__init__.py`, module imports** - how Python packages work

---

## API Connector in Python

_This is Task 3 equivalent - highest chance of appearing in their interview_

- [ ] **`requests` library** - GET, POST, headers, query params, auth tokens
  ```python
  import requests
  resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, params={"state": "open"})
  resp.raise_for_status()
  data = resp.json()
  ```
- [ ] **Pagination** - Link header parsing (`rel="next"`)
  ```python
  # CORRECT way
  link_header = resp.headers.get("Link", "")
  next_url = None
  for part in link_header.split(","):
      if 'rel="next"' in part:
          next_url = part.split(";")[0].strip().strip("<>")
  ```
- [ ] **Retry logic** - 429 (rate limit) vs 5xx (server error)
  - 429 → read `Retry-After` header → sleep → **`continue`** (not fall through!)
  - 5xx → exponential backoff → retry
  - 403 → could be permission denied, NOT always rate limit
- [ ] **Data normalization** - converting raw API response to a standard schema
- [ ] **`while True` loop with pagination** - don't put `return` inside the item loop

**Practice task:** Build a connector for GitHub Issues API - fetch all open issues from a public repo with pagination and retry.

---

## Testing in Python

_Samen AI explicitly checked for tests - and Kartik lost marks for missing them_

- [ ] **`pytest` basics** - writing test functions, running with `pytest`
- [ ] **`assert` statements** - what to assert and how
- [ ] **`unittest.mock`** - mocking HTTP calls so tests don't hit real APIs

  ```python
  from unittest.mock import patch, MagicMock

  @patch("requests.get")
  def test_fetch_issues(mock_get):
      mock_get.return_value.status_code = 200
      mock_get.return_value.json.return_value = [{"id": 1, "title": "Bug"}]
      mock_get.return_value.headers = {}
      # call your connector and assert
  ```

- [ ] **Test cases to always write:**
  - Normal case - happy path
  - Pagination - does it fetch page 2, 3?
  - Rate limit (429) - does it retry?
  - Empty response - does it handle gracefully?
  - Wrong data type - does it not crash?

---

## Machine Learning (Deepen What You Know)

_You know regression/classification - go deeper on the parts Samen AI will test_

### Deepen Scikit-learn

- [ ] **`Pipeline`** - chain preprocessor + model in one object

  ```python
  from sklearn.pipeline import Pipeline
  from sklearn.preprocessing import StandardScaler
  from sklearn.ensemble import RandomForestClassifier

  pipe = Pipeline([("scaler", StandardScaler()), ("model", RandomForestClassifier())])
  pipe.fit(X_train, y_train)
  ```

- [ ] **`ColumnTransformer`** - apply different transforms to different columns
- [ ] **`GridSearchCV`** - hyperparameter tuning
- [ ] **Feature importance** - `model.feature_importances_`, which features matter most
- [ ] **`cross_val_score`** - k-fold cross validation
- [ ] **Model saving** - `joblib.dump(model, "model.pkl")`

### Model Evaluation (Know These Cold)

- [ ] **Confusion matrix** - TP, TN, FP, FN - what each means
- [ ] **Precision vs Recall** - when to prioritize which
- [ ] **F1 Score** - harmonic mean of precision and recall
- [ ] **ROC-AUC** - what it means, how to plot
- [ ] **Classification report** - `sklearn.metrics.classification_report`

### Unsupervised Learning (Add This)

- [ ] **K-Means** - how it works, elbow method for k selection
- [ ] **Anomaly detection** - Isolation Forest, Local Outlier Factor
- [ ] **PCA** - dimensionality reduction intuition

### Time Series (Medium Priority)

- [ ] **Rolling averages, lag features** - for forecasting
- [ ] **Train/test split for time series** - never shuffle time series data
- [ ] **Seasonal decomposition** - trend + seasonality + residual

---

## Reinforcement Learning Basics

_JD explicitly mentions RL - Task 4 tested it. You must know Q-learning._

- [ ] **What is RL** - agent, environment, state, action, reward, episode
- [ ] **MDP** - Markov Decision Process - formal definition
- [ ] **Q-Learning update rule** - memorize and understand this:

  ```
  Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a')) - Q(s,a)]
  ```

  - `alpha` = learning rate
  - `gamma` = discount factor (how much future rewards matter)
  - `r` = current reward
  - `max_a'(Q(s',a'))` = best possible future Q-value

- [ ] **Epsilon-greedy** - explore (random) vs exploit (best known action), epsilon decay
- [ ] **Grid world implementation** - implement Task 4 correctly from scratch
- [ ] **Policy** - what the agent learned - show learned path visually
- [ ] **Random baseline comparison** - compare trained agent vs random agent

**Practice task:** Implement Q-learning on the exact grid world from Samen AI assessment. Make sure update rule is correct, epsilon decays, and you show the learned policy.

---

## System Design Basics

_Task 2 tested this - freshers often struggle here_

- [ ] **What is a REST API** - endpoints, HTTP methods, status codes
- [ ] **What is an ETL pipeline** - Extract, Transform, Load
- [ ] **What is a connector** - adapter between two systems
- [ ] **What is rate limiting** - why APIs throttle, how to handle 429
- [ ] **What is pagination** - offset/cursor/link-header approaches
- [ ] **What is authentication** - API keys, OAuth2, bearer tokens
- [ ] **What is normalization** - converting different data formats to one standard schema
- [ ] **How to design for failure** - retry, fallback, dead letter queue
- [ ] **What is observability** - logging, metrics, alerts

**Be able to answer:** "Design a system that connects to 100 different enterprise APIs, fetches their data, normalizes it, and feeds it to an AI model."

---

## LLM / AI Integration Basics

_Samen AI's core practice - know the concepts and basic code_

- [ ] **What is RAG** - Retrieval Augmented Generation, why it exists
- [ ] **What are embeddings** - converting text to vectors, semantic similarity
- [ ] **What is a vector database** - storing/searching embeddings (Chroma, Pinecone)
- [ ] **Claude/OpenAI API basics in Python**
  ```python
  import anthropic
  client = anthropic.Anthropic(api_key="...")
  message = client.messages.create(
      model="claude-opus-4-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Analyze this data: ..."}]
  )
  print(message.content[0].text)
  ```
- [ ] **Prompt engineering basics** - system prompt, user prompt, context injection
- [ ] **What is a copilot** - AI assistant on top of enterprise data

---

## FastAPI Basics

_Likely daily work - expose connector data via API_

- [ ] **Create a basic endpoint**

  ```python
  from fastapi import FastAPI
  app = FastAPI()

  @app.get("/issues")
  def get_issues():
      return {"issues": [...]}
  ```

- [ ] **Pydantic models** - request/response validation
- [ ] **Path params and query params**
- [ ] **HTTP status codes** - 200, 201, 400, 401, 404, 422, 429, 500
- [ ] **Running with uvicorn** - `uvicorn main:app --reload`
- [ ] **Basic error handling** - `HTTPException`

---

## Resume Project Confidence

_Your resume has fabricated projects. You MUST be able to speak to them fluently._

### Manufacturing Process Optimization (Resume Project)

Be ready to explain:

- [ ] What was the business problem? (manufacturing inefficiencies, cost reduction)
- [ ] What data was used? (production logs, sensor data, time-series)
- [ ] What models were used? (regression for prediction, clustering for anomaly)
- [ ] What was the outcome? (X% efficiency improvement)
- [ ] What Python libraries? (Pandas, NumPy, Scikit-learn, TensorFlow)

### Demand Forecasting Project (Resume Project)

Be ready to explain:

- [ ] Time-series forecasting - how lag features work
- [ ] What models? (ARIMA, Prophet, or ML-based forecasting)
- [ ] Inventory optimization logic
- [ ] How was it deployed?

### Recommendation Engine (Resume Project)

Be ready to explain:

- [ ] Collaborative filtering vs content-based
- [ ] Similarity metrics - cosine similarity, Euclidean distance
- [ ] Cold start problem - what is it, how to handle
- [ ] How was it evaluated?

> ⚠️ **Important:** Don't memorize scripts. Understand the concepts so you can answer follow-up questions naturally. If you don't know something, say "I'd approach it by..." - show thinking, not just answers.

---

## Computer Vision Basics

_Samen AI has a CV practice - good to know_

- [ ] **What is MediaPipe** - Google's pipeline for face, hand, pose detection
- [ ] **What is YOLO** - real-time object detection
- [ ] **OpenCV basics** - reading image, resizing, drawing bounding boxes
- [ ] **What is object detection vs classification** - detect WHERE + WHAT vs just WHAT
- [ ] **Proctoring system story** - understand Kartik's proctoring project well enough to explain it (face detection + speaker diarization + violation flagging)

---

## 📋 Practice Tasks (Do These, Don't Just Read)

| Task                                                                              | What It Practices | Time    |
| --------------------------------------------------------------------------------- | ----------------- | ------- |
| Build GitHub Issues connector with pagination + retry + tests                     | Priority 2 + 3    | 4-6 hrs |
| Implement Q-learning grid world correctly                                         | Priority 5        | 3-4 hrs |
| Train a classification model end-to-end with Pipeline + GridSearchCV + evaluation | Priority 4        | 3-4 hrs |
| Build a FastAPI endpoint that exposes connector data                              | Priority 8        | 2-3 hrs |
| Explain your resume projects out loud (record yourself)                           | Priority 9        | 1-2 hrs |
| Draw the Intelligence OS architecture on paper                                    | Priority 6        | 1 hr    |

---

## 🎯 Mock Interview Prep

**Expect 4 tasks, 1 hour each - same format as Kartik's assessment**

Most likely tasks for freshers:

| Task Slot | Most Likely                               | Backup                    |
| --------- | ----------------------------------------- | ------------------------- |
| Task 1    | Python debugging - fix broken code        | Data cleaning task        |
| Task 2    | System design - design a connector system | Architecture explanation  |
| Task 3    | Build an API connector                    | Data pipeline task        |
| Task 4    | ML model - train, evaluate, explain       | Q-learning implementation |

**Common verbal questions to prepare:**

- Walk me through how you would build a connector for Salesforce API
- What is the difference between precision and recall - when do you use which?
- How does gradient descent work?
- What is overfitting? How do you fix it?
- Explain RAG in simple terms
- What would you do if your API connector keeps hitting rate limits?
- How would you test your connector without calling the real API?
