import pygame 

pygame.init()
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock() 
FPS = 30

class Striker:
		# Take the initial position, dimensions, speed and color of the object
	def __init__(self, posx, posy, width, height, speed, color):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.speed = speed
		self.color = color
		# Rect that is used to control the position and collision of the object
		self.geekRect = pygame.Rect(posx, posy, width, height)
		# Object that is blit on the screen
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	# Used to display the object on the screen
	def display(self):
		self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

	def update(self, yFac):
		self.posy = self.posy + self.speed*yFac

		# Restricting the striker to be below the top surface of the screen
		if self.posy <= 0:
			self.posy = 0
		# Restricting the striker to be above the bottom surface of the screen
		elif self.posy + self.height >= HEIGHT:
			self.posy = HEIGHT-self.height

		# Updating the rect with the new values
		self.geekRect = (self.posx, self.posy, self.width, self.height)

	def displayScore(self, text, score, x, y, color):
		text = font20.render(text+str(score), True, color)
		textRect = text.get_rect()
		textRect.center = (x, y)

		screen.blit(text, textRect)

	def getRect(self):
		return self.geekRect


# Ball class
class Ball:
	def __init__(self, posx, posy, radius, speed, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.speed = speed
		self.color = color
		self.xFac = 1
		self.yFac = -1
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)
		self.firstTime = 1

	def display(self):
		self.ball = pygame.draw.circle(
			screen, self.color, (self.posx, self.posy), self.radius)

	def update(self):
		self.posx += self.speed*self.xFac
		self.posy += self.speed*self.yFac

		# If the ball hits the top or bottom surfaces, 
		# then the sign of yFac is changed and 
		# it results in a reflection
		if self.posy <= 0 or self.posy >= HEIGHT:
			self.yFac *= -1

		if self.posx <= 0 and self.firstTime:
			self.firstTime = 0
			return 1
		elif self.posx >= WIDTH and self.firstTime:
			self.firstTime = 0
			return -1
		else:
			return 0

	def reset(self):
		self.posx = WIDTH//2
		self.posy = HEIGHT//2
		self.xFac *= -1
		self.firstTime = 1

	# Used to reflect the ball along the X-axis
	def hit(self):
		self.xFac *= -1

	def getRect(self):
		return self.ball
	

class PingPong:

	def __init__(self):
		# Initialize the strikers and ball once
		self.geek1 = Striker(20, 0, 10, 100, 10, GREEN)
		self.geek2 = Striker(WIDTH-30, 0, 10, 100, 10, GREEN)
		self.ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, WHITE)

		self.geek1Score = 0
		self.geek2Score = 0
		self.geek1YFac = 0
		self.geek2YFac = 0

	def step(self):
		screen.fill(BLACK)

		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				match event.key:
					case pygame.K_w:
						self.geek1YFac = -1
					case pygame.K_s:
						self.geek1YFac = 1
					case pygame.K_UP:
						self.geek2YFac = -1
					case pygame.K_DOWN:
						self.geek2YFac = 1

			if event.type == pygame.KEYUP:
				if event.key in (pygame.K_w, pygame.K_s):
					self.geek1YFac = 0
				if event.key in (pygame.K_UP, pygame.K_DOWN):
					self.geek2YFac = 0

		# Check for collisions between the ball and strikers
		if pygame.Rect.colliderect(self.ball.getRect(), self.geek1.getRect()) or \
		   pygame.Rect.colliderect(self.ball.getRect(), self.geek2.getRect()):
			self.ball.hit()

		# Update positions
		self.geek1.update(self.geek1YFac)
		self.geek2.update(self.geek2YFac)
		point = self.ball.update()

		# Update scores if the ball goes out of bounds
		if point == -1:
			self.geek1Score += 1
		elif point == 1:
			self.geek2Score += 1

		if point:
			self.ball.reset()

		# Display the objects and scores
		self.geek1.display()
		self.geek2.display()
		self.ball.display()

		self.geek1.displayScore("Geek_1 : ", self.geek1Score, 100, 20, WHITE)
		self.geek2.displayScore("Geek_2 : ", self.geek2Score, WIDTH-100, 20, WHITE)

		pygame.display.update()
		clock.tick(FPS)



if __name__ == "__main__":
	pingpong = PingPong()
	running = True 

	while running:
		pingpong.step()


