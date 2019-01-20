import numpy as np
import pandas as pd


class Table:
    def __init__(self, actions, q_table, learning_rate=0.1, gamma=0.8,
                 epsilon=0.8):
        self.actions = actions
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = q_table

    def choose_action(self, observation):
        self.add_state(observation)
        state_action = self.q_table.ix[observation, :]

        if np.random.uniform() < self.epsilon:
            state_action = state_action.reindex(
                np.random.permutation(state_action.index)
            )

            action = state_action.idxmax()
        else:
            action = np.random.choice(state_action.index)

        return action

    def learn(self, from_state, action, reward, to_state):
        if from_state == to_state:
            return

        self.add_state(to_state)
        self.add_state(from_state)

        q_predict = self.q_table.ix[from_state, action]
        s_rewards = self.q_table.ix[to_state, :]

        internal_reward = reward + self.gamma * s_rewards.max()
        q_target = internal_reward if to_state != 'terminal' else reward

        self.q_table.ix[from_state, action] += self.lr * (q_target - q_predict)

    def add_state(self, state):
        if state in self.q_table.index:
            return
        self.q_table = self.q_table.append(
            pd.Series(
                [0] * len(self.actions),
                index=self.q_table.columns,
                name=state
            )
        )
