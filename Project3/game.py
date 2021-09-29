# cited: https://blog.csdn.net/Zhangguohao666/article/details/103280740
###############################
## FIle name: game.py
## Name: Jianglong Yu
## Date: 8/7
## descripution: Set a game class for the chat
#################################
class Game():
    def __init__(self):
        self.board = list("012345678")
        # This list is store place where don't have chess
        self.avaliable_place = []
        self.client_move = -1
        self.server_move = -1
        self.clientChess = 'p'
        self.serverChess = 's'

    # print the board
    def display_board(self):
        print("\t{0} | {1} | {2}".format(self.board[0], self.board[1], self.board[2]))
        print("\t_ | _ | _")
        print("\t{0} | {1} | {2}".format(self.board[3], self.board[4], self.board[5]))
        print("\t_ | _ | _")
        print("\t{0} | {1} | {2}".format(self.board[6], self.board[7], self.board[8]))

    # check if the input number is vaild
    def legal_moves(self):
        # this list is store place where don't have chess
        for i in range(9):
            if self.board[i] in list("012345678"):
                self.avaliable_place.append(i)

    # ask players input the number of position where what to set the chess
    def getClientMove(self):
        while self.client_move not in self.avaliable_place:
            self.client_move = int(input("Please choose where to play chess(0-8):"))
            return self.client_move

    def setClientMove(self, move):
        self.client_move = move
        return self.client_move

    # ask players input the number of position where what to set the chess       
    def getServerMove(self):
        while self.server_move not in self.avaliable_place:
            self.server_move = int(input("Please choose where to play chess(0-8):"))
            return self.server_move

    def setServerMove(self, move):
        self.server_move = move
        return self.client_move

    # get client chess
    def getClientchess(self):
        self.clientChess = input("please choose your chess X or O(just press the letter, X is first): ")
        return self.clientChess
    
    def setClientchess(self, c):
        self.clientChess = c
        return self.clientChess
    
    # set server chess
    def setServerchess(self, c):
        self.serverChess = c
        return self.serverChess

    # determine who is winner
    def isWinner(self):
        # only these eight sitution will have winner
        WAYS_TO_WIN = {(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)}
        for i in WAYS_TO_WIN:
            # if there are the same chess in one of these sitution, then this chess win
            if self.board[i[0]] == self.board[i[1]] == self.board[i[2]]:
                return True
        return False

    # determine if this game is draw
    def isDraw(self):
        for i in list("012345678"):
            if i in self.board:
                return False
        return True