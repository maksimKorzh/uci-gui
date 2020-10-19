#
# Web based GUI for BBC chess engine
#

# packages
from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine

# create web app instance
app = Flask(__name__)

# root(index) route
@app.route('/')
def root():
    return render_template('bbc.html')

# make move API
@app.route('/make_move', methods=['POST'])
def make_move():
    # create chess engine instance
    engine = chess.engine.SimpleEngine.popen_uci('./engine/bbc_1.3')
   
    # extract FEN string from HTTP POST request body
    fen = request.form.get('fen')

    # extract fixed depth value
    fixed_depth = request.form.get('fixed_depth')

    # extract move time value
    move_time = request.form.get('move_time')

    # init python chess board instance
    board = chess.Board(fen)
    
    # if move time is available
    if move_time != '0':
        if move_time == 'instant':
            try:
                # search for best move instantly
                info = engine.analyse(board, chess.engine.Limit(time=0.1))
            except:
                print('ERROR INSTANT!')
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
        
        # extract FEN from current board state
        fen = board.fen()
        
        # terminate engine process
        engine.quit()
        
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
            'fen': fen,
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
