from flask import Flask, request, jsonify
import BotRespon as botrespon

app = Flask(__name__)
bot = botrespon.BotResponses()

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        user_message = request.json.get('user_message')
        if not user_message:
            return jsonify({"message": "pesan tidak boleh kosong"}), 400

        # Generate a response using the bot instance
        response = bot.generate_bot_response(user_message)
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    # Start the Flask application using Waitress
    app.run(host='0.0.0.0', port=8000)

