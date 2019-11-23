from cisc453final import *

def create():
    width = 7
    height = 6
    env = Game(width, height)  # a classic 7x6 connect-4 board
    np_grid = np.array(env.grid)  # convert the grid to a numpy array - easier for machine learning
    state = np_grid.flatten()  # first state from the board is an empty board
    action_space = width  # possible actions

    dqn_solver1 = DQNSolver(len(state), action_space)
    dqn_solver2 = DQNSolver(len(state), action_space)

    return env, dqn_solver1, dqn_solver2

def train():

    env, agent1, agent2 = create()

    # Keep track of number of wins, losses and ties
    winCounter = 0
    lossCounter = 0
    tieCounter = 0

    win2Counter = 0
    loss2Counter = 0
    tie2Counter = 0

    run = 0

    # Train for 1000 games
    while run < 1000:
        run += 1
        env.resetBoard()  # need to reset the connect 4 board
        np_grid = np.array(env.grid)
        state = np_grid.flatten()  # our initial state is the reset connect 4 board

        # Initialize reward to 0
        reward = 0

        while True:

            # Submit the next reinforcement learning agent action
            action = agent1.act(state)

            # Submit the action with the highest q-value - if that isn't available pick a random action
            if action in env.getLegalMoves():
                env.submitMove(action, 1)
            else:
                env.submitMove(random.choice(env.getLegalMoves()), 1)

            np_grid = np.array(env.grid)
            state_next = np_grid.flatten()

            # Check if it's a win or a tie
            win = env.checkWin(1)
            tie = env.checkTie()
            loss = env.checkWin(2)

            # Keep track of number of wins, losses and ties
            if win:
                reward += 100
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
                reward -= 1
                terminal = False

            # add our agent's state-action-reward-next state to memory
            agent1.remember(state, action, reward, state_next, terminal)
            state = state_next

            # end game if we've reached an end state
            if terminal:
                break

            agent1.experience_replay()

            # Submit the next reinforcement learning agent action
            action = agent2.act(state)

            # Submit the action with the highest q-value - if that isn't available pick a random action
            if action in env.getLegalMoves():
                env.submitMove(action, 2)
            else:
                env.submitMove(random.choice(env.getLegalMoves()), 2)

            np_grid = np.array(env.grid)
            state_next = np_grid.flatten()

            # Check if it's a win or a tie
            win = env.checkWin(2)
            tie = env.checkTie()
            loss = env.checkWin(1)

            # Keep track of number of wins, losses and ties
            if win:
                reward += 100
                terminal = True
                win2Counter += 1
            elif tie:
                reward += 0
                terminal = True
                tie2Counter += 1
            elif loss:
                reward -= 10
                terminal = True
                loss2Counter += 1
            else:
                reward -= 1
                terminal = False

            # add our agent's state-action-reward-next state to memory
            agent2.remember(state, action, reward, state_next, terminal)
            state = state_next

            # end game if we've reached an end state
            if terminal:
                break

            # train the network
            agent2.experience_replay()

    print("Wins: ", winCounter, ", Losses: ", lossCounter, ", Ties: ", tieCounter)
    print("Wins: ", win2Counter, ", Losses: ", loss2Counter, ", Ties: ", tie2Counter)

    if winCounter >= lossCounter:
        # serialize model to JSON
        model_json = agent1.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        agent1.model.save_weights("model.h5")
        print("Saved model to disk")
    else:
        # serialize model to JSON
        model_json = agent2.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        agent2.model.save_weights("model.h5")
        print("Saved model to disk")

train()

