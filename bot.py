import os
import sys
import time

import requests
import schedule
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
LATITUDE = float(os.getenv("LATITUDE", "-6.2"))
LONGITUDE = float(os.getenv("LONGITUDE", "106.8"))
LOCATION_NAME = os.getenv("LOCATION_NAME", "Lokasi Anda")

TEMP_MAX_C = float(os.getenv("TEMP_MAX_C", "35"))
UV_MAX = float(os.getenv("UV_MAX", "8"))
RAIN_MAX_MM = float(os.getenv("RAIN_MAX_MM", "10"))

CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "15"))
COOLDOWN_MINUTES = int(os.getenv("COOLDOWN_MINUTES", "180"))

API_URL = "https://api.open-meteo.com/v1/forecast"

last_sent = {}


def get_current_weather():
    response = requests.get(
        API_URL,
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": "temperature_2m,precipitation,uv_index",
            "timezone": "auto",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["current"]


def check_alerts(current):
    alerts = {}

    temp = current.get("temperature_2m")
    uv = current.get("uv_index")
    rain = current.get("precipitation")

    if temp is not None and temp >= TEMP_MAX_C:
        alerts["suhu"] = f"🌡️ Suhu ekstrem: {temp:.1f}°C (batas {TEMP_MAX_C:g}°C)"
    if uv is not None and uv >= UV_MAX:
        alerts["uv"] = f"☀️ Indeks UV berbahaya: {uv:.1f} (batas {UV_MAX:g})"
    if rain is not None and rain >= RAIN_MAX_MM:
        alerts["hujan"] = f"🌧️ Curah hujan tinggi: {rain:.1f} mm (batas {RAIN_MAX_MM:g} mm)"

    return alerts


def send_discord(message):
    try:
        response = requests.post(WEBHOOK_URL, json={"content": message}, timeout=15)
        response.raise_for_status()
        return True
    except requests.RequestException as error:
        print(f"[ERROR] Gagal kirim ke Discord: {error}")
        return False


def job():
    try:
        current = get_current_weather()
    except (requests.RequestException, KeyError) as error:
        print(f"[ERROR] Gagal ambil data cuaca: {error}")
        return

    print(
        f"[{time.strftime('%H:%M:%S')}] suhu={current.get('temperature_2m')}°C "
        f"uv={current.get('uv_index')} hujan={current.get('precipitation')} mm"
    )

    now = time.time()
    due = {
        kind: text
        for kind, text in check_alerts(current).items()
        if now - last_sent.get(kind, 0) >= COOLDOWN_MINUTES * 60
    }
    if not due:
        return

    message = (
        f"⚠️ **Peringatan cuaca ekstrem - {LOCATION_NAME}**\n"
        + "\n".join(due.values())
        + "\n\n_Data: Open-Meteo.com_"
    )
    if send_discord(message):
        for kind in due:
            last_sent[kind] = now


if __name__ == "__main__":
    if not WEBHOOK_URL:
        sys.exit("DISCORD_WEBHOOK_URL belum diisi di file .env")

    if "--test" in sys.argv:
        sys.exit(0 if send_discord("Tes bot cuaca ✅") else 1)

    print(f"Bot berjalan untuk {LOCATION_NAME}, cek tiap {CHECK_INTERVAL_MINUTES} menit.")
    job()
    schedule.every(CHECK_INTERVAL_MINUTES).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
