import pygame

class Goal(pygame.sprite.Sprite):
    # This class represents a Goalpost. It inherits the Sprite class of pygame

    def __init__(self, x, y, flip=False):
        """
        Goal Object consists of the goal and a post so the goal will be drawn
        behind the ball and the post before the ball creating the illusion the ball is in the goal
        :param x: int
        :param y: int
        :param flip: boolean
        """
        # Call parent class constructor
        super().__init__()

        self.x = x
        self.y = y

        # Initialize Goal
        self.surf = pygame.image.load("Images/goal.png")
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = x, y

        # Initialize Post
        self.post = pygame.image.load("Images/post.png")
        self.post_rect = self.post.get_rect()

        # Position Post
        self.post_rect.right = self.rect.right
        self.post_rect.bottom = self.rect.bottom


        self.goal_line_position = self.rect.right, self.rect.top -10

        # Change Position if needed to fliip
        if flip:
            # Flip images
            self.surf = pygame.transform.flip(self.surf, True, False)
            self.post = pygame.transform.flip(self.post, True, False)

            # Reposition post and goal line
            self.post_rect.left = self.rect.left
            self.goal_line_position = self.rect.left, self.rect.top - 10


    def get_rect(self):
        rect = pygame.Rect(self.rect.left, -100, 0, self.rect.height*3)
        return rect

    def draw_post(self):
        return self.post, self.post_rect

    def draw(self):
        return self.surf, self.rect

