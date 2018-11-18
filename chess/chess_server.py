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
import json

from multiprocessing import Process

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

# Initialize a dictionary of chess game
games_dict = {}

def play(id, game_data):
    '''
    Determines what type of game to start.
    Returns the matrix representation of the board
    after a move.
    '''

    game_type = game_data["game_type"]
    if game_type == 'twoRandomBots':
        return play_two_bots(id, game_data)
    
    if game_type == "oneBotOneHuman":
        return play_one_bot_one_human(id, game_data)
    
    return "invalid game type"

def play_two_bots(id, game_data):
    '''
    Starts a game between two bots.
    Returns a matrix representation of the board
    after a move.
    '''
    global games_dict
    if game_data["new_game"] == "true" or game_data["new_game"] == True:
        if id in games_dict:
            games_dict.pop(id, None)

    if id in games_dict:
        chess_game = games_dict[id]["chess_game"]
        random_p = games_dict[id]["player"] 
    else:
        chess_game = game.Game(10, 8)
        random_p = players.RandomPlayer(chess_game)
        
        games_dict[id] = {}
        games_dict[id]["chess_game"] = chess_game
        games_dict[id]["player"] = random_p
        games_dict[id]["is_over"] = chess_game.get_game_ended()

    if not chess_game.get_game_ended():
        move = random_p.play()
        chess_game.get_next_state(chess_game.cur_player, move)
        random_p.promote_pawn()
        matrix_board = chess_game.convert_to_nums()

        if chess_game.cur_player == -1:
            matrix_board = np.flip(matrix_board, 0)

        chess_board = matrix_board

        games_dict[id]["chess_game"] = chess_game
        games_dict[id]["player"] = random_p
        games_dict[id]["is_over"] = chess_game.get_game_ended()
    else:
        chess_board = np.array([])
        games_dict.pop(id, None)
    
    return chess_board

def play_one_bot_one_human(id, game_data):
    global games_dict
    if game_data["new_game"] == "true" or game_data["new_game"] == True:
        if id in games_dict:
            games_dict.pop(id, None)

    if id in games_dict:
        chess_game = games_dict[id]["chess_game"]
        random_p = games_dict[id]["player"] 
    else:
        chess_game = game.Game(10, 8)
        print(chess_game.board.board)
        random_p = players.RandomPlayer(chess_game)
        
        games_dict[id] = {}
        games_dict[id]["chess_game"] = chess_game
        games_dict[id]["player"] = random_p
        games_dict[id]["is_over"] = chess_game.get_game_ended()
    
    print("starting game between human and bot")
    move = game_data["move"]
    old_pos = move[0]
    new_pos = move[1]

    legal_moves = chess_game.board.get_legal_actions(chess_game.cur_player)

    # Check whether the player made a valid move
    correct_move = None
    for cur_move in legal_moves:
        cur_pos = cur_move[0].pos
        if cur_pos[0] == old_pos[0] and cur_pos[1] == old_pos[1]:
            for action in cur_move[1]:
                pos_after_action = [old_pos[0] + action[0], old_pos[1] + action[1]]
                if new_pos[0] == pos_after_action[0] and new_pos[1] == pos_after_action[1]:
                    correct_move = (cur_move[0], action)
                    break
            
            if correct_move != None:
                break
    
    if correct_move == None:
        print("Invalid move")
        matrix_board = chess_game.convert_to_nums()
        
        if chess_game.cur_player == -1:
            matrix_board = np.flip(matrix_board, 0)
        print(matrix_board)
        return matrix_board
    
    # If the move was valid, then get the next state in the chess board
    chess_game.get_next_state(chess_game.cur_player, correct_move)
    random_p.promote_pawn()
    matrix_board = chess_game.convert_to_nums()

    # Then make the bot play a move
    if not chess_game.get_game_ended():
        move = random_p.play()
        chess_game.get_next_state(chess_game.cur_player, move)
        random_p.promote_pawn()
        matrix_board = chess_game.convert_to_nums()

        if chess_game.cur_player == -1:
            matrix_board = np.flip(matrix_board, 0)

        chess_board = matrix_board

        games_dict[id]["chess_game"] = chess_game
        games_dict[id]["player"] = random_p
        games_dict[id]["is_over"] = chess_game.get_game_ended()
    else:
        chess_board = np.array([])
        games_dict.pop(id, None)
    
    return chess_board

def on_request(ch, method, props, body):
    '''
    Response to a request from server.js for
    a board state.
    '''
    game_data = json.loads(body)
    chess_board = play(props.correlation_id, game_data)
    # import pdb; pdb.set_trace()
    if len(chess_board) == 0:
        response = "Game Over"
    else:
        response = chess_board.tolist()
    # print("Sent\n {}".format(response))

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print("[x] Awaiting RPC requests")
channel.start_consuming()

