from flask import Flask, request, jsonify
import traceback
import DatabaseManager as dbs
import os

# Anda mungkin perlu mengimpor DatabaseManager Anda di sini

app = Flask(__name__)

UPLOAD_FOLDER = '../gambar/'

# Inisialisasi objek DatabaseManager
db_manager = dbs.DatabaseManager()  # Pastikan DatabaseManager diimpor dengan benar

@app.route('/save_makanan', methods=['POST'])
def save_makanan():
    try:
        nama = request.form['nama']
        tempat = request.form['tempat']
        image = request.files['gambar']
        harga = request.form['harga']
        kategori_ids = request.form.getlist('kategori_ids[]')

        filename = image.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(save_path)

        success = db_manager.save_makanan(nama, tempat, image, harga, kategori_ids)

        if success:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Failed to save makanan"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/kategori_options', methods=['GET'])
def get_kategori_options():
    kategori_options = db_manager.get_kategori_options()
    return jsonify({"kategori_options": kategori_options})

@app.route('/kategori_id', methods=['GET'])
def get_kategori_id():
    description = request.args.get('description')
    id_kategori = db_manager.get_kategori_id_by_description(description)
    return jsonify({"id_kategori": id_kategori})

@app.route('/search_food', methods=['GET'])
def search_food():
    try:
        # Mendapatkan kata-kunci dari parameter query string
        keywords = request.args.get('keywords', '').split(',')

        # Inisialisasi result dengan nilai None
        result = None
        
        # Memanggil metode search_food_by_keywords dari objek DatabaseManager
        result = db_manager.search_food_by_keywords(keywords)

        if result:
            # Membuat daftar dari hasil
            result_list = [{"nama_makanan": item[0]} for item in result]
            return jsonify(result_list)
        else:
            return jsonify({"message": "Data tidak ditemukan"}), 404
    except Exception as e:
        traceback.print_exc()  # Mencetak traceback kesalahan untuk debugging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
