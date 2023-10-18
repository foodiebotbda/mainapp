import mysql.connector
import hashlib
import os
import shutil

class DatabaseManager:
    def __init__(self):
        # Konfigurasi koneksi ke database MySQL
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan nama pengguna Anda
            port=3306,
            password="12345",  # Ganti dengan kata sandi Anda
            database="foodiebot"  # Ganti dengan nama database yang ingin Anda gunakan
        )
        self.cursor = self.connection.cursor()

    def hash_gambar(self, image_binary):
        # Menghitung hash dari gambar_binary
        return hashlib.md5(image_binary).hexdigest()

    def save_makanan(self, nama, tempat, image, harga, kategori_ids):
        try:
            # Menghitung hash dari gambar
            hash_gambar = self.hash_gambar(image)

            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
                                (nama, tempat, hash_gambar, harga))
            self.connection.commit()
            id_makanan = self.cursor.lastrowid

            for id_kategori in kategori_ids:
                self.cursor.execute("INSERT INTO Kategori_Makanan (id_kategori, id_makanan) VALUES (%s, %s)",
                                    (id_kategori, id_makanan))
                self.connection.commit()

            # Menyimpan gambar ke direktori lokal
            image_directory = "../gambar/"  # Ganti dengan direktori lokal yang Anda inginkan
            if not os.path.exists(image_directory):
                os.makedirs(image_directory)

            # menyimpan ke direktori lokal dengan nama asli

            # image_path = os.path.join(image_directory, image.filename)
            # image.save(image_path)

            # menyimpan ke direktori lokal dengan nama hash
            image_path = os.path.join(image_directory, hash_gambar + '.jpg')
            image.save(image_path)


            return True
        except Exception as e:
            print("Error:", str(e))
            return False

    def get_kategori_options(self):
        try:
            self.cursor.execute("SELECT deskripsi_makanan FROM Kategori")
            kategori_records = self.cursor.fetchall()
            kategori_options = [record[0] for record in kategori_records]
            return kategori_options
        except Exception as e:
            print("Error:", str(e))
            return []

    def get_kategori_id_by_description(self, description):
        try:
            self.cursor.execute("SELECT id_kategori FROM Kategori WHERE deskripsi_makanan = %s", (description,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print("Error:", str(e))
            return None

    def search_food_by_keywords(self, keywords):
        # Membuat string placeholder untuk klausa IN
        placeholders = ', '.join(['%s'] * len(keywords))

        # Eksekusi pernyataan SQL untuk mencari makanan berdasarkan kata-kunci yang relevan
        query = f"""
            SELECT m.nama_makanan
            FROM kategori_makanan AS km
            JOIN kategori AS k ON km.id_kategori = k.id_kategori
            JOIN makanan AS m ON km.id_makanan = m.id_makanan
            WHERE k.deskripsi_makanan IN ({placeholders})
            GROUP BY m.nama_makanan
            HAVING COUNT(DISTINCT k.deskripsi_makanan) = {len(keywords)}
        """
        self.cursor.execute(query, keywords)
        result = self.cursor.fetchall()

        return result

    def close_connection(self):
        # Menutup koneksi ke database MySQL
        self.connection.close()
