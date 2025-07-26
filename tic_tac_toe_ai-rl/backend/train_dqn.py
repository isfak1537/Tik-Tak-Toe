import numpy as np
from game import TicTacToe
from rl_agent import RLAgent
import random

def preprocess_state(state):
    # Convert board state to numerical representation
    return np.array([1 if c == 'O' else -1 if c == 'X' else 0 for c in state])

def train_dqn(episodes=10000):
    env = TicTacToe()
    agent = RLAgent()
    
    for episode in range(episodes):
        state = env.reset()
        state_processed = preprocess_state(state)
        done = False
        
        while not done:
            # Agent's turn
            valid_moves = env.get_valid_moves()
            action = agent.get_action(state, valid_moves, use_dqn=True)
            env.make_move(action)
            next_state = env.get_state()
            next_state_processed = preprocess_state(next_state)
            reward = 0
            
            if env.game_over:
                if env.winner == 'O':  # Agent won
                    reward = 1
                elif env.winner == 'X':  # Agent lost
                    reward = -1
                done = True
                # Train DQN
                target = reward
                agent.model.fit(state_processed.reshape(1, -1), 
                              np.array([target if i == action else 0 for i in range(9)]).reshape(1, -1),
                              verbose=0)
                break
            
            # Opponent's turn (random)
            if not env.game_over:
                opponent_move = random.choice(env.get_valid_moves())
                env.make_move(opponent_move)
                next_state = env.get_state()
                next_state_processed = preprocess_state(next_state)
                
                if env.game_over:
                    if env.winner == 'X':
                        reward = -1
                    done = True
            
            # Train DQN
            if not done:
                future_rewards = agent.model.predict(next_state_processed.reshape(1, -1), verbose=0)
                target = reward + 0.9 * np.max(future_rewards)
            else:
                target = reward
                
            target_f = agent.model.predict(state_processed.reshape(1, -1), verbose=0)
            target_f[0][action] = target
            agent.model.fit(state_processed.reshape(1, -1), target_f, verbose=0)
            
            state = next_state
            state_processed = next_state_processed
    
    agent.model.save('dqn_model.h5')
    print("Training completed!")

if __name__ == '__main__':
    train_dqn()