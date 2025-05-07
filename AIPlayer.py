# コンピュータ（AI）としての意思決定を行う処理
import random
from constants import constants

class AIPlayer:

    def __init__(self, game_logic):
        self.game_logic = game_logic

    # 石の重みマップを用いて、盤面のスコアを評価
    def evaluate_board(self, board, player):
        score = 0
        for r in range(constants.BOARD_SIZE):
            for c in range(constants.BOARD_SIZE):
                if board[r][c] == player:
                    score += constants.WEIGHTS[r][c]
        return score

    # 静的評価関数（evaluate_board）を使って最良の手を選択
    def get_best_move(self, player):
        moves = self.game_logic.get_valid_moves(player) # valid_movesを取得
        if not moves:
            return None
    
        best_score = float('-inf')
        best_move = None

        for r, c in moves:
            # 一時的に盤面をコピーして、その手を仮に打ってみる
            temp_board = [row[:] for row in self.game_logic.board] # boardを参照
            self.game_logic.place_disc(r, c, player, temp_board)
            score = self.evaluate_board(temp_board, player) # 評価関数を呼び出し

            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    # ランダムに1手選んで石を置く処理
    def computer_move(self):
        # global current_player
        best = self.get_best_move(constants.WHITE_DISC) # コンピュータ(白)の最良手を選択
        if best:
            row, col = best
            self.game_logic.place_disc(row, col, constants.WHITE_DISC) # ゲームロジックで石を置く
            self.game_logic.current_player = constants.BLACK_DISC # プレイヤーを黒に変更