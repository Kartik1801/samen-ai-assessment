# Test 4: Reinforcement Learning

## Goal

Implement a simple reinforcement learning agent using tabular Q-learning.

## Scenario

You are given a small grid world. The agent must learn to reach the goal while avoiding a blocked cell.

## Environment rules

- Grid size: 4x4
- Start: (0, 0)
- Goal: (3, 3)
- Blocked cell: (1, 1)
- Actions:
  - 0 = up
  - 1 = right
  - 2 = down
  - 3 = left

## Reward

- +10 for reaching the goal
- -1 per step

Episode ends when the goal is reached or after 50 steps

## Starter code

```python
import random from collections import defaultdict ACTIONS = [0, 1, 2, 3] class GridWorld: def __init__(self): self.start = (0, 0) self.goal = (3, 3) self.blocked = {(1, 1)} self.state = self.start self.steps = 0 def reset(self): self.state = self.start self.steps = 0 return self.state def step(self, action): x, y = self.state if action == 0: nx, ny = x - 1, y elif action == 1: nx, ny = x, y + 1 elif action == 2: nx, ny = x + 1, y else: nx, ny = x, y - 1 nx = max(0, min(3, nx)) ny = max(0, min(3, ny)) if (nx, ny) in self.blocked: nx, ny = self.state self.state = (nx, ny) self.steps += 1 if self.state == self.goal: return self.state, 10, True, {} if self.steps >= 50: return self.state, -1, True, {} return self.state, -1, False, {} def epsilon_greedy(q, state, epsilon): if random.random() < epsilon: return random.choice(ACTIONS) values = [q[(state, a)] for a in ACTIONS] return ACTIONS[values.index(max(values))]
```

## Your task

- Implement Q-learning.
- Train the agent for multiple episodes.
- Use epsilon-greedy exploration.
- Show the learned policy or learned path.
- Compare against a random baseline if possible.
- Explain how the algorithm works.
- Required update rule `Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]`

## What we are evaluating

- Can you translate the RL formula into code?
- Do you understand exploration vs exploitation?
- Can you reason about reward and convergence?
- Can you show the policy learned by the agent?

## Deliverable after 1 hour

- Q-learning implementation.
- Brief evaluation output.
- Short explanation of the training loop and policy.

## Strong signals

- Correct update rule.
- Epsilon decay or a reasonable exploration strategy.
- The learned policy reaches the goal more often than random.
- Clear explanation of what changed during training.
