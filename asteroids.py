
import pygame
import random
import math
from os import path

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 700
HEIGHT = 400
img_dir = path.join(path.dirname(__file__), 'SpaceShooterRedux/PNG')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()


# --- Classes

class Block(pygame.sprite.Sprite):
    """ This class represents the block. """

    def __init__(self, color, width, height):
        """ Constructor that create's the ball's image. """
        super().__init__()
        #self.image = pygame.Surface([width, height])
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        #self.image.fill(color)
        self.rect = self.image.get_rect()

        # The "center" the sprite will orbit
        self.center_x = 0
        self.center_y = 0

        # Current angle in radians
        self.angle = 0

        # How far away from the center to orbit, in pixels
        self.radius = 0

        # How fast to orbit, in radians per frame
        self.speed = 0.05

    def update(self):
        """ Update the ball's position. """
        # Calculate a new x, y
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y

        # Increase the angle in prep for the next round.
        self.angle += self.speed


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self, x, y):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)


        #self.rect = self.image.get_rect()

       # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0


    def changespeed(self, x, y):
       """ Change the speed of the player"""
       self.change_x += x
       self.change_y += y


    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        #pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        #self.rect.x = pos[0]
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y



class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set up the image for the bullet
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

    def update(self):
        """ Move the bullet. """

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


# --- Create the window
meteor_img = pygame.image.load(path.join(img_dir, "Meteors/meteorBrown_med1.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()

# Initialize Pygame
#pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
#screen = pygame.display.set_mode([screen_width, screen_height])

# --- Sprite lists

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# --- Create the sprites

for i in range(10): #how many blocks to create
    # This represents a block
    block = Block(BLACK, 20, 15)

    # Set a random center location for the block to orbit
    block.center_x = random.randrange(WIDTH)
    block.center_y = random.randrange(HEIGHT)
    # Random radius from 10 to 200
    block.radius = random.randrange(10, 200)
    # Random start angle from 0 to 2pi
    block.angle = random.random() * 2 * math.pi
    # radians per frame
    block.speed = 0.008
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a red player block
player = Player(50,50)
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
player.rect.y = 370



# -------- Main Program Loop -----------
while not done:


    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True

        # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               player.changespeed(-3, 0)
           elif event.key == pygame.K_RIGHT:
               player.changespeed(3, 0)
           elif event.key == pygame.K_UP:
               player.changespeed(0, -3)
           elif event.key == pygame.K_DOWN:
               player.changespeed(0, 3)

        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT:
               player.changespeed(3, 0)
           elif event.key == pygame.K_RIGHT:
               player.changespeed(-3, 0)
           elif event.key == pygame.K_UP:
               player.changespeed(0, 3)
           elif event.key == pygame.K_DOWN:
               player.changespeed(0, -3)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]
            mouse_y = pos[1]

            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)

            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

    # --- Game logic

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, block_list, False)
    if hits:
        done = True

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    # --- Draw a frame

    # Clear the screen
    screen.fill(WHITE)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
