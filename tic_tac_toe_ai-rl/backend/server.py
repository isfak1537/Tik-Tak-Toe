from flask import Flask, request, jsonify
from flask_cors import CORS
from game import TicTacToe
from rl_agent import RLAgent

app = Flask(__name__)
CORS(app)

game = TicTacToe()
agent = RLAgent()
stats = {'wins': 0, 'losses': 0, 'draws': 0}

@app.route('/reset', methods=['POST'])
def reset():
    try:
        data = request.get_json() or {}
        difficulty = data.get('difficulty', 'medium')
        agent.difficulty = difficulty
        
        game.reset()
        return jsonify({
            'board': game.board,
            'currentPlayer': game.current_player,
            'stats': stats,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        if not data or 'position' not in data:
            return jsonify({'error': 'Invalid move data'}), 400
            
        position = int(data['position'])
        
        if not game.make_move(position):
            return jsonify({'error': 'Invalid move'}), 400
            
        response = {
            'board': game.board,
            'gameOver': game.game_over,
            'winner': game.winner or None,
            'stats': stats  # Always include stats
        }
        
        if game.game_over:
            update_stats(game.winner)
            response['stats'] = stats
        else:
            state = game.get_state()
            valid_moves = game.get_valid_moves()
            ai_move = agent.get_action(state, valid_moves)
            game.make_move(ai_move)
            
            response.update({
                'board': game.board,
                'gameOver': game.game_over,
                'winner': game.winner or None,
                'aiMove': ai_move,
                'stats': stats  # Include for AI move
            })
            
            if game.game_over:
                update_stats(game.winner)
                response['stats'] = stats
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify(stats)

def update_stats(winner):
    if winner == 'X':
        stats['wins'] += 1
    elif winner == 'O':
        stats['losses'] += 1
    else:
        stats['draws'] += 1

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')