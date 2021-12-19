import pygame
from pygame.math import Vector2 as Vector

class Ball(pygame.sprite.Sprite):
    # This class represents a Disc. It inherits the Sprite class of pygame

    def __init__(self, position, gravity=.20, friction=-.025):
        # Call parent class constructor
        super().__init__()

        self.radius = self.get_radius()

        self.on_ground = False
        self.gravity = gravity
        self.friction = friction

        self.position = position
        self.x, self.y = self.position
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, self.gravity)

    def collision(self, rect):
        return self.get_rect().colliderect(rect) == 1

    def dist(self, player):
        """
        Check if ball is close to player to allow more forgiving ball movement
        :param player: Player()
        :return: boolean
        """
        dist_x = abs((self.position.x + self.radius) - (player.position.x + player.width/2))
        dist_y = abs((self.position.y + self.radius) - (player.position.y + player.height / 2))
        return dist_x < 60 and dist_y < 40

    def horizontal_movement(self, player, dt):
        """
        Handles the players horizontal movement using
        Newton's Equations of Motions:
        new velocity = previous velocity + acceleration * time
        new position = previous position + (velocity*time) + (.5*acceleration*(time^2))
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """
        # if keys not pressed than the default acceleration is 0
        self.acceleration.x = 0

        if self.collision(player.get_rect()):
            if player.LEFT_KEY or player.RIGHT_KEY:
                self.acceleration.x += player.acceleration.x / 2
                self.velocity.x += player.velocity.x

            else:
                self.acceleration.x = -self.acceleration.x / 2
                self.velocity.x = -self.velocity.x

        """
        since self.friction has a negative multiplier,
        if a player is moving to a certain direction, the following line of code will simulate
        a force going to the opposite direction
        """
        if self.on_ground:
            self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.x = int(self.position.x)

    def vertical_movement(self, player, bottom, dt):
        """
        Handles the players vertical movement using
        Newton's Equations of Motions:
        new velocity = previous velocity + acceleration * time
        new position = previous position + (velocity*time) + (.5*acceleration*(time^2))
        :param bottom: int - bottom boundary
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """

        if self.dist(player):
            if player.is_jumping:
                self.velocity.y = player.velocity.y * 1.2

            else:
                self.velocity.y = -self.velocity.y

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
        else:
            self.on_ground = False
        self.y = self.position.y - self.radius


    def update(self, player, boundaries, dt):
        pass
        """
        updates players movement
        :param boundaries: tuple(left, right, top, bottom)
        :param dt: float - Multiplier that makes up for loss of frames
        :return: None
        """
        left, right, top, bottom = boundaries
        self.horizontal_movement(player, dt)
        self.vertical_movement(player, bottom, dt)


    def get_radius(self):
        image = pygame.image.load(
            "Images/ball.png")
        return image.get_width()/2

    def get_rect(self):
        radius = self.get_radius()
        return pygame.Rect(self.x, self.y, radius, radius)


    def draw(self):
        image = pygame.image.load(
            "Images/ball.png")

        radius = image.get_width()/2
        return image, (int(self.x), int(self.y), int(radius), int(radius))


