// worker.c
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#define MAXQ 16

typedef struct Job
{
    // File Descriptor
    int fd;
} Job;

static pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER;

static pthread_cond_t qcv = PTHREAD_COND_INITIALIZER;

// A job queue.
static Job *queue[MAXQ];

static int head = 0;
static int tail = 0;
static int count = 0;
// Flag used by worker function for processing jobs in queue.
static int running = 1;

static void enqueue(Job *j)
{
    // request for lock, wait until the lock is available, and then acquire the lock
    pthread_mutex_lock(&qlock);

    queue[tail] = j;
    // % will handle overflow.
    tail = (tail + 1) % MAXQ;
    count++;

    pthread_cond_signal(&qcv);
    // release the lock after adding the job to the queue and signaling the condition variable
    pthread_mutex_unlock(&qlock);
}

static Job *dequeue(void)
{
    pthread_mutex_lock(&qlock);
    // BUG 1: As per the google AI result on how the pthread_cond_signal work
    // if => while
    while (count == 0)
    {
        // blocks a thread until a specific condition is signaled, atomically unlocking the associated mutex and suspending the thread
        pthread_cond_wait(&qcv, &qlock);
    }

    // dequeue the job at the head of the queue and update the head index and count
    Job *j = queue[head];

    head = (head + 1) % MAXQ;

    count--;

    pthread_mutex_unlock(&qlock);
    return j;
}

// Handles the job
static void process(Job *j)
{
    char buf[128];
    // BUG - 2: read function is used but not closed
    ssize_t n = read(j->fd, buf, sizeof(buf));

    // check for error (-1)
    if (n < 0)
    {   
        // added this to close the file descriptor & -[1]
        close(j->fd);
        free(j);
        // - [1] free the job structure in case of an error while reading from the file descriptor
        return;
    }

    write(j->fd, buf, n);
    close(j->fd);
    free(j);
}

void *worker(void *arg)
{
    while (running)
    {
        Job *j = dequeue();
        if (j)
        {
            process(j);
        }
    }
    return NULL;
}

int main(void)
{
    while (1)
    {
        /*
        Accepts some sort of socket connection and returns an integer
        Success: Returns a non-negative integer, which is the file descriptor for the newly accepted socket. Use this new descriptor for read() and write() operations with that specific client.
        Failure: Returns -1 and sets errno to indicate the error.
        */
        // contains the file descriptor for the newly accepted socket connection
        int fd = accept(0, NULL, NULL);
        // Filters out invalid file descriptors
        if (fd < 0)
        {
            continue;
        }

        // allocate a memory for a new job
        Job *j = malloc(sizeof(Job));
        // assign the file descriptor to the job structure
        j->fd = fd;

        enqueue(j);
    }
    return 0;
}