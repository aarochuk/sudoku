import pygame, sys, copy
import requests
from time import sleep

def new_board(diff=1):
    board = requests.get(f'https://sudoku--api.herokuapp.com/new-board?diff={diff}').json()['response']['unsolved-sudoku']

    return board


class Sudoku():
    def __init__(self, diff=1):
        self.org = new_board(diff)
        self.second = copy.deepcopy(self.org)
        self.solu_board = copy.deepcopy(self.org)
        self._solve()

        self.text_r = [[], [], [], [], [], [], [], [], []]

    def find_next(self):
        for y in range(9):
            for x in range(9):
                if self.solu_board[y][x] == 0:
                    return y, x
        return None

    def valid(self, n, y, x):
        for i in range(9):
            if self.solu_board[y][i] == n:
                return False
        for i in range(9):
            if self.solu_board[i][x] == n:
                return False
        x_ = (x // 3) * 3
        y_ = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.solu_board[y_ + i][x_ + j] == n:
                    return False
        return True

    def _solve(self):
        find = self.find_next()
        if find:
            col, row = find
        else:
            return True
        for i in range(1, 10):
            if self.valid(i, col, row):
                self.solu_board[col][row] = i
                if self._solve():
                    return True
                self.solu_board[col][row] = 0
        return

    def fn(self):
        for y in range(9):
            for x in range(9):
                if self.org[y][x] == 0:
                    return y, x
        return None

    def v(self, n, y, x):
        for i in range(9):
            if self.org[y][i] == n:
                return False
        for i in range(9):
            if self.org[i][x] == n:
                return False
        x_ = (x // 3) * 3
        y_ = (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.org[y_ + i][x_ + j] == n:
                    return False
        return True

    def _s(self):
        find = self.fn()
        if find:
            col, row = find
        else:
            return True
        for i in range(1, 10):
            if self.v(i, col, row):
                self.org[col][row] = i
                pygame.time.delay(60)
                self.draw_grid()
                if self._s():
                    return True
                self.org[col][row] = 0
                pygame.time.delay(60)
                self.draw_grid()
        return

    def restart(self):
        self.org = copy.deepcopy(self.second)

    def draw_grid(self):
        x_const = 0
        y_const = 0
        for i in range(9):
            for j in range(9):

                self.text_r[i].append(pygame.Rect(305 + (j * 67) + x_const, 5 + (i * 67) + y_const, 67, 67))
                if (j + 1) % 3 == 0:
                    x_const += 5
                else:
                    x_const += 1
                center = list(self.text_r[i][j].center)
                center[0] -= 5
                center[1] -= 15

                if board.second[i][j] == 0:
                    pygame.draw.rect(screen, (211, 211, 211), self.text_r[i][j])
                else:
                    pygame.draw.rect(screen, (255, 255, 255), self.text_r[i][j])

                if board.org[i][j] != 0:
                    screen.blit(game_font.render(str(self.org[i][j]), False, (0)), center)

                if board.second[i][j] == 0:
                    if self.org[i][j] != 0 and self.org[i][j] == self.solu_board[i][j]:
                        screen.blit(game_font.render(str(self.org[i][j]), False, (0)), center)
                    elif board.org[i][j] != 0 and board.org[i][j] != self.solu_board[i][j]:
                        screen.blit(game_font.render(str(self.org[i][j]), False, (255, 0, 0)), center)

            if (i + 1) % 3 == 0:
                y_const += 5
            else:
                y_const += 1
            x_const = 0
        pygame.display.flip()


pygame.init()

pygame.display.set_caption("Sudoku!")
screen = pygame.display.set_mode((930, 630))
screen.fill(0)

game_font = pygame.font.Font("font.ttf", 28)
win_font = pygame.font.Font("font.ttf", 20)

settings = pygame.Rect(0, 0, 300, 630)
easy_mode = pygame.Rect(20, 30, 260, 60)
medium_mode = pygame.Rect(20, 110, 260, 60)
hard_mode = pygame.Rect(20, 190, 260, 60)
restart = pygame.Rect(20, 340, 260, 60)
solve = pygame.Rect(20, 420, 260, 60)
exit_game = pygame.Rect(20, 500, 260, 60)

board = Sudoku()

def draw_menu(mode='easy'):
    pygame.draw.rect(screen, (255, 255, 255), settings)

    if mode == 'easy':
        select_box = pygame.Rect(18, 28, 264, 64)
        pygame.draw.rect(screen, (0), select_box, border_radius=3)
    pygame.draw.rect(screen, (124, 252, 0), easy_mode, border_radius=3)
    easy = game_font.render("easy", False, (0))
    screen.blit(easy, (129, 45))

    if mode == 'medium':
        select_box = pygame.Rect(18, 108, 264, 64)
        pygame.draw.rect(screen, (0), select_box, border_radius=3)
    pygame.draw.rect(screen, (255, 255, 0), medium_mode, border_radius=3)
    medium = game_font.render("medium", False, (0))
    screen.blit(medium, (114, 125))

    if mode == 'hard':
        select_box = pygame.Rect(18, 188, 264, 64)
        pygame.draw.rect(screen, (0), select_box, border_radius=3)
    pygame.draw.rect(screen, (250, 0, 0), hard_mode, border_radius=3)
    hard = game_font.render("hard", False, (0))
    screen.blit(hard, (129, 205))

    pygame.draw.rect(screen, (123, 104, 238), restart, border_radius=3)
    restart_ = game_font.render("restart", False, (0))
    screen.blit(restart_, (110, 355))
    pygame.draw.rect(screen, (255, 165, 0), solve, border_radius=3)
    solve_ = game_font.render("solve", False, (0))
    screen.blit(solve_, (125, 435))
    pygame.draw.rect(screen, (0, 191, 255), exit_game, border_radius=3)
    exit_ = game_font.render("exit", False, (0))
    screen.blit(exit_, (129, 515))


time = "00:00:00"
mode = 'easy'

left_click = False
right_click = False

timer_started = False

milliseconds = 0
seconds = 0
minutes = 0
hours = 0

a_key = False
key = 0
comp_solved = False
over = False

editable = True
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Checks if the user quit the game
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True
                mx, my = pygame.mouse.get_pos()

            if event.button == 3:
                guess = True
                mx, my = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            a_key = True
            key = event.key % 48 if event.key >= 48 and event.key <= 58 else 0

    draw_menu(mode)
    if not over:
        screen.blit(game_font.render(time, False, (0)), (100, 280))
    else:
        screen.blit(game_font.render(time, False, (124, 252, 0)), (40, 280))

    if left_click:

        if easy_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'easy'
            board = Sudoku()
            timer_started = False
            comp_solved = False
            left_click = False


        elif medium_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'medium'
            board = Sudoku(2)
            timer_started = False
            comp_solved = False
            left_click = False


        elif hard_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'hard'
            timer_started = False
            comp_solved = False
            board = Sudoku(3)
            left_click = False

        elif restart.collidepoint(mx, my):
            editable = True
            over = False
            board.restart()
            comp_solved = False
            timer_started = False
            left_click = False

        elif exit_game.collidepoint(mx, my):
            pygame.quit()
            sys.exit()

        elif solve.collidepoint(mx, my):
            editable = False
            board._s()
            left_click = False
            a_key = False
            key = 0
            timer_started = False

        elif not editable:
            key = 0

        else:
            for i in range(9):
                for j in range(9):
                    if editable and board.second[i][j] == 0 and board.text_r[i][j].collidepoint(mx, my):
                        if not timer_started:
                            start_time = pygame.time.get_ticks()
                            milliseconds = 0
                            minutes = 0
                            seconds = 0
                            hours = 0
                            timer_started = True

                        if a_key:
                            board.org[i][j] = key
                            a_key = False
                            key = 0

    if timer_started and not over:
        milliseconds = pygame.time.get_ticks() - start_time

        if milliseconds >= 1000:
            seconds = milliseconds//1000

        if seconds >= 60:
            minutes = seconds // 60
            seconds %= 60

        if minutes >= 60:
            hours = minutes // 60
            minutes %= 60

        if hours == 23 and minutes == 59 and seconds == 60:
            milliseconds = 0

        dis_hour = str(hours) if len(str(hours)) == 2 else '0' + str(hours)
        dis_minute = str(minutes) if len(str(minutes)) == 2 else '0' + str(minutes)
        dis_second = str(seconds) if len(str(seconds)) == 2 else '0' + str(seconds)

        time = f'{dis_hour}:{dis_minute}:{dis_second}'
        last_time = copy.deepcopy(time)
    else:
        time = f'00:00:00'

    if board == board.solu_board and not comp_solved:
        over = True
        time = 'Solved in: ' + last_time
        editable = False

    board.draw_grid()

