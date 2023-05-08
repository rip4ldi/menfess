import config

from pyrogram import Client, types, enums
from plugins import Helper, Database

async def start_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = f'{first} {last}' if last else first
    username = (
        f'@{msg.from_user.username}'
        if msg.from_user.username
        else '@chatjomblohalu_bot'
    )
    mention = msg.from_user.mention
    await msg.reply_text(
        text = config.start_msg.format(
            id = msg.from_user.id,
            mention = mention,
            username = username,
            first_name = await helper.escapeHTML(first),
            last_name = await helper.escapeHTML(last),
            fullname = await helper.escapeHTML(fullname),
            ),
        disable_web_page_preview = True,
        quote = True
    )

async def status_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    db = Database(msg.from_user.id).get_data_pelanggan()
    pesan = '<b>🏷Info user</b>\n'
    pesan += f'├ID : <code>{db.id}</code>\n'
    pesan += f'├Nama : {db.mention}\n'
    pesan += f'└Status : {db.status}\n\n'
    pesan += '<b>📝Lainnya</b>\n'
    pesan += f'├Coin : {helper.formatrupiah(db.coin)}💰\n'
    pesan += f'├Menfess : {db.menfess}/{config.batas_kirim}\n'
    pesan += f'├Semua Menfess : {db.all_menfess}\n'
    pesan += f'└Bergabung : {db.sign_up}'
    await msg.reply(pesan, True, enums.ParseMode.HTML)

async def statistik_handler(client: Helper, id_bot: int):
    db = Database(client.user_id)
    bot = db.get_data_bot(id_bot)
    pesan = "<b>📊 STATISTIK BOT\n\n"
    pesan += f"▪️Pelanggan: {db.get_pelanggan().total_pelanggan}\n"
    pesan += f"▪️Admin: {len(bot.admin)}\n"
    pesan += f"▪️Talent: {len(bot.talent)}\n"
    pesan += f"▪️Daddy sugar: {len(bot.daddy_sugar)}\n"
    pesan += f"▪️Moans girl: {len(bot.moansgirl)}\n"
    pesan += f"▪️Moans boy: {len(bot.moansboy)}\n"
    pesan += f"▪️Girlfriend rent: {len(bot.gfrent)}\n"
    pesan += f"▪️Boyfriend rent: {len(bot.bfrent)}\n"
    pesan += f"▪️Banned: {len(bot.ban)}\n\n"
    pesan += f"🔰Status bot: {'AKTIF' if bot.bot_status else 'TIDAK AKTIF'}</b>"
    await client.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def list_admin_handler(helper: Helper, id_bot: int):
    db = Database(helper.user_id).get_data_bot(id_bot)
    pesan = "<b>Owner bot</b>\n"
    pesan += (
        f"• ID: {str(config.id_admin)} | <a href='tg://user?id={str(config.id_admin)}"
        + "'>Owner bot</a>\n\n"
    )
    if len(db.admin) > 0:
        pesan += "<b>Daftar Admin bot</b>\n"
        for ind, i in enumerate(db.admin, start=1):
            pesan += (
                f"• ID: {str(i)} | <a href='tg://user?id={str(i)}'>Admin {str(ind)}"
                + "</a>\n"
            )
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def list_ban_handler(helper: Helper, id_bot: int):
    db = Database(helper.user_id).get_data_bot(id_bot)
    if len(db.ban) == 0:
        return await helper.message.reply_text('<i>Tidak ada user dibanned saat ini</i>', True, enums.ParseMode.HTML)
    pesan = "<b>Daftar banned</b>\n"
    for ind, i in enumerate(db.ban, start=1):
        pesan += (
            f"• ID: {str(i)} | <a href='tg://openmessage?user_id={str(i)}'>( {str(ind)}"
            + " )</a>\n"
        )
    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML)

async def gagal_kirim_handler(client: Client, msg: types.Message):
    anu = Helper(client, msg)
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    fullname = f'{first_name} {last_name}' if last_name else first_name
    username = (
        f'@{msg.from_user.username}'
        if msg.from_user.username
        else '@chatjomblohalu_bot'
    )
    mention = msg.from_user.mention
    return await msg.reply(config.gagalkirim_msg.format(
        id = msg.from_user.id,
        mention = mention,
        username = username,
        first_name = await anu.escapeHTML(first_name),
        last_name = await anu.escapeHTML(last_name),
        fullname = await anu.escapeHTML(fullname)
    ), True, enums.ParseMode.HTML, disable_web_page_preview=True)

async def help_handler(client, msg):
    db = Database(msg.from_user.id)
    member = db.get_data_pelanggan()
    pesan = "Supported commands\n" + '/status — melihat status\n'
    pesan += '/talent — melihat talent\n'
    if member.status == 'admin':
        pesan += '\nHanya Admin\n'
        pesan += '/tf_coin — transfer coin\n'
        pesan += '/settings — melihat settingan bot\n'
        pesan += '/list_admin — melihat list admin\n'
        pesan += '/list_ban — melihat list banned\n\n'
        pesan += 'Perintah banned\n'
        pesan += '/ban — ban user\n'
        pesan += '/unban — unban user\n'
    elif member.status == 'owner':
        pesan += '\n=====OWNER COMMAND=====\n'
        pesan += '/tf_coin — transfer coin\n'
        pesan += '/settings — melihat settingan bot\n'
        pesan += '/list_admin — melihat list admin\n'
        pesan += '/list_ban — melihat list banned\n'
        pesan += '/stats — melihat statistik bot\n'
        pesan += '/bot — setbot (on|off)\n'
        pesan += '\n=====FITUR TALENT=====\n'
        pesan += '/addtalent — menambahkan talent baru\n'
        pesan += '/addsugar — menambahkan talent daddy sugar\n'
        pesan += '/addgirl — menambahkan talent moans girl\n'
        pesan += '/addboy — menambahkan talent moans boy\n'
        pesan += '/addgf — menambahkan talent girlfriend rent\n'
        pesan += '/addbf — menambahkan talent boyfriend rent\n'
        pesan += '/hapus — menghapus talent\n'
        pesan += '\n=====BROADCAST OWNER=====\n'
        pesan += '/broadcast — mengirim pesan broadcast kesemua user\n'
        pesan += '/admin — menambahkan admin baru\n'
        pesan += '/unadmin — menghapus admin\n'
        pesan += '/list_ban — melihat list banned\n'
        pesan += '\n=====BANNED COMMAND=====\n'
        pesan += '/ban — ban user\n'
        pesan += '/unban — unban user\n'
    await msg.reply(pesan, True)