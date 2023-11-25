import mysql.connector
from cryptography.fernet import Fernet
import os

class DatabaseManager:
    
    def __init__(self):
        # Konfigurasi koneksi ke database MySQL
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan nama pengguna Anda
            port=3306,
            password="12345",  # Ganti dengan kata sandi Anda
            database="foodie"  # Ganti dengan nama database yang ingin Anda gunakan
        )
        self.cursor = self.connection.cursor()
        self.key = (b'bWP-ZLdoHNJ7c5ugSYBcelI7gKBC1OrJooAeUokxiqg=')
    
    def decrypt_string(self,encrypted_string):
        f = Fernet(self.key)
        decrypted = f.decrypt(encrypted_string).decode()
        return decrypted
    
    def save_makanan(self, nama, tempat, filename, harga, kategori_ids):
        try:
            # Menghitung hash dari gambar
            f = Fernet(self.key)
            encrypted = f.encrypt(filename.encode())

            self.cursor.execute("INSERT INTO Makanan (nama_makanan, tempat, gambar, harga) VALUES (%s, %s, %s, %s)",
                                (nama, tempat, encrypted, harga))
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
        
    def get_tempat_options(self):
        try:
            self.cursor.execute("SELECT tempat FROM makanan")
            tempat_records = self.cursor.fetchall()
            tempat_options = [record[0] for record in tempat_records]
            return tempat_options
        except mysql.connector.Error as e:
            print("Error:", str(e))
            return []
        
    def get_data(self):
        try:

            query = """
                SELECT k.deskripsi_makanan, m.nama_makanan, m.tempat, m.harga
                FROM kategori k
                JOIN kategori_makanan km ON k.id_kategori = km.id_kategori
                JOIN makanan m ON km.id_makanan = m.id_makanan
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        
        except mysql.connector.Error as e:
            print("Error:", str(e))
            return []
    
    def search_food_by_tempat(self, keywords):
        # Eksekusi pernyataan SQL untuk mencari makanan berdasarkan kata-kunci yang relevan
        query = """
            SELECT nama_makanan FROM makanan WHERE tempat = %s
        """
        self.cursor.execute(query, (keywords,))
        result = self.cursor.fetchall()

        return result

        
    
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
