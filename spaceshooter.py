import random
import math
from os import path
import os
import time
import contextlib
import pygame

# Initialize the game
pygame.init()
pygame.display.set_caption("testing")
# Define variables
myfont = pygame.font.SysFont("monospace", 20)
WIDTH = 700
HEIGHT = 800
black = (0, 0, 0)
green = (0,255,0)
clock = pygame.time.Clock()
frame_count = 0
frame_rate = 60
# Space ship variables
x = 50
y = 50
vel = 15
direction = "Right"

# Create a sized screen
screen = pygame.display.set_mode([700, 800])
# set the name of the window
pygame.display.set_caption('Space Shooter')

# initialize pygame and load images
pygame.mixer.init()
clock = pygame.time.Clock()
background_position = [0, 0]
background_image = pygame.image.load("starbackground.jpg").convert()
ship_img = pygame.image.load("playerShip2_green.png").convert()
bullet = pygame.image.load("laserGreen15.png").convert()
bullet_img = pygame.transform.scale(bullet, (17,17))
meteor_images = []
meteor_list = [
    'meteorBrown_big2.png',
    'meteorBrown_big3.png',
    'meteorBrown_med3.png',
    'meteorBrown_tiny1.png',
    'meteorBrown_small1.png'
]
for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join("meteor_images", image)).convert())

# load the game sounds
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join('sounds', filename))

die_sound = load_sound('die.wav')
asteroid_sound = load_sound('asteroid.wav')
missile_sound = load_sound('laser.wav')
missile_sound.set_volume(.7)
soundtrack = load_sound('soundtrack.wav')
soundtrack.set_volume(.3)
soundtrack.play()


# --- Classes
class Asteroid(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location."""
        self.rect.y = random.randrange(-1000, -10)
        self.rect.x = random.randrange(0, WIDTH)

    def update(self):
        """ Called each frame. """
        # Move block down one pixel
        self.rect.y += 8
        # If block is too far down, reset to top of screen.
        if self.rect.y > 810:
            self.reset_pos()


class Ship(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.transform.scale(ship_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = x
        self.rect.y = 740

    # Move ship side to side
    def animate(self, x, direction):
        self.rect.y = 740
        if x < 0:
            direction = 'Right'
        elif x > 650:
            direction = 'Left'
        if direction == 'Right':
            x += vel
        elif direction == 'Left':
            x -= vel
        self.rect.x = x
        return x, direction


class Bullet(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, dest_x, dest_y):
        super().__init__()

        # Set up the image for the bullet
        self.image = bullet_img
        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 30
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

    def update(self):
        # The floating point x and y hold accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, kill it
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


# --- Sprite lists
# This is a list of every sprite. All asteroids and the ship asteroid as well.
all_sprites_list = pygame.sprite.Group()
# List of each asteroid in the game
asteroid_list = pygame.sprite.Group()
# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the asteroids
for i in range(100): # how many asteroids to create
    # This represents a asteroid
    asteroid = Asteroid()

    # Set a random center location for the asteroid to orbit
    asteroid.rect.x = random.randrange(0, WIDTH)
    asteroid.rect.y = random.randrange(-5000, HEIGHT-500)

    # Add the asteroid to the list of objects
    asteroid_list.add(asteroid)
    all_sprites_list.add(asteroid)

# Create a ship
ship = Ship()
all_sprites_list.add(ship)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# keep track of stats
score = 1
shots = 1
ticks=pygame.time.get_ticks() #starter tick

# -------- Main Program Loop -----------
RUNNING, PAUSE = 0, 1
state = RUNNING
while not done:

    # Draw background image
    screen.blit(background_image, background_position)

    # Update ship position
    x, direction = ship.animate(x, direction)
    seconds=(pygame.time.get_ticks())/1000 #calculate how many seconds

    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True

        # if a key is pressed
        elif event.type == pygame.KEYDOWN:
            # if the space bar is pressed - shoot
            if event.key == pygame.K_SPACE:
                #pos = pygame.mouse.get_pos()
                #mouse_x = pos[0]
                #mouse_y = pos[1]

                # Create the bullet based on where we are, and where we want to go.
                bullet = Bullet(ship.rect.x, ship.rect.y, x, 0) # replaced mouse_x, mouse_y with x, y
                missile_sound.play()
                shots +=1
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)

    # -- Show Stats and Countdown Timer
    output_string = "Time Remaining: {0:.2f}".format(30-seconds,4)
    # Exit game if timer ends
    if seconds > 30:
        done=True
    text = myfont.render(output_string, True, green)
    screen.blit(text, (400, 10))
    scoretext = myfont.render("Score: {0}".format(score), 1, (green))
    screen.blit(scoretext, (5, 10))
    shotstext = myfont.render("Shooting Percentage: {:.1%}".format(score/shots), 1, (green))
    screen.blit(shotstext, (5, 35))

    # check to see if an asteroid hit the ship
    hits = pygame.sprite.spritecollide(ship, asteroid_list, False)
    if hits:
        die_sound.play()
        done = True

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit an asteroid
        asteroid_hit_list = pygame.sprite.spritecollide(bullet, asteroid_list, True)

        # For each asteroid hit, remove the bullet and add to the score
        for asteroid in asteroid_hit_list:
            score += 1
            asteroid_sound.play()
            asteroid.reset_pos()
        for bullet in asteroid_hit_list:
            bullet_list.remove(bullet)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # Draw all the spites
    all_sprites_list.draw(screen)
    frame_count += 1
    # Limit frames per second
    clock.tick(frame_rate)

    # update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(20)

print("\n\n==============================================\n")
print("GAME OVER!!!!!\nFinal Score: " + str(score) + "\nShooting Percentage: {:.1%}".format(score/shots))
print("\n==============================================\n")

pygame.quit()

# Code adapted and modified from modules demonstrated in: http://programarcadegames.com/index.php?chapter=example_code
