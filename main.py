# Import library yang dibutuhkan
from flask import Flask, render_template, request, jsonify
import requests  # Untuk melakukan request HTTP ke News API

# Inisialisasi Flask App
app = Flask(__name__)

# Konfigurasi API dan Template HTML
NEWS_API_URL = "https://newsapi.org/v2/everything?domains=cnn.com&apiKey=9599d5760b4d4db3b8f40c459c4f3c9b"  
# URL untuk mengambil berita dari News API (gunakan API key Anda sendiri)

# Template HTML untuk halaman utama
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Website</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        body {
            padding: 20px;
        }
        .news-card {
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>CNN News</h1>
    <div id="news-container"></div>
    <div id="loading" style="text-align:center; margin-top:20px;">Loading...</div>

    <script>
    // Variabel untuk kontrol pagination dan loading
    let page = 1; 
    let loading = false;

    // Fungsi untuk memuat berita dari endpoint Flask
    function loadNews() {
        if (loading) return;  // Hindari request berulang saat loading
        loading = true;
        $.get(`/get_news?page=${page}`, function (data) {
            if (data.length > 0) {  // Jika terdapat artikel pada response
                data.forEach(article => {
                    const newsHTML = `
                        <div class="news-card">
                            <h4>${article.title}</h4>
                            <p>${article.description || ''}</p>
                            <a href="${article.url}" target="_blank">Read more</a>
                        </div>
                    `;
                    $('#news-container').append(newsHTML);  // Tambahkan artikel ke container
                });
                page++;  // Pindah ke halaman berikutnya
            } else {
                $('#loading').text('No more news available.');  // Tampilkan pesan jika tidak ada berita lagi
            }
            loading = false;
        });
    }

    // Event handler saat halaman siap
    $(document).ready(function () {
        loadNews();  // Muat berita saat halaman pertama kali dibuka
        $(window).on('scroll', function () {  // Muat berita saat scroll ke bawah
            if ($(window).scrollTop() + $(window).height() >= $(document).height() - 50) {
                loadNews();
            }
        });
    });
    </script>
</body>
</html>
"""

# Route untuk halaman utama
@app.route('/')
def index():
    return (HTML_TEMPLATE)  # Render HTML Template langsung

# Route untuk mengambil berita dari API
@app.route('/get_news')
def get_news():
    page = request.args.get('page', 1, type=int)  # Ambil parameter 'page' dari request
    response = requests.get(f"{NEWS_API_URL}&page={page}")  # Request berita ke News API
    if response.status_code == 200:  # Jika response berhasil
        news_data = response.json()  # Parse JSON response
        articles = news_data.get('articles', [])  # Ambil daftar artikel dari JSON
        return jsonify(articles)  # Kembalikan daftar artikel dalam bentuk JSON
    else:
        return jsonify([])  # Jika terjadi error, kembalikan array kosong

# Jalankan Flask App
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=3213)  # Aplikasi berjalan pada localhost dengan port 3213
