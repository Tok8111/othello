# ゲームの盤面ロジックやルールを扱う（判定や処理系のメソッドを定義）
import pygame
import sys
from constants import constants
from BoardRenderer import BoardRenderer

class GameLogic:

    def __init__(self):
        self.board = [[constants.EMPTY for _ in range(constants.BOARD_SIZE)] for _ in range(constants.BOARD_SIZE)]

        # 初期の石の配置
        self.board[3][3], self.board[4][4] = constants.WHITE_DISC, constants.WHITE_DISC
        self.board[3][4], self.board[4][3] = constants.BLACK_DISC, constants.BLACK_DISC

        # 初期手番を黒にする
        self.current_player = constants.BLACK_DISC

    def get_board(self):
        return self.board
    
    # 指定のマス(row, col)に、そのプレイヤーの石が置けるかを判定
    def is_valid_move(self, row, col, player):
        # 指定位置が空(None)でなければ、不可
        if self.board[row][col] is not constants.EMPTY:
            return False
    
        opponent = constants.WHITE_DISC if player == constants.BLACK_DISC else constants.BLACK_DISC

        for dr, dc in constants.DIRECTIONS:
            r, c = row + dr, col + dc
            found_opponent = False

            while 0 <= r < constants.BOARD_SIZE and 0 <= c < constants.BOARD_SIZE:
                if self.board[r][c] == opponent:
                    found_opponent = True
                elif self.board[r][c] == player:
                    if found_opponent:
                        return True
                    else:
                        break
                else:
                    break
                r += dr
                c += dc

        return False

    # 指定のプレイヤーにとって有効な手（置けるマス）の一覧を取得する
    def get_valid_moves(self, player):
        return[(r, c) for r in range(constants.BOARD_SIZE) for c in range(constants.BOARD_SIZE) if self.is_valid_move(r, c, player)]

    # 石を置いた後に、その手で裏返る相手の石を反転させる処理（target_board は対象の盤面（コピーか本物か）を指定）
    def flip_discs(self, row, col, player, target_board):
        opponent = constants.WHITE_DISC if player == constants.BLACK_DISC else constants.BLACK_DISC

        for dr, dc in constants.DIRECTIONS:
            r, c = row + dr, col + dc
            path = []

            while 0 <= r < constants.BOARD_SIZE and 0 <= c < constants.BOARD_SIZE:
                if target_board[r][c] == opponent:
                    path.append((r, c))
                elif target_board[r][c] == player:
                    for pr, pc in path:
                        target_board[pr][pc] = player
                    break
                else:
                    break
                r += dr
                c += dc

    # 指定のマスに石を置き、裏返し処理も行う（target_board を指定しないと実際の盤面に反映される）
    def place_disc(self, row, col, player, target_board=None):
        if target_board is None:
            target_board = self.board # デフォルトは実盤面

        target_board[row][col] = player
        self.flip_discs(row, col, player, target_board)

    # 盤面上の石（黒・白）の数を数える
    def count_discs(self):
        black = sum(row.count(constants.BLACK_DISC) for row in self.board)
        white = sum(row.count(constants.WHITE_DISC) for row in self.board)
        return black, white

    # 黒・白の合法手の有無をチェックする
    def has_valid_moves(self, player):
        for row in range(constants.BOARD_SIZE):
            for col in range(constants.BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    return True
        return False        
  

    # 勝敗判定処理
    def check_game_end(self):
        black_moves = self.get_valid_moves(constants.BLACK_DISC)
        white_moves = self.get_valid_moves(constants.WHITE_DISC)

        if black_moves or white_moves:
            return None # ゲーム継続

        # 両者打てない　→　終了＆勝敗判定
        black_count = sum(row.count(constants.BLACK_DISC) for row in self.board)
        white_count = sum(row.count(constants.WHITE_DISC) for row in self.board)

        if black_count > white_count:
            return 'Black wins!'
        elif white_count > black_count:
            return 'White wins!'
        else:
            return 'Draw!'