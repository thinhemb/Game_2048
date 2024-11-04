# build 2048 in python using pygame!!
import pygame
import random

from config import *
from utils import read_high_score

class Game_2048():
    def __init__(self):
        
        pygame.init()
        # initial set up

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('2048')
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        # game variables initialize
        self.board_values = [[0 for _ in range(4)] for _ in range(4)]
        self.game_over = False
        self.spawn_new = True
        self.init_count = 0
        self.direction = ''
        self.score = 0
        self.init_high = read_high_score()
        self.high_score = self.init_high


    # draw game over and restart text
    def draw_over(self):
        pygame.draw.rect(self.screen, 'black', [50, 50, 300, 100], 0, 10)
        game_over_text1 = self.font.render('Game Over!', True, 'white')
        game_over_text2 = self.font.render('Press Enter to Restart', True, 'white')
        self.screen.blit(game_over_text1, (130, 65))
        self.screen.blit(game_over_text2, (70, 105))


    # take your turn based on direction
    def take_turn(self,direc, board):
        global score
        merged = [[False for _ in range(4)] for _ in range(4)]
        if direc == 'UP':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    if i > 0:
                        for q in range(i):
                            if board[q][j] == 0:
                                shift += 1
                        if shift > 0:
                            board[i - shift][j] = board[i][j]
                            board[i][j] = 0
                        if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                                and not merged[i - shift - 1][j]:
                            board[i - shift - 1][j] *= 2
                            self.score += board[i - shift - 1][j]
                            board[i - shift][j] = 0
                            merged[i - shift - 1][j] = True

        elif direc == 'DOWN':
            for i in range(3):
                for j in range(4):
                    shift = 0
                    for q in range(i + 1):
                        if board[3 - q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[2 - i + shift][j] = board[2 - i][j]
                        board[2 - i][j] = 0
                    if 3 - i + shift <= 3:
                        if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                                and not merged[2 - i + shift][j]:
                            board[3 - i + shift][j] *= 2
                            self.score += board[3 - i + shift][j]
                            board[2 - i + shift][j] = 0
                            merged[3 - i + shift][j] = True

        elif direc == 'LEFT':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][j - shift] = board[i][j]
                        board[i][j] = 0
                    if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                            and not merged[i][j - shift]:
                        board[i][j - shift - 1] *= 2
                        self.score += board[i][j - shift - 1]
                        board[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

        elif direc == 'RIGHT':
            for i in range(4):
                for j in range(4):
                    shift = 0
                    for q in range(j):
                        if board[i][3 - q] == 0:
                            shift += 1
                    if shift > 0:
                        board[i][3 - j + shift] = board[i][3 - j]
                        board[i][3 - j] = 0
                    if 4 - j + shift <= 3:
                        if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                                and not merged[i][3 - j + shift]:
                            board[i][4 - j + shift] *= 2
                            self.score += board[i][4 - j + shift]
                            board[i][3 - j + shift] = 0
                            merged[i][4 - j + shift] = True
        return board


    # spawn in new pieces randomly when turns start
    @staticmethod
    def new_pieces(board):
        count = 0
        full = False
        while any(0 in row for row in board) and count < 1:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board[row][col] == 0:
                count += 1
                if random.randint(1, 10) == 10:
                    board[row][col] = 4
                else:
                    board[row][col] = 2
        if count < 1:
            full = True
        return board, full


    # draw background for the board
    def draw_board(self):
        pygame.draw.rect(self.screen, colors['bg'], [0, 0, 400, 400], 0, 10)
        score_text = self.font.render(f'Score: {self.score}', True, 'black')
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, 'black')
        self.screen.blit(score_text, (10, 410))
        self.screen.blit(high_score_text, (10, 450))
        pass


    # draw tiles for game
    def draw_pieces(self,board):
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value > 8:
                    value_color = colors['light text']
                else:
                    value_color = colors['dark text']
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors['other']
                pygame.draw.rect(self.screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                    self.screen.blit(value_text, text_rect)
                    pygame.draw.rect(self.screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

    def start(self):
        # main game loop
        run = True
        while run:
            self.timer.tick(fps)
            self.screen.fill('gray')
            self.draw_board()
            self.draw_pieces(self.board_values)

            if self.direction != '':
                self.board_values = self.take_turn(self.direction, self.board_values)
                self.direction = ''
                self.spawn_new = True
                
            if self.spawn_new or self.init_count < 2:
                self.board_values, game_over = self.new_pieces(self.board_values)
                self.spawn_new = False
                self.init_count += 1
            if game_over:
                self.draw_over()
                if self.high_score > self.init_high:
                    file = open('high_score', 'w')
                    file.write(f'{self.high_score}')
                    file.close()
                    self.nit_high = self.high_score

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 'RIGHT'

                    if game_over:
                        if event.key == pygame.K_RETURN:
                            self.board_values = [[0 for _ in range(4)] for _ in range(4)]
                            self.spawn_new = True
                            self.init_count = 0
                            self.score = 0
                            self.direction = ''
                            self.game_over = False

            if self.score > self.high_score:
                self.high_score = self.score

            pygame.display.flip()
        pygame.quit()


if __name__ =='__main__':
    game = Game_2048()
    game.start()
