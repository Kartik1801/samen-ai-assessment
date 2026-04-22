# Test 1: Systems Debugging and Kernel-Style Reasoning

## Goal

Debug a low-level concurrency and resource-handling problem in a small server worker program.

## What you receive

A C program with a queue, a worker thread, and socket handling. It has at least one concurrency bug and one resource leak.

## Your task

- Read the code.
- Identify the bug(s).
- Fix the code.
- Explain the root cause.
- If possible, add a small regression test or reproduction note.

## Starter code

```c
// worker.c #include <pthread.h> #include <unistd.h> #include <stdlib.h> #include <stdio.h> #define MAXQ 16 typedef struct Job { int fd; } Job; static pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER; static pthread_cond_t qcv = PTHREAD_COND_INITIALIZER; static Job *queue[MAXQ]; static int head = 0; static int tail = 0; static int count = 0; static int running = 1; static void enqueue(Job *j) { pthread_mutex_lock(&qlock); queue[tail] = j; tail = (tail + 1) % MAXQ; count++; pthread_cond_signal(&qcv); pthread_mutex_unlock(&qlock); } static Job *dequeue(void) { pthread_mutex_lock(&qlock); if (count == 0) { pthread_cond_wait(&qcv, &qlock); } Job *j = queue[head]; head = (head + 1) % MAXQ; count--; pthread_mutex_unlock(&qlock); return j; } static void process(Job *j) { char buf[128]; ssize_t n = read(j->fd, buf, sizeof(buf)); if (n < 0) { return; } write(j->fd, buf, n); free(j); } void *worker(void *arg) { while (running) { Job *j = dequeue(); if (j) { process(j); } } return NULL; } int main(void) { while (1) { int fd = accept(0, NULL, NULL); if (fd < 0) { continue; } Job \*j = malloc(sizeof(Job)); j->fd = fd; enqueue(j); } return 0; }
```

## Constraints

- Assume this is a simplified server component.
- You do not need to make it production-grade.
- You should focus on correctness and clarity.

## What we are evaluating

- Can you find concurrency bugs quickly?
- Do you understand condition variables and spurious wakeups?
- Do you notice file descriptor and memory leaks?
- Can you explain the fix clearly?

## Deliverable after 1 hour

- Fixed code or a patch.
- Short explanation of the bug(s) and your fix.
- Any test, repro, or notes you can provide.

## Strong signals

- Uses while around pthread_cond_wait.
- Handles queue shutdown safely.
- Closes file descriptors correctly.
- Mentions why the bug appears under load.
