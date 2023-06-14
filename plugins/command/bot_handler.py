import os
import re
from pyrogram import Client, enums, types
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from plugins import Database

# Get channel ID from config.py
channel_1 = int(os.environ.get("CHANNEL_1", "-1001884106616"))

async def send_notification(text):
    await client.send_message(channel_1, text)

async def bot_handler(client: Client, msg: Message):
    if re.search(r"^[\/]bot(\s|\n)*$", msg.text):
        return await msg.reply("*Cara penggunaan command*\n\nEX : `/bot <on|off>`\nContoh : `/bot on`", quote=True, parse_mode=enums.ParseMode.MARKDOWN)

    if not (x := re.search(r"^[\/]bot\s*(on|off|<on>|<off>)$", msg.text)):
        return await msg.reply("*Cara penggunaan command*\n\nEX : `/bot <on|off>`\nContoh : `/bot on`", quote=True, parse_mode=enums.ParseMode.MARKDOWN)
    status = x[1]
    my_db = Database(msg.from_user.id)
    db_bot = my_db.get_data_bot(client.id_bot)
    if status in ['on', '<on>']:
        if db_bot.bot_status:
            return await msg.reply(
                text='<i>Terjadi kesalahan, bot saat ini dalam kondisi aktif</i>', quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        await my_db.bot_handler(status)
        await send_notification("Bot: On")
        return await msg.reply(
            text='Bot: <b>On</b>', quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        if not db_bot.bot_status:
            return await msg.reply(
                text='<i>Terjadi kesalahan, bot saat ini dalam kondisi tidak aktif</i>', quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        await my_db.bot_handler(status)
        await send_notification("Bot: Off")
        return await msg.reply(
            text='Bot: <b>Off</b>', quote=True,
            parse_mode=enums.ParseMode.HTML
        )


async def setting_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id).get_data_bot(client.id_bot)
    pesan = (
        "<b>💌 Menfess User\n\n✅ = AKTIF\n❌ = TIDAK AKTIF</b>\n"
        + "______________________________\n\n"
    )
    photo = ["AKTIF", "✅"] if db.kirimchannel.photo else ["TIDAK AKTIF", "❌"]
    video = ["AKTIF", "✅"] if db.kirimchannel.video else ["TIDAK AKTIF", "❌"]
    voice = ["AKTIF", "✅"] if db.kirimchannel.voice else ["TIDAK AKTIF", "❌"]
    status_bot = "AKTIF" if db.bot_status else "TIDAK AKTIF"
    pesan += f"📸 Foto = <b>{photo[0]}</b>\n"
    pesan += f"🎥 Video = <b>{video[0]}</b>\n"
    pesan += f"🎤 Voice = <b>{voice[0]}</b>\n\n"
    pesan += f"🤖 Bot Status = <b>{status_bot}</b>\n\n"
    pesan += "<i>*Apabila Ingin Mengaktifkan/Nonaktifkan Gunakan Command Berikut*</i>\n\n"
    pesan += "<code>/foto <on/off></code>\n"
    pesan += "<code>/video <on/off></code>\n"
    pesan += "<code>/voice <on/off></code>\n"
    pesan += "<code>/bot <on/off></code>\n"
    await msg.reply_text(pesan, quote=True, parse_mode="html")



