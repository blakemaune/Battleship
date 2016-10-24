from random import randint

CPUboard = []
USRboard = []

print("Let's play Battleship!")
#Default Options
rows = 6
cols = 6
turnlimit = 8
hints = 1
ai = 1
error = 0.5

while True:
	menu1 = input("Main Menu\nS: Start Game\nO: Options\nChoice: ").lower()
	if menu1 == 's':
		break
	elif menu1 == 'o':
		while True:
			menu2 = input("Options Menu\nT: Turn limit\nD: dimensions\nH: Hints\nA: AI Settings\nE: AI Error\nX: Exit\nChoice: ").lower()
			if menu2 == 't':
				turnlimit = int(input("Enter max turns: "))
				
			elif menu2 == 'd':
				rows = int(input("Enter rows: "))
				cols = int(input("Enter cols: "))
			
			elif menu2 == 'h':
				hints = int(input("Hints\n2: SuperHints on\n1: Hints on\n0: Hints off\nChoice:"))
			
			elif menu2 == 'a':
				ai = int(input("AI Settings\n1: AI On\n2: AI Off\nChoice:"))
			
			elif menu2 == 'e':
				error = int(input("AI Error\n1:Enter degrees of error for AI guesses:"))
				
			else:
				break
			

for x in range(rows):
    CPUboard.append([" "] * cols)
    USRboard.append([" "] * cols)

def print_board(board):
	cols = (list(range(len(board))))
	print("  " + str(cols))
	for i in list(range(len(board[0]))):
		print(i, end="")
		print("  ", end="")
		print("  ".join(board[i]))



def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

CPU_ship_row = random_row(CPUboard)
CPU_ship_col = random_col(CPUboard)

USR_ship_row = int(input("Enter your ship's row: "))
USR_ship_col = int(input("Enter your ship's column: "))
USRboard[USR_ship_row][USR_ship_col] = "%"

print ("CPU Board: ")
print_board(CPUboard)
print ("USR Board: ")
print_board(USRboard)

def take_turn(guess_row, guess_col, ship_row, ship_col, OPPboard, turn):
	if guess_row == ship_row and guess_col == ship_col:
		OPPboard[guess_row][guess_col] = "O"
		print ("Congratulations! You sunk my battleship!")
		return 1
	else:
		if (guess_row < 0 or guess_row > rows) or (guess_col < 0 or guess_col > cols):
			print ("Oops, that's not even in the ocean.")
			return -1
		elif(OPPboard[guess_row][guess_col] == "X"):
			print ("You guessed that one already.")
			return -1
		else:
			print ("You missed my battleship!")
			OPPboard[guess_row][guess_col] = str(turn)
			return 0

def distForm(guess_row, guess_col, ship_row, ship_col):
	x1 = guess_row
	x2 = ship_row
	y1 = guess_col
	y2 = ship_col
	dist = (((x2-x1)**2 + (y2-y1)**2)) ** .5
	return dist

def rangeFind(row, col, dist):
	moves = []
	for i in list(range(rows)):
		for j in list(range(cols)):
			if distForm(row, col, i, j) == dist:
				moves.append([[i],[j]])
	print(moves)
	return moves

def CPUrangeFind(row, col, dist, error):
	print("Calculating moves, with some error")
	moves = []
	for i in list(range(rows)):
		for j in list(range(cols)):
			calcDist = distForm(row, col, i, j)
			if (dist - error <= calcDist) and (calcDist <= dist + error):
				moves.append([[i],[j]])
	print(moves)
	return moves

"""
def CPUrangeFind(row, col, dist):
	dist = distForm(CPU_guess_row, CPU_guess_col, USR_ship_row, USR_ship_col)
	moves = rangeFind(CPU_guess_row, CPU_guess_col, dist, error)
	move = moves[randint(0, len(moves) - 1)]
	return move
"""
	
# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(turnlimit):
	input("press ENTER to continue...")
	print("".join(["-"]*30))
	#CPU TURN
	print("CPU TURN ", turn+1)
	
	if turn == 0 or ai <= 0:
		CPU_guess_row = random_row(USRboard)
		CPU_guess_col = random_col(USRboard)
	else:
		dist = distForm(CPU_guess_row, CPU_guess_col, USR_ship_row, USR_ship_col)
		moves = CPUrangeFind(CPU_guess_row, CPU_guess_col, dist, error)
		index = randint(0, len(moves) - 1)
		move = moves[index]
		print("Distance to target: ",dist)
		CPU_guess_row = move[0][0]
		CPU_guess_col = move[1][0]
	
	
	print("Guess Row: ", CPU_guess_row)
	print("Guess Col: ", CPU_guess_col)
	res = take_turn(CPU_guess_row, CPU_guess_col, USR_ship_row, USR_ship_col, USRboard, turn)
	print("USR Board: ")
	print_board(USRboard)
	print("\n")
	if res == 1:
		break
	print("".join(["-"]*30))
	
	
	#USR TURN
	print("USR TURN ", turn+1)
	USR_guess_row = int(input("Guess Row:"))
	USR_guess_col = int(input("Guess Col:"))
	res = take_turn(USR_guess_row, USR_guess_col, CPU_ship_row, CPU_ship_col, CPUboard, turn)
	
	if hints >= 1:
		print("Distance to target: ", distForm(USR_guess_row, USR_guess_col, CPU_ship_row, CPU_ship_col))
	if hints >= 2:
		print("Suggested moves:")
		dist = distForm(USR_guess_row, USR_guess_col, CPU_ship_row, CPU_ship_col)
		rangeFind(USR_guess_row, USR_guess_col, dist)

	print("CPU Board: ")
	print_board(CPUboard)
	print("\n")
	if res == 1:
		break

if res != 1:
	print("CPU Final Board: ")
	CPUboard[CPU_ship_row][CPU_ship_col] = '%'
	print_board(CPUboard)
