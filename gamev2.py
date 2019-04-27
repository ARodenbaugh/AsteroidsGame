
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
HEIGHT = 700
img_dir = path.join(path.dirname(__file__), 'SpaceShooterRedux/PNG')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
screen.fill(BLACK)


# --- Classes

class Asteroid(pygame.sprite.Sprite):
    """ This class represents the asteroid. """

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

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.orig_image = pygame.transform.scale(player_img, (50, 38))
        self.image = self.orig_image
        self.orig_image.set_colorkey(BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.angle = 0
        self.distance = 0
        self.angle_offset = 0

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def get_angle(self):
        mouse = pygame.mouse.get_pos()
        offset = (self.rect.centerx-mouse[0],self.rect.centery-mouse[1])
        self.angle = math.degrees(math.atan2(*offset)) - self.angle_offset
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
        self.distance = math.sqrt((offset[0] * offset[0]) + (offset[1] * offset[1]))

    def update(self):
        self.get_angle()
        self.display = 'angle:{:.2f} disatance:{:.2f}'.format(self.angle, self.distance)

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

        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 20
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

# --- Sprite lists

# This is a list of every sprite. All asteroids and the player asteroid as well.
all_sprites_list = pygame.sprite.Group()

# List of each asteroid in the game
asteroid_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

bg = pygame.image.load("starbackground.jpg")

# --- Create the sprites

for i in range(10): #how many asteroids to create
    # This represents a asteroid
    asteroid = Asteroid(BLACK, 20, 15)

    # Set a random center location for the asteroid to orbit
    asteroid.center_x = random.randrange(WIDTH)
    asteroid.center_y = random.randrange(HEIGHT)
    # Random radius from 10 to 200
    asteroid.radius = random.randrange(10, 200)
    # Random start angle from 0 to 2pi
    asteroid.angle = random.random() * 2 * math.pi
    # radians per frame
    asteroid.speed = 0.01
    # Add the asteroid to the list of objects
    asteroid_list.add(asteroid)
    all_sprites_list.add(asteroid)

# Create a red player asteroid
player = Player()
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0
player.rect.y = 350
player.rect.x = 350



# -------- Main Program Loop -----------
while not done:
    player.update()
    player.render(screen)


    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True


        elif event.type == pygame.KEYDOWN:

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
    hits = pygame.sprite.spritecollide(player, asteroid_list, False)
    if hits:
        done = True

    # Call the update() method on all the sprites
    all_sprites_list.update()

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a asteroid
        asteroid_hit_list = pygame.sprite.spritecollide(bullet, asteroid_list, True)

        # For each asteroid hit, remove the bullet and add to the score
        for asteroid in asteroid_hit_list:
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
