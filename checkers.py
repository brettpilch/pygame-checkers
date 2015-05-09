import pygame
import math
import random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
YELLOW   = ( 255, 255,   0)
TRANS    = (   1,   2,   3)

# CONSTANTS:
WIDTH = 700
HEIGHT = 700

class Game:
	"""class to keep track of the status of the game."""
	def __init__(self):
		"""
		Start a new game with an empty board and random player going first.
		"""
		self.status = 'playing'
		self.turn = 0
		self.players = ['X','O']
		rando = random.randrange(0,2)
		self.ai = self.players[rando]
		self.human = self.players[1 - rando]
		pygame.display.set_caption("%s's turn" % self.players[self.turn % 2])
		self.game_board = [['X','-','X','-','X','-','X','-'],
						   ['-','X','-','X','-','X','-','X'],
			  			   ['X','-','X','-','X','-','X','-'],
						   ['-','-','-','-','-','-','-','-'],
						   ['-','-','-','-','-','-','-','-'],
						   ['-','O','-','O','-','O','-','O'],
						   ['O','-','O','-','O','-','O','-'],
						   ['-','O','-','O','-','O','-','O']]

	def is_empty(self, row, column):
		return self.game_board[row][column] == '-'

	def evaluate_click(self, mouse_pos):
		"""
		Play in a square if it is empty.
		Start a new game if the game is over.
		"""
		if self.status == 'playing':
			row, column = get_clicked_row(mouse_pos), get_clicked_column(mouse_pos)
			if self.is_empty(row, column):
				self.play(self.players[self.turn % 2], row, column)
		elif self.status == 'game over':
			self.__init__()

	def play(self, player, row, column):
		"""
		play in a square, then check to see if the game is over.
		"""
		self.game_board[row][column] = player
		self.turn += 1
		winner = self.check_winner(player, row, column)
		if winner is None:
			pygame.display.set_caption("%s's turn" % game.players[game.turn % 2])
		elif winner == 'draw':
			pygame.display.set_caption("Cat's Game! Click to start again")
			self.status = 'game over'
		else:
			pygame.display.set_caption("%s wins! Click to start again" % winner)
			self.status = 'game over'

	def check_winner(self, player, row, column):
		"""
		check to see if someone won, or if it is a draw.
		"""
		if self.game_board[row].count(player) == 3:
			return player
		if (self.game_board[0][column] == player and
			self.game_board[1][column] == player and 
			self.game_board[2][column] == player):
			return player
		if ((self.game_board[0][0] == player and
			 self.game_board[1][1] == player and
			 self.game_board[2][2] == player) or
			(self.game_board[0][2] == player and
			 self.game_board[1][1] == player and
			 self.game_board[2][0] == player)):
			return player
		flat = [mark for row in self.game_board for mark in row]
		if flat.count('-') == 0:
			return 'draw'
		return None
			

	def draw(self):
		"""
		Draw the game board and the X's and O's.
		"""
		pygame.draw.line(screen, WHITE, [WIDTH / 3, 0], [WIDTH / 3, HEIGHT], 10)
		pygame.draw.line(screen, WHITE, [2 * WIDTH / 3, 0], [2 * WIDTH / 3, HEIGHT], 10)
		pygame.draw.line(screen, WHITE, [0, HEIGHT / 3], [WIDTH, HEIGHT / 3], 10)
		pygame.draw.line(screen, WHITE, [0, 2 * HEIGHT / 3], [WIDTH, 2 * HEIGHT / 3], 10)
		pygame.draw.rect(screen, WHITE, [0,0,WIDTH,HEIGHT], 10)
		font = pygame.font.SysFont('Calibri', MARK_SIZE, False, False)
		for r in range(len(self.game_board)):
			for c in range(len(self.game_board[r])):
				mark = self.game_board[r][c]
				if mark != '-':
					mark_text = font.render(self.game_board[r][c], True, WHITE)
					x = WIDTH / 3 * c + WIDTH / 6
					y = HEIGHT / 3 * r + HEIGHT / 6
					screen.blit(mark_text, [x - mark_text.get_width() / 2, y - mark_text.get_height() / 2])

# Helper functions:
def get_clicked_column(mouse_pos):
	x = mouse_pos[0]
	if x < WIDTH / 3:
		return 0
	if x < 2 * WIDTH / 3:
		return 1
	return 2

def get_clicked_row(mouse_pos):
	y = mouse_pos[1]
	if y < HEIGHT / 3:
		return 0
	if y < 2 * HEIGHT / 3:
		return 1
	return 2

def transpose(board):
	return [[board[col][row] for col in range(len(board[row]))] for row in range(len(board))]

# start pygame:
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

# start tic-tac-toe game:
game = Game()

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# game loop:
while not done:
    # --- Main event loop
    if game.status == 'playing':
    	game.ai_play(game.ai_choice())
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            entry = str(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
        	mouse_x, mouse_y = pygame.mouse.get_pos()
        	game.evaluate_click(pygame.mouse.get_pos())

    # --- Drawing code should go here
 
    # First, clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # draw the game board and marks:
    game.draw()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()