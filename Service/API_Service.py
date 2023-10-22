from flask import Flask, request, jsonify, redirect
import requests

app = Flask(__name__)

MAIN_SERVER_URL = 'https://8cjrhv6h-8000.asse.devtunnels.ms/send-message'  # Ganti dengan alamat server Flask utama Anda
Database_URL = 'https://8cjrhv6h-8080.asse.devtunnels.ms/'

# Inisialisasi log chat
chat_log = []

# Endpoint untuk mengirim pesan dari pengguna ke server utama
@app.route('/api/bot', methods=['POST'])
def bot_api():
    try:
        user_message = request.json.get('user_message')

        data = {'user_message': user_message}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(MAIN_SERVER_URL, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            bot_response = response_data.get('response')

            # Simpan respon bot ke log chat
            # chat_log.append({'user': user_message, 'bot': bot_response})
            # message = ''

            # for chat in chat_log:
            #     message += chat['user'] + '\n' + chat['bot'] + '\n'

            # return jsonify({"response": message}), 200
            return jsonify({"response": bot_response}), 200
        else:
            return jsonify({"error": f'{response.status_code} - {response.text}'}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint untuk mendapatkan log chat
@app.route('/api/bot/log', methods=['GET'])
def get_chat_log():
    return jsonify(chat_log)

# Teruskan permintaan API makanan ke layanan API makanan Anda
# @app.route('/api/food/save_makanan', methods=['POST'])
# def food_save_makanan():
#     try:
#         # Teruskan permintaan ke API makanan
#         save_makanan = Database_URL + 'save_makanan'
#         response = requests.post(save_makanan, data=request.form)

#         if response.status_code == 200:
#             return jsonify(response.json()), 200
#         else:
#             return jsonify({"error": f'{response.status_code} - {response.text}'}), response.status_code

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Tambahkan rute API terkait makanan lainnya dengan cara yang sama...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
