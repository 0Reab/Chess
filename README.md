# Chess

Chess built from scratch in Python, OOP style. Has a web frontend served locally.

## Structure

```
Chess/
├── game.py      # game loop, move validation, turn management
├── board.py     # board, files, diagonals, path logic
├── pieces.py    # piece types and properties
├── squares.py   # square model + notation
├── tests.py     # tests
└── server/      # local web server + HTML/CSS/JS frontend
```

## Running it

```bash
git clone https://github.com/0Reab/Chess.git
cd Chess
python server/server.py
```

Then open `http://localhost:<port>` in your browser.

## Implemented

- Move validation for all pieces
- Check, double check, pins
- Castling (with checks-through-path validation)
- Pawn promotion (queen only)
- Web UI rendered from White's perspective

## TODO

- En passant
- Stalemate detection
- Draw conditions (50-move, threefold repetition, etc.)
- Promotion choice (currently always queens)
- Game over screen
- Matchmaking via code
- Security auditing :)
