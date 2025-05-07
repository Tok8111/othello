import pygame
import sys
from constants import constants
from GameLogic import GameLogic
from AIPlayer import AIPlayer
from BoardRenderer import BoardRenderer
from GameController import GameController

def main():
    # 初期化
    pygame.init()
    screen = pygame.display.set_mode((constants.WINDOW_SIZE, constants.TOTAL_HEIGHT))
    pygame.display.set_caption('Othello - Turn Based')
    clock = pygame.time.Clock()

    # クラスのインスタンス生成
    game_logic = GameLogic()
    ai_player = AIPlayer(game_logic)
    renderer = BoardRenderer(screen, game_logic)
    controller = GameController(game_logic, ai_player, renderer)

    # ゲームループ開始
    controller.run_game_loop(screen)

    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()