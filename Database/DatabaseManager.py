import mysql.connector
import hashlib
import os

class DatabaseManager:
    
    def __init__(self):
        # Konfigurasi koneksi ke database MySQL
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan nama pengguna Anda
            port=3306,
            password="12345",  # Ganti dengan kata sandi Anda
            database="foodiebot2"  # Ganti dengan nama database yang ingin Anda gunakan
        )
        self.cursor = self.connection.cursor()

    def hash_gambar(self, image_binary):
        # Menghitung hash dari gambar_binary
        return hashlib.md5(image_binary).hexdigest()
    
    def generate_unique_filename(filename):
        import uuid
        _, ext = os.path.splitext(filename)
        unique_filename = str(uuid.uuid4()) + ext
        
        return unique_filename

    def save_makanan(self, nama, tempat, image, harga, kategori_ids):
        try:
            # Menghitung hash dari gambar
            image_binary = image.read()  # Membaca gambar sebagai biner
            hash_gambar = self.hash_gambar(image_binary)

            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
                                (nama, tempat, hash_gambar, harga))
            self.connection.commit()
            id_makanan = self.cursor.lastrowid

            for id_kategori in kategori_ids:
                self.cursor.execute("INSERT INTO Kategori_Makanan (id_kategori, id_makanan) VALUES (%s, %s)",
                                    (id_kategori, id_makanan))
                self.connection.commit()

            return True
        except mysql.connector.Error as e:
            print("Error:", str(e))
            return False

    def get_kategori_options(self):
        try:
            self.cursor.execute("SELECT deskripsi_makanan FROM Kategori")
            kategori_records = self.cursor.fetchall()
            kategori_options = [record[0] for record in kategori_records]
            return kategori_options
        except mysql.connector.Error as e:
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
        except mysql.connector.Error as e:
            print("Error:", str(e))
            return None

    def search_food_by_keywords(self, keywords):
        # Membuat string placeholder untuk klausa IN
        placeholders = ', '.join(['%s'] * len(keywords))

        # Eksekusi pernyataan SQL untuk mencari makanan berdasarkan kata-kunci yang relevan
        query = f"""
            SELECT m.nama_makanan
            FROM Kategori_Makanan AS km
            JOIN Kategori AS k ON km.id_kategori = k.id_kategori
            JOIN Makanan AS m ON km.id_makanan = m.id_makanan
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
