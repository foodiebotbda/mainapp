from flask import Flask, request, jsonify
import Database.DatabaseManager as dbs
import traceback

app = Flask(__name__)

# Inisialisasi objek DatabaseManager
db_manager = dbs.DatabaseManager()

@app.route('/search_food', methods=['GET'])
def search_food():
    try:
        # Mendapatkan kata-kunci dari parameter query string
        keywords = request.args.get('keywords', '').split(',')

        # Inisialisasi result dengan nilai None
        result = None
        
        # Memanggil metode search_food_by_keywords dari objek DatabaseManager
        result = db_manager.search_food_by_keywords(keywords)

        # Menutup koneksi setelah penggunaan
        db_manager.close_connection()

        if result:
            # Membuat daftar dari hasil
            result_list = [{"nama_makanan": item[0]} for item in result]
            return jsonify(result_list)
        else:
            return jsonify({"message": "Data tidak ditemukan"}), 404
    except Exception as e:
        traceback.print_exc()  # Mencetak traceback kesalahan untuk debugging
        return jsonify({"error": str(e)}), 500
    finally:
        # Selalu pastikan koneksi database ditutup, bahkan jika terjadi pengecualian
        db_manager.close_connection()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
