# by ztoohn

import io, disnake, json
from PIL import Image, ImageDraw, ImageFont
from disnake.ext import commands
from datetime import datetime

from utils.database import connection

class InfoPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.last = 0

    @commands.slash_command(description='Статистика игрока')
    async def infoplayer(self, interaction: disnake.ApplicationCommandInteraction, *, identifier: str):
        font_path = "other/Gilroy-Medium.ttf"

        with Image.open("other/bg.png") as img:
            draw = ImageDraw.Draw(img)
            fontpl = ImageFont.truetype(font_path, size=25)
            fonttime = ImageFont.truetype(font_path, size=28)
            fontstat = ImageFont.truetype(font_path, size=40)
            try:
                with connection.cursor() as cursor:
                    if identifier.isdigit():
                        sql = 'SELECT level, nickname, accesslevel, donate, money, id, reg_date, last_date, playing_time, permanent_data FROM nrp_players WHERE id = %s'
                        cursor.execute(sql, (int(identifier),))
                    else:
                        sql = 'SELECT level, nickname, accesslevel, donate, money, id, reg_date, last_date, playing_time, permanent_data FROM nrp_players WHERE nickname = %s'
                        cursor.execute(sql, (identifier,))

                    info = cursor.fetchone()

                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске информации об аккаунте', color=0x2b2d31)
                        embed.description = 'Аккаунта не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed)

                    level, nickname, accesslevel, donate, money, user_id, reg_date, last_date, playing_time, permanent_data = info

                    admin = [
                        (0, 'Игрок'),
                        (1, 'Стажёр'),
                        (2, 'Хелпер'),
                        (3, 'Ст.Хелпер'),
                        (4, 'Модер'),
                        (5, 'Ст.Модер'),
                        (6, 'Гейм-мастер'),
                        (7, 'Админ'),
                        (8, 'Ст.Админ'),
                        (9, 'Упр.сервера'),
                        (10, 'Гл.Админ'),
                        (11, 'Админ-леад'),
                        (12, 'Руководство')
                    ]

                    accesslevel, adminname = admin[accesslevel]

                    registerdate = datetime.fromtimestamp(reg_date)
                    lastdate = datetime.fromtimestamp(last_date)

                    registerdate_formatted = registerdate.strftime("%d/%m/%Y")
                    lastdate_formatted = lastdate.strftime("%d/%m/%Y")
                    playing_time_hours = playing_time // 3600
                    formatted_money = '{:,}'.format(money).replace(',', ' ')
                    formatted_donate = '{:,}'.format(donate).replace(',', ' ')

                    json_data = permanent_data
                    data = json.loads(json_data)
                    values_coin = str(data[0]['inventory_data'].get('136', 0))
                    values_save = str(data[0]['inventory_data'].get('154', 0))

                    values_coin = values_coin.replace('[', '').replace(']', '')
                    values_save = values_save.replace('[', '').replace(']', '')

                    if values_coin is None:
                        values_coin = '0'
                    if values_save is None:
                        values_save = '0'

                    x_name = 201
                    y_name = 77
                    draw.text(xy=(x_name, y_name), text=f'{str(nickname)}[{str(user_id)}]', font=fontpl)

                    x_level = 326
                    y_level = 286
                    draw.text(xy=(x_level, y_level), text=f'Уровень: {str(level)}', font=fontpl)

                    x_access = 352
                    y_access = 560
                    draw.text(xy=(x_access, y_access), text=f'{str(adminname)}', font=fontpl)

                    x_reg = 600
                    y_reg = 649
                    draw.text(xy=(x_reg, y_reg), text=f'{str(registerdate_formatted)}', font=fonttime)

                    x_last = 836
                    y_last = 649
                    draw.text(xy=(x_last, y_last), text=f'{str(lastdate_formatted)}', font=fonttime)

                    x_ply = 1059
                    y_ply = 647
                    draw.text(xy=(x_ply, y_ply), text=f'{str(playing_time_hours)} часов', font=fonttime)

                    x_mon = 658
                    y_mon = 165
                    draw.text(xy=(x_mon, y_mon), text=f'{str(formatted_money)}', font=fontstat)

                    x_don = 658
                    y_don = 245
                    draw.text(xy=(x_don, y_don), text=f'{str(formatted_donate)}', font=fontstat)

                    x_coin = 658
                    y_coin = 342
                    draw.text(xy=(x_coin, y_coin), text=f'{str(values_coin)} штук', font=fontstat)

                    x_save = 658
                    y_save = 449
                    draw.text(xy=(x_save, y_save), text=f'{str(values_save)} штук', font=fontstat)

                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    file = disnake.File(img_bytes, filename="infoplayer.png")
                    await interaction.response.send_message(file=file)

            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(InfoPlayer(bot))