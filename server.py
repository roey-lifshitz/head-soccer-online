# SERVER CODE
# creates a server, initialized each client and send and receives data from clients
from constants import *

import threading
import pickle
import time
from player import Player
from ball import Ball


"""
Create Socket
AF_INET- type of addresses that socket can communicate with (in this case ip4)
SOCK_STREAM- TCP socket - >
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Game objects and variables that are handled by the server
score = [0, 0]
connections = 0
client_id = 0
players = [Player(pygame.math.Vector2(0, 0), True), Player(pygame.math.Vector2(1864, 0), False)]
ball = Ball((pygame.math.Vector2(928, 714)))

def _print(msg):
    """
    display prints depending on DISPLAY_PRINT variable
    :param msg: String
    :return:
    """
    if DISPLAY_PRINT:
        print(msg)

def send(conn, info):
    """
    sends info to conn
    :param conn: socket, data destination
    :param info: game classes, what to send
    :return: None
    """

    conn.sendall(pickle.dumps(info))
    _print(f"[SENT] sent {info}")


def if_goal(id, line, top):
    global ball
    # Check if goal
    if id == 0:
        if ball.position.x > line:
            if ball.position.y > top:
                score[id] += 1
                ball = Ball((pygame.math.Vector2(928, 300)))
            else:
                ball.velocity.x = -ball.velocity.x

    else:
        if ball.position.x + ball.radius < line:
            if ball.position.y > top:
                score[id] += 1
                ball = Ball((pygame.math.Vector2(928, 300)))
            else:
                ball.velocity.x = -ball.velocity.x

def handle_client(conn, addr, client_id):
    """
    threaded function for each client that connects to server
    :param conn: socket, data destination
    :param addr: socket address, tuple (host, port)
    :param client_id: current client id
    :return: None
    """

    global players, ball, connections

    print(f"[New Connection] {addr} connected.\n")

    # Send initial data to clients
    if client_id == 0:
        data = {
            'player': players[0],
            'opponent': players[1]
        }
    else:
        data = {
            'player': players[1],
            'opponent': players[0]
        }
    data.update({'ball': ball, 'id': client_id, 'score': score, 'connection': connections})
    send(conn, data)

    connected = True
    while connected:
        reply = {'connections': connections}
        """" This block wait to receive information from the client,
         Processes the information, sends new information back to the client """
        try:
            # Blocking line of code until new information is received
            data = pickle.loads(conn.recv(4096))
            if data:
                players[client_id] = data['player']
                bound, dt = data['ball_data']
                opponent_goal_position = data['opponent_goal_position']

                # update ball according to sent data
                ball.update(players[client_id], bound, dt)

                if_goal(client_id, *opponent_goal_position)

            # send new data to clients

                if client_id == 0:
                    reply = {"player": players[1]}
                else:
                    reply = {"player": players[0]}
                reply.update({'ball': ball, 'score': score, 'connections': connections})

            send(conn, reply)

        except socket.error as e:
            print(e)

    conn.close()


_print("[Server is starting]")

def start():
    """
    Start function, listens for connections and creates a thread for each connection
    :return: None
    """
    global connections, client_id

    # Blocking line of code until someone tries to connect
    server.listen()
    while True:
        # Blocking line of code until a new connection is received
        conn, addr = server.accept()
        if client_id >= 2:
            print({"[Can not Connect, Two clients already connected"})
            break

        # Create a new thread for the client
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()

        client_id += 1
        connections = threading.active_count() - 1

        print(f"[Active Connections: {connections}]")

start()
