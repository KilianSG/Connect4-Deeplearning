from agents.common import *
from agents.minimax.minimax_agent import from_board_to_possible_moves
import csv
import numpy as np


def next_move(play_ground, player):
    if player == PLAYER1:
        counter_player = PLAYER2
    else:
        counter_player = PLAYER1
    action = deep_learning_minimax(play_ground, 3, player, counter_player, -10000000, 10000000, None)
    return action


def get_end_data_end(evaluation, player):
    if player == PLAYER1:
        if not evaluation:
            return 1
        return 0
    else:
        if not evaluation:
            return 0
        return 1


def deep_learning_minimax(play_ground, depth, player, counter_player, alpha, beta, best_move: np.int8):
    is_won = play_ground.is_won(counter_player)
    if is_won:
        new_entry = play_ground.board.flatten().astype('float32')
        new_entry = new_entry.reshape(1, 42)
        generate_new_data = open('Dataset/new_data.csv', 'a', newline='')
        writer = csv.writer(generate_new_data)
        writer.writerow(np.concatenate((new_entry, get_end_data_end(not is_won, player)), axis=None))
        generate_new_data.close()
        return -1*(depth + 1)
    elif depth == 0:
        return play_ground.heuristic(counter_player)
    return_this_move = None
    max_value = alpha
    list_of_moves = from_board_to_possible_moves(play_ground)
    for move in list_of_moves:
        play_ground.apply_player_move(move, player, False)
        new_value = -deep_learning_minimax(play_ground, depth - 1, counter_player, player, -beta, -max_value, move)
        play_ground.take_back_player_move(move, player)
        if new_value > max_value:
            if best_move is None:
                return_this_move = move
            max_value = new_value
            if max_value >= beta:
                break
    if best_move is None:
        if return_this_move is None:
            return None
        return return_this_move
    else:
        return max_value
