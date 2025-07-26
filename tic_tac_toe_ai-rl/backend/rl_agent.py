import numpy as np
import random
from collections import defaultdict

class RLAgent:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.q_table = defaultdict(lambda: np.zeros(9))
        self.set_difficulty()

    def set_difficulty(self):
        if self.difficulty == 'easy':
            self.epsilon = 0.7  # 70% random moves
            self.alpha = 0.1    # Slow learning
        elif self.difficulty == 'hard':
            self.epsilon = 0.05  # 5% random moves
            self.alpha = 0.9     # Fast learning
            self.load_strategies()  # Load pre-trained strategies
        else:  # medium
            self.epsilon = 0.3
            self.alpha = 0.5
        self.gamma = 0.9  # Discount factor

    def load_strategies(self):
        """Pre-trained winning strategies for hard mode"""
        # Center control
        self.q_table['         '][4] = 1.0  # Prefer center
        
        # Winning moves
        self.q_table['X X      '][1] = 10.0  # Complete row
        self.q_table['  X   X  '][4] = 10.0  # Complete diagonal
        # Add more strategic patterns as needed

    def get_action(self, state, valid_moves):
        # First check for immediate win/loss
        if self.difficulty == 'hard':
            # Check if AI can win immediately
            for move in valid_moves:
                temp_state = list(state)
                temp_state[move] = 'O'
                if self.check_win(''.join(temp_state), 'O'):
                    return move
            
            # Block opponent's winning move
            for move in valid_moves:
                temp_state = list(state)
                temp_state[move] = 'X'
                if self.check_win(''.join(temp_state), 'X'):
                    return move

        # Then use Q-learning with exploration
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        
        q_values = self.q_table[state]
        valid_q = {i: q_values[i] for i in valid_moves}
        return max(valid_q.items(), key=lambda x: x[1])[0]

    def check_win(self, state, player):
        """Check if player has winning position"""
        wins = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]            # diagonals
        ]
        for a,b,c in wins:
            if state[a] == state[b] == state[c] == player:
                return True
        return False

    def learn(self, state, action, reward, next_state, done):
        current_q = self.q_table[state][action]
        max_next_q = np.max(self.q_table[next_state]) if not done else 0
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q