import pygame
import time  # Need this to use time function
from pygame.locals import *  # this is for event loop
import random # Need this for randint function

SIZE = 40  # coordinate of the block
BACKGROUND_COLOR = (50, 168, 129)
TOTAL_BALLS = 50


class Ball:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen  # This is the background of the game
        self.image0 = pygame.image.load("resources/ball0.png").convert()
        self.image1 = pygame.image.load("resources/ball1.jpg").convert()
        self.image2 = pygame.image.load("resources/ball2.png").convert()
        self.image3 = pygame.image.load("resources/ball3.jpg").convert()
        self.length = TOTAL_BALLS
        self.x = [0]*self.length
        self.y = [0]*self.length  # It has to be a multiple of the size or it won't allign
        for i in range(self.length):
            self.move(i)

    def draw(self):  # Dnt need the fill line bcz that'll happen in snake draw function
        j = 0
        for i in range(self.length):
            if j == 0:
                self.parent_screen.blit(self.image0, (self.x[i], self.y[i]))
            elif j == 1:
                self.parent_screen.blit(self.image1, (self.x[i], self.y[i]))
            elif j == 2:
                self.parent_screen.blit(self.image2, (self.x[i], self.y[i]))
            elif j == 3:
                self.parent_screen.blit(self.image3, (self.x[i], self.y[i]))
            j += 1
            if j > 3:
                j = 0

    def move(self, i_ball): # Need to move apple to a random position
        new_x = random.randint(1, 24)
        while new_x in self.x:
            new_x = random.randint(1, 24)

        new_y = random.randint(1, 18)
        while new_y in self.y:
            new_y = random.randint(1, 24)

        self.x[i_ball] = new_x * SIZE # It'll give me a number from 0 to 25 and it'll multiply by 40
        self.y[i_ball] = new_y * SIZE  # It'll give me a number from 0 to 25 and it'll multiply by 40


class Snake1:
    def __init__(self, parent_screen, length):  # input was the window, snake size
        self.parent_screen = parent_screen  # This is the background of the game
        self.image = pygame.image.load("resources/snake1_body.png").convert()  # img loadin
        self.head_right = pygame.image.load("resources/snake1_right.png").convert()
        self.head_left = pygame.image.load("resources/snake1_left.png").convert()
        self.head_up = pygame.image.load("resources/snake1_up.png").convert()
        self.head_down = pygame.image.load("resources/snake1_down.png").convert()
        self.direction = "right"  # default direction, if you write nothing then it won't move until press keyboard
        self.length = length
        self.x = [SIZE]*length  # This will create multiple blocks, if len 2 = [40, 40]
        self.y = [SIZE]*length  # initial position of the block

    def increase_length(self):
        self.length += 1  # increases the the length
        self.x.append(self.x[-1]+40)   # To update the list. The value doesn't matter bcz this value will change to prev block's value in walk function
        self.y.append(self.y[-1]+40)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):

        for i in range(self.length-1, 0, -1):  # It will count up till 0 bcz every block will follow self.x[0] (head of the snake)
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i - 1]


        # we need to
        if self.direction == "left":
            self.x[0] -= SIZE  # This is for the 1st (head of the snake) block.
            if self.x[0] < 0:
                self.x[0] = 960

        if self.direction == "right":
            self.x[0] += SIZE  # The difference is size bcz we want them to be 40 pixels apart
            if self.x[0] >= 1000:
                self.x[0] = 0

        if self.direction == "up":
            self.y[0] -= SIZE
            if self.y[0] < 0:
                self.y[0] = 720

        if self.direction == "down":
            self.y[0] += SIZE
            if self.y[0] >= 760:
                self.y[0] = 0

        self.draw()  # After changing coordinates these will draw the block at the new position

    def draw(self):  # To draw the snake on the surface

        for i in range(1, self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        if self.direction == "left":
            self.parent_screen.blit(self.head_left, (self.x[0], self.y[0]))

        if self.direction == "right":
            self.parent_screen.blit(self.head_right, (self.x[0], self.y[0]))

        if self.direction == "up":
            self.parent_screen.blit(self.head_up, (self.x[0], self.y[0]))

        if self.direction == "down":
            self.parent_screen.blit(self.head_down, (self.x[0], self.y[0]))


class Game:
    def __init__(self):
        pygame.init()  # To initialize pygame
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()  # for music
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 760))  # To set your window size (in pixels)
        self.game_over = pygame.image.load("resources/game over.jpg").convert()
        self.snake1 = Snake1(self.surface, 1)  # As the game will have snake, we need the snake function
        self.snake1.draw()
        self.ball = Ball(self.surface)
        self.ball.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE: # if we did x1 <= x2 + SIZE then jst by going around the apple, the length would increase
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_3.mp3")  # diff between music and sound is that music is long term
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")  # stores music
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/black_bg.jpg")
        self.surface.blit(bg, (0, 0))

    def reduce_balls(self):
        if self.ball.length > 5:
            max_snake_length = max(self.snake1.length, self.snake1.length)
            self.ball.length = TOTAL_BALLS - 5*(max_snake_length//10)



    def play(self):
        self.render_background()
        self.ball.draw()  # Will draw apple
        self.reduce_balls()
        self.snake1.walk()  # Will walk on its own. To stop walking too fast need to use timer.sleep method
        self.display_score()
        pygame.display.flip()

        # snake1 collide with ball
        for i in range(self.ball.length):
            if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.ball.x[i], self.ball.y[i]): # If collision apple moves
                self.play_sound("ding")
                self.snake1.increase_length()
                self.ball.move(i)


        # snake1 collide with snake2
        for i in range(1, self.snake1.length): # start with 0 cuz snake head can't collide with 1 and 2
            if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.snake1.x[i], self.snake1.y[i]):
                self.play_sound("boing")
                self.won = "Snake2"
                raise "Collision Occured"


    def display_score(self):
        font = pygame.font.SysFont("arial", 30) # To choose font size and color
        snake1_score = font.render(f"Snake1: {self.snake1.length}", True, (43, 255, 71)) # ("What to write", , font color)
        self.surface.blit(snake1_score, (100,10)) # Whenever u need to show something on the screen, u need to use blit

    def show_game_over(self, snake_num):
        self.render_background()
        font = pygame.font.SysFont("arial", 30, bold= True)
        # line1 = font.render(f"Congrats {snake_num}! You won!", True, (255, 255, 255))
        # self.surface.blit(line1, (340, 300))
        line2 = font.render(f"To play again press Enter. To escape press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (220, 340))
        self.surface.blit(self.game_over, (375, 250))
        pygame.display.flip() # if you want to show anything this is a must
        pygame.mixer.music.pause() # When game over, music pauses

    def reset(self):
        self.snake1 = Snake1(self.surface, 1)
        self.ball = Ball(self.surface)

    def run(self):  # run function is one of the main function
        # time.sleep(5)  # Window will only exit after 5 second even if click escape
        # event loop
        running = True
        pause = False
        # Set the end event to restart the music when it finishes
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:  # KEYDOWN came from import *
                    if event.key == K_ESCAPE:  # if you click esc window will stop running
                        running = False

                    if event.key == K_RETURN: # if press enter then restart game
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        # These are conditions to change position of block
                        # ------------------------
                        if event.key == K_LEFT:
                            self.snake1.move_left()

                        if event.key == K_RIGHT:
                            self.snake1.move_right()

                        if event.key == K_UP:
                            self.snake1.move_up()

                        if event.key == K_DOWN:
                            self.snake1.move_down()

                        # ------------------------
                elif event.type == pygame.USEREVENT:
                    # Restart the music when the end event is triggered
                    pygame.mixer.music.play()

                elif event.type == QUIT:
                    running = False  # If you click cross the window will stop running

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over(self.won)
                pause = True
                self.reset()

            if self.snake1.length > 20:
                time.sleep(0.09)
            else:
                time.sleep(0.12)  # Will walk every 0.2 sec. If dnt do this snake will move rlly fast


if __name__ == "__main__":
    game = Game()
    game.run()

