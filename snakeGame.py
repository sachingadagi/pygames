
import pygame, sys, random, time

check_errors = pygame.init()

if check_errors[1] > 0:
	print "Error initialising pygame, {0} error(s)".format(check_errors[1])
	sys.exit()
else:
	print "Hold on your seat belts, game is starting soon!!"

# game window dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720

# colors
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLACK = pygame.Color(0,0,0) #score
WHITE = pygame.Color(255,255,255)
BROWN = pygame.Color(165,42,42)

playSurface = pygame.display.set_mode([SCREEN_HEIGHT,SCREEN_WIDTH])
pygame.display.set_caption('I cant sleep')

#FPS settings
fpsController = pygame.time.Clock()


# Global variables that we need
snakeHeadPos = None
snakeBody = None
score = None
gamePaused = None
foodPosition = None
foodSpawn = None
direction = None
changeto = None

def init():
	global snakeHeadPos, snakeBody,score,gamePaused,foodPosition,foodSpawn,direction,changeto
	
	snakeHeadPos = [100,50]
	snakeBody =  [[100,50],[90,50],[80,50],[50,50],[40,50],[30,50]]
	score = 0
	gamePaused = False
	foodPosition = [random.randrange(1,72) * 10, random.randrange(1,48) * 10]
	foodSpawn = True
	direction = 'RIGHT'
	changeto = direction

# Game over function
def gameOver():
	my_font = pygame.font.SysFont('Arial', 48)
	GoSurf =  my_font.render('Game Over, Press R to restart', True, RED)
	GORect = GoSurf.get_rect()
	GORect.midtop  = (360,15)
	playSurface.blit(GoSurf, GORect)
	showScore(False)
	pygame.display.flip() # Update ~ to repaint
	while True:
		for event in pygame.event.get():
			if event.key == ord('r') or event.key == ord('R'):
				restartGame()
			else:
				pygame.quit()
				sys.exit()

def restartGame():
	global score, snakeBody, snakeHeadPos, direction,changeto
	pygame.event.clear(pygame.USEREVENT)
	pygame.event.clear(pygame.KEYDOWN)
	pygame.event.clear(pygame.KEYUP)
	init()
	startGame()

def showScore(isGameOver):
	my_font = pygame.font.SysFont('Arial', 24)
	scoreSurf =  my_font.render('Score {0}'.format(score)  , True, RED)
	scoreRect = scoreSurf.get_rect()
	if not isGameOver:
		scoreRect.midtop  = (360,120)
	else:
		scoreRect.midtop = (80,10)
	playSurface.blit(scoreSurf, scoreRect)

def pauseOrResumeGame():
	global gamePaused
	gamePaused = not gamePaused

def startGame():
	global changeto, direction, snake, snakeBody, snakeHeadPos, foodPosition, foodSpawn, score
	init()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pauseOrResumeGame()
				if event.key == pygame.K_RIGHT or event.key == ord('d') or event.key == ord('D'):
					changeto = 'RIGHT'
				if event.key == pygame.K_LEFT or event.key == ord('a') or event.key == ord('A'):
					changeto = 'LEFT'
				if event.key == pygame.K_UP or event.key == ord('w') or event.key == ord('W'):
					changeto = 'UP'
				if event.key == pygame.K_DOWN or event.key == ord('s') or event.key == ord('s'):
					changeto = 'DOWN'

				if event.key == pygame.K_ESCAPE or event.key == ord('q') or event.key == ord('Q'):
					pygame.quit()
					sys.exit()

			#Validation
			if changeto == 'RIGHT' and not direction =='LEFT':
				direction = 'RIGHT'
			if changeto == 'LEFT' and not direction =='RIGHT':
				direction = 'LEFT'
			if changeto == 'UP' and not direction =='DOWN':
				direction = 'UP'
			if changeto == 'DOWN' and not direction =='UP':
				direction = 'DOWN'

		if not gamePaused:
			if direction == 'RIGHT':
				snakeHeadPos[0] += 10
			if direction == 'LEFT':
				snakeHeadPos[0] -= 10
			if direction == 'UP':
				snakeHeadPos[1] -= 10
			if direction == 'DOWN':
				snakeHeadPos[1] += 10

			# Snake Body
			snakeBody.insert(0,list(snakeHeadPos))

			# Snake eats food
			if snakeHeadPos[0] == foodPosition[0] and foodPosition[1] == snakeHeadPos[1]:
				foodSpawn = False
				score+=1
			else:
				snakeBody.pop()
			
			# Redraw food in new position
			if foodSpawn == False:
					foodPosition = [random.randrange(1,72) * 10, random.randrange(1,48) * 10]
			foodSpawn = True
			playSurface.fill(WHITE)

			for pos in snakeBody[1:]:
				pygame.draw.rect(playSurface,GREEN,pygame.Rect(pos[0],pos[1],10,10))

			pygame.draw.rect(playSurface,BLACK,pygame.Rect(pos[0],pos[1],10,10))
			pygame.draw.rect(playSurface,RED,pygame.Rect(snakeHeadPos[0],snakeHeadPos[1],10,10))
			
			# snake head in red
			pygame.draw.circle(playSurface, RED, (snakeHeadPos[0]+5, snakeHeadPos[1]+5), 8, 3)
			pygame.draw.rect(playSurface,BROWN,pygame.Rect(foodPosition[0],foodPosition[1],10,10))

			if snakeHeadPos[0] > 710 or snakeHeadPos[0] < 0 or snakeHeadPos[1] > 470 or snakeHeadPos[1] < 0:
				gameOver()

			for bodyParts in snakeBody[1:]:
				if snakeHeadPos[0] == bodyParts[0] and snakeHeadPos[1] ==  bodyParts[1]:
					gameOver()
		fpsController.tick(25)
		pygame.display.flip()
		showScore(True)
		pygame.display.flip() # Update ~ to repaint

def main():
	startGame()

if __name__ == "__main__":
	main()