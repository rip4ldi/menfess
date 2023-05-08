import config
import re

from pyrogram import Client, enums, types
from plugins import Database


async def tambah_admin_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]admin(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah admin</b>\n\n<code>/admin id_user</code>\n\nContoh :\n<code>/admin 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (y := re.search(r"^[\/]admin(\s|\n)*(\d+)$", msg.text)):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah admin</b>\n\n<code>/admin id_user</code>\n\nContoh :\n<code>/admin 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan user admin", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
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
    if member.status in status:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    try:
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.update_admin(int(target), client.id_bot)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi admin bot</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
            parse_mode=enums.ParseMode.HTML
        )


async def hapus_admin_handler(client: Client, msg: types.Message):
    if re.search(r"^[\/]unadmin(\s|\n)*$", msg.text):
        return await msg.reply_text(
            text="<b>Cara penggunaan mencabut status admin</b>\n\n<code>/unadmin id_user</code>\n\nContoh :\n<code>/unadmin 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if y := re.search(r"^[\/]unadmin(\s|\n)*(\d+)$", msg.text):
        target = y[2]
        db = Database(int(target))
        if not await db.cek_user_didatabase():
            return await msg.reply_text(
                text=f"<i><a href='tg://user?id={str(target)}'>user</a> tidak terdaftar didatabase</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        status = [
            'owner', 'talent', 'daddy sugar', 'moans girl',
            'moans boy', 'girlfriend rent', 'boyfriend rent'
        ]
        member = db.get_data_pelanggan()
        if member.status in status:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()}</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        if member.status != 'admin':
            return await msg.reply_text(
                text=f"<i><a href='tg://openmessage?user_id={str(target)}'>User</a> bukan seorang admin</i>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        try:
            await client.send_message(
                int(target),
                text=f"<i>Sayangnya owner telah mencabut jabatanmu sebagai admin</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
                parse_mode=enums.ParseMode.HTML
            )
            await db.hapus_admin(int(target), client.id_bot)
            return await msg.reply_text(
                text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil diturunkan menjadi member</i>\n└Diturunkan oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            return await msg.reply_text(
                text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await msg.reply_text(
            text="<b>Cara penggunaan mencabut status admin</b>\n\n<code>/unadmin id_user</code>\n\nContoh :\n<code>/unadmin 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
