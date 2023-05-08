from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import Bot, data, Database

async def reset_menfess():
    db = Database(data[0])
    x = await db.reset_menfess()
    await Bot().kirim_pesan(x=str(x))
    print('BOT BERHASIL DIRESET')

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(reset_menfess, trigger="cron", hour=1, minute=0)
scheduler.start()

Bot().run()
