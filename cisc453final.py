"""This program plays a random agent against a reinforcement agent using deep q-learning
Q-values are approximated using a sequential neural network model
After each move, a batch of past moves is sampled and the network is trained on these state-action-reward-next state pairs"""

from keras.models import Sequential
from keras.layers import Input, Dense, Dropout
from keras.optimizers import Adam
from collections import deque
from Game import Game
from Visualization import *
import numpy as np
import random

# Initialize constants
GAMMA = 0.9
LEARNING_RATE = 0.1

MEMORY_SIZE = 1000000
BATCH_SIZE = 4

#Decaying exploration - the longer we train, the less we explore
EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995

# Class to approximate the q-values using a neural network
class DQNSolver:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX # start with as much exploration as possible

        self.action_space = action_space # all possible actions (width of the board)
        self.memory = deque(maxlen=MEMORY_SIZE) # store a memory of maxlen most recent actions

        #Create the neural network model
        self.model = Sequential()
        self.model.add(Dense(64, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(64, activation="relu"))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(self.action_space, activation="softmax"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))
        self.model.summary()

    # Function that adds the most recent move and corresponding reward to the memory
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # Function to pick an action based on e-greedy action selection
    def act(self, state, board):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)

        all_actions = list(range(0, board.WIDTH))

        # get values of each action
        action_arr = self.model.predict(np.expand_dims(state, 0), batch_size=1)
        action_arr = action_arr[0]

        # convert to lists to 2-tuple and sort by action value
        action_tuples = list(zip(all_actions, action_arr))
        action_tuples.sort(key=lambda x: x[1], reverse=True)

        # Check to see if action is a legal action, if not do next best action
        # legal moves
        legal_moves = board.getLegalMoves()
        for tuple in action_tuples:
            if tuple[0] in legal_moves:
                return tuple[0]

    # Function to train the neural network
    def experience_replay(self):
        #Only start training if we have enough moves in memory
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)

        #Go through all the state-action-reward-next state pairs in the batch
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            # If we haven't reached the end of the game, calculate the next state q-values using the model
            if not terminal:
              x = np.expand_dims(state_next, 0)
              q_update = (reward + GAMMA * np.amax(self.model.predict(x, batch_size = 1)[0]))
            q_values = self.model.predict(np.expand_dims(state, 0), batch_size = 1) # calculate q-values of current state
            q_values[0][action] = q_update
            self.model.fit(np.expand_dims(state, 0), q_values, batch_size = 1, verbose=0) # train model between predicted q-values and calculated q-values

        #Decrease exploration as time goes on
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)


#WE ARE RED
def connect4():
    # Keep track of number of wins, losses and ties
    winCounter = 0
    lossCounter = 0
    tieCounter = 0

    width = 7
    height = 6
    env = Game(width, height) # a classic 7x6 connect-4 board
    np_grid = np.array(env.grid) # convert the grid to a numpy array - easier for machine learning
    state = np_grid.flatten() # first state from the board is an empty board
    action_space = width # possible actions

    dqn_solver = DQNSolver(len(state), action_space)
    run = 0

    frontEnd = Visualization(500, 500)
    frontEnd.board = Board(width, height)

    #Train for 1000 games
    while run < 1000:
        run += 1
        env.resetBoard() #need to reset the connect 4 board
        np_grid = np.array(env.grid)
        state = np_grid.flatten() # our initial state is the reset connect 4 board

        #Initialize reward to 0
        reward = 0

        while True:

            #Submit the next random action
            action = random.choice(env.getLegalMoves())
            env.submitMove(action, 2)
            np_grid = np.array(env.grid)
            state_next = np_grid.flatten()

            #Check if it's a win or a tie
            win = env.checkWin(1)
            tie = env.checkTie()
            loss = env.checkWin(2)

            #Keep track of number of wins, losses and ties
            if win:
              reward += 10
              terminal = True
              winCounter += 1
            elif tie:
              reward += 0
              terminal = True
              tieCounter += 1
            elif loss:
              reward -= 10
              terminal = True
              lossCounter += 1
            else:
              #reward -= 1
              terminal = False

            state = state_next

            #end game if we've reached an end state
            if terminal:
                break

            #Submit the next reinforcement learning agent action
            action = dqn_solver.act(state, env)

            #Submit the action returned
            env.submitMove(action, 1)

            np_grid = np.array(env.grid)
            state_next = np_grid.flatten()

            #Check if it's a win or a tie
            win = env.checkWin(1)
            tie = env.checkTie()
            loss = env.checkWin(2)

            #Keep track of number of wins, losses and ties
            if win:
              reward += 100
              terminal = True
              winCounter +=1
            elif tie:
              reward += 0
              terminal = True
              tieCounter +=1
            elif loss:
              reward -= 10
              terminal = True
              lossCounter +=1
            else:
              reward -= 1
              terminal = False

            # add our agent's state-action-reward-next state to memory
            dqn_solver.remember(state, action, reward, state_next, terminal)
            state = state_next

            # end game if we've reached an end state
            if terminal:
                break

            # train the network
            dqn_solver.experience_replay()

    print("Wins: ", winCounter, ", Losses: ", lossCounter, ", Ties: ", tieCounter)

    # serialize model to JSON
    model_json = dqn_solver.model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    dqn_solver.model.save_weights("model.h5")
    print("Saved model to disk")

if __name__ == "__main__":
    connect4()