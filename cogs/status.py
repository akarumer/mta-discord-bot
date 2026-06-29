import disnake
import ping3
import time
from disnake.ext import commands
from mta.monitoring import Server as Srv

class StatusServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description='Информация о сервере')
    async def status(self, interaction: disnake.ApplicationCommandInteraction):
        ip = '194.169.160.48'
        port = 22003

        # Пингуем IP-адрес
        ping_time = ping3.ping(ip, timeout=1)
        ping_time_seconds = ping_time
        ping_time_ms = ping_time_seconds * 1000
        integer_part = int(ping_time_ms)
        
        s1 = Srv('194.169.160.48', 22003)
        link = 'https://discord.com/users/1157713984049389731'

        status = disnake.Embed(title='Miruku', color=0x2b2d31)
        status.description = f'''
Developer: **[selfpsycho.]({link})**
🔗 ・ **Information**
・ Game: **{s1.game}**
・ Name: **{s1.name}**
・ Gamemode: **{s1.gamemode}**
・ Map: **{s1.map}**
・ Version: **{s1.version}**
・ Somewhat: **{s1.somewhat}**
🔮 ・ **Shards**
・ ID: **1** | Ping: **{integer_part if integer_part is not None else "N/A"} ms**
'''
        status.set_footer(text=f'Онлайн: {s1.players} | {s1.maxplayers}. << {interaction.user.name}')

        await interaction.response.send_message(embed=status)

def setup(bot):
    bot.add_cog(StatusServer(bot))
