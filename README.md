# 🌦️ Bot Pemantau Cuaca

Bot Python yang memantau parameter iklim dan cuaca ekstrem secara real time melalui API cuaca, lalu mengirim peringatan otomatis ke Discord setiap 15 menit jika terdeteksi kondisi berbahaya.

## 📖 Deskripsi Proyek

### Tujuan

Perubahan iklim membuat cuaca ekstrem semakin sering dan sulit ditebak: suhu yang sangat panas, indeks UV yang berbahaya bagi kulit dan mata, serta hujan lebat yang dapat memicu banjir. Informasi ini sebenarnya tersedia di aplikasi cuaca, tetapi kita harus membukanya sendiri dan sering terlambat menyadarinya.

Proyek ini bertujuan membuat pemantauan tersebut **otomatis dan proaktif**. Bot yang berjalan di latar belakang akan mengecek kondisi cuaca secara berkala dan langsung memberi tahu lewat Discord ketika ada parameter yang melewati ambang batas, lengkap dengan tips yang sesuai dengan jenis cuacanya.

## ⚙️ Fungsi dan Fitur

### 1. Pemantauan Cuaca Real Time
Bot mengambil data cuaca terbaru dari [Open-Meteo API](https://open-meteo.com/) untuk lokasi yang dipilih, sehingga data selalu mutakhir tanpa perlu input manual.

### 2. Deteksi Tiga Jenis Cuaca Ekstrem

| Parameter | Yang dipantau | Kapan peringatan dikirim |
|---|---|---|
| 🌡️ **Suhu** | Suhu udara saat ini | Melewati batas suhu ekstrem |
| ☀️ **Indeks UV** | Tingkat radiasi UV | Mencapai level berbahaya |
| 🌧️ **Curah hujan** | Intensitas hujan | Di atas normal |

### 3. Pengecekan Otomatis Setiap 15 Menit
Penjadwalan memakai library `schedule`. Bot menjalankan pengecekan berulang setiap 15 menit selama program aktif.

### 4. Notifikasi Discord Otomatis
Peringatan dikirim melalui **Discord Webhook** ke channel yang Anda tentukan. Pesan tampil sebagai **kartu embed berwarna** agar mudah dikenali sekilas, berisi:

- jenis peringatan dan nilai yang terdeteksi,
- lokasi pemantauan,
- tips yang relevan dengan jenis cuacanya.

### 5. Tips Sesuai Jenis Cuaca
Setiap peringatan menyertakan tips praktis, misalnya minum cukup air saat suhu tinggi, memakai tabir surya dan topi saat UV tinggi, atau menyiapkan payung dan waspada genangan saat hujan lebat.

### 6. Cooldown Anti-Spam
Setiap jenis peringatan (suhu, UV, hujan) memiliki **cooldown 180 menit**. Jika kondisi ekstrem berlangsung lama, channel Anda tidak dibanjiri pesan yang sama setiap 15 menit.

### 7. Konfigurasi Aman
Webhook Discord disimpan di file `.env` (dibaca dengan `python-dotenv`) sehingga tidak ikut terunggah ke GitHub.

## 🛠️ Teknologi

- Python 3
- [Open-Meteo API](https://open-meteo.com/) (data cuaca)
- [`requests`](https://pypi.org/project/requests/) (permintaan HTTP)
- [`schedule`](https://pypi.org/project/schedule/) (penjadwalan 15 menit)
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) (variabel lingkungan)
- Discord Webhook (pengiriman notifikasi)

## 🚀 Cara Menggunakan

### 1. Unduh proyek
```bash
git clone https://github.com/Aesteh/Bot-Pemantau-Cuaca.git
cd Bot-Pemantau-Cuaca
```
Atau unduh sebagai ZIP lewat tombol **Code → Download ZIP** di GitHub.

### 2. Pasang dependensi
```bash
pip install requests python-dotenv schedule
```

### 3. Buat Discord Webhook
1. Buka Discord, lalu masuk ke **Pengaturan Channel → Integrasi → Webhook**.
2. Klik **Webhook Baru**, lalu **Salin URL Webhook**.

### 4. Buat file `.env`
Di folder proyek, buat file bernama `.env`:
```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxx/xxxxxxxx
```

### 5. Jalankan bot
```bash
python bot.py
```
Biarkan program tetap berjalan. Bot akan mengecek cuaca setiap 15 menit dan mengirim peringatan ke Discord bila ada kondisi ekstrem.

## 📚 Referensi

- [Open-Meteo: Weather Forecast API](https://open-meteo.com/en/docs)
- [BMKG: Badan Meteorologi, Klimatologi, dan Geofisika](https://www.bmkg.go.id/)
- [Dokumentasi Discord Webhook](https://discord.com/developers/docs/resources/webhook)

Dibuat oleh Aesteh
