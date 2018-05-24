'''
Starts a chess game when server.js sends a request. 
Each response contains the board orientation after 
each move.
'''
import sys
sys.path.append('chess')
import numpy as np
import time
import pika


import ChessLogic as logic
import ChessGame as game
import ChessPieces as piece
import ChessPlayers as players
import ChessBoard as board

HOST='localhost'
np.random.seed(0)

# Initialize pika queues
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

# Initialize chess game
test_game = game.Game(10, 8)
random_p = players.RandomPlayer(test_game)
whites_turn = True

def play(game_type):
    '''
    Determines what type of game to start.
    Returns the matrix representation of the board
    after a move.
    '''
    game_type = game_type.decode("utf-8")
    if game_type == 'two random bots':
        return play_two_bots()
    
    return "invalid game type"

def play_two_bots():
    '''
    Starts a game between two bots.
    Returns a matrix representation of the board
    after a move.
    '''
    global test_game
    global random_p
    global whites_turn

    move = random_p.play()
    test_game.get_next_state(test_game.cur_player, move)
    random_p.promote_pawn()
    matrix_board = test_game.convert_to_nums()
    if not whites_turn:
        matrix_board = np.flip(matrix_board, 1)
        whites_turn = True
    else:
        whites_turn = False
    
    return np.transpose(matrix_board)

def on_request(ch, method, props, body):
    '''
    Response to a request from server.js for
    a board state.
    '''
    game_type = body

    response = play(game_type)
    print("Sent\n {}".format(response))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" [x] Awaiting RPC requests")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print("[x] Awaiting RPC requests")
channel.start_consuming()

