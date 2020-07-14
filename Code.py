import random
import copy
import time

class GameError(AttributeError):
	pass

class Game:

	def __init__(self, n):
		self.size = n
		self.half_the_size = int(n/2)
		self.reset()

	def reset(self):
		self.board = []
		value = 'B'
		for i in range(self.size):
			row = []
			for j in range(self.size):
				row.append(value)
				value = self.opponent(value)
			self.board.append(row)
			if self.size%2 == 0:
				value = self.opponent(value)

	def __str__(self):
		result = "  "
		for i in range(self.size):
			result += str(i) + " "
		result += "\n"
		for i in range(self.size):
			result += str(i) + " "
			for j in range(self.size):
				result += str(self.board[i][j]) + " "
			result += "\n"
		return result

	def valid(self, row, col):
		return row >= 0 and col >= 0 and row < self.size and col < self.size

	def contains(self, board, row, col, symbol):
		return self.valid(row,col) and board[row][col]==symbol

	def countSymbol(self, board, symbol):
		count = 0
		for r in range(self.size):
			for c in range(self.size):
				if board[r][c] == symbol:
					count += 1
		return count

	def opponent(self, player):
		if player == 'B':
			return 'W'
		else:
			return 'B'

	def distance(self, r1, c1, r2, c2):
		return abs(r1-r2 + c1-c2)

	def makeMove(self, player, move):
		self.board = self.nextBoard(self.board, player, move)

	def nextBoard(self, board, player, move):
		r1 = move[0]
		c1 = move[1]
		r2 = move[2]
		c2 = move[3]
		next = copy.deepcopy(board)
		if not (self.valid(r1, c1) and self.valid(r2, c2)):
			raise GameError
		if next[r1][c1] != player:
			raise GameError
		dist = self.distance(r1, c1, r2, c2)
		if dist == 0:
			if self.openingMove(board):
				next[r1][c1] = "."
				return next
			raise GameError
		if next[r2][c2] != ".":
			raise GameError
		jumps = int(dist/2)
		dr = int((r2 - r1)/dist)
		dc = int((c2 - c1)/dist)
		for i in range(jumps):
			if next[r1+dr][c1+dc] != self.opponent(player):
				raise GameError
			next[r1][c1] = "."
			next[r1+dr][c1+dc] = "."
			r1 += 2*dr
			c1 += 2*dc
			next[r1][c1] = player
		return next

	def openingMove(self, board):
		return self.countSymbol(board, ".") <= 1

	def generateFirstMoves(self, board):
		moves = []
		moves.append([0]*4)
		moves.append([self.size-1]*4)
		moves.append([self.half_the_size]*4)
		moves.append([(self.half_the_size)-1]*4)
		return moves

	def generateSecondMoves(self, board):
		moves = []
		if board[0][0] == ".":
			moves.append([0,1]*2)
			moves.append([1,0]*2)
			return moves
		elif board[self.size-1][self.size-1] == ".":
			moves.append([self.size-1,self.size-2]*2)
			moves.append([self.size-2,self.size-1]*2)
			return moves
		elif board[self.half_the_size-1][self.half_the_size-1] == ".":
			pos = self.half_the_size -1
		else:
			pos = self.half_the_size
		moves.append([pos,pos-1]*2)
		moves.append([pos+1,pos]*2)
		moves.append([pos,pos+1]*2)
		moves.append([pos-1,pos]*available2)
		return moves

	def check(self, board, r, c, rd, cd, factor, opponent):
		if self.contains(board,r+factor*rd,c+factor*cd,opponent) and \
		   self.contains(board,r+(factor+1)*rd,c+(factor+1)*cd,'.'):
			return [[r,c,r+(factor+1)*rd,c+(factor+1)*cd]] + \
				   self.check(board,r,c,rd,cd,factor+2,opponent)
		else:
			return []

	def generateMoves(self, board, player):
		if self.openingMove(board):
			if player=='B':
				return self.generateFirstMoves(board)
			else:
				return self.generateSecondMoves(board)
		else:
			moves = []
			rd = [-1,0,1,0]
			cd = [0,1,0,-1]
			for r in range(self.size):
				for c in range(self.size):
					if board[r][c] == player:
						for i in range(len(rd)):
							moves += self.check(board,r,c,rd[i],cd[i],1,
												self.opponent(player))
			return moves

	def playOneGame(self, p1, p2, show):
		self.reset()
		while True:
			if show:
				print(self)
				print("player B's turn")
			move = p1.getMove(self.board)
			if move == []:
				print("Game over")
				return 'W'
			try:
				self.makeMove('B', move)
			except GameError:
				print("Game over: Invalid move by", p1.name)
				print(move)
				print(self)
				return 'W'
			if show:
				print(move)
				print(self)
				print("player W's turn")
			move = p2.getMove(self.board)
			if move == []:
				print("Game over")
				return 'B'
			try:
				self.makeMove('W', move)
			except GameError:
				print("Game over: Invalid move by", p2.name)
				print(move)
				print(self)
				return 'B'
			if show:
				print(move)

	def playNGames(self, n, p1, p2, show):
		first = p1
		second = p2
		for i in range(n):
			print("Game", i)
			winner = self.playOneGame(first, second, show)
			if winner == 'B':
				first.won()
				second.lost()
				print(first.name, "wins")
			else:
				first.lost()
				second.won()
				print(second.name, "wins")
			first, second = second, first


class Player:
	name = "Player"
	wins = 0
	losses = 0
	def results(self):
		result = self.name
		result += " Wins:" + str(self.wins)
		result += " Losses:" + str(self.losses)
		return result
	def lost(self):
		self.losses += 1
	def won(self):
		self.wins += 1
	def reset(self):
		self.wins = 0
		self.losses = 0

	def initialize(self, side):
		abstract()

	def getMove(self, board):
		abstract()


class SimplePlayer(Game, Player):
	def initialize(self, side):
		self.side = side
		self.name = "Simple"
	def getMove(self, board):
		moves = self.generateMoves(board, self.side)
		n = len(moves)
		if n == 0:
			return []
		else:
			return moves[0]

class RandomPlayer(Game, Player):
	def initialize(self, side):
		self.side = side
		self.name = "Random"
	def getMove(self, board):
		moves = self.generateMoves(board, self.side)
		n = len(moves)
		if n == 0:
			return []
		else:
			return moves[random.randrange(0, n)]

class HumanPlayer(Game, Player):
	def initialize(self, side):
		self.side = side
		self.name = "Human"
	def getMove(self, board):
		moves = self.generateMoves(board, self.side)
		while True:
			print("Possible moves:", moves)
			n = len(moves)
			if n == 0:
				print("You must concede")
				return []
			index = input("Enter index of chosen move (0-"+ str(n-1) +
						  ") or -1 to concede: ")
			try:
				index = int(index)
				if index == -1:
					return []
				if 0 <= index <= (n-1):
					print("returning", moves[index])
					return moves[index]
				else:
					print("Invalid choice, try again.")
			except Exception as e:
				print("Invalid choice, try again.")
		


class MinimaxPlayer (Player,Game):
    def initialize(self,side):
        self.side = side
        self.name = "Ai Player"
        self.depth = 0

        self.me = side
        self.enemy = self.opponent(self.side)
    
    def getMove(self,board):
        value,path = self.max_value(board)
        return path

    

    def min_value(self,board):

        value = self.evaluationFunc(board)
        if(value != "none"):
            return value, []
        minmoves = self.generateMoves(board,self.enemy)
        
        minValue = 10
        bestPath = []


        
        for move in minmoves:
            self.depth +=1
            value,path = self.max_value(self.nextBoard(board,self.enemy,move))
            self.depth += -1

            if(value < minValue):
                minValue = value
                bestPath = move

        return minValue,bestPath
        

    def max_value(self,board):
        
        value = self.evaluationFunc(board)
        if(value != "none"):
            return value, []
        maxmoves = self.generateMoves(board,self.me)
        
        maxValue = -10
        bestPath = []

        for move in maxmoves:
            self.depth +=1
            value,path = self.min_value(self.nextBoard(board,self.me,move))
            self.depth += -1

            if(value > maxValue):
                maxValue = value
                bestPath = move

        return maxValue,bestPath

        
        
    def evaluationFunc(self,board):
        maxMoves = self.generateMoves(board,self.me)
        minMoves = self.generateMoves(board,self.enemy)

        me = 0
        enemy = 0

        for i in range(0,len(board)):
            for j in range(0,len(board[i])):
                if board[i][j] == self.side:
                    me = me + 1
                elif board[i][j] == self.opponent(self.side):
                    enemy = enemy + 1
        

        if(len(maxMoves) == 0):
            return -1
        if(len(minMoves) == 0):
            return 1
        if(self.depth == 3):
            return (len(maxMoves)-len(minMoves))/(len(maxMoves)+len(minMoves))
        
        return "none"
        


class AlphaBeta(Player,Game):
    def initialize(self,side):
        self.side = side
        self.name = "Ai Player"
        self.depth = 0
        self.alpha = -10
        self.beta = 10
        self.me = side
        self.enemy = self.opponent(self.side)
    
    def getMove(self,board):
        value,path = self.max_value(board)
        return path

    

    def min_value(self,board):

        value = self.evaluationFunc(board)
        if(value != "none"):
            return value, []
        minmoves = self.generateMoves(board,self.enemy)
        
        minValue = 10
        bestPath = []

        for move in minmoves:
            self.depth +=1
            value,path = self.max_value(self.nextBoard(board,self.enemy,move))
            self.depth += -1

            if(value < minValue):
                minValue = value
                bestPath = move
            
            if minValue <= self.alpha and self.depth != 0:
                return minValue,bestPath
            self.beta = min(self.beta,minValue)
        return minValue,bestPath
        

    def max_value(self,board):
        

        value = self.evaluationFunc(board)
        if(value != "none"):
            return value, []
        maxmoves = self.generateMoves(board,self.me)
        
        maxValue = -10
        bestPath = []

        for move in maxmoves:
            self.depth +=1
            value,path = self.min_value(self.nextBoard(board,self.me,move))
            self.depth += -1

            if(value > maxValue):
                maxValue = value
                bestPath = move

            if maxValue >= self.beta and self.depth != 0:
                return maxValue,bestPath
            self.alpha = max(self.alpha,maxValue)

        return maxValue,bestPath

        
        
    def evaluationFunc(self,board):
        maxMoves = self.generateMoves(board,self.me)
        minMoves = self.generateMoves(board,self.enemy)

        me = 0
        enemy = 0

        for i in range(0,len(board)):
            for j in range(0,len(board[i])):
                if board[i][j] == self.side:
                    me = me + 1
                elif board[i][j] == self.opponent(self.side):
                    enemy = enemy + 1
        

        if(len(maxMoves) == 0):
            return -1
        if(len(minMoves) == 0):
            return 1
        if(self.depth == 3):
            return (len(maxMoves)-len(minMoves))/(len(maxMoves)+len(minMoves))
        
        return "none"
        

        

#if __name__ == '__main__':
game = Game(8)
starttime = time.time()
AI = AlphaBeta(8)
AI.initialize("W")
simp = SimplePlayer(8)
simp.initialize("B")
game.playOneGame(simp, AI, True)   
endtime = time.time()

print("ToTal Duration is :", endtime-starttime)
