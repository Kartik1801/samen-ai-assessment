# References

## Data Camp

<https://www.datacamp.com/tutorial/introduction-q-learning-beginner-tutorial>

## From Google Search AI

```plain
In Q-learning, the epsilon-greedy strategy is used to balance exploration (trying new things) and exploitation (using what you already know). The "epsilon end" value (typically denoted as 
 or 
) is the final, lowest probability of choosing a random action that the agent maintains once the training has sufficiently converged. 
Medium
Medium
 +4
Why use an "epsilon end"?
Preventing Stagnation: If 
 decayed to absolute zero, the agent would never explore again. Keeping a small "epsilon end" (e.g., 0.01 or 0.1) ensures the agent can still discover improvements if the environment changes or if it was stuck in a local optimum.
Stability: Once the agent has a strong policy, a high exploration rate would cause it to make too many random mistakes, hindering its final performance score. 
Stack Overflow
Stack Overflow
 +3
1. Initialize Epsilon Parameters 
To implement a decay schedule, you must define the starting probability, the target end probability, and the rate at which you move between them.
Epsilon Start (
): Usually 
 (complete exploration).
Epsilon End (
): Usually between 
 and 
 (minimal residual exploration).
Decay Rate: The speed at which 
 decreases (e.g., 
 for exponential decay). 
Medium
Medium
 +3
2. Choose a Decay Method
You can reduce 
 using different mathematical schedules. 
Linear Decay: Subtract a fixed amount every step/episode until reaching 
.

Exponential Decay: Multiply by a factor less than 1 (most common for smooth transition).

 
3. Implement Selection Logic
During each step of the episode, the agent uses the current 
 value to decide its action. 
Generate a random number 
 between 0 and 1.
If 

: Choose a random action (Exploration).
If 

: Choose the action with the highest Q-value for the current state (Exploitation). 
pylessons.com
pylessons.com
 +4
4. Update Epsilon
After each episode or step (depending on your design), update the value of 
 based on your chosen decay method, ensuring it never drops below your defined epsilon end. 
Reddit
Reddit
 +1
```

```plain
In Q-Learning, the 
-greedy strategy balances discovering new rewards (exploration) and using known high-value paths (exploitation). 
 (epsilon) represents the probability of choosing a random action. Epsilon decay is the process of gradually reducing this probability as the agent learns, shifting from high exploration to steady exploitation. 
Stack Overflow
Stack Overflow
 +5
1. Action Selection Rule
At each step, the agent generates a random number 






: 
CodeSignal
CodeSignal
 +1
Explore: If 

, select a random action from the environment.
Exploit: If 

, select the action with the highest Q-value: 






. 
Stack Overflow
Stack Overflow
 +2
2. Common Decay Schedules
As training progresses, 
 is typically reduced from an initial value (often 
) to a minimum threshold (e.g., 
 or 
) to stabilize the learned policy. 
Medium
Medium
 +1
Linear Decay: 
 decreases by a fixed amount at each step or episode.

Exponential Decay: 
 is multiplied by a decay rate (e.g., 
) after every episode, causing it to drop quickly at first and then level off.

Discrete Interval Decay: 
 stays constant for a set number of steps before dropping to a new lower value. 
Medium
Medium
 +3
3. Implementation Visualization
The chart below illustrates how different decay rates (
) affect the transition from exploration to exploitation over 
 episodes.
Graph image
4. Why Use Epsilon Decay?
Initial Discovery: High 
 (near 
) ensures the agent visits many states early on when Q-values are mostly unknown or random.
Convergence: As the agent gains knowledge, reducing 
 allows it to focus on the optimal path. If 
 remains high, the agent will continue to take suboptimal random actions, preventing the reward from stabilizing.
Avoiding Local Optima: Unlike a purely greedy strategy (

), 
-greedy helps the agent "break out" of locally optimal cycles by occasionally trying something new. 
Stack Overflow
Stack Overflow
 +3
Summary of Parameters
Parameter  Typical Value Purpose
Initial 

Start with total exploration.
Minimum 

 to 
Ensure a tiny amount of lifelong exploration.
Decay Rate 
 to 
Controls how fast the agent becomes "greedy".
```
