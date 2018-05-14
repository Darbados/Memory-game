# the imports
import pygame
import random
from itertools import product
from pygame.locals import *
from pygame.color import Color


class MemoryGame(object):

    # the constants
    FPS = 30
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    SQUARE_GAP = 10


    # the icon_formss
    DIAMOND = 'diamond'
    SQUARE = 'square'
    TRIANGLE = 'triangle'
    CIRCLE = 'circle'

    SURFACE_COLOR = Color('white')

    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.SQUARE_SIZE = (80 if (self.board_height <= 4 and self.board_height <= 4) else 40)
        self.X_MARGIN = (MemoryGame.SCREEN_WIDTH - (self.board_width * (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP))) // 2
        self.Y_MARGIN = (MemoryGame.SCREEN_HEIGHT - (self.board_height * (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP))) // 2

    # the main function
    def main(self):
        global screen, clock
        pygame.font.init()
        font = pygame.font.SysFont("arial", 22)
        player1_score, player2_score = 0, 0
        player1_turn = random.sample([True, False], 1)
        player2_turn = not player1_turn

        pygame.init()

        screen = pygame.display.set_mode((MemoryGame.SCREEN_WIDTH, MemoryGame.SCREEN_HEIGHT))
        pygame.display.set_caption('MEMORY')

        clock = pygame.time.Clock()

        icon_forms = (MemoryGame.DIAMOND, MemoryGame.SQUARE, MemoryGame.TRIANGLE, MemoryGame.CIRCLE)
        colors = (Color('cyan'), Color('magenta'), Color('gray'), Color('chocolate'))

        # There should be enough symbols
        assert len(icon_forms) * len(colors) >= self.board_height * self.board_width // 2, 'There are not sufficient icons'

        board = self.get_random_board(icon_forms, colors)
        revealed = [[False] * self.board_width for ii in range(self.board_height)]  # keeps track of visibility of square

        mouse_x = None
        mouse_y = None
        mouse_clicked = False
        first_selection = None

        running = True
        self.start_game_animation(board)

        while running:
            screen.fill(MemoryGame.SURFACE_COLOR)
            self.draw_board(board, revealed)
            self.draw_players(player1_score, player2_score, font, self.all_revealed(revealed), player1_turn)

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    running = False
                elif event.type == MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    mouse_clicked = True

            x, y = self.get_pos(mouse_x, mouse_y)

            if x is not None and y is not None:
                if not revealed[x][y]:
                    if mouse_clicked:
                        revealed[x][y] = True
                        self.draw_square(board, revealed, x, y)

                        if first_selection is None:
                            first_selection = (x, y)
                        else:
                            pygame.time.wait(1000)
                            if board[x][y] != board[first_selection[0]][first_selection[1]]:
                                revealed[x][y] = False
                                revealed[first_selection[0]][first_selection[1]] = False

                                player1_turn = not player1_turn
                                player2_turn = not player2_turn

                            else:
                                if player1_turn:
                                    player1_score += 1
                                    player1_turn = not player1_turn
                                    player2_turn = not player2_turn
                                else:
                                    player2_score += 1
                                    player1_turn = not player1_turn
                                    player2_turn = not player2_turn

                            pygame.display.update()
                            self.draw_players(player1_score, player2_score, font, self.all_revealed(revealed), player1_turn)
                            first_selection = None

                        if self.all_revealed(revealed):
                            pygame.time.wait(500)
                            self.game_won_animation(board, revealed)

                            player1_score, player2_score = 0, 0
                            player1_turn = random.sample([True, False], 1)[0]
                            player2_turn = not player1_turn

                            board = self.get_random_board(icon_forms, colors)
                            revealed = [[False] * self.board_width for rev in range(self.board_height)]

                            self.draw_players(player1_score, player2_score, font, self.all_revealed(revealed), player1_turn)
                            self.start_game_animation(board)

                    else:
                        self.draw_select_square(x, y)

            mouse_clicked = False
            pygame.display.update()

    def all_revealed(self, revealed):
        # Check for won game.
        return all(all(x) for x in revealed)

    def game_won_animation(self, board, revealed):
        color1 = Color('cyan')
        color2 = MemoryGame.SURFACE_COLOR
        for i in range(10):
            color1, color2 = color2, color1
            screen.fill(color1)
            self.draw_board(board, revealed)
            pygame.display.update()
            pygame.time.wait(300)

    def start_game_animation(self, board):
        # The function that shows all icon_formss under the squares

        coordinates = list(product(range(self.board_height), range(self.board_width)))
        random.shuffle(coordinates)

        revealed = [[False] * self.board_width for i in range(self.board_height)]

        screen.fill(MemoryGame.SURFACE_COLOR)
        self.draw_board(board, revealed)
        pygame.display.update()
        pygame.time.wait(250)

        for sz in range(0, self.board_height * self.board_width, 5):
            l = coordinates[sz: sz + 5]
            for x in l:
                revealed[x[0]][x[1]] = True
                self.draw_square(board, revealed, *x)
            pygame.time.wait(250)
            for x in l:
                revealed[x[0]][x[1]] = False
                self.draw_square(board, revealed, *x)

    def get_random_board(self, icon_forms, colors):
        # This function draws the actual bord with icon_formss which stays beneath the mask squares.

        icons = list(product(icon_forms, colors))
        num_icons = self.board_height * self.board_width // 2
        icons = icons[:num_icons] * 2

        random.shuffle(icons)
        board = [icons[i:i + self.board_width] for i in range(0, self.board_height * self.board_width, self.board_width)]
        return board

    def get_coordinates(self, x, y):
        # Gets the coordinates of particular square.

        top = self.X_MARGIN + y * (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP)
        left = self.Y_MARGIN + x * (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP)
        return top, left

    def draw_icon(self, icon, x, y):
        # The actual draw icon's function.

        px, py = self.get_coordinates(x, y)
        if icon[0] == MemoryGame.DIAMOND:
            pygame.draw.polygon(screen, icon[1],
                                ((px + self.SQUARE_SIZE // 2, py + 5), (px + self.SQUARE_SIZE - 5, py + self.SQUARE_SIZE // 2),
                                 (px + self.SQUARE_SIZE // 2, py + self.SQUARE_SIZE - 5), (px + 5, py + self.SQUARE_SIZE // 2)))
        elif icon[0] == MemoryGame.SQUARE:
            pygame.draw.rect(screen, icon[1],
                             (px + 5, py + 5, self.SQUARE_SIZE - 10, self.SQUARE_SIZE - 10))
        elif icon[0] == MemoryGame.TRIANGLE:
            pygame.draw.polygon(screen, icon[1],
                                ((px + self.SQUARE_SIZE // 2, py + 5), (px + 5, py + self.SQUARE_SIZE - 5),
                                 (px + self.SQUARE_SIZE - 5, py + self.SQUARE_SIZE - 5)))
        elif icon[0] == MemoryGame.CIRCLE:
            pygame.draw.circle(screen, icon[1],
                               (px + self.SQUARE_SIZE // 2, py + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 2 - 5)

    def get_pos(self, cx, cy):
        # Store the square x,y coordinates.

        if cx < self.X_MARGIN or cy < self.Y_MARGIN:
            return None, None

        x = (cy - self.Y_MARGIN) // (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP)
        y = (cx - self.X_MARGIN) // (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP)

        if x >= self.board_height or y >= self.board_width or (cx - self.X_MARGIN) % (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP) > self.SQUARE_SIZE or (cy - self.Y_MARGIN) % (self.SQUARE_SIZE + MemoryGame.SQUARE_GAP) > self.SQUARE_SIZE:
            return None, None
        else:
            return x, y

    def draw_square(self, board, revealed, x, y):
        # The square draw function.

        coordinates = self.get_coordinates(x, y)
        square_rect = (*coordinates, self.SQUARE_SIZE, self.SQUARE_SIZE)
        pygame.draw.rect(screen, MemoryGame.SURFACE_COLOR, square_rect)

        if revealed[x][y]:
            self.draw_icon(board[x][y], x, y)
        else:
            pygame.draw.rect(screen, Color('green'), square_rect)
        pygame.display.update(square_rect)

    def draw_board(self, board, revealed):
        # This function draws all squares in the board.

        for x in range(self.board_height):
            for y in range(self.board_width):
                self.draw_square(board, revealed, x, y)

    def draw_select_square(self, x, y):
        # Simulate the mouse over effect, i.e. the nice black outline.

        pos_x, pos_y = self.get_coordinates(x, y)
        pygame.draw.rect(screen, Color('black'), (pos_x - 3, pos_y - 3, self.SQUARE_SIZE + 7, self.SQUARE_SIZE + 7), 3)

    def draw_players(self, p1_score, p2_score, font_obj, game_won, player_to_make_turn):
        # Function to draw the players score and turn. It fails to display the final victory, unknown why...

        player1_label = font_obj.render("Player 1 score: {0} {1}".format(p1_score, (" ---> Your turn" if player_to_make_turn else "")), 1, (0, 0, 0))
        player2_label = font_obj.render("Player 2 score: {0} {1}".format(p2_score, (" ---> Your turn" if not player_to_make_turn else "")), 1, (0, 0, 0))
        screen.blit(player1_label, (100, 25))
        screen.blit(player2_label, (100, 50))

        if p1_score > p2_score:
            player1_won = font_obj.render("At this moment player 1 wins the game with score: {0}:{1}".format(p1_score, p2_score), 1, (0, 0, 0))
            screen.blit(player1_won, (100, 75))
        elif p1_score < p2_score:
            player2_won = font_obj.render("At this moment player 2 wins the game with score: {0}:{1}".format(p2_score, p1_score), 1, (0, 0, 0))
            screen.blit(player2_won, (100, 75))
        else:
            draw_game = font_obj.render("No winner, the game is even: {0}:{1}".format(p1_score, p2_score), 1, (0, 0, 0))
            screen.blit(draw_game, (100, 75))


if __name__ == '__main__':
    metric_x = input("Enter a number for boxes to have horizontal.")
    metric_y = input("Enter a number for boxes to have vertically.")

    while not (int(metric_x)*int(metric_y))%2 == 0:
        metric_x = input("Enter a number for boxes to have horizontal.")
        metric_y = input("Enter a number for boxes to have vertically.")

    game = MemoryGame(int(metric_x),int(metric_y))
    game.main()