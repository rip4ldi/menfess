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
            text=f"<i>{await get_mention_name(target, client)}</i> tidak terdaftar didatabase", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    status = [
        'admin', 'owner', 'talent', 'daddy sugar', 'moans girl',
        'moans boy', 'girlfriend rent', 'boyfriend rent'
    ]
    member = db.get_data_pelanggan()
    if member.status == 'admin' in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, {await get_mention_name(target, client)} adalah seorang {member.status.upper()} tidak dapat dibanned</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    update = 'Alasan berhasil diupdate' if member.status == 'banned' else ''
    text_split = msg.text.split(None, 2)
    alasan = "-" if len(text_split) <= 2 else text_split[2]
    await db.banned_user(int(target), client.id_bot, alasan)

    # Get user information
    user_info = await client.get_users(int(target))

    # Send notification to channel_1
    notification_text = f"User {await get_mention_name(target, client)} dengan Id: {target} sudah di banned. karena: {alasan}"
    await client.send_message(config.channel_1, notification_text)

    return await msg.reply_text(
        text=f"{get_user_link(target)} <i>berhasil dibanned</i>\n└Dibanned oleh : {get_user_link(config.id_admin)}\n\nAlasan: {str(alasan)}\n\n{update}", quote=True,
        parse_mode=enums.ParseMode.HTML
    )


async def unban_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]unban(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (x := re.search(r"^[\/]unban(\s|\n)*(\d+)", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan unban user</b>\n\n<code>/unban id_user alasan unbanned</code>\n\nContoh :\n<code>/unban 121212021</code>\n<code>/unban 12121 sudah selesai</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = x[2]
    db = Database(int(target))
    if await db.cek_user_didatabase():
        if target in db.get_data_bot(client.id_bot).ban:

            # Get user information
            user_info = await client.get_users(int(target))

            await db.unban_user(int(target), client.id_bot)

            # Send notification to channel_1
            notification_text = f"User {await get_mention_name(target, client)} dengan Id: {target} telah unbanned. Alasan: {alasan}"
            await client.send_message(config.channel_1, notification_text)

            return await msg.reply_text(
                text=f"{get_user_link(target)} <i>berhasil diunbanned</i>\n└Diunbanned oleh : {get_user_link(config.id_admin)}\n\nAlasan: {str(alasan)}", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            return await msg.reply_text(
                text=f"<i>{await get_mention_name(target, client)}</i> sedang tidak dalam kondisi banned", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        return await msg.reply_text(
            text=f"<i>{await get_mention_name(target, client)}</i> tidak terdaftar didatabase", quote=True,
            parse_mode=enums.ParseMode.HTML
        )


def get_user_link(user_id: str):
    return f"<a href='tg://openmessage?user_id={str(user_id)}'>User</a>"


async def get_mention_name(user_id: str, client: Client):
    # Get user information
    user_info = await client.get_users(int(user_id))

    # Get the mention name of the user
    mention_name = user_info.first_name if not user_info.last_name else f"{user_info.first_name} {user_info.last_name}"

    return mention_name
