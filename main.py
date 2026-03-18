import os
import requests
import json
from google_play_scraper import Sort, reviews

# 1. AMBIL URL DARI SECRETS
url_google_sheets = os.environ.get('URL_GOOGLE_SHEETS') 
app_id_target = 'id.meteor.alfamind'

def kirim_data(sumber, isi):
    try:
        data = {"sumber": sumber, "isi": isi}
        requests.post(url_google_sheets, data=json.dumps(data), timeout=10)
    except:
        print("Gagal mengirim ke Sheets")

print("--- Memulai Robot Rekap Harian ---")

# --- TUGAS 1: AMBIL PLAY STORE (PASTI BERHASIL) ---
try:
    hasil, _ = reviews(app_id_target, lang='id', country='id', sort=Sort.NEWEST, count=5)
    for ulasan in hasil:
        label = "🔴" if ulasan['score'] <= 3 else "🟢"
        isi_rekap = f"[{label}] Bintang: {ulasan['score']} | {ulasan['content']}"
        kirim_data(f"Play Store - {ulasan['userName']}", isi_rekap)
    print("Rekap Play Store Selesai.")
except Exception as e:
    print(f"Error Play Store: {e}")

# --- TUGAS 2: STATUS TIKTOK (SEMENTARA) ---
# Kita beri catatan saja di Sheets agar kamu tahu robot TikTok masih 'standby'
kirim_data("System Monitor", "Robot TikTok sedang maintenance keamanan. Rekap manual Followers hari ini.")

print("--- Semua Proses Selesai ---")
