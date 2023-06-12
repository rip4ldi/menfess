import config
from pyrogram import Client, types
from plugins import Database, Helper
from plugins.command.check_handler import setup_handlers as check_handler_setup_handlers


async def ban_check_command(client: Client, msg: types.Message):
    db = Database(msg.from_user.id)
    user_id = int(msg.text.split()[1])  # Extract the user ID from the command
    banned_users = db.get_banned_users()

    if user_id in banned_users:
        ban_reason = db.get_ban_reason(user_id)
        await msg.reply(f"User is banned. Reason: {ban_reason}")
    else:
        await msg.reply("User is not banned.")

# Register the command and handler
client.add_handler(types.MessageHandler(ban_check_command, commands=['check_ban']))

# Inside your main function where you run the client, add the following line to load the banned users from the database:
db.load_banned_users()

# Add a method to your Database class to load the banned users from the database:
class Database:
    def load_banned_users(self):
        # Load banned users and their reasons from the database and store them in a dictionary
        self.banned_users = {123: 'Spamming', 456: 'Inappropriate behavior'}  # Example dictionary of banned user IDs and their reasons

    def get_banned_users(self):
        return self.banned_users.keys()

    def get_ban_reason(self, user_id):
        return self.banned_users.get(user_id, "Reason not available")
    
def setup_handlers(client):
    client.add_handler(types.MessageHandler(ban_check_command, commands=['check_ban']))
