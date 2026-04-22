/*
 * worker.c - fixed version
 *
 * Bugs fixed vs. the original:
 *   1. pthread_cond_wait was guarded by `if`, not `while` - vulnerable to
 *      spurious wakeups AND to the "someone else drained the queue before
 *      I got the mutex" case. Now uses `while`.
 *   2. `running` was a plain int read/written across threads with no
 *      memory-ordering guarantees, AND nothing ever broadcast the cv on
 *      shutdown, so workers blocked in pthread_cond_wait would sleep
 *      forever. Replaced with a `shutting_down` flag protected by qlock
 *      plus a broadcast to both cvs.
 *   3. enqueue() didn't bound the queue. When count == MAXQ it quietly
 *      overwrote slot[tail] and leaked the previous Job + fd. Now blocks
 *      on a second condition variable qcv_not_full.
 *   4. process() leaked fd on n < 0 (never closed) and on n == 0 (peer
 *      closed cleanly - was not even detected). Now closes in all paths
 *      and handles EINTR.
 *   5. write() return value was ignored. Short writes silently dropped
 *      data. Replaced with write_all() loop.
 *   6. malloc() in main was not null-checked; on failure the code
 *      dereferenced NULL. Now checked, fd closed on allocation failure.
 *   7. Added SIGINT/SIGTERM handler that triggers a clean shutdown:
 *      acceptor stops, workers drain queue, queue remnants get their fds
 *      closed, then main returns.
 *
 * Compile: cc -O2 -Wall -Wextra -pthread worker.c -o worker
 */

#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <sys/socket.h>

#define MAXQ        16
#define NUM_WORKERS  4

typedef struct Job {
    int fd;
} Job;

static pthread_mutex_t qlock         = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t  qcv_not_empty = PTHREAD_COND_INITIALIZER;
static pthread_cond_t  qcv_not_full  = PTHREAD_COND_INITIALIZER;

static Job *queue[MAXQ];
static int head = 0;
static int tail = 0;
static int count = 0;

/* Protected by qlock. */
static int shutting_down = 0;

/* Set from signal handler; sig_atomic_t so the read in main is safe. */
static volatile sig_atomic_t got_signal = 0;

static void handle_sig(int sig) { (void)sig; got_signal = 1; }

/* Returns 0 on success, -1 if shutdown was requested. Caller owns `j`
 * on failure and must free/close it. */
static int enqueue(Job *j)
{
    pthread_mutex_lock(&qlock);
    while (count == MAXQ && !shutting_down) {
        pthread_cond_wait(&qcv_not_full, &qlock);
    }
    if (shutting_down) {
        pthread_mutex_unlock(&qlock);
        return -1;
    }
    queue[tail] = j;
    tail = (tail + 1) % MAXQ;
    count++;
    pthread_cond_signal(&qcv_not_empty);
    pthread_mutex_unlock(&qlock);
    return 0;
}

/* Returns NULL only when shutting down AND queue is empty. */
static Job *dequeue(void)
{
    pthread_mutex_lock(&qlock);
    while (count == 0 && !shutting_down) {
        pthread_cond_wait(&qcv_not_empty, &qlock);
    }
    if (count == 0) {                       /* implies shutting_down */
        pthread_mutex_unlock(&qlock);
        return NULL;
    }
    Job *j = queue[head];
    head = (head + 1) % MAXQ;
    count--;
    pthread_cond_signal(&qcv_not_full);
    pthread_mutex_unlock(&qlock);
    return j;
}

static void request_shutdown(void)
{
    pthread_mutex_lock(&qlock);
    shutting_down = 1;
    pthread_cond_broadcast(&qcv_not_empty);
    pthread_cond_broadcast(&qcv_not_full);
    pthread_mutex_unlock(&qlock);
}

/* Write the full buffer, looping on partial writes and EINTR. */
static ssize_t write_all(int fd, const char *buf, size_t n)
{
    size_t written = 0;
    while (written < n) {
        ssize_t w = write(fd, buf + written, n - written);
        if (w < 0) {
            if (errno == EINTR) continue;
            return -1;
        }
        if (w == 0) return -1;             /* shouldn't happen on write */
        written += (size_t)w;
    }
    return (ssize_t)written;
}

static void process(Job *j)
{
    char buf[128];
    for (;;) {
        ssize_t n = read(j->fd, buf, sizeof(buf));
        if (n < 0) {
            if (errno == EINTR) continue;
            break;                         /* real read error */
        }
        if (n == 0) break;                 /* peer closed cleanly */
        if (write_all(j->fd, buf, (size_t)n) < 0) break;
    }
    close(j->fd);                          /* always close */
    free(j);
}

static void *worker(void *arg)
{
    (void)arg;
    for (;;) {
        Job *j = dequeue();
        if (!j) return NULL;               /* shutdown + drained */
        process(j);
    }
}

int main(void)
{
    struct sigaction sa = {0};
    sa.sa_handler = handle_sig;
    sigaction(SIGINT,  &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);

    pthread_t workers[NUM_WORKERS];
    for (int i = 0; i < NUM_WORKERS; i++) {
        if (pthread_create(&workers[i], NULL, worker, NULL) != 0) {
            perror("pthread_create");
            return 1;
        }
    }

    /* Acceptor loop. Assumes fd 0 is a listening socket (per the
     * original starter). In real code we'd socket()+bind()+listen()
     * ourselves; kept as-is to match the test case. */
    while (!got_signal) {
        int fd = accept(0, NULL, NULL);
        if (fd < 0) {
            if (errno == EINTR) continue;  /* signal interrupted accept */
            continue;
        }

        Job *j = malloc(sizeof(Job));
        if (!j) {
            close(fd);                     /* don't leak on OOM */
            continue;
        }
        j->fd = fd;

        if (enqueue(j) < 0) {              /* shutdown raced us */
            close(j->fd);
            free(j);
            break;
        }
    }

    request_shutdown();
    for (int i = 0; i < NUM_WORKERS; i++) pthread_join(workers[i], NULL);

    /* Drain anything left (workers exit when they see empty+shutdown). */
    pthread_mutex_lock(&qlock);
    while (count > 0) {
        Job *j = queue[head];
        head = (head + 1) % MAXQ;
        count--;
        close(j->fd);
        free(j);
    }
    pthread_mutex_unlock(&qlock);

    return 0;
}
