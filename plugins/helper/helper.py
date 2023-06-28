import io
import config
import pytz
import pyrogram
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Update
from pyrogram import enums, Client
from datetime import datetime
from ..database import Database
from .waktu import Waktu


class Helper():
    def __init__(self, bot: Client, message: Message):
        self.bot = bot
        self.client = bot  
        self.message = message
        self.msg = message
        self.user_id = message.from_user.id
        self.first = message.from_user.first_name
        self.last = message.from_user.last_name
        self.fullname = f'{self.first} {self.last}' if self.last else self.first
        self.premium = message.from_user.is_premium
        self.username = (
            f'@{self.message.from_user.username}'
            if self.message.from_user.username
            else "-"
        )
        self.mention = self.message.from_user.mention
        
    async def estimate_message(self, image):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        file_id = await self.client.send_photo(chat_id=self.msg.chat.id, photo=img_byte_arr)

        file_link = f'tg://openmessage?user_id={self.msg.from_user.id}&message_id={file_id}'
        message_text = f'<a href="{file_link}">&#8203;</a>'

        return message_text

    async def escapeHTML(self, text: str):
        if text is None:
            return ''
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    async def cek_langganan_channel(self, user_id: int):
        if user_id == config.id_admin:
            return True
        try:
            member = await self.bot.get_chat_member(config.channel_1, user_id)
        except UserNotParticipant:
            return False
        try:
            member = await self.bot.get_chat_member(config.channel_2, user_id)
        except UserNotParticipant:
            return False

        status = [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR
        ]
        return member.status in status

    async def pesan_langganan(self):
        link_1 = await self.bot.export_chat_invite_link(config.channel_1)
        link_2 = await self.bot.export_chat_invite_link(config.channel_2)
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Channel base', url=link_1), InlineKeyboardButton('Group base', url=link_2)],
            [InlineKeyboardButton('Coba lagi', url=f'https://t.me/{self.bot.username}?start=start')]
        ])
        await self.bot.send_message(self.user_id, config.pesan_join, reply_to_message_id=self.message.id, reply_markup=markup)

    async def daftar_pelanggan(self):
        database = Database(self.user_id)

        nama = self.fullname

        status = 'member'
        coin = f"0_{str(self.user_id)}"
        if self.user_id == config.id_admin:
            status = 'owner'
            coin = f"9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999_{str(self.user_id)}"

        nama = await self.escapeHTML(nama)
        data = {
            '_id': self.user_id,
            'nama': nama,
            'status': f"{status}_{str(self.user_id)}",
            'coin': coin,
            'menfess': 0,
            'all_menfess': 0,
            'sign_up': self.get_time().full_time
        }
        return await database.tambah_pelanggan(data)

    async def send_to_channel_log(self, type: str = None, link: str = None):
        if type == 'log_channel':
            pesan = "INFO MESSAGE 💌\n"
            pesan += f"├ Nama -: <b>{await self.escapeHTML(self.fullname)}</b>\n"
            pesan += f"├ ID -: <code>{self.user_id}</code>\n"
            pesan += f"├ Username -: {self.username}\n"
            pesan += f"├ Mention -: {self.mention}\n"
            pesan += f"├ Kirim pesan -: <a href='tg://openmessage?user_id={self.user_id}'>{await self.escapeHTML(self.fullname)}</a>\n"
            pesan += f"├ Cek Pesan : {link}\n"
            pesan += f"└ Waktu -: {self.get_time().full_time}"
        elif type == 'log_daftar':
            pesan = "<b>📊DATA USER BERHASIL DITAMBAHKAN DIDATABASE</b>\n"
            pesan += f"├ Nama -: <b>{await self.escapeHTML(self.fullname)}</b>\n"
            pesan += f"├ ID -: <code>{self.user_id}</code>\n"
            pesan += f"├ Username -: {self.username}\n"
            pesan += f"├ Mention -: {self.mention}\n"
            pesan += f"├ Kirim pesan -: <a href='tg://openmessage?user_id={self.user_id}'>{await self.escapeHTML(self.fullname)}</a>\n"
            pesan += f"└ Telegram Premium -: {'✅' if self.premium else '❌'}"
        else:
            pesan = "Jangan Lupa main bot @chatjomblohalu_bot"
        await self.bot.send_message(config.channel_log, pesan, enums.ParseMode.HTML, disable_web_page_preview=True)

    def formatrupiah(self, uang):
        y = str(uang)
        if int(y) < 0:
            return y
        if len(y) <= 3:
            return y
        p = y[-3:]
        q = y[:-3]
        return f'{self.formatrupiah(q)}.{p}'

    def get_time(self):
        hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]
        bulan = {
            "01": "Januari",
            "02": "Februari",
            "03": "Maret",
            "04": "April",
            "05": "Mei",
            "06": "Juni",
            "07": "Juli",
            "08": "Agustus",
            "09": "September",
            "10": "Oktober",
            "11": "November",
            "12": "Desember"
        }
        now = datetime.now(pytz.timezone('Asia/Jakarta'))
        waktu = now.strftime('%w %d %m %Y %H:%M:%S').split()
        full_time = f"{hari[int(waktu[0])]}, {waktu[1]} {bulan[waktu[2]]} {waktu[3]} {waktu[4]}"
        return Waktu({
            'hari': hari[int(waktu[0])],
            'tanggal': waktu[1],
            'bulan': bulan[waktu[2]],
            'tahun': waktu[3],
            'jam': waktu[4],
            'full': full_time
        })
