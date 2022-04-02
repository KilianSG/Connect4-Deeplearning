from typing import Callable

import numpy as np
import tensorflow as tf

import building_model.create_model_keras as new_model
from agents.common import Board, BoardPiece, PLAYER1, PLAYER2, PlayerAction, GameState, GenMove, PLAYER1_PRINT, \
    PLAYER2_PRINT
from agents.deep_learning.deep_learning import next_move as generate_move_deep_learning
from agents.minimax.minimax_agent import next_move as generate_move


def user_move(game_table, _player: BoardPiece):
    action = PlayerAction(-1)
    while not 0 <= action < game_table.board.shape[1]:
        try:
            action = PlayerAction(input("Column? "))
        except ValueError:
            print("Input could not be converted to the dtype PlayerAction, try entering an integer.")
    return action


def human_vs_agent(
        generate_move_1: GenMove,
        generate_move_2: GenMove = user_move,
        player_1: str = "Player 1",
        player_2: str = "Player 2",
        args_1: tuple = (),
        args_2: tuple = (),
        init_1: Callable = lambda board, player: None,
        init_2: Callable = lambda board, player: None,
):
    import time

    players = (PLAYER1, PLAYER2)
    for play_first in (1, -1):
        for init, player in zip((init_1, init_2)[::play_first], players):
            init(Board, player)

        saved_state = {PLAYER1: None, PLAYER2: None}

        playing_board = Board()
        gen_moves = (generate_move_1, generate_move_2)[::play_first]
        player_names = (player_1, player_2)[::play_first]
        gen_args = (args_1, args_2)[::play_first]

        playing = True
        while playing:
            for player, player_name, gen_move, args in zip(
                    players, player_names, gen_moves, gen_args,
            ):
                t0 = time.time()
                print(playing_board.get_pretty_print_board())
                print(
                    f'{player_name} you are playing with {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
                )
                action = gen_move(
                    playing_board, player, *args
                )
                print(f"Move time: {time.time() - t0:.3f}s")
                playing_board.apply_player_move(action, player)
                end_state = playing_board.get_game_state()
                if end_state != GameState.STILL_PLAYING:
                    print(playing_board.get_pretty_print_board())
                    if end_state == GameState.IS_DRAW:
                        print("Game ended in draw")
                    else:
                        print(
                            f'{player_name} won playing {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
                        )
                    playing = False
                    break


if __name__ == '__main__':
    opponent = input("Play against Minimax?(m)\nPlay against deep learning?(d)\nLet deep learning learn vs Minimax?(d x)\nCreate new Empty Model.... (Model)")
    if opponent == "d":
        human_vs_agent(user_move, generate_move_deep_learning)
    elif opponent == "m":
        human_vs_agent(user_move, generate_move)
    elif opponent.startswith('d '):
        num = ""
        for c in opponent:
            if c.isdigit():
                num = num + c
        for count in range(int(num)):
            remove_content = open("Dataset/new_data.csv", "w")
            remove_content.truncate()
            remove_content.close()
            human_vs_agent(generate_move, generate_move_deep_learning)
            dataset = np.loadtxt("Dataset/new_data.csv", delimiter=',')
            data_input = dataset[:, 0:42]
            data_output = dataset[:, 42]
            model = tf.keras.models.load_model("evaluation")
            model.fit(data_input, data_output, batch_size=1, epochs=7)
            model.save("evaluation")
    elif opponent == 'Model':
        new_model.make_new_model()
