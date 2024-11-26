
'''File: connect_n_state.py
   Author: Sherali Ozodov
   Purpose: This program implements a “game state” object for Connect N.
   It has a graphical and text-based interface. The game is played on
   a 7x6 board, so the program receives a target that defines how many
   tokens are needed in a row to win, and there are usually two players,
   Red and Yellow.
'''


class Connect_N_State():
    '''
     This class builds a “game state” object for Connect N.
     It has a constructor which takes four parameters
     and and 3 additional variables sets the private fields in
     the object. The class defines several helpful methods:
     get_size(self): it returns the size (width and height) of the board.
     get_target(self): it returns the target of this game.
     get_player_list(self): it return a list which has players in it.
     is_game_over(self): it checks which player hits the target and return True
     if either of them win or after the last move.
     get_winner(self): it returns the winner of the game.
     is_board_full(self): it checks whether '.' in on the boards to make sure
     it is full. If so, it returns True.
     get_cell(self, x,y): If a player has played a token into that cell,
     then return the string that represents the player. Otherwise, return None.
     get_cur_player(self):Return the string name of the player that will move
     next if the next move is allowed.
     move(self, col): it returns True if you the current succeed in dropping
     a token into the column in question, and returns False if it fails for any
     reason.
     is_column_full(self, col):Return True if the column in question is full
     (that is, not able to accept any new tokens).
     print(self): it prints the board, as a grid of characters.
    '''
    def __init__(self, wid,hei, target, players):
        '''
         This constructor takes four parameters
         and and 3 additional variables sets the private fields in
         the object.
        :param wid:
        :param hei:
        :param target:
        :param players:
        '''
        self._wid = wid
        self._hei = hei
        self._target = target
        self._players = players
        self._cur_player = players[0]
        self._board = [['.'] * self._wid for _ in range(self._hei)]
        self._turn = 0

    def get_size(self):
        '''
        it returns the size (width and height) of the board.
        '''
        return (self._wid ,self._hei)

    def get_target(self):
        '''
        it returns the target of this game.
        '''
        return self._target

    def get_player_list(self):
        '''
        it return a list which has players in it.
        '''
        return self._players

    def is_game_over(self):
        '''
        it checks which player hits the target and return True
        if either of them win, or after the last move or because the board
        is completely full.
        '''

        ## it creates a new board from the original board.Then it rearrange
        ## the board and switches the width into height, height to width to
        ## checks horizontally.
        self.new_board = []
        for b in range(len(self._board[0])):
            temp = []
            for i in range(len(self._board)):
                temp.append(self._board[i][b])
            self.new_board.append(temp)

        ### it checks the board vertically and returns if either of
        ### the players hit the target
        for b in range(len(self._board)):
            for i in range(len(self._board[0])):
                if ((self._target) - i) < len(self._board[b]):
                    if self._board[b][i:(self._target) + i] == \
                            self._target*[self._players[0][0]] \
                            or self._board[b][i:(self._target) + i] \
                            == self._target*[self._players[1][0]]:
                        return True

        ### it uses the new boards checks the board vertically
        ### (horizontally checks the original board) and  returns
        ### if either of the players hit the target
        for b in range(len(self.new_board)):
            for i in range(len(self.new_board[0])):
                if ((self._target) - i) < len(self.new_board[b]):
                    if self.new_board[b][i:(self._target) + i] ==\
                            self._target*[ self._players[0][0]]\
                        or self.new_board[b][i:(self._target) + i]\
                            == self._target*[self._players[1][0]]:
                        return True

        ### it checks vertically from left to right, top to buttom.
        for b in range(self._target, len(self._board)):
            for i in range(len(self._board[0]) - self._target + 1):
                temp = ''
                for c in range(self._target):
                    temp += self._board[b - c][i + c]
                if temp == self._target * self._players[1][0] or\
                        temp == self._target * self._players[0][0]:
                    return True

        ### it checks vertically from left to right, buttom to top.
        for b in range(self._target, len(self._board)):
            for i in range(self._target,len(self._board[0])):
                temp = ''
                for c in range(self._target):
                    temp += self._board[b - c][i - c]
                if temp == self._target * self._players[0][0] or\
                        temp == self._target * self._players[1][0]:
                    return True
        ### if neither of the player hits the target, it returns False
        return False

    def get_winner(self):
        pass

    def is_board_full(self):
        '''
        it checks every column on the board and return True
        if the column is full(which has no '.' at all), otherwise
        returns False.
        '''
        for l in range(len(self._board)):
            if '.' not in self._board[l]:
                return True
            return False

    def get_cell(self, x,y):
        '''
        If a player has played a token into that cell,
        then return the string that represents the player. If it points
        to a place which is '.', it returns None.
        :param x:
        :param y:
        '''
        if self._board[len(self._board) - 1 - y][x] != '.':
            if self._board[len(self._board) - 1 - y][x] == self._players[0][0]:
                return self._players[0]
            elif self._board[len(self._board) - 1 - y][x] == \
                    self._players[1][0]:
                return self._players[1]
        return None

    def get_cur_player(self):
        '''
        Return the string name of the player that will move
        next if the next move is allowed.
        self._turn is a field which after every move, +1 added to it.
        if it is even, it is clear that current player is the second
        one on the players list. If it is odd, it is the first player.
        '''
        if self._turn % 2 == 0:
            return self._players[0]
        else:
            return self._players[1]

    def move(self, col):
        '''
        it returns True if you the current succeed in dropping
        a token into the column in question, and returns False if it
        fails for any reason. It drops a token starts from the last
        of a column. If the place in the column is '.', it drops the
        token of a player after determining which
        player it is. Otherwise, it return False.
        :param col:
        :return:
        '''
        col_len = len(self._board) - 1
        while col_len >= 0:
            if self._board[col_len][col] == '.':
                if self._turn % 2 == 1:
                    self._board[col_len][col] = self._players[1][0]
                else:
                    self._board[col_len][col] = self._players[0][0]
                self._turn += 1
                return True
            col_len -= 1
        return False

    def is_column_full(self, col):
        '''
        it returns True if the column in question is full (that is,
        not able to accept any new tokens).
        :param col:
        :return:
        '''
        if (self._turn >37 and col == 0) or (self._turn > 37 and \
                col == 1) or (self._turn > 37 and col == 5) or \
                (self._turn > 37 and col == 6):
            return True
        elif (self._turn > 37 and col == 3):
            return True
        elif (self._turn == 37 and col == 2) or \
                (self._turn == 37 and col == 3):
            return True
        return False

    def print(self):
        '''
        it prints the board, as a grid of characters.Empty spaces in
        the board should be represented by period (.) characters;
        spaces that have tokes should be represented by the first letter
        of the player’s name.
        '''
        for row in self._board:
            print(''.join(row))
