import pygame
import sys

class Player(object):
    def __init__(self, board):
        self.board = board
        board.spawn_puyo_pair()

    def update(self, fast):
        self.board.update(fast)

    def drop_neutrals(self, other):
        self.board.score.drop_neutrals += other.board.score.neutrals_scored()

    def game_over(self):
        return self.board.game_over


class HumanPlayer(Player):
    def __init__(self, board, keys):
        Player.__init__(self, board)
        self.rotate_key, self.left_key, self.right_key, self.speed_key = keys

    def key_press(self, key):
        if key == self.rotate_key:
            self.board.rotate()
        elif key == self.left_key:
            self.board.move(False)
        elif key == self.right_key:
            self.board.move(True)

    def update(self):
        Player.update(self, pygame.key.get_pressed()[self.speed_key])

class ComputerPlayer(Player):
    def __init__(self, board):
        Player.__init__(self, board)
        self.next_move()

    def key_press(self, key):
        pass

    def update(self):
        fast = True
        if self.move[1] > 0:
            self.board.rotate()
            self.move[1] -= 1
            fast = False
        elif self.board.current_pair:
            if self.move[0] > self.board.current_pair[0].col:
                self.board.move(True)
                fast = False
            elif self.move[0] < self.board.current_pair[0].col:
                self.board.move(False)
                fast = False
        else:
            fast = False

        Player.update(self, fast)
        if self.board.spawned:
            self.next_move()

    def next_move(self):
        board = self._clone_board()
        start_score = self._calculate_points(board)
        pair = [puyo.color for puyo in self.board.current_pair]
        next_pair = [puyo.color for puyo in self.board.score.next_pair]

        max_score = -10000000000000

        for p, cols, rot in self._get_drops(pair):
            new_board = self._drop_pair(board, p, cols)
            score = self._delete_touching(new_board) - 30
            for next_p, next_cols, next_rot in self._get_drops(next_pair):
                next_board = self._drop_pair(new_board, next_p, next_cols)
                next_score = self._calculate_points(next_board) - pow(self._max_height(next_board), 2) - start_score
                if next_score > score:
                    score = next_score
            if score > max_score:
                best_move = [cols[0], rot, score]
                max_score = score

        self.move = best_move


    def _get_drops(self, pair):
        drops = []
        for col in range(self.board.cols_count):
            drops.append((pair, (col, col), 0))
            if col > 0:
                drops.append((pair, (col, col - 1), 1))
            drops.append(((pair[1], pair[0]), (col, col), 2))
            if col < self.board.cols_count - 1:
                drops.append((pair, (col, col + 1), 3))
        return drops

    def _delete_touching(self, board):
        points = 0
        visited = [[False for puyo in row] for row in board]
        deleted = True
        while deleted:
            deleted = False
            for row in range(len(board)):
                for col in range(len(board[row])):
                    p = self._calculate_points_from(board, visited, row, col, board[row][col])
                    if p >= 4:
                        deleted = True
                        points += p * p
                        self._delete_touching_from(board, row, col, board[row][col])

            dropping = True
            while dropping:
                dropping = False
                for r in range(len(board) - 1):
                    for col in range(len(board[row])):
                        row = len(board) - r - 1
                        if not board[row][col] and board[row - 1][col]:
                            board[row][col] = board[row - 1][col]
                            board[row - 1][col] = None
                            dropping = True
        return points

    def _delete_touching_from(self, board, row, col, color):
        if row < 0 or col < 0 or row >= len(board) or col >= len(board[row]) or \
                board[row][col] is None or board[row][col] != color:
            return

        current_color = board[row][col]
        board[row][col] = None
        if board[row][col] != 'neutral':
            self._delete_touching_from(board, row - 1, col, color)
            self._delete_touching_from(board, row, col - 1, color)
            self._delete_touching_from(board, row + 1, col, color)
            self._delete_touching_from(board, row, col + 1, color)


    def _drop_pair(self, old_board, pair, cols):
        board = [[color for color in row] for row in old_board]
        self._drop_puyo(board, pair[1], cols[1])
        self._drop_puyo(board, pair[0], cols[0])
        return board

    def _calculate_points(self, board):
        visited = [[False for puyo in row] for row in board]
        points = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                color = board[row][col]
                if color != 'neutral':
                    p = self._calculate_points_from(board, visited, row, col, color)
                    points += pow(p, 2)

        return points

    def _max_height(self, board):
        for row in range(len(board)):
            for puyo in board[row]:
                if puyo:
                    return len(board) - row
        return 0

    def _calculate_points_from(self, board, visited, row, col, color):
        if row < 0 or col < 0 or row >= len(board) or col >= len(board[row]) or \
                board[row][col] is None or board[row][col] != color or visited[row][col]:
            return 0

        visited[row][col] = True
        if board[row][col] == 'neutral':
            return 1

        return 1 + self._calculate_points_from(board, visited, row - 1, col, color) + \
            self._calculate_points_from(board, visited, row, col - 1, color) + \
            self._calculate_points_from(board, visited, row + 1, col, color) + \
            self._calculate_points_from(board, visited, row, col + 1, color)

    def _drop_puyo(self, board, puyo, col):
        for r in range(len(board)):
            row = len(board) - r - 1
            if board[row][col] == None:
                board[row][col] = puyo
                return True
        return False

    def _clone_board(self):
        board = self.board.empty_board()
        for puyo in self.board.sprites():
            if not puyo in self.board.current_pair:
                board[puyo.row][puyo.col] = puyo.color
        return board

