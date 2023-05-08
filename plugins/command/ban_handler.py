import config
import re

from pyrogram import Client, enums, types
from plugins import Database


async def ban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]ban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (y := re.search(r"^[\/]ban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    if member.status == 'admin' in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat dibanned</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    update = 'Alasan berhasil diupdate' if member.status == 'banned' else ''
    text_split = msg.text.split(None, 2)
    alasan = "-" if len(text_split) <= 2 else text_split[2]
    await db.banned_user(int(target), client.id_bot, alasan)
    return await msg.reply_text(
        text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil dibanned</i>\n└Dibanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>\n\nAlasan: {str(alasan)}\n\n{update}", quote=True,
        parse_mode=enums.ParseMode.HTML
    )


async def unban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]unban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user</code>\n\nContoh :\n<code>/unban 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (x := re.search(r"^[\/]unban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user</code>\n\nContoh :\n<code>/unban 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = x[2]
    db = Database(int(target))
    if await db.cek_user_didatabase():
        if target in db.get_data_bot(client.id_bot).ban:
            await db.unban_user(int(target), client.id_bot)
            return await msg.reply_text(
                text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diunbanned</i>\n└Diunbanned oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> sedang tidak dalam kondisi banned</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
