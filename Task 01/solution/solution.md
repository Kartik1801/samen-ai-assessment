# Test 1

1. Possible `Spurious Wakeups` or `Missing Signals`. If `pthread_cond_signal` is called before a thread enters `pthread_cond_wait`, the signal is lost.

2. Possible memory leak since we are not calling `close` after reading data from `fd`