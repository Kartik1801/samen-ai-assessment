# Test 1 - what the reviewer was probably looking for

Your original submission caught two things:

1. `if` → `while` around `pthread_cond_wait` (correct).
2. Missing `close(fd)` in `process` on the error path (correct, but incomplete).

Here is the larger set of bugs that a hands-on reviewer expects you to
find in this sort of snippet, with the reason each one matters.

## 1. Spurious wakeups (you got this one)

`pthread_cond_wait` can return without anyone signaling, and even with a
signal another thread may drain the queue before you re-acquire the
mutex. Always recheck the predicate in a `while`.

## 2. Shutdown was unreachable

`running` was a plain `int`, read by workers and (presumably) written by
someone else later. Two problems:

- Plain `int` across threads is a data race. Either use `atomic_int`
  (C11), `_Atomic int`, or a mutex-protected flag.
- Even if you flip it to 0, any worker already parked in
  `pthread_cond_wait` will never wake up, because nothing broadcasts.

The fix: a `shutting_down` flag protected by `qlock`, set by
`request_shutdown()`, which then `pthread_cond_broadcast`es both
condition variables. Workers re-check `shutting_down` inside their
`while` predicate and return when the queue is drained.

## 3. Unbounded enqueue (the bug you missed)

The queue is a fixed-size ring of length `MAXQ`. The original
`enqueue` never checked `count == MAXQ`, so under load it would silently
overwrite `queue[tail]`, leaking both the `Job*` and the fd inside it.
This is the bug that "appears under load" the task description hints at.

Fix: second condition variable `qcv_not_full`, enqueue blocks while
`count == MAXQ`.

## 4. `process()` leaked fds on multiple paths

Original `process()`:

```c
ssize_t n = read(j->fd, buf, sizeof(buf));
if (n < 0) { return; }   // fd leaked, Job* leaked
write(j->fd, buf, n);    // partial writes ignored
free(j);                 // fd never closed
```

Three problems: error path leaks both, success path never closes fd, and
`write()` can return less than `n`. Also `read() == 0` (peer closed)
wasn't even noticed - the loop just keeps processing a dead connection.

Fix: loop on read, break on EOF or error, `write_all()` helper that
loops on partial writes and handles `EINTR`, and `close(fd); free(j);`
on every exit path.

## 5. `malloc` in `main` not null-checked

```c
Job *j = malloc(sizeof(Job));
j->fd = fd;   // segfault if malloc returned NULL
```

Under OOM you crash. Fix: check, close fd on failure.

## 6. Signal handling

A real server needs to stop cleanly. Added `SIGINT`/`SIGTERM` handler
that sets `got_signal`, breaks the acceptor loop, and triggers
`request_shutdown()`.

## Reproducing the original "under load" bug

You can demonstrate the overwrite bug by temporarily shrinking `MAXQ`
to 2, spawning a client that opens many connections in a tight loop
while the worker is sleeping, and observing either (a) a leaked fd
count in `/proc/<pid>/fd`, or (b) a use-after-free from AddressSanitizer
(`cc -fsanitize=address,undefined -pthread ...`).

## What "going deeper" looked like for this task

A 5/5 answer would mention: spurious wakeup, unbounded enqueue,
shutdown broadcast, fd lifetime across every return path, partial
writes, and reproduction under load. A 2/5 answer lists two of those
and stops. That is the delta the reviewer is describing.
