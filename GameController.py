# ゲーム進行の管理（入力処理、手番の切り替え、状態管理）

import pygame
import sys
from constants import constants

class GameController:

    def __init__(self, game_logic, ai_player, renderer):
        self.game_logic = game_logic
        self.ai_player = ai_player
        self.renderer = renderer
        self.current_player = constants.BLACK_DISC
        self.running = True
        self.ai_wait_time = None # AIのウェイト時間管理用

    # プレイヤーが盤面をクリックした時の処理（黒プレイヤーの手番であれば、クリック位置に石を置く）
    def handle_click(self, pos):
        if self.current_player != constants.BLACK_DISC:
            return
    
        col = pos[0] // constants.CELL_SIZE
        row = pos[1] // constants.CELL_SIZE

        if self.game_logic.is_valid_move(row, col, constants.BLACK_DISC):
            self.game_logic.place_disc(row, col, constants.BLACK_DISC)
            self.switch_player()
    
    # プレイヤーの手番切り替え処理（AIの手もここで処理）（石を打てない場合は、パス）
    def switch_player(self):
        if not self.running:
            return

        # 両者ともに打てない場合は、ゲーム終了
        if not self.game_logic.has_valid_moves(constants.BLACK_DISC) and not self.game_logic.has_valid_moves(constants.WHITE_DISC):
            self.running = False
            return

        if self.current_player == constants.BLACK_DISC: # 黒の手番の時
            if self.game_logic.has_valid_moves(constants.WHITE_DISC): # 黒が打てない場合
                self.current_player = constants.WHITE_DISC # 白のターンに戻る
                self.ai_wait_time = pygame.time.get_ticks() # AIターンの開始時刻
        else: # 白の手番の時
            if self.game_logic.has_valid_moves(constants.BLACK_DISC): # 白が打てない場合
                self.current_player = constants.BLACK_DISC # 白が打てない場合は、黒のターンに戻る


    # 白番(AI)のターン処理
    def handle_ai_turn(self):
        if self.current_player != constants.WHITE_DISC:
            return
       
        if not self.ai_wait_time:
            self.ai_wait_time = pygame.time.get_ticks()

        elapsed = pygame.time.get_ticks() - self.ai_wait_time

        if elapsed > 500: # 500ms待ってから、AIが石を置く
            ai_move = self.ai_player.get_best_move(constants.WHITE_DISC)
            if ai_move:
                self.game_logic.place_disc(ai_move[0], ai_move[1], constants.WHITE_DISC)
            self.switch_player()
            self.ai_wait_time = None

    # ゲームループ実行（イベント処理と描画）
    def run_game_loop(self, screen):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.handle_click(pygame.mouse.get_pos())
            
            # 毎フレーム AI のターンかどうかをチェックして、手を打たせる
            self.handle_ai_turn()

            self.renderer.draw_board()
            self.renderer.draw_discs()
            self.renderer.draw_score()
            pygame.display.flip()

            # ゲーム終了判定（pygameに勝敗を表示して終了）
            result = self.game_logic.check_game_end()

            if result:
                font = pygame.font.SysFont(None, 48)
                text = font.render(result, True, (255, 0, 0)) # 赤色の文字
                # screen.fill((0, 0, 0)) # 画面をクリア
                screen.blit(text, (constants.WINDOW_SIZE // 2 - 100, constants.TOTAL_HEIGHT // 2 - 20))
                pygame.display.flip()
                pygame.time.wait(5000) # 5秒間表示してから終了
                pygame.quit()
                sys.exit() # ゲームを終了する

    # ゲームを初期状態にリセットし、手番を黒にする
    def reset_game(self):
        self.game_logic.reset_board()
        self.current_player = constants.BLACK_DISC
        self.ai_wait_time = None