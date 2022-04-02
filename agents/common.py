from enum import Enum
from typing import Callable, Tuple

import numpy as np
import tensorflow as tf

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece
PlayerAction = np.int8  # The column to be played
BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0
    IS_LOST = -2


print_dict = {
    NO_PLAYER: NO_PLAYER_PRINT,
    PLAYER1: PLAYER1_PRINT,
    PLAYER2: PLAYER2_PRINT
}


class Board:
    def __init__(self):
        self.board = np.ndarray(shape=(6, 7), dtype=BoardPiece)
        self.board.fill(NO_PLAYER)
        self.state_of_game = GameState.STILL_PLAYING

    def apply_player_move(self, move: np.int8, player: int, copy_board=False):
        """
        :param move: next move
        :param player: by whome
        :param copy_board: if copy should be done of the board
        :return: True if done, False if not possible
        """
        if copy_board:
            board_copy = self.copy_board()
        for x in range(6):
            if self.board[x, move] == NO_PLAYER:
                self.board[x, move] = player
                break
        if copy_board:
            return board_copy

    def take_back_player_move(self, move: np.int8, player):
        """
        :param move: move to retour
        :param player: whoms move should be taken back
        :return: bool if succesfull or not
        """
        for x in reversed(range(6)):
            if self.board[x, move] != NO_PLAYER:
                if self.board[x, move] == player:
                    self.board[x, move] = NO_PLAYER
                    return True
                else:
                    return False
        return False

    def get_possible_moves(self) -> list:
        """
        if no turn ist playable, put state_of_game to Draw
        :return: list with row-number for each action that is possible to take
        """
        this_ones_are_empty = [-1, -1, -1, -1, -1, -1, -1]
        for line in range(7):
            if self.board[5, line] == NO_PLAYER:
                this_ones_are_empty[line] = line
        if this_ones_are_empty == [-1, -1, -1, -1, -1, -1, -1]:
            self.state_of_game == GameState.IS_DRAW
        return this_ones_are_empty

    def is_won(self, player):
        """
        check if player won the game and return True or False
        :rtype: bool
        """
        def check_row(row):
            line_score = 0
            for symbol in row:
                if symbol == player:
                    line_score += 1
                else:
                    if line_score >= 4:
                        return True
                    line_score = 0
            if line_score >= 4:
                return True
            return False

        def check_by_lines(b: np.ndarray) -> bool:
            for i in range(b.shape[0]):
                if check_row(b[i]):
                    return True
            return False

        def check_by_diagonal(b: np.ndarray) -> bool:
            offset = list(range(-2, 4))
            for i in offset:
                diagonal = list(np.diagonal(b, offset=i))
                if check_row(diagonal):
                    return True
            return False
        # checking horizontally
        if check_by_lines(self.board):
            return True
        # checking vertically
        if check_by_lines(self.board.T):
            return True
        # checking diagonally
        if check_by_diagonal(self.board):
            return True
        if check_by_diagonal(np.flipud(self.board)):
            return True
        return False

    def get_pretty_print_board(self):
        """
        :return: return Board as string
        """
        return_board = '|===============|\n'
        for row in reversed(self.board):
            return_board += '| '
            for piece in row:
                return_board += f"{print_dict[piece]} "
            return_board += '|\n'
        return_board += '|===============|\n'
        return_board += '| 0 1 2 3 4 5 6 |'
        return return_board

    def copy_board(self) -> np.ndarray:
        """
        make a deep copy
        :return: deep copy
        """
        send_this_board = Board()
        send_this_board.board = self.board.copy()
        send_this_board.state_of_game = self.state_of_game
        return send_this_board

    def get_game_state(self) -> GameState:
        end_state = self.evaluation(PLAYER1)
        if end_state[0] != 0:
            return end_state[0]
        return GameState.STILL_PLAYING

    def evaluation(self, player: int) -> (int, int):
        """
        looks if the game is won by the player or by the counterplayer, if that is the case return -1 or 1 for wins
        or return 0 for no win and return the evaluation of the board
        :param player:
        :return: State of Play, Evaluation of position
        """
        if player == PLAYER1:
            counter_player = PLAYER2
        else:
            counter_player = PLAYER1

        evaluation = 0

        for row in range(6):
            for line in range(4):
                list_of_board = [self.board[row][line], self.board[row][line + 1], self.board[row][line + 2],
                                 self.board[row][line + 3]]
                evaluated = evaluate_list(list_of_board, player, counter_player)
                if evaluated[0] != 0:
                    return evaluated

                evaluation += evaluated[1]

        for line in range(7):
            for row in range(3):
                list_of_board = [self.board[row][line], self.board[row + 1][line], self.board[row + 2][line],
                                 self.board[row + 3][line]]
                evaluated = evaluate_list(list_of_board, player, counter_player)
                if evaluated[0] != 0:
                    return evaluated
                evaluation += evaluated[1]

        for line in range(4):
            for row in range(3, 6):
                list_of_board = [self.board[row][line], self.board[row - 1][line + 1], self.board[row - 2][line + 2],
                                 self.board[row - 3][line + 3]]
                evaluated = evaluate_list(list_of_board, player, counter_player)
                if evaluated[0] != 0:
                    return evaluated
                evaluation += evaluated[1]

        for line in range(3, 7):
            for row in range(3, 6):
                list_of_board = [self.board[row][line], self.board[row - 1][line - 1], self.board[row - 2][line - 2],
                                 self.board[row - 3][line - 3]]
                evaluated = evaluate_list(list_of_board, player, counter_player)
                if evaluated[0] != 0:
                    return evaluated
                evaluation += evaluated[1]

        return 0, evaluation

    def heuristic(self, player: int) -> float:
        return deep_learning_heuristic(self.board, player)


def deep_learning_heuristic(board: np.ndarray, player: int) -> float:
    if reconstructed_model == None:
        reconstructed_model = tf.keras.models.load_model("connect4-objects\evaluation")
    flatten_board = board.flatten().astype('float32')
    flatten_board = flatten_board.reshape(1, 42)
    if player == PLAYER1:
        return reconstructed_model.predict(flatten_board)
    else:
        return 1 - reconstructed_model.predict(flatten_board)


def evaluate_list(list_of_board: list, player: int, counter_player: int):
    """
    :param list_of_board: list of the board that needs to be checked for winning conditions
    :param player: the player who is getting a 1 if he wins, and a -1 if he loses
    :param counter_player: the player who is getting a -1 if he loses, and a 1 if he wins
    :return: return 0,1 or -1 for Gamestate, and a evaluation for the board
    """
    evaluation = 0
    sum = 1
    if list_of_board == [player, player, player, player]:
        return 1, 3200

    elif list_of_board == [counter_player, counter_player, counter_player, counter_player]:
        return -1, -3200

    elif counter_player not in list_of_board:
        for z in list_of_board:
            if z == player:
                sum *= 5
        evaluation += sum

    elif player not in list_of_board:
        for z in list_of_board:
            if z == counter_player:
                sum *= 5
        evaluation -= sum
    return 0, evaluation


GenMove = Callable[
    [Board, BoardPiece],  # Arguments for the generate_move function
    Tuple[PlayerAction]  # Return type of the generate_move function
]
