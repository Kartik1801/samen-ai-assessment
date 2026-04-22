"""
Tabular Q-learning for the 4x4 grid world - fixed version.

The critical bug in the original q-learning.py was the update rule.
The canonical Q-learning update is:

    Q(s,a) <- Q(s,a) + alpha * [ r + gamma * max_a' Q(s',a') - Q(s,a) ]

The original code wrote:

    q[(s,a)] = q[(s,a)] + (alpha * (r + gamma * next) - q[(s,a)])

The parentheses are in the wrong place. That simplifies to:

    q = q + alpha*(r + gamma*next) - q
      = alpha*(r + gamma*next)

so the old Q(s,a) disappears and the TD error never forms. The agent
overwrites Q with a shrunken one-step target each visit, which does
not converge to the optimal value function.

The correct form, used below:

    td_target = r + gamma * max_a' Q(s', a')     (0 if s' is terminal)
    td_error  = td_target - Q(s, a)
    Q(s, a)  += alpha * td_error

Other issues fixed:
  - `for episodes in range(episodes)` shadowed the parameter.
  - No random baseline was provided (task required a comparison).
  - No policy/path was displayed (task required one).
  - epsilon-greedy argmax always picked index 0 on ties, biasing
    action 0 when Q is initialised at zero.
"""

import random
from collections import defaultdict


ACTIONS = [0, 1, 2, 3]
ACTION_NAMES = {0: "^", 1: ">", 2: "v", 3: "<"}
GRID_SIZE = 4


class GridWorld:
    def __init__(self):
        self.start = (0, 0)
        self.goal = (3, 3)
        self.blocked = {(1, 1)}
        self.state = self.start
        self.steps = 0

    def reset(self):
        self.state = self.start
        self.steps = 0
        return self.state

    def step(self, action):
        x, y = self.state
        if action == 0:
            nx, ny = x - 1, y
        elif action == 1:
            nx, ny = x, y + 1
        elif action == 2:
            nx, ny = x + 1, y
        else:
            nx, ny = x, y - 1

        nx = max(0, min(GRID_SIZE - 1, nx))
        ny = max(0, min(GRID_SIZE - 1, ny))
        if (nx, ny) in self.blocked:
            nx, ny = self.state

        self.state = (nx, ny)
        self.steps += 1

        if self.state == self.goal:
            return self.state, 10, True, {}
        if self.steps >= 50:
            return self.state, -1, True, {}
        return self.state, -1, False, {}


def epsilon_greedy(q, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    values = [q[(state, a)] for a in ACTIONS]
    best = max(values)
    # Random tiebreak so an all-zero Q-table doesn't always pick action 0.
    candidates = [a for a, v in zip(ACTIONS, values) if v == best]
    return random.choice(candidates)


def train(
    n_episodes=500,
    alpha=0.1,
    gamma=0.9,
    epsilon_start=1.0,
    epsilon_end=0.05,
    epsilon_decay=0.995,
):
    env = GridWorld()
    q = defaultdict(float)
    epsilon = epsilon_start
    rewards, successes = [], []

    for _ in range(n_episodes):
        state = env.reset()
        total = 0.0
        done = False

        while not done:
            action = epsilon_greedy(q, state, epsilon)
            next_state, reward, done, _ = env.step(action)

            # If next state is terminal there is no future value.
            if done:
                td_target = reward
            else:
                best_next = max(q[(next_state, a)] for a in ACTIONS)
                td_target = reward + gamma * best_next

            td_error = td_target - q[(state, action)]
            q[(state, action)] += alpha * td_error          # CORRECT update

            state = next_state
            total += reward

        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        rewards.append(total)
        successes.append(1 if env.state == env.goal else 0)

    return q, rewards, successes


def random_baseline(n_episodes=500):
    env = GridWorld()
    rewards, successes = [], []
    for _ in range(n_episodes):
        env.reset()
        total = 0.0
        done = False
        while not done:
            _, reward, done, _ = env.step(random.choice(ACTIONS))
            total += reward
        rewards.append(total)
        successes.append(1 if env.state == env.goal else 0)
    return rewards, successes


def greedy_policy(q):
    policy = {}
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            values = [q[((x, y), a)] for a in ACTIONS]
            best = max(values)
            candidates = [a for a, v in zip(ACTIONS, values) if v == best]
            policy[(x, y)] = candidates[0]
    return policy


def render_policy(policy, env):
    rows = []
    for x in range(GRID_SIZE):
        row = []
        for y in range(GRID_SIZE):
            if (x, y) == env.goal:
                row.append(" G ")
            elif (x, y) in env.blocked:
                row.append(" # ")
            else:
                row.append(f" {ACTION_NAMES[policy[(x, y)]]} ")
        rows.append("".join(row))
    return "\n".join(rows)


def rollout_greedy(q, env, max_steps=50):
    policy = greedy_policy(q)
    env.reset()
    path = [env.state]
    for _ in range(max_steps):
        state, _, done, _ = env.step(policy[env.state])
        path.append(state)
        if done:
            break
    return path


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


if __name__ == "__main__":
    random.seed(0)

    q, q_rewards, q_success = train(n_episodes=500)
    r_rewards, r_success = random_baseline(n_episodes=500)

    last = 100
    print("=== Evaluation (last 100 episodes) ===")
    print(f"  Q-learning  avg reward = {_mean(q_rewards[-last:]):+.2f}"
          f"   success = {_mean(q_success[-last:]):.0%}")
    print(f"  Random      avg reward = {_mean(r_rewards[-last:]):+.2f}"
          f"   success = {_mean(r_success[-last:]):.0%}")

    env = GridWorld()
    print("\n=== Learned policy (^>v<, G=goal, #=blocked) ===")
    print(render_policy(greedy_policy(q), env))

    print("\n=== Greedy rollout from start ===")
    print(rollout_greedy(q, GridWorld()))
