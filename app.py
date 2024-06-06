from flask import Flask, jsonify, render_template
import asyncio
import aiohttp
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import atexit
import logging
import time

# Initialisasi logging
logging.basicConfig(level=logging.INFO)

# Inisialisasi aplikasi Flask
app = Flask(__name__, template_folder='html', static_folder='css')

# List URL Web yang akan dicek
urls = [
    'https://ittelkom-sby.ac.id/',
    'https://www.unpad.ac.id',
    'https://www.itb.ac.id',
    'https://www.upi.edu',
    'https://www.uinsgd.ac.id',
    'https://www.telkomuniversity.ac.id',
    'https://www.unpar.ac.id',
    'https://www.unpas.ac.id',
    'https://www.unikom.ac.id',
    'https://www.widyatama.ac.id',
    'https://www.unla.ac.id',
    'https://www.unjani.ac.id',
    'https://www.umbandung.ac.id',
    'https://www.unai.edu',
    'https://www.unisba.ac.id',
    'https://www.unfari.ac.id',
    'https://www.unsil.ac.id',
    'https://www.unsika.ac.id',
    'https://www.unsub.ac.id',
    'https://www.uniku.ac.id',
    'https://www.unma.ac.id',
    'https://www.unswagati.ac.id',
    'https://www.ucic.ac.id',
    'https://www.pelitabangsa.ac.id',
    'https://www.unpam.ac.id',
    'https://www.untara.ac.id',
    'https://www.binus.ac.id',
    'https://www.president.ac.id',
    'https://www.uph.edu',
    'https://www.upj.ac.id',
    'https://www.umn.ac.id',
    'https://www.unis.ac.id',
    'https://www.unma.ac.id',
    'https://www.unbaja.ac.id',
    'https://www.unsera.ac.id',
    'https://www.untirta.ac.id',
    'https://www.prasetiyamulya.ac.id',
    'https://www.mercubuana.ac.id',
    'https://www.untagcirebon.ac.id',
    'https://www.unas.ac.id',
    'https://www.pasim.ac.id',
    'https://www.unwim.ac.id',
    'https://www.ubharajaya.ac.id',
    'https://www.unnur.ac.id',
    'https://www.uninus.ac.id',
    'https://www.satyagama.ac.id',
    'https://www.untad.ac.id/'
]

# untuk menyimpan status setiap URL
status_data = {}

# Fungsi asinkronus untuk mengecek status setiap website
async def fetch_status(session, url):
    try:
        async with session.get(url, timeout=10, allow_redirects=False) as response:
            if response.status == 200:
                status_data[url] = 'UP'
            elif 300 <= response.status <= 400:
                status_data[url] = 'REDIRECT'
            else:
                status_data[url] = 'DOWN'
    except (aiohttp.ClientError, asyncio.TimeoutError):
        status_data[url] = 'DOWN'
    except Exception as e:
        logging.error(f"Error checking {url}: {e}")
        status_data[url] = 'DOWN'

# Fungsi asinkronus untuk mengecek status semua website secara bersamaan
async def check_website_status():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            # Set interval pengecekan berdasarkan status
            interval = 60 if status_data.get(url) == 'UP' else 30
            tasks.append(fetch_status(session, url))
        await asyncio.gather(*tasks)

# Inisialisasi penjadwalan
scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(func=lambda: asyncio.run(check_website_status()), trigger="interval", seconds=60)
scheduler.start()

# Penjadwalan akan berhenti ketika aplikasi berhenti
atexit.register(lambda: scheduler.shutdown())

# Rute API untuk mendapatkan data status
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(status_data)

# Ini untuk htmlnya
@app.route('/')
def index():
    return render_template('index.html')

# jalankankan html
if __name__ == "__main__":
    asyncio.run(check_website_status())
    app.run(host='0.0.0.0', port=11010)
