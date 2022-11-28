# python-chess

## Playing the game

You can start the game by running the `pychess.py` file from the command line. You will then be presented with a view of the board and the text "White to move." Moves can be performed by entering commands of the form `d2 d4`, where the first term is the coordinates of a piece you control and the second term is the coordinates of the destination tile. If the move is valid, it will execute and the turn will pass to the other player.

## Tournaments

You can use the option -t to run a tournament between two AIs. A tournament, by default, consists of 100 games between the two. A game is considered a draw if it lasts 200 turns or 1 second. At the moment, there are two AIs implemented:
- random: picks moves at random
- boardstate_heuristic: deterministic AI which picks moves according to a utility function which favors boardstate in which it has more high-value pieces in the middle of the board, and avoids boardstates in which its opponent has high-value pieces in the middle of the board. However, it only looks one move ahead.

I hope to implement more AIs, such as:
- an AI that looks several turns ahead
- an AI that uses simulated annealing to randomize behaviour
- an AI that begins using set openings and then switches to a utility function
