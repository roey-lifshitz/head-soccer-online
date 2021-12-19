# CLIENT CODE
# handles the game loop for each client
from constants import *

import time

from network import Network
from ground import Ground
from goal import Goal

# Game Objects and variables that are handled by the client
goals = [Goal(-100, 480, False), Goal(SCREEN_WIDTH - 150, 480, True)]
font = pygame.font.Font('freesansbold.ttf', 32)


class Client:

    def __init__(self):

        self.server = Network()
        initial_data = self.server.connect()

        # initialize data from server
        self.player, self.opponent, self.ball, self.id, self.score, self.connected = initial_data.values()

        # id = if player one or player two
        # Camera margin- the initial position of camera
        if self.id == 0:
            self.player_goal, self.opponent_goal = goals
            self.camera_margin = (SCREEN_WIDTH / 2 - self.player.x) / 3
        else:
            self.opponent_goal, self.player_goal = goals
            self.camera_margin = (SCREEN_WIDTH / 2 - (self.player.x + self.player.width)) / 3

        self.ground = Ground(0, SCREEN_HEIGHT)
        self.ground.rect.move_ip(-SCREEN_WIDTH//3, 0)

        # create screens
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE)
        # draw everything on fake_screen then draw fake_screen on screen to make drawn stuff resizable
        self.fake_screen = self.screen.copy()

        self.bg = pygame.image.load("Images/bg.jpg")
        self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, int(SCREEN_HEIGHT * 1.5)))


        # FPS clock, limits max fps
        self.clock, self.target_fps = pygame.time.Clock(), TARGET_FPS
        # Loop boolean
        self.exit = False

        self.loop()

    @staticmethod
    def _print(msg):
        if DISPLAY_PRINT:
            print(msg)

    @staticmethod
    def play_music():
        # Pl
        song = "Audio/background_song.mp3"
        pygame.mixer.init() # initialize mixer
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1) # -1 -> infinite

    def handle_events(self):
        """"
        handle
        events: keyboard, mouse, etc.
        """
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.exit = True

            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, RESIZABLE)
        # ---------------------------------------------------------
            elif event.type == pygame.KEYDOWN:

                if event.key == K_RIGHT:
                    self.player.RIGHT_KEY = True
                    self.player.FACING_RIGHT = True

                if event.key == K_LEFT:
                    self.player.LEFT_KEY = True
                    self.player.FACING_RIGHT = False

                if event.key == K_UP:
                    self.player.jump()

                if event.key == K_ESCAPE:
                    self.exit = True
        # -----------------------------------------------------------
            elif event.type == pygame.KEYUP:

                if event.key == K_RIGHT:
                    self.player.RIGHT_KEY = False

                if event.key == K_LEFT:
                    self.player.LEFT_KEY = False

                if event.key == K_UP:
                    if self.player.is_jumping:
                        # if player moving upwards
                        if self.player.velocity.y < 0:
                            # make velocity smaller so player would stop moving upwards
                            self.player.velocity.y *= .25
                            self.player.is_jumping = False
                            self.player.JUMP_KEY = False
        # ------------------------------------------------------------

    def draw(self, waiting, t, *objects):
        """
        NOTE: all objects have a draw() function that returns (pygame.Image(), pygame.Rect())
        :param t: time since start of game
        :param waiting: boolean, if 2 players connected to server
        :param objects: Tuple() of either Player(), Ground(), Ball(), Goal() classes
        :return:
        """
        self.fake_screen.blit(self.bg, (0, -220))

        # loop through all objects
        for _object in objects:
            # get the (surf, rect) of object
            n = _object.draw()
            # get the x,y values of the rect inside n
            # n[1] = pygame.Rect(x, y, width, height)
            x = n[1][0]
            y = n[1][1]
            width = n[1][2]
            height = n[1][3]
            # draw surface on screen, adds the camera_margin to create a moving camera effect
            self.fake_screen.blit(n[0], (int(x + self.camera_margin), int(y), width, height))

        # Draw the goals post at the end to create illusion ball is inside the goal
        post = self.player_goal.draw_post()
        self.fake_screen.blit(post[0], (post[1][0] + int(self.camera_margin), post[1][1]))
        post = self.opponent_goal.draw_post()
        self.fake_screen.blit(post[0], (post[1][0] + int(self.camera_margin), post[1][1]))

        # Draw txt
        first_score = font.render("Score: " + str(self.score[0]), False, (255, 255, 255))
        second_score = font.render("Score: " + str(self.score[1]), True, (255, 255, 255))
        # convert to h:m:s
        t = time.strftime("%H:%M:%S", time.gmtime(t))
        time_txt = font.render(str(t), False, (255, 255, 255))

        self.fake_screen.blit(first_score, (0, SCREEN_HEIGHT - first_score.get_height() - 50))
        self.fake_screen.blit(second_score, (SCREEN_WIDTH - second_score.get_width(), SCREEN_HEIGHT - second_score.get_height() - 50))
        self.fake_screen.blit(time_txt, (int(SCREEN_WIDTH/2 - time_txt.get_width()/2), 20))

        if waiting:
            msg = font.render("Waiting for players", False, (255, 255, 255))
            x = int(SCREEN_WIDTH / 2 - msg.get_width() / 2)
            y = int(SCREEN_HEIGHT / 2 - msg.get_height() / 2)
            self.fake_screen.blit(msg, (x, y))

        # Draw fake_screen on screen
        self.screen.blit(pygame.transform.scale(self.fake_screen, self.screen.get_rect().size), (0, 0))
        pygame.display.flip()

    def loop(self):
        """
        GAME LOOP:
        responsible for every frame in game
        :return: None
        """

        # self.play_music()

        start_time = time.time()
        # Constant variables of game loop
        player_boundaries = [0, SCREEN_WIDTH - self.player.width, 0, SCREEN_HEIGHT - self.ground.rect.height]
        ball_boundaries = [0, SCREEN_WIDTH - self.ball.radius * 2, 0, SCREEN_HEIGHT - self.ground.rect.height]

        # if not two players connected
        while self.connected < 2:
            self.handle_events()
            self.draw(True, time.time() - start_time, self.ground, self.player_goal, self.opponent_goal)
            self.clock.tick(self.target_fps)
            data = self.server.get({})
            self.connected = data['connections']

        start_time = time.time()
        prev_time = time.time()

        while self.exit is False:
            self.handle_events()

            # Calculate Delta Time
            """
            What is Delta Time?
            delta_time or dt is a float that represents the number of seconds passed between each frame
            every movement  is multiplied by dt to create movement that isnt dependent on framerate
            dt is multiplied by the TARGET_FPS velocities wont have to be multiplied by TARGET_FPS           
            """
            now = time.time()
            dt = (now - prev_time) * self.target_fps
            prev_time = now

            self.player.update(player_boundaries, dt)
            self.camera_margin -= self.player.velocity.x * .5

            # what to send to server
            sent_info = {
                'player': self.player,
                'ball_data': [ball_boundaries, dt],
                'opponent_goal_position': self.opponent_goal.goal_line_position
            }

            # send to server and receive what server has sent
            received_info = self.server.get(sent_info)

            self.opponent = received_info['player']
            self.ball = received_info['ball']
            self.score = received_info['score']

            self.draw(False, now-start_time, self.player, self.opponent, self.ground, self.player_goal, self.opponent_goal, self.ball)
            self.clock.tick(self.target_fps)


client = Client()

