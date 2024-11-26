#! /usr/bin/python3

import graphics
import connect_n_state


SQUARE_COLOR        = "gray"
EMPTY_CIRCLE_COLOR  = "white"
CIRCLE_BORDER_COLOR = "black"

PLAYER_COLORS   = ["Red", "Yellow", "Blue", "Green", "Black"]
GRAPHICS_COLORS = ["red", "yellow", "blue", "green", "black"]
assert len(PLAYER_COLORS) == len(GRAPHICS_COLORS)



def draw_one_Connect_N_board(win, offset_x,offset_y, wid,hei, state,
                             color_map = None):

    # if no color map is provided, then assign default colors
    if color_map is None:
        color_map = {}

        players = state.get_player_list()
        assert len(players) <= len(GRAPHICS_COLORS)

        color_map = dict(zip(players, GRAPHICS_COLORS))

    # color_map must map the same things as the game's players.
    assert len(color_map) == len(state.get_player_list())
    players_sorted = sorted(state.get_player_list())
    assert len(players_sorted) == len(color_map)
    assert players_sorted == sorted(color_map)


    board_wid,board_hei = state.get_size()
    assert board_wid > 0
    assert board_hei > 0

    # this is the size of each square, in pixels
    x_size = wid / board_wid
    y_size = hei / board_hei

    for col in range(board_wid):
        for row in range(board_hei):
            # x1,y1 - the upper-left corner of the square
            # x2,y2 - the lower-right corner of the square
            # xC,yC - the center of the circle
            # xS,yS - the dimensions of the circle, as diameters

            x1 = offset_x + x_size*col
            y1 = offset_y + y_size*(board_hei-1-row)

            xC = x1 + x_size/2
            yC = y1 + y_size/2

            # the circle is 90% of the size of the square
            xS = x_size * .9
            yS = y_size * .9

            win.rectangle(x1,y1, x_size,y_size, fill=SQUARE_COLOR)

            disk = state.get_cell(col,row)
            if disk is None:
                circ_color = EMPTY_CIRCLE_COLOR
            else:
                circ_color = color_map[disk]
            win.ellipse(xC,yC, xS,yS, fill=circ_color, outline=CIRCLE_BORDER_COLOR)



def parameters():
    size = input("What is the board size, as 'wid hei' ? ").split()
    if len(size) != 2:
        print("ERROR: Give exactly two sizes, separated by whitespace.")
        return [None]*4
    try:
        wid = int(size[0])
        hei = int(size[1])
    except:
        wid = None
    if wid is None or wid < 2 or hei < 2 or wid > 10 or hei > 10:
        print("ERROR: The width and height must be integers, in the ranges 2..10")
        return [None]*4


    target = input("How many in a row are required to win ? ")
    try:
        target = int(target)
    except:
        target = None
    if target is None or target < 2 or target > max(wid,hei):
        print("ERROR: The count must be an integer, and in a reasonable range.")
        return [None]*4


    num_players = input("How many players ? ")
    try:
        num_players = int(num_players)
    except:
        num_players = None
    if num_players is None or num_players < 2 or num_players > len(PLAYER_COLORS):
        print("ERROR: The count must be an integer, and in a reasonable range.")
        return [None]*4


    return wid,hei,target,num_players



def main():
    print("+----------------------------+")
    print("|    WELCOME TO CONNECT N    |")
    print("+----------------------------+")
    print()

    wid,hei,target,num_players = parameters()
    if wid is None:
        return

    win = graphics.graphics(750,700, "Connect N Display")

    state = connect_n_state.Connect_N_State(wid,hei, target, PLAYER_COLORS[:num_players])


    def draw():
        win.clear()
        draw_one_Connect_N_board(win, 25,25, 700,600, state)
        if state.is_game_over() == False:
            cp = state.get_cur_player()
            win.text(25,650, f"{cp} to move.")
        else:
            if state.get_winner() is not None:
                win.text(25,650, f"GAME OVER.  {state.get_winner()} wins!")
            else:
                win.text(25,650, "TIE GAME.")
    draw()


    def handle_click(x,y):
        if state.is_game_over():
            print("Game is over, ignoring the click.")
            return
        if x < 25 or y < 25 or x > 725 or y > 625:
            print(f"({x},{y}) is outside the board, ignoring the click.")
            return
        col = int((x-25)/(700/wid))
        if state.is_column_full(col):
            print(f"Column {col} is already full, ignoring the click.")
            return
        state.move(col)
        draw()
    win.set_left_click_action(lambda win,x,y: handle_click(x,y))


    win.mainloop()



if __name__ == "__main__":
    main()

