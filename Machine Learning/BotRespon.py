import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests

# Inisialisasi NLTK dan unduh corpus (data teks) yang dibutuhkan
nltk.download('punkt')
nltk.download('stopwords')

class BotResponses:
    def generate_bot_response(self, user_message):
        def respon_greeting(user_message):
            greetings = ["hi", "halo", "hai", "he", "hey", "mas", "bro", "p"]
            message_words = user_message.lower().split()

            if message_words and message_words[0] in greetings:
                return f"{message_words[0].capitalize()}! Ada yang bisa saya bantu?"
            return ""
            
        bot_response = respon_greeting(user_message)
        if bot_response == "":
            # Inisialisasi variabel kata_kunci_yang_ingin_dihapus untuk NLP tahap 2
            kata_kunci_yang_ingin_dihapus = ["berikan", "makanan", "rasa", "rekomendasi"]
            kata_permintaan_maaf = False
            perulangan = True

            while perulangan:
                # Tokenisasi input pengguna menjadi kata-kata
                kata_kata_input = word_tokenize(user_message)

                # Hapus kata-kata berhenti (stop words) + Kata yang ingin dihapus manual
                stop_words = set(stopwords.words('indonesian'))
                kata_kunci = [kata for kata in kata_kata_input if kata.lower() not in stop_words and kata.lower() not in kata_kunci_yang_ingin_dihapus]


                # Mendefinisikan URL API Flask yang akan dipanggil
                api_url = "https://8cjrhv6h-8080.asse.devtunnels.ms/search_food"

                # Mengirim permintaan GET ke API Flask dengan kata kunci sebagai parameter
                response = requests.get(api_url, params={"keywords": ",".join(kata_kunci)})

                # Memeriksa apakah permintaan berhasil
                if response.status_code == 200:
                    try:
                        # Mendapatkan data hasil dari API
                        result = response.json()
                        if result:
                            bot_response = "Mohon maaf, makanan tidak bisa ditemukan. Kami menyarankan makanan yang menyerupai seperti: " if kata_permintaan_maaf else "Makanan yang sesuai dengan kata kunci: "
                            bot_response += ", ".join(item['nama_makanan'] for item in result)
                        else:
                            bot_response = "Maaf, tidak ada data yang sesuai dengan pesan Anda."
                    except ValueError:
                        bot_response = "Maaf, respons dari server tidak valid."
                else:
                    bot_response = "Maaf, terjadi masalah saat menghubungi API Database"

                if result:
                    break  # Keluar dari loop jika hasil ditemukan
                else:
                    # Jika tidak ada hasil, hapus kategori terakhir
                    if kata_kunci:
                        kata_kunci_yang_ingin_dihapus.append(kata_kunci.pop())
                        kata_permintaan_maaf = True
                    else:
                        break  # Keluar dari loop jika tidak ada hasil dan tidak ada kategori yang dapat dihapus

            return bot_response
        return bot_response