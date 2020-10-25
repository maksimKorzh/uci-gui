# Web based GUI for UCI chess engine
A simple web based GUI to play versus my engine BBC. You can replace BBC with whatever UCI chess engine and get the same result!

# PLAY ONLINE
[![IMAGE ALT TEXT HERE](https://github.com/maksimKorzh/uci-gui/blob/main/gui.png)](https://maksimkorzh.pythonanywhere.com)

# Features
 - online play
 - opening book in text format (from TSCP chess engine)
 - flip board
 - force computer move
 - fixed time mode
 - fixed depth mode
 - set FEN
 - download PGN
 
 # Used packages
 - Flask (minimalist WEB framework)
 - python-chess (chess library to communicate with engine over UCI protocol)
 - chessboardjs (chess board widget)
 - chessjs (chess library to keep track of the game state in the UI)
 
 # How to run it locally
  - install Python 3.6 or higher
  - install flask via "pip install flask"
  - install python chess via "pip install python-chess"
  - clone repo, cd into /src and run command "python app.py"
  - open browser, navigate to "localhost:5000"

# YouTube tutorials
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/_0uKZbHWVKM/0.jpg)](https://www.youtube.com/watch?v=_0uKZbHWVKM&list=PLmN0neTso3Jz-6--Mj51Hc3jiLhkQm0DB)
