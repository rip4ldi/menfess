import config
import re

from pyrogram import Client, enums, types
from plugins import Database, Helper

async def daddy_sugar_handler(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    daddy_sugar = db.get_data_bot(client.id_bot).daddy_sugar
    if len(daddy_sugar) == 0:
        return await msg.reply('<b>Saat ini tidak ada daddy sugar yang tersedia.</b>', True, enums.ParseMode.HTML)
    top_rate = [] # total rate daddy_sugar
    top_id = [] # id daddy_sugar
    for uid in daddy_sugar:
        rate = daddy_sugar[str(uid)]['rate']
        if rate >= 0:
            top_rate.append(rate)
            top_id.append(uid)
    top_rate.sort(reverse=True)
    pesan = "<b>Daftar Daddy sugar trusted</b>\n\n" + "No — Daddy Sugar — Rating\n"
    index = 1
    for i in top_rate:
        if index > config.batas_daddy_sugar:
            break
        for j in top_id:
            if daddy_sugar[j]['rate'] == i:
                pesan += f"<b> {str(index)}.</b> {daddy_sugar[j]['username']} ➜ {str(daddy_sugar[j]['rate'])} 🥂\n"
                top_id.remove(j)
                index += 1
    pesan += f"\nmenampilkan Real daddy sugar yang trusted membiayai wanita wanita di fwb"
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def tambah_sugar_daddy_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    if re.search(r"^[\/]addsugar(\s|\n)*$", msg.text or msg.caption):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Daddy Sugar</b>\n\n<code>/addsugar id_user</code>\n\nContoh :\n<code>/addsugar 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    if not (
        y := re.search(r"^[\/]addsugar(\s|\n)*(\d+)$", msg.text or msg.caption)
    ):
        return await msg.reply_text(
            text="<b>Cara penggunaan tambah Daddy Sugar</b>\n\n<code>/addsugar id_user</code>\n\nContoh :\n<code>/addsugar 121212021</code>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    target = y[2]
    db = Database(int(target))
    if target in db.get_data_bot(client.id_bot).ban:
        return await msg.reply_text(
            text=f"<i><a href='tg://user?id={str(target)}'>User</a> sedang dalam kondisi banned</i>\n└Tidak dapat menjadikan Daddy Sugar", quote=True,
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
            text=f"❌<i>Terjadi kesalahan, <a href='tg://user?id={str(target)}'>user</a> adalah seorang {member.status.upper()} tidak dapat ditambahkan menjadi daddy sugar</i>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    try:
        a = await client.get_chat(target)
        nama = await helper.escapeHTML(
            f'{a.first_name} {a.last_name}' if a.last_name else a.first_name
        )
        await client.send_message(
            int(target),
            text=f"<i>Kamu telah menjadi daddy sugar</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>",
            parse_mode=enums.ParseMode.HTML
        )
        await db.tambah_sugar_daddy(int(target), client.id_bot, nama)
        return await msg.reply_text(
            text=f"<a href='tg://openmessage?user_id={str(target)}'>User</a> <i>berhasil menjadi daddy sugar</i>\n└Diangkat oleh : <a href='tg://openmessage?user_id={str(config.id_admin)}'>Admin</a>", quote=True,
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        return await msg.reply_text(
            text=f"❌<i>Terjadi kesalahan, sepertinya user memblokir bot</i>\n\n{e}", quote=True,
            parse_mode=enums.ParseMode.HTML
        )