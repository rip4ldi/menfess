import config
import re

from pyrogram import Client, enums, types
from plugins import Database


async def ban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]ban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (y := re.search(r"^[\/]ban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan ban user</b>\n\n<code>/ban id_user alasan ban</code>\n<code>/ban id_user</code>\n\nContoh :\n<code>/ban 121212021</code>\n<code>/ban 12121 share porn</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if not await db.cek_user_didatabase():
        return await msg.reply_text(
            text=f"<i>{get_user_mention(target)}</i> tidak terdaftar didatabase",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    if member.status == 'admin' in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, {get_user_mention(target)} adalah seorang {member.status.upper()} tidak dapat dibanned</i>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    update = 'Alasan berhasil diupdate' if member.status == 'banned' else ''
    text_split = msg.text.split(None, 2)
    alasan = "-" if len(text_split) <= 2 else text_split[2]
    await db.banned_user(int(target), client.id_bot, alasan)

    # Send notification to channel_1
    notification_text = f"User {get_user_mention(target)} dengan Id: {target} sudah di banned. karena: {alasan}"
    await client.send_message(config.channel_1, notification_text)

    admin_mention = get_user_mention(config.id_admin)
    return await msg.reply_text(
        text=f"{get_user_link(target)} <i>berhasil dibanned</i>\n└Dibanned oleh : {admin_mention}\n\nAlasan: {str(alasan)}\n\n{update}",
        quote=True,
        parse_mode=enums.ParseMode.HTML
    )


async def unban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]unban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (x := re.search(r"^[\/]unban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = x[2]
    db = Database(int(target))
    if await db.cek_user_didatabase():
        if target in db.get_data_bot(client.id_bot).ban:
            await db.unban_user(int(target), client.id_bot)

            # Send notification to channel_1
            notification_text = f"User {get_user_mention(target)} dengan Id: {target} telah unbanned. Alasan: {alasan}"
            await client.send_message(config.channel_1, notification_text)

            admin_mention = get_user_mention(config.id_admin)
            return await msg.reply_text(
                text=f"{get_user_link(target)} <i>berhasil diunbanned</i>\n└Diunbanned oleh : {admin_mention}\n\nAlasan: {str(alasan)}",
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            return await msg.reply_text(
                text=f"<i>{get_user_mention(target)}</i> sedang tidak dalam kondisi banned",
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text=f"<i>{get_user_mention(target)}</i> tidak terdaftar didatabase",
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )


def get_user_link(user_id: str):
    return f"<a href='tg://openmessage?user_id={str(user_id)}'>User</a>"


def get_user_mention(user_id: str):
    return f"<a href='tg://user?id={str(user_id)}'>Mention</a>"
