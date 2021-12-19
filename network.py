import socket
import pickle
from constants import *

DISPLAY_PRINT = False

class Network:

    def __init__(self):

        self.port = PORT
        self.host = HOST  # Automatically get local ip4 address
        self.addr = (self.host, self.port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    @staticmethod
    def print(msg):
        """
        prints messages according to DISPLAY_PRINT
        :param msg: String to print
        :return:
        """
        if DISPLAY_PRINT:
            print(msg)

    def connect(self):
        """
        connects to server and return initial data sent from server to help initialize client's game objects
        :return: dict{'player': Player(), 'opponent': Player(), 'ball': Ball(), 'id': int}
        """
        self.client.connect(self.addr)
        data = pickle.loads(self.client.recv(4096))
        self.print(str(data))
        return data

    def receive(self):
        """
        listen for data sent from server and return it
        :return: dict{'player': Player(), 'ball': Ball(), 'score': [int, int], 'connectios': int}
        """
        try:
            # Blocking line of code
            data = pickle.loads(self.client.recv(4096))
            self.print(f"[Received From Server] {str(data)}")
            return data
        except socket.error as e:
            print(e)

    def send(self, data):
        """
        sends data to server
        :param data: dict{'player': Player(), 'ball_data': [ball_boundaries, dt], 'opponent_goal_position' : double}
        :return: None
        """
        try:
            self.client.sendall(pickle.dumps(data))
            self.print(f"[Sent To Server] {str(data)}")
        except socket.error as e:
            print(e)

    def get(self, data):
        """
        sends data and returns servers reply
        :param data: dict{'player': Player(), 'ball_data': [ball_boundaries, dt], 'opponent_goal_position' : double}
        :return: dict{'player': Player(), 'ball': Ball(), 'score': [int, int], 'connectios': int}
        """
        self.send(data)
        return self.receive()
