import pygame
from pygame.math import Vector2 as Vector


class Player(pygame.sprite.Sprite):
    # This class represents a Player. It inherits the Sprite class of pygame

    def __init__(self, position, facing_right, gravity=.35, friction=-.12):
        """
        Player Class:

        handles all player actions
        :param position: pygame.Math.Vector2(x, y), Players starting position
        :param facing_right: boolean
        :param gravity: float
        :param friction: float
        """
        # Call parent class constructor
        super().__init__()

        # image PATH
        image = pygame.image.load("Images/player.png")
        self.width, self.height = image.get_size()

        self.is_jumping, self.on_ground = False, False
        self.gravity = gravity
        self.friction = friction

        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.FACING_RIGHT = facing_right

        self.position = position
        self.x, self.y = self.position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, self.gravity)

    def limit_velocity(self, vel):
        """
        limits the x value of self.velocity by requested amount
        :param max_vel:
        :return: None
        """

        # the min() checks that the velocity isn't bigger than the max velocity- בדיקה כאשר מהירות חיובית
        # this max() checks that the velocity isn't smaller than - max velocity- בדיקה כאשר מהירות שלילית
        self.velocity.x = max(-vel, min(self.velocity.x, vel))
        # if velocity is really small, round it to 0
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def horizontal_movement(self, left, right, dt):
        """
        Handles the players horizontal movement using
        Newton's Equations of Motions:

        new velocity = previous velocity + acceleration * time
        new position = previous position + (velocity*time) + (.5*acceleration*(time^2))

        v = v0 + at
        x = x0 + vt + .5*a*(t^2)
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """
        # if keys not pressed than the default acceleration is 0
        self.acceleration.x = 0

        if self.RIGHT_KEY:
            self.acceleration.x += 1

        elif self.LEFT_KEY:
            self.acceleration.x -= 1

        """
        since self.friction has a negative multiplier,
        if a player is moving to a certain direction, the following line of code will simulate
        a force going to the opposite direction
        """
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(15)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)

        # Bound X position
        if self.position.x < left:
            self.acceleration.x = 0
            self.velocity.x = 0
            self.position.x = left

        if self.position.x > right - self.width:
            self.acceleration.x = 0
            self.velocity.x = 0
            self.position.x = right - self.width

        self.x = int(self.position.x)

    def vertical_movement(self, bottom, dt):
        """
        Handles the players vertical movement using
        Newton's Equations of Motions:

        new velocity = previous velocity + acceleration * time
        new position = previous position + (velocity*time) + (.5*acceleration*(time^2))

        v = v0 + at
        y = y0 + vt + .5*a*(t^2)
        :param bottom: int - bottom boundary
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """
        self.velocity.y += self.acceleration.y * dt

        # Limit Velocity
        if self.velocity.y > 15:
            self.velocity.y = 15

        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)

        # Bound Y Position
        if self.position.y > bottom:
            self.on_ground = True
            self.velocity.y = 0
            self.position.y = bottom

        self.y = int(self.position.y - self.height)

    def jump(self):
        """
        Makes player jump when called
        :return: None
        """
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 12
            self.on_ground = False

    def update(self, boundaries, dt):
        """
        updates players movement
        :param boundaries: tuple(left, right, top, bottom)
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """
        left, right, top, bottom = boundaries
        self.horizontal_movement(left, right, dt)
        self.vertical_movement(bottom, dt)

    def get_size(self):
        """
        returns Image's size
        :return: tuple (width, height)
        """
        return self.width, self.height

    def get_rect(self):
        """
        returns the rect of player
        :return: pygame.Rect(x, y, width, height)
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """
        Returns required data to draw the player
        :return: tuple (pygame.Image(), Rect(x, y, width, height)
        """

        # image PATH
        image = pygame.image.load(
            "Images/player.png")

        # rotate image
        if not self.FACING_RIGHT:
            image = pygame.transform.flip(image, True, False)

        return image, (self.x, self.y, self.width, self.height)
