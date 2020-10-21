#
# Web based GUI for BBC chess engine
#

# packages
from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine
import chess.pgn
import io

# create chess engine instance
engine = chess.engine.SimpleEngine.popen_uci('./engine/bbc_1.3')

# create web app instance
app = Flask(__name__)

# root(index) route
@app.route('/')
def root():
    return render_template('bbc.html')

# make move API
@app.route('/make_move', methods=['POST'])
def make_move():
    
   
    # extract FEN string from HTTP POST request body
    pgn = io.StringIO(request.form.get('pgn'))
    
    # read game moves from PGN
    game = chess.pgn.read_game(pgn)    
    
    # init board
    board = game.board()
    
    # loop over moves in game
    for move in game.mainline_moves():
        # make move on chess board
        board.push(move)
    
    # extract fixed depth value
    fixed_depth = request.form.get('fixed_depth')

    # extract move time value
    move_time = request.form.get('move_time')
    
    # if move time is available
    if move_time != '0':
        if move_time == 'instant':
            try:
                # search for best move instantly
                info = engine.analyse(board, chess.engine.Limit(time=0.1))
            except:
                info = {}
        else:
            try:
                # search for best move with fixed move time
                info = engine.analyse(board, chess.engine.Limit(time=int(move_time)))
            except:
                info = {}

    # if fixed depth is available
    if fixed_depth != '0':
        try:
            # search for best move instantly
            info = engine.analyse(board, chess.engine.Limit(depth=int(fixed_depth)))
        except:
            info = {}
    
    try:
        # extract best move from PV
        best_move = info['pv'][0]

        # update internal python chess board state
        board.push(best_move)
        
       
        
        # get best score
        try:
            score = -int(str(info['score'])) / 100
        
        except:
            score = str(info['score'])
            
            # inverse score
            if '+' in score:
                score = score.replace('+', '-')
            
            elif '-' in score:
                score = score.replace('-', '+')
          
        return {
            'fen': board.fen(),
            'best_move': str(best_move),
            'score': score,
            'depth': info['depth'],
            'pv': ' '.join([str(move) for move in info['pv']]),
            'nodes': info['nodes'],
            'time': info['time']
        }
    
    except:
        return {
            'fen': board.fen(),
            'score': '#+1'
        }

# main driver
if __name__ == '__main__':
    # start HTTP server
    app.run(debug=True, threaded=True)
    
    # terminate engine process
    engine.quit()
