from colorama import Fore, Back
from collections import deque


class Colors:
    red_system = Fore.RED + Back.BLACK  # for wrong input
    blue_system = Fore.BLUE + Back.BLACK  # for entering input
    red = Fore.RED  # for circle
    blue = Fore.BLUE  # for cross
    green = Fore.GREEN  # for player mark coloring
    yellow = Fore.YELLOW  # for player mark coloring
    black = Fore.BLACK  # for player mark coloring
    magenta = Fore.MAGENTA  # for player mark coloring
    cyan = Fore.CYAN  # for player mark coloring
    white = Fore.WHITE  # for player mark coloring


def player_details():
    players_que = deque()

    for player_num in range(1, 3):  # game is playable for exact two players
        player = input(Colors.blue_system + f'Player {player_num} please enter your screen name >>> ')

        while player in players_que:
            player = input(Colors.red_system + f'{player} is already taken, please choose another one >>> ')

        players_que.append(player)

    return players_que


def initial_matrix():
    # Anywhen will be used this dimensions, the standard of this game

    matrix_rows = 3
    matrix_cols = 3

    print(Colors.yellow + 'This is the numeric board representation:')
    for row in range(matrix_rows):
        for col in range(matrix_cols):
            print(Colors.green + '| ' + Colors.red + f'{(row * matrix_rows) + (col + 1)} ', end='')
        print(Colors.green + '|')


def check_for_win(current_matrix, current_symbol):
    possible_winning_positions = (
        (1, 0),
        (1, 1),
        (1, - 1),
        (0, 1),
        (0, - 1),
        (- 1, - 1),
        (- 1, 0),
        (-1, 1)
    )

    for current_row_index in range(3):
        for current_col_index in range(3):
            if current_matrix[current_row_index][current_col_index] != current_symbol:
                continue

            for current_direction in possible_winning_positions:
                row_move, col_move = current_direction
                next_row = current_row_index + row_move
                next_col = current_col_index + col_move

                for wining_streak in range(2):
                    if next_row < 0 or next_row >= 3 or next_col < 0 or next_col >= 3:
                        break

                    if current_matrix[next_row][next_col] != current_symbol:
                        break

                    next_row += row_move
                    next_col += col_move

                else:
                    return True

    else:
        return False


def gameplay(players_names):
    starting_player = players_names[0]
    matrix = [[' ' for _ in range(3)] for _ in range(3)]  # the empty cells will be notated with space
    available_position_on_desk = [int(i) for i in range(1, 10)]
    available_marks = [Colors.red + 'X', Colors.blue + 'O']

    print(Colors.blue_system + f'{starting_player}' + Colors.green + ' starts first')
    player_mark = input(Colors.blue_system + f'{starting_player}, ' + Colors.green + f'please choose on of the following marks: {", ".join(available_marks)} >>> ')

    while player_mark.lower() != 'x' and player_mark.lower() != 'o':
        player_mark = input(Colors.red_system + f'{starting_player}, ' + Colors.green + f'"{player_mark}" not valid, please choose on of the following marks: {", ".join(available_marks)} >>> ')

    players_dict = {starting_player: player_mark}
    second_player = players_names[1]

    if player_mark == 'x':
        second_player_mark = 'O'

    else:
        second_player_mark = 'X'

    players_dict[second_player] = second_player_mark

    winner = False

    initial_matrix()

    while not winner:
        player_on_turn = players_names.popleft()
        players_names.append(player_on_turn)
        valid_command = False
        chosen_cell = 0

        while not valid_command:

            try:
                chosen_cell = int(input(Colors.blue_system + f'{player_on_turn}' + Colors.yellow + ', please select a free position from 1 to 9 >>> '))

            except ValueError:
                print(Colors.red_system + f'{player_on_turn} you do not enter a valid number!')
                continue

            if 0 > chosen_cell or chosen_cell > 9:
                print(Colors.red_system + f'{player_on_turn} you do not enter a valid number!')
                continue

            elif chosen_cell not in available_position_on_desk:
                print(Colors.red_system + f'{player_on_turn} this position is already occupied!')
                continue

            else:
                available_position_on_desk.remove(chosen_cell)
                valid_command = True

        chosen_cell_index = chosen_cell - 1  # because of index starting from zero
        chosen_row = chosen_cell_index // 3
        chosen_col = chosen_cell_index % 3

        current_player_mark = players_dict[player_on_turn]

        matrix[chosen_row][chosen_col] = current_player_mark

        for row in matrix:
            for col in row:
                if col.lower() == 'x':
                    print(Colors.green + '| ' + Colors.red + f'{col} ', end='')
                elif col.lower() == 'o':
                    print(Colors.green + '| ' + Colors.blue + f'{col} ', end='')
                else:
                    print(Colors.green + '| ' + Colors.green + f'{col} ', end='')
            print(Colors.green + '|')

        winner = check_for_win(matrix, current_player_mark)

        if winner:
            print(Colors.cyan + f'{player_on_turn}' + Colors.yellow + ' congrats, you just take an incredible victory!!!')
            break

        elif not available_position_on_desk:
            print(Colors.magenta + 'The game ended as draw!')
            break


player_deque = player_details()
gameplay(player_deque)
