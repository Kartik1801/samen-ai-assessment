# Samen AI - Assignment

This repository contains solutions for the Samen AI technical assignment, which consists of four distinct tests covering various domains of software engineering, including systems programming, architecture design, API integrations, and reinforcement learning.

## Repository Structure

The repository is organized into four tasks, each contained within its own directory:

### [Task 01: Systems Debugging and Kernel-Style Reasoning](./Task%2001)

A low-level C programming task focused on debugging a concurrency and resource-handling problem in a small server worker program.

- **Goal**: Identify and fix thread synchronization issues (using condition variables and mutexes) and resource leaks (memory and file descriptors).

### [Task 02: Architecture Design for a Universal API Connector](./Task%2002)

A system design task focused on building a scalable platform to ingest, normalize, and create functional connectors from thousands of diverse API definitions.

- **Goal**: Design a comprehensive end-to-end architecture covering API ingestion, normalization, connector generation, rate limiting, authentication, and error handling.

### [Task 03: Build a GitHub Issues Connector](./Task%2003)

A practical API integration task to build a robust connector for the GitHub REST API.

- **Goal**: Implement a script (in Python) that authenticates, fetches, and paginates through GitHub repository issues while correctly handling transient errors, rate limits, and response normalization.

### [Task 04: Reinforcement Learning](./Task%2004)

A machine learning task centered around tabular Q-learning.

- **Goal**: Implement a reinforcement learning agent capable of navigating a 4x4 grid world to reach a target while avoiding blocked cells, utilizing epsilon-greedy exploration and the Q-learning update rule.
