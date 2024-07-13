from flask import Flask, request, jsonify
from threading import Lock
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

lock = Lock()
players = {}
choices = {}
last_result = None

def determine_winner(choices):
    app.logger.debug(f"Determine winner with choices: {choices}")
    p1, p2 = list(choices.keys())
    c1, c2 = choices[p1], choices[p2]
    if c1 == c2:
        return "Match nul !"
    elif (c1 == "rock" and c2 == "scissors") or (c1 == "scissors" and c2 == "paper") or (c1 == "paper" and c2 == "rock"):
        return f"{p1} gagne, {p2} perd!"
    else:
        return f"{p2} gagne, {p1} perd!"

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    player_id = data['player_id']
    choice = data['choice']
    
    app.logger.debug(f"Received choice {choice} from player {player_id}")

    with lock:
        if player_id not in players:
            players[player_id] = choice
            choices[player_id] = choice
            app.logger.debug(f"Current players: {players}")
            app.logger.debug(f"Current choices: {choices}")
            if len(players) == 2:
                winner = determine_winner(choices)
                result = {
                    "choices": choices.copy(),
                    "winner": winner
                }
                global last_result
                last_result = result
                app.logger.debug(f"Result calculated: {result}")
                players.clear()
                choices.clear()
                return jsonify(result), 200
            return jsonify({"message": "En attente du choix du joueur."}), 200
        else:
            return jsonify({"message": "Le joueur a déjà fait un choix."}), 400

@app.route('/result', methods=['GET'])
def result():
    global last_result
    app.logger.debug(f"Fetching last result: {last_result}")
    if last_result:
        return jsonify(last_result), 200
    else:
        return jsonify({"message": "No results available"}), 200

@app.route('/reset', methods=['POST'])
def reset():
    with lock:
        global last_result
        last_result = None
        players.clear()
        choices.clear()
        app.logger.debug("Game reset")
        return jsonify({"message": "Game reset"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)