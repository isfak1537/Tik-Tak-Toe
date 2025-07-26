class TicTacToe:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        return self.get_state()
    
    def make_move(self, position):
        if self.game_over or self.board[position] != ' ':
            return False
        
        self.board[position] = self.current_player
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif ' ' not in self.board:
            self.game_over = True  # Draw
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]               # diagonals
        ]
        
        for combo in winning_combinations:
            a, b, c = combo
            if self.board[a] != ' ' and self.board[a] == self.board[b] == self.board[c]:
                return True
        return False
    
    def get_valid_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def get_state(self):
        return ''.join(self.board)
    
    def get_board(self):
        return self.board.copy()