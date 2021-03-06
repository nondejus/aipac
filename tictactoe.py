#!/usr/bin/env python
# coding=utf-8
__author__ = 'Xevaquor'
__license__ = 'MIT'

from copy import deepcopy
import random

from minmax import MinmaxAgent
from common import Field


class RandomAgent(object):
    def __init__(self, symbol=Field.Circle):
        self.symbol = symbol

    def make_move(self, state, game):
        valid_moves = filter(lambda m: m[0] == self.symbol, game.get_legal_moves(state))
        return random.choice(valid_moves)


class HumanAgent(object):
    def __init__(self, symbol=Field.Cross):
        self.symbol = symbol

    def make_move(self, state, game):
        while True:
            coords = tuple(map(int, raw_input("Gimme coordinates: (y x) ").split(' ')))
            move = (self.symbol, coords)
            if move in game.get_legal_moves(state, self.symbol):
                return move


class State(object):
    def __init__(self):
        self.grid = [
            [Field.Empty, Field.Empty, Field.Empty],
            [Field.Empty, Field.Empty, Field.Empty],
            [Field.Empty, Field.Empty, Field.Empty]
        ]

    def __str__(self):
        lines = []
        for y in range(3):
            # noinspection PyTypeChecker
            lines.append('|' + ''.join(self.grid[y]) + '|')
        return '+---+\n' + '\n'.join(lines) + '\n+---+\n'


# noinspection PyMethodMayBeStatic
class TicTacToe(object):
    def __init__(self):
        pass

    def get_start_state(self):
        return State()

    def get_legal_moves(self, state, player):
        moves = []
        for y in range(3):
            for x in range(3):
                if state.grid[y][x] == Field.Empty:
                    moves += [(player, (y, x))]

        return moves

    def apply_move(self, state, move):
        player, coord = move
        y, x = coord
        new_state = deepcopy(state)
        new_state.grid[y][x] = player
        return new_state

    def has_won(self, state, player):
        winning_combinations = [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],

            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],


            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)]
        ]

        for combination in winning_combinations:
            streak = True
            for y, x in combination:
                if state.grid[y][x] != player:
                    streak = False
                    break
            if streak:
                return True
        return False

    def has_lose(self, state, player):
        opponent = Field.Circle if player == Field.Cross else Field.Cross
        return self.has_won(state, opponent)

    def is_terminal(self, state):
        if self.has_won(state, Field.Circle):
            return True
        if self.has_won(state, Field.Cross):
            return True
        for y in range(3):
            for x in range(3):
                if state.grid[y][x] == Field.Empty:
                    return False
        return True


if __name__ == "__main__":
    ha = HumanAgent()
    ca = MinmaxAgent()
    g = TicTacToe()
    s = g.get_start_state()

    human_turn = True

    while True:
        if g.has_won(s, Field.Circle):
            print "Circle won!"
            break
        elif g.has_won(s, Field.Cross):
            print "Cross won!"
            break
        elif g.is_terminal(s):
            print "DRAW!"
            break

        if human_turn:
            print s
            taken_move = ha.make_move(s, g)
        else:
            taken_move = ca.make_move(s, g)
        s = g.apply_move(s, taken_move)
        human_turn = not human_turn

    print "Game finished"
    print s
