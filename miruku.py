# by ztoohn
import disnake, os, datetime, asyncio
from disnake.ext import commands, tasks
from datetime import datetime
from colorama import Fore, init

from utils.database import db
from utils.succroles import roles
from mta.monitoring import Server as Srv

bot = commands.Bot(command_prefix='.', intents=disnake.Intents.all(), test_guilds=[1202355886383972463])

init(autoreset=True)
white = Fore.RESET
red = Fore.LIGHTRED_EX
dblue = Fore.MAGENTA
gray = Fore.LIGHTBLACK_EX

@tasks.loop(minutes=1)
async def update_online():
    await bot.wait_until_ready()
    try:
        s1 = Srv('194.169.160.48', 22003)
        await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(name=f'онлайн: {s1.players} из {s1.maxplayers}', type=disnake.ActivityType.watching))
        print(f'Онлайн сервера: {s1.players} из {s1.maxplayers}')
    except Exception as e:
        print('Произошла ошибка при попытке подключения, пробую переподключиться.')


@bot.event
async def on_member_join(member):
    cursor = db.cursor()
    if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
        info = 'INSERT INTO users VALUES (?, 0)'
        cursor.execute(info, (member.id,))
        db.commit()

@bot.event
async def on_ready():
    update_online.start()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INT,
                    warns INT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS promocodes (
                    column_use INT  
                    promo_name TEXT,
                    money INT,
                    donate INT,
                    coin INT,
                    save INT
    )''')

    db.commit()


    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
                info = 'INSERT INTO users VALUES (?, 0)'
                cursor.execute(info, (member.id,))
            else:
                pass
    db.commit()

    for cog in os.listdir('mta-grand/cogs'):
        if cog.endswith('.py'):
            bot.load_extension(f'cogs.{cog[:-3]}')
            print(f'{gray}[{dblue}!{gray}]{white} Ког {red} {cog} {white} был запущен')

@bot.command()
@commands.has_any_role(*roles)
async def test(ctx):
    await ctx.send('test')

bot.run("")