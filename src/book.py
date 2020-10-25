import chess

# open book file
with open('./engine/book.txt') as f:
    # read book games
    book_raw = f.read()

    # define book variations
    book_variations = []

    # init board        
    board = chess.Board()

    # loop over book lines
    for line in book_raw.split('\n')[0:-1]:
        # define variation
        variation = []
        
        # loop over line moves
        for move in line.split():
            variation.append(chess.Move.from_uci(move))
        
        # append variation
        book_variations.append(board.variation_san(variation))

    print(book_variations[0])
            
