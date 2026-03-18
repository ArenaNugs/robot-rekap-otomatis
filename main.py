import requests
import json
from google_play_scraper import Sort, reviews

# 1. Konfigurasi
app_id_target = 'id.meteor.alfamind'
url_google_sheets = "https://script.google.com/macros/s/AKfycbwzBYtPJMXExkkclUIOcCoeDXjmuVypbRutfazsQc4D7qi6X9SKTJbx5_Q1cGvTftxe/exec" # Isi kembali dengan URL milikmu

print("Robot sedang bekerja menganalisis ulasan...")

# 2. Ambil 10 ulasan terbaru
hasil, _ = reviews(app_id_target, lang='id', country='id', sort=Sort.NEWEST, count=10)

# 3. Proses Analisis Otomatis
for ulasan in hasil:
    skor = ulasan['score']
    komentar = ulasan['content']
    user = ulasan['userName']
    
    # LOGIKA MONITORING: Jika bintang 1, 2, atau 3, beri label peringatan
    if skor <= 3:
        status_rekap = "🔴 PERLU FOLLOW UP (Rating Rendah)"
    else:
        status_rekap = "🟢 Aman (Rating Bagus)"
    
    # Susun data untuk dikirim
    data_untuk_dikirim = {
        "sumber": f"Play Store - {user}",
        "isi": f"[{status_rekap}] | Bintang: {skor} | Pesan: {komentar}"
    }
    
    # Kirim ke Google Sheets
    requests.post(url_google_sheets, data=json.dumps(data_untuk_dikirim))

print("Analisis selesai! Cek Google Sheets kamu untuk melihat label otomatisnya.")
