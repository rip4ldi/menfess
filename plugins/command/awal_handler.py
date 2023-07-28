import config
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO 

from pyrogram import Client, types, enums
from plugins import Helper, Database
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_handler(client: Client, msg: types.Message):
    helper = Helper(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = f'{first} {last}' if last else first
    username = (
        f'@{msg.from_user.username}'
        if msg.from_user.username
        else '@OwnNeko'
    )
    mention = msg.from_user.mention
    await msg.reply_text(
        text=config.start_msg.format(
            id=msg.from_user.id,
            mention=mention,
            username=username,
            first_name=await helper.escapeHTML(first),
            last_name=await helper.escapeHTML(last),
            fullname=await helper.escapeHTML(fullname),
        ),
        disable_web_page_preview=True,
        quote=True
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
    # Load the image
    image = Image.open('20230508_142127.jpg')  # Replace with the actual image path

    # Create a BytesIO stream to save the image
    image_stream = BytesIO()
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)

    # Reply with the photo and description
    await msg.reply_photo(photo=image_stream, caption=pesan, parse_mode=enums.ParseMode.HTML)
    
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


def divide_list_into_chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

async def list_ban_handler(helper: Helper, id_bot: int, page=1):
async def list_ban_handler(helper: Helper, id_bot: int, page=1):
    db = Database(helper.user_id).get_data_bot(id_bot)
    banned_users = list(db.ban)
    per_page = 10
    total_pages = (len(banned_users) + per_page - 1) // per_page
    if page < 1 or page > total_pages:
        return await helper.message.reply_text('<i>Halaman tidak valid.</i>', True, enums.ParseMode.HTML)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    current_page_users = banned_users[start_index:end_index]

    pesan = "<b>Daftar banned</b>\n"
    for ind, i in enumerate(current_page_users, start=start_index + 1):
        pesan += (
            f"• ID: {str(i)} | <a href='tg://openmessage?user_id={str(i)}'>( {str(ind)}"
            + " )</a>\n"
        )

    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("Back", callback_data=f"list_ban_{id_bot}_{page-1}"))
    if page < total_pages:
        buttons.append(InlineKeyboardButton("Next", callback_data=f"list_ban_{id_bot}_{page+1}"))
    inline_keyboard = list(divide_list_into_chunks(buttons, 2))

    markup = InlineKeyboardMarkup(inline_keyboard)

    # Menambahkan tombol 'Back' dan 'Next' di atas daftar banned
    if page > 1:
        pesan = "Ketikkan '/list_ban' untuk kembali ke halaman sebelumnya.\n" + pesan
    if page < total_pages:
        pesan += f"\nKetikkan '/list_ban {page + 1}' untuk melihat daftar banned selanjutnya."

    await helper.message.reply_text(pesan, True, enums.ParseMode.HTML, reply_markup=markup)



async def gagal_kirim_handler(client: Client, msg: types.Message):
    anu = Helper(client, msg)
    first_name = msg.from_user.first_name
    last_name = msg.from_user.last_name
    fullname = f'{first_name} {last_name}' if last_name else first_name
    username = (
        f'@{msg.from_user.username}'
        if msg.from_user.username
        else '@OwnNeko'
    )
    mention = msg.from_user.mention
    return await msg.reply(config.gagalkirim_msg.format(
        id=msg.from_user.id,
        mention=mention,
        username=username,
        first_name=await anu.escapeHTML(first_name),
        last_name=await anu.escapeHTML(last_name),
        fullname=await anu.escapeHTML(fullname)
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
    await msg.reply_text(pesan, True)

async def reply_with_image_text(client: Client, msg: types.Message, text: str, image_path: str):
    helper = Helper(client, msg)
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    fullname = f'{first} {last}' if last else first
    username = (
        f'@{msg.from_user.username}'
        if msg.from_user.username
        else '@OwnNeko'
    )
    mention = msg.from_user.mention
    with Image.open(image_path) as image:
        await msg.reply_photo(
            photo=image,
            caption=config.start_msg.format(
                id=msg.from_user.id,
                mention=mention,
                username=username,
                first_name=await helper.escapeHTML(first),
                last_name=await helper.escapeHTML(last),
                fullname=await helper.escapeHTML(fullname),
            ),
            disable_web_page_preview=True,
            quote=True
        )
