# Import Packages
import pygame
import random
import math

# Constants
num_players = 102 # number of players (should be divisible by 3)
player_size = 30 # size of the player icons

# Initialize pygame and set background size/colour
pygame.init()
window_wide = 1200 # window width in pixels
window_high = 800 # window height in pixels
colour = [255, 255, 255] # background colour

# Create the class for each rock paper scissors player
class Item:
	
	def __init__(self, state):
		
		# Create a random starting position for each object
		self.x = random.randint(0, window_wide - player_size - 1)
		self.y = random.randint(0, window_high - player_size - 1)
		self.state = state # specify what state the object should start in 
		
		# Update who the object is "attacking" or "running" from based on its state
		if self.state == 'rock':
			self.attack = 'scissors'
			self.run = 'paper'

		elif self.state == 'paper':
			self.attack = 'rock'
			self.run = 'scissors'

		elif self.state == 'scissors':
			self.attack = 'paper'
			self.run = 'rock'

	def update_state(self, items):
		
		# Find all agents that can change current objects state
		others = [item for item in items if item.state == self.run]
		
		# Check if the agent is touching current object 
		boolean = check_state(self, others)
		
		# If touching update state
		if boolean:

			if self.state == "rock":
				self.state = 'paper'
				self.attack = 'rock'
				self.run = 'scissors'

			elif self.state == "paper":
				self.state = 'scissors'
				self.attack = 'paper'
				self.run = 'rock'

			elif self.state == 'scissors':
				self.state = "rock"
				self.attack = 'scissors'
				self.run = 'paper'

	def move(self, items):
		
		# Find agents we want object to move towards
		others = [item for item in items if item.state == self.attack]
		
		# Find distance to closest object to attack
		attack_x, attack_y = distance_item(self, others)
		
		# If no agents left, moves randomly
		if (attack_x == 0) and (attack_y == 0): 

			self.x += random.randint(-1, +1)
			self.y += random.randint(-1, +1)

		# If there are agents left, move towards closest agent to attack
		else:

			angle = math.degrees(math.atan2(attack_y, attack_x))
			angle = int(45 * round(angle / 45))
			self.dx = math.cos(math.radians(angle))
			self.dy = math.sin(math.radians(angle))
		
			self.x += self.dx
			self.y += self.dy
		
		# Constraints so object can move past/leave window
		if self.x < 0:
			self.x = 0
		elif self.x > window_wide:
			self.x = window_wide
		
		if self.y < 0:
			self.y = 0
		elif self.y > window_high:
			self.y = window_high

def distance_item(agent, others):
	distances = []
	closest_x = 0
	closest_y = 0
	
	# Calculates distances to other objects
	for other in others:
		delta_x = other.x - agent.x
		delta_y = other.y - agent.y
		distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
		distances.append(distance)
		
		# Updates the minimum distance to the closest object
		if min(distances) == distance:
			closest_x = delta_x
			closest_y = delta_y
	
	# Returns the distance to the closest object
	return closest_x, closest_y	
	
def check_state(agent, others):

	# Returns boolean if there is another agent touching current object
	for other in others:
		if ((-1 * player_size) <= (other.x - agent.x) <= player_size) and ((-1 * player_size) <= (other.y - agent.y) <= player_size):
			return True
		
	return False


# Main code to initalize the of program
def main():
	
	# Create a winddow for the game to run
	window = pygame.display.set_mode((window_wide, window_high))	
	
	# Load the icon images for the rock, paper, and scissors
	img_rock = pygame.image.load("rock.png")
	img_rock = pygame.transform.scale(img_rock, (player_size, player_size))
	
	img_paper = pygame.image.load("paper.jpg")
	img_paper = pygame.transform.scale(img_paper, (player_size, player_size))
	
	img_scissors = pygame.image.load("scissors.jpg")
	img_scissors = pygame.transform.scale(img_scissors, (player_size, player_size))
	
	# Create three sets of rock, paper, and scissor objects
	items = []
	for i in range(num_players):
		if i < (num_players // 3):
			items.append(Item('rock'))
		elif i < ((num_players // 3) * 2):
			items.append(Item('paper'))
		else:
			items.append(Item('scissors'))
	
	# Loop to run the game
	simulation_is_running = True
	while simulation_is_running:

		# draw a background on the screen
		pygame.draw.rect(window, colour, (0, 0, window_wide, window_high))

		# Update the icon image for each object
		for item in items:
			if item.state == 'rock':
				img = img_rock
			elif item.state == 'paper':
				img = img_paper
			elif item.state == 'scissors':
				img = img_scissors
			
			# Update the object states and move objects
			window.blit(img, (item.x, item.y))
			item.update_state(items)
			item.move(items)
		
		# update screen and wait breifly between each turn
		pygame.display.update()
		pygame.time.wait(10)

		# Simulation ends when window is closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				simulation_is_running = False

# Runs program
if __name__ == "__main__":
	main()