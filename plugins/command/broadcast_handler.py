import asyncio
from pyrogram import Client
from pyrogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
from pyrogram.errors import (
    FloodWait, PeerIdInvalid, UserIsBlocked, InputUserDeactivated
)
from plugins import Database

async def broadcast_handler(client: Client, msg: Message):
    if msg.reply_to_message is None:
        await msg.reply('Harap reply sebuah pesan', True)
    else:
        # Tidak perlu menggunakan await anu.copy() disini
        anu = msg.reply_to_message
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Ya', 'ya_confirm'), InlineKeyboardButton('Tidak', 'tidak_confirm')]
        ])
        await anu.reply('apakah kamu akan mengirimkan pesan broadcast ?', True, reply_markup=markup)

async def broadcast_pin_handler(user_id: int, message_id: int):
    db = Database(user_id)
    last_status = db.get_data_pelanggan().status_full
    try:
        # Menggunakan metode pin_chat_message() untuk menyematkan pesan berdasarkan message_id
        await client.pin_chat_message(user_id, message_id)
        mycol.update_one({"status": last_status}, {"$set": {"status": f"pinned_{user_id}"}})
    except:
        pass

async def broadcast_ya(client: Client, query: CallbackQuery):
    msg = query.message
    db = Database(msg.from_user.id)
    if not msg.reply_to_message:
        await query.answer('Pesan tidak ditemukan', True)
        await query.message.delete()
        return
    message = msg.reply_to_message
    user_ids = db.get_pelanggan().id_pelanggan

    berhasil = 0
    dihapus = 0
    blokir = 0
    gagal = 0
    await msg.edit('Broadcast sedang berlangsung, tunggu sebentar', reply_markup=None)
    for user_id in user_ids:
        try:
            sent_message = await message.copy(user_id)
            await broadcast_pin_handler(user_id, sent_message)  # Menyematkan pesan yang berhasil terkirim
            berhasil += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            sent_message = await message.copy(user_id)
            await broadcast_pin_handler(user_id, sent_message)  # Menyematkan pesan yang berhasil terkirim
            berhasil += 1
        except UserIsBlocked:
            blokir += 1
        except PeerIdInvalid:
            gagal += 1
        except InputUserDeactivated:
            dihapus += 1
            await db.hapus_pelanggan(user_id)
    text = f"""<b>Broadcast selesai</b>
    
Jumlah pengguna: {len(user_ids)}
Berhasil terkirim: {str(berhasil)}
Pengguna diblokir: {str(blokir)}
Akun yang dihapus: {str(dihapus)} (<i>Telah dihapus dari database</i>)
Gagal terkirim: {str(gagal)}"""

    await msg.reply(text)
    await msg.delete()
    await message.delete()

async def close_cbb(client: Client, query: CallbackQuery):
    try:
        await query.message.reply_to_message.delete()
    except:
        pass
    try:
        await query.message.delete()
    except:
        pass
