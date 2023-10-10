import mysql.connector

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
