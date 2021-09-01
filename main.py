import pygame, sys, copy
from get_board import new_board
from sudoku_solver import _solve

board = new_board()
second = copy.deepcopy(board)
solu_board = copy.deepcopy(board)
_solve(solu_board)

text_r = [[], [], [], [], [], [], [], [], []]

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


def draw_grid(grid, org):
    x_const = 0
    y_const = 0
    for i in range(9):
        for j in range(9):

            text_r[i].append(pygame.Rect(305+(j * 67)+x_const, 5+(i * 67)+y_const, 67, 67))
            if (j + 1) % 3 == 0:
                x_const += 5
            else:
                x_const += 1
            center = list(text_r[i][j].center)
            center[0] -= 5
            center[1] -= 15

            if org[i][j] == 0:
                pygame.draw.rect(screen, (211, 211, 211), text_r[i][j])
            else:
                pygame.draw.rect(screen, (255, 255, 255), text_r[i][j])

            if grid[i][j] != 0:
                screen.blit(game_font.render(str(grid[i][j]), False, (0)), center)

            if second[i][j] == 0:
                if grid[i][j] != 0 and grid[i][j] == solu_board[i][j]:
                    screen.blit(game_font.render(str(grid[i][j]), False, (0)), center)
                elif grid[i][j] != 0 and grid[i][j] != solu_board[i][j]:
                    screen.blit(game_font.render(str(grid[i][j]), False, (255,0,0)), center)

        if (i+1) % 3 == 0:
            y_const += 5
        else:
            y_const += 1
        x_const = 0


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
    draw_grid(board, second)
    if not over:
        screen.blit(game_font.render(time, False, (0)), (100, 280))
    else:
        screen.blit(game_font.render(time, False, (124, 252, 0)), (40, 280))

    if left_click:

        if easy_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'easy'
            board = new_board()
            timer_started = False
            comp_solved = False
            second = copy.deepcopy(board)
            left_click = False

        elif medium_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'medium'
            board = new_board(2)
            timer_started = False
            comp_solved = False
            second = copy.deepcopy(board)
            left_click = False

        elif hard_mode.collidepoint(mx, my):
            editable = True
            over = False
            mode = 'hard'
            timer_started = False
            comp_solved = False
            board = new_board(3)
            second = copy.deepcopy(board)
            left_click = False

        elif restart.collidepoint(mx, my):
            editable = True
            over = False
            board = copy.deepcopy(second)
            comp_solved = False
            timer_started = False
            left_click = False

        elif exit_game.collidepoint(mx, my):
            pygame.quit()
            sys.exit()

        elif solve.collidepoint(mx, my):
            #TODO: Show whats going on in solve
            comp_solved = True
            board = solu_board
            left_click = False

        else:
            for i in range(9):
                for j in range(9):
                    if editable and second[i][j] == 0 and text_r[i][j].collidepoint(mx, my):
                        if not timer_started:
                            start_time = pygame.time.get_ticks()
                            milliseconds = 0
                            minutes = 0
                            seconds = 0
                            hours = 0
                            timer_started = True

                        if a_key:
                            board[i][j] = key
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

    if board == solu_board and not comp_solved:
        over = True
        time = 'Solved in: ' + last_time
        editable = False

    pygame.display.flip()
