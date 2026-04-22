# Assignment Review & Feedback: Why You Scored 2.25 / 5

This document outlines the detailed feedback for your recent assignment submission. While you attempted all sections and grasped several core concepts, critical execution details, logic errors, and incomplete requirements significantly impacted the correctness and robustness of the solutions.

Below is a breakdown of your performance across the four tasks.

---

## Task 1: Systems Debugging (C)

> [!NOTE]
> **What went well:** You correctly identified the spurious wakeup bug by replacing the `if` statement with a `while` loop around `pthread_cond_wait`. You also identified that file descriptors were leaking on the error path.

> [!WARNING]
> **Where you lost points:**
>
> - **Unbounded Enqueue (Critical Bug Missed):** The queue was implemented as a fixed-size ring buffer (`MAXQ = 16`). Your solution did not check if the queue was full before enqueuing. Under heavy load, this silently overwrites pointers, leaking both memory and file descriptors.
> - **Unreachable Shutdown:** The `running` flag was a plain `int` read across threads (creating a data race). Even if set to 0, parked workers would wait indefinitely because `pthread_cond_broadcast` was never called to wake them up during shutdown.
> - **Incomplete File Descriptor Management:** While you added a `close(fd)` on the error path, you missed it on the success path. Additionally, your `process()` method ignored partial writes and failed to detect `read() == 0` (peer closed), causing it to process dead connections indefinitely.
> - **Missing Safeguards:** `malloc()` was not null-checked, risking segmentation faults under memory pressure.

---

## Task 2: Architecture Design

> [!NOTE]
> **What went well:** You provided a logical, high-level breakdown of the necessary system components (Ingestion, Parsing, Normalization, Registry, Generation, Runtime).

> [!WARNING]
> **Where you lost points:**
>
> - **Lack of Technical Depth:** The prompt explicitly asked for specific architectural details, such as how to safely execute untrusted API definitions, handle schema drift, and manage complex pagination abstractions. Your response remained mostly at a surface level.
> - **Missing Error Handling Strategies:** You mentioned having "common interfaces" for retries and rate limits but failed to specify the architecture behind exponential backoff strategies for 5xx errors or how rate limiting (429s) would be managed across thousands of APIs in a distributed system.
> - **Missing Contract Testing:** The prompt requested details on contract testing with mocked API responses, which was omitted from your design.

---

## Task 3: GitHub Issues Connector (Python)

> [!NOTE]
> **What went well:** You structured the connector nicely with dataclasses and implemented the basic rate-limiting sleep logic and normalization.

> [!CAUTION]
> **Where you lost points:**
>
> - **Broken Pagination Logic:** Your pagination code only fetched the first page! Both the `url = self._parse_next_link()` update and the `return records` statement were placed _inside_ the per-item `for` loop. This caused the function to return immediately after parsing the very first issue.
> - **Broken Rate Limit Retries:** When encountering a 429 or 403, your code slept correctly but failed to use `continue` to jump to the next loop iteration. Instead, it fell through to `resp.raise_for_status()`, crashing the connector immediately after the first sleep.
> - **Incorrect 403 Handling:** You assumed all 403 responses were rate limits. GitHub also returns 403 for permission denied errors, which your code would incorrectly retry repeatedly.
> - **Missing Tests:** The assignment specifically requested tests for pagination, retry behavior, and PR filtering, which were absent from your submission.

---

## Task 4: Reinforcement Learning (Python)

> [!NOTE]
> **What went well:** You implemented the GridWorld environment accurately and successfully established the overall structure for the Q-learning training loop.

> [!CAUTION]
> **Where you lost points:**
>
> - **Mathematical Error in Update Rule:** Your Q-learning formula had misplaced parentheses:
>
>   ```python
>   q[(state, action)] + (alpha * (reward + gamma * next) - q[(state, action)])
>   ```
>
>   This simplifies algebraically to `alpha * (reward + gamma * next)`, which completely drops the old Q-value. Because of this, the Temporal Difference error never forms properly, and the agent fails to converge to an optimal policy.
>
> - **Biased Epsilon-Greedy:** Your `argmax` implementation (`ACTIONS[values.index(max(values))]`) always selected the first action on ties (index 0). When the Q-table initializes at zero, this biases the agent to almost exclusively move "up".
> - **Incomplete Requirements:** The task explicitly required you to compare your agent against a random baseline and output/display the final learned policy (e.g., a visual path). Neither of these were implemented.

---

### Summary

A 5/5 score required deeper attention to edge cases (Task 1), technical specifics on failure scaling (Task 2), rigorous loop/control-flow testing (Task 3), and strict adherence to mathematical formulas and prompt requirements (Task 4).
