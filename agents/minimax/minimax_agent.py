from agents.common import *
import numpy as np
import random
import csv


def get_end_data_end(evaluation, player):
    if player == PLAYER1:
        if evaluation[0] == -1:
            return 1
        return 0
    else:
        if evaluation[0] == -1:
            return 0
        return 1


def from_board_to_possible_moves(play_ground):
    list_possible_moves = play_ground.get_possible_moves()
    list_of_moves = []
    for move in range(7):
        if list_possible_moves[move] != -1:
            list_of_moves.append(move)
    return list_of_moves


def next_move(play_ground, player):
    if player == PLAYER1:
        counter_player = PLAYER2
    else:
        counter_player = PLAYER1
    action = minimax(play_ground, 6, player, counter_player, -10000000, 10000000, None)
    return action


def minimax(play_ground, depth, player, counter_player, alpha, beta, best_move: np.int8):
    evaluation = play_ground.evaluation(counter_player)
    if evaluation[0] != 0 or depth == 0:
        return -(depth + 1) * evaluation[1]
    return_this_move = None
    max_value = alpha

    list_of_moves = from_board_to_possible_moves(play_ground)

    for move in list_of_moves:
        play_ground.apply_player_move(move, player, False)  # do move
        new_value = -minimax(play_ground, depth-1, counter_player, player, -beta, -max_value, move)  # recursive
        play_ground.take_back_player_move(move, player)  # take back move
        if new_value > max_value:
            if best_move is None:
                return_this_move = move
            max_value = new_value
            if max_value >= beta:
                break
    if best_move is None:
        if return_this_move is None:
            list_of_moves[0]
            return list_of_moves[0]
        return return_this_move
    else:
        return max_value

