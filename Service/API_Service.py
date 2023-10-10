from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Alamat server utama
MAIN_SERVER_URL = 'https://8cjrhv6h-8000.asse.devtunnels.ms/api/bot'  # Ganti dengan alamat server Flask utama Anda

# Inisialisasi log chat
chat_log = []

# Endpoint untuk mengirim pesan dari pengguna ke server utama
@app.route('/api/bot', methods=['POST'])
def bot_api():
    try:
        user_message = request.json.get('user_message')

        # Simpan pesan dari pengguna ke log chat
        chat_log.append({'user': user_message, 'bot': ''})

        data = {'user_message': user_message}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(MAIN_SERVER_URL, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            bot_response = response_data.get('response')

            # Simpan respon bot ke log chat
            chat_log[-1]['bot'] = bot_response

            return jsonify({"bot_response": bot_response}), 200
        else:
            return jsonify({"error": f'{response.status_code} - {response.text}'}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mendapatkan log chat
@app.route('/api/bot/log', methods=['GET'])
def get_chat_log():
    return jsonify(chat_log)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)