# 描画系の処理（UI）を専任で行う
import pygame
from constants import constants

class BoardRenderer:

    def __init__(self, screen, game_logic):
        self.screen = screen
        self.game_logic = game_logic

    # 盤面のマス目を描画(8×8)
    def draw_board(self):
        self.screen.fill(constants.BG_COLOR)
        for r in range(constants.BOARD_SIZE):
            for c in range(constants.BOARD_SIZE):
                rect = pygame.Rect(c * constants.CELL_SIZE, r * constants.CELL_SIZE, constants.CELL_SIZE, constants.CELL_SIZE)
                pygame.draw.rect(self.screen, constants.LINE_COLOR, rect, 1)

    # 盤面上にある石（黒、白）の描画
    def draw_discs(self):
        board = self.game_logic.board
        for row in range(constants.BOARD_SIZE):
            for col in range(constants.BOARD_SIZE):
                if board[row][col] is not None:
                    color = constants.BLACK if board[row][col] == constants.BLACK_DISC else constants.WHITE
                    center = (col * constants.CELL_SIZE + constants.CELL_SIZE // 2, row * constants.CELL_SIZE + constants.CELL_SIZE // 2)
                    pygame.draw.circle(self.screen, color, center, constants.CELL_SIZE // 2 - 5)

    # 現在のスコア（石の数（黒・白））表示
    def draw_score(self):
        black, white = self.game_logic.count_discs()
        font = pygame.font.SysFont(None, 36)
        text = font.render(f'Black: {black} White: {white}', True, constants.WHITE)
        self.screen.blit(text, (20, constants.WINDOW_SIZE + 10))