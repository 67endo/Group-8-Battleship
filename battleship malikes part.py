"""
battleship.py
The classic board game battleship
Erin, Aniel, and Malik
"""

import random

rowNames = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
board_size = 10

# ship name, id, length
ships = [
    ("Carrier", 1, 5),
    ("Battleship", 2, 4),
    ("Destroyer", 3, 3),
    ("Submarine", 4, 3),
    ("Patrol Boat", 5, 2),
]


# makes a blank board
# each cell is [shot_fired, ship_id]
def create_board():
    board = {}
    for row in rowNames:
        board[row] = []
        for col in range(board_size):
            board[row].append([False, 0])
    return board


# maliks stuff below

def fire_shot(target_board, row, col):
    # already shot here?
    if target_board[row][col][0] == True:
        return "already shot"
    
    target_board[row][col][0] = True
    
    if target_board[row][col][1] != 0:
        return "hit"
    else:
        return "miss"


def check_sunk(target_board, ship_id):
    for row in rowNames:
        for col in range(board_size):
            if target_board[row][col][1] == ship_id:
                if target_board[row][col][0] == False:
                    return False  # found a part that hasnt been hit
    return True


def check_winner(target_board):
    for row in rowNames:
        for col in range(board_size):
            if target_board[row][col][1] != 0:
                if target_board[row][col][0] == False:
                    return False
    return True


# ai is just random for now
# to do next submission we make it smarter and stuff

def ai_pick_shot(ai_shots_fired):
    untried = []
    for row in rowNames:
        for col in range(board_size):
            coordinate = (row, col)
            if coordinate not in ai_shots_fired:
                untried.append(coordinate)
    pick = random.choice(untried)
    return pick


def play_game():
    player_board = create_board()
    ai_board = create_board()

    place_ships(player_board)   # somebodys elses
    place_ships(ai_board)

    ai_shots_fired = []

    while True:
        draw_board(player_board, ai_board)  # erin's setting that up

        # players turn to shoot at the ai
        print("YOUR TURN")
        row, col = get_player_shot()   # aniel's function
        result = fire_shot(ai_board, row, col)

        if result == "already shot":
            print("you already shot there try again")
            continue
        elif result == "hit":
            ship_id = ai_board[row][col][1]
            ship_name = ""
            for name, sid, length in ships:
                if sid == ship_id:
                    ship_name = name
                    break
            print("HIT!! you hit their " + ship_name + "!")
            if check_sunk(ai_board, ship_id) == True:
                print("you sunk their " + ship_name + "!!")
        else:
            print("miss :( " + row + str(col + 1))

        if check_winner(ai_board) == True:
            draw_board(player_board, ai_board)
            print("YOU WIN!!!")
            break

        # this is the ais turn and stuff
        print("\noppenent is thinking...")
        ai_row, ai_col = ai_pick_shot(ai_shots_fired)
        ai_shots_fired.append((ai_row, ai_col))
        ai_result = fire_shot(player_board, ai_row, ai_col)

        if ai_result == "hit":
            ship_id = player_board[ai_row][ai_col][1]
            ship_name = ""
            for name, sid, length in ships:
                if sid == ship_id:
                    ship_name = name
            print("ai hit your " + ship_name + " at " + ai_row + str(ai_col + 1) + "!")
            if check_sunk(player_board, ship_id) == True:
                print("ai sunk your " + ship_name + "...")
        else:
            print("oppenent missed at " + ai_row + str(ai_col + 1))

        if check_winner(player_board) == True:
            draw_board(player_board, ai_board)
            print("game over :( ai wins")
            break


play_game()
