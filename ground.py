import pygame

class Ground(pygame.sprite.Sprite):
    # This class represents a Disc. It inherits the Sprite class of pygame

    def __init__(self, x, y):
        # Call parent class constructor
        super().__init__()

        self.x = x
        self.y = y
        # Create the pygame game object
        self.surf = pygame.image.load("C:/Users/rnm24/PycharmProjects/SoccerHead/Images/ground.png")
        self.rect = self.surf.get_rect()

        self.rect.bottomleft = (x, y)

    def draw(self):
        return self.surf, self.rect
