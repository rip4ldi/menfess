from pyrogram.types import InlineKeyboardButton

class Data:
    JASA = """
<b>DAFTAR:</b>

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

Untuk informasi lebih lanjut dan pemesanan, silakan hubungi @OwnNeko.
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
            InlineKeyboardButton("DANA", callback_data="dana"),
            InlineKeyboardButton("QRIS", callback_data="qris"),
            InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")
        ],
    ]

    DANA = """
DANA : 081398871823
"""

    QRIS = """
 Klik Disini </b><a href='https://telegra.ph/file/3a8701cb42f9af1483800.jpg'>QRIS BrotherCloth</a>
"""
