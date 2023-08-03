from pyrogram.types import InlineKeyboardButton

class Data:
    JASA = """
<b>JASA PEMBUATAN BOT</b>

1. Pembuatan Bot Menfess
   Deskripsi: Bot untuk mengelola layanan postingan anonim (menfess) di grup.
   Fitur:
   - Menfess dalam grup dengan anonim.
   - Tampilan yang menarik dan mudah digunakan.
   - Pengaturan batas waktu menfess.
   - Dukungan berbagai perintah kustom.
   - Integrasi dengan database.

2. Pembuatan Bot Music
   Deskripsi: Bot untuk memutar musik di grup atau saluran.
   Fitur:
   - Memutar musik dari YouTube dan platform lainnya.
   - Kontrol musik lengkap (play, pause, skip, dll.).
   - Tampilan informasi musik yang sedang diputar.
   - Dukungan daftar putar.
   - Integrasi dengan database.

3. Pembuatan Bot File Sharing (Fsub Telegram)
   Deskripsi: Bot untuk menyimpan dan berbagi file melalui tautan khusus.
   Fitur:
   - Mengunggah file ke bot dan mendapatkan tautan unik.
   - Mengelola file yang diunggah (menghapus, dll.).
   - Tampilan statistik unduhan file.
   - Dukungan untuk berbagai jenis file.

Untuk informasi lebih lanjut dan pemesanan, silakan hubungi @SayaNeko.
"""

    close = [
        [InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")]
    ]

    mbuttons = [
        [
            InlineKeyboardButton("JASA", callback_data="jasa"),
            InlineKeyboardButton("QRIS", callback_data="qris"),
            InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")
        ],
    ]

    buttons = [
        [
            InlineKeyboardButton("ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ", callback_data="dana"),
            InlineKeyboardButton("QRIS", callback_data="qris"),
            InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")
        ],
    ]

    DANA = """
DANA : 081398871823
"""

    QRIS = """
Ini adalah gambar QRIS (Quick Response Indonesia Standard) yang dapat digunakan untuk melakukan pembayaran melalui berbagai aplikasi pembayaran di Indonesia.

[![](https://github.com/nekolocal/nekomenfess/blob/main/qr_Brother%20Cloth_04.03.23_1677873385.png)](https://github.com/nekolocal/nekomenfess/blob/main/qr_Brother%20Cloth_04.03.23_1677873385.png)

Develoved by </b><a href='https://t.me/SayaNeko'>SayaNeko</a>
"""
