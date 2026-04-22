import random
from collections import defaultdict

""" 
Environment Rules

- Grid size: 4x4
- Start: (0, 0)
- Goal: (3, 3)
- Blocked cell: (1, 1)
- Actions:
    - 0 = up
    - 1 = right
    - 2 = down
    - 3 = left
- Reward:
    - +10 for reaching the goal
    - -1 per step
- Episode ends when the goal is reached or after 50 steps

"""

ACTIONS = [0, 1, 2, 3]


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

        nx = max(0, min(3, nx))
        ny = max(0, min(3, ny))

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

    return ACTIONS[values.index(max(values))]


def training(
    episodes=100,
    alpha=0.1,
    gamma=0.9,
    epsilon_start=1.0,
    epsilon_end=0.1,
    epsilon_decay=0.995,
):
    """
    Q-Learning

    Q Value
    => Q(s,a) = Q(s,a) + alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]

    s => current state
    a => action taken
    s` => next state agent moves to
    a` => best action in state S`
    r => reward for taking action A in state S.
    alpha => learning rate determines how much new info affect old Q Value
    gamma => discount factor to balance immediate reward with future reward
    """
    environment = GridWorld()
    # Initializing the Q-Table with Float type value
    q = defaultdict(float)

    epsilon = epsilon_start
    rewards = []  # tracking reward per episode
    success = []  # tracking success per episode

    # For each episode, start from 0,0.
    for episodes in range(episodes):
        state = environment.reset()
        total_reward = 0
        done = False

        while not done:
            # Select action using epsilon greedy
            action = epsilon_greedy(q, state, epsilon)
            # evaluate result of action
            next_state, reward, done, _ = environment.step(action)
            # Evaluate max q value achievable from each action
            next = max(q[(next_state, act)] for act in ACTIONS)
            # Find Q-Value based on above formula
            q[(state, action)] = q[(state, action)] + (
                alpha * (reward + gamma * next) - q[(state, action)]
            )
            # move to next state
            state = next_state
            total_reward += reward
        # Exponential Epsilon
        epsilon = max(epsilon_end, epsilon * epsilon_decay)

        rewards.append(total_reward)
        success.append(1 if environment.state == environment.goal else 0)

    return q, rewards, success


q_table, reward, success = training()
print(q_table)
print(reward)
print(success)
