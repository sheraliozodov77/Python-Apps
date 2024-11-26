#! /usr/bin/python3

import sys

import connect_n_state



def main(simple):
    game = connect_n_state.Connect_N_State(7,6, 4, ["Red","Yellow"])

    while True:
        if not simple:
            if game.is_game_over():
                print("GAME HAS ENDED")
                print()
                break

        print("CURRENT GAME STATE:")
        game.print()
        print()

        if not simple:
            move = input(f"{repr(game.get_cur_player())} to move: ").strip()
        else:
            move = input().strip()

        if move == "":
            continue      # empty command, silent response is intentional

        if move == "quit":
            print()
            print("GAME TERMINATED BY USER COMMAND.")
            print()
            break

        try:
            move = int(move)
        except:
            print(f"ERROR: {repr(move)} is not an integer.")
            continue

        if not simple:
            if move < 0 or move >= game.get_size()[0]:
                print(f"ERROR: The valid column numbers are 0..{game.get_size()[0]-1} (inclusive)")
                continue

        if not simple:
            if game.is_column_full(move):
                print(f"ERROR: The column {move} is already full.")
                continue

        game.move(move)
        print()

    print("FINAL GAME STATE:")
    game.print()



if __name__ == "__main__":
    if sys.argv[1:2] == ["--simple"]:
        simple = True
    else:
        simple = False

    main(simple)

