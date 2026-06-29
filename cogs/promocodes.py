# by akarumay
import disnake
from disnake.ext import commands

from utils.succroles import roles
from utils.database import connection, promodb

promo_channel = 1207968478104133632

class promoButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Получить промокод', style=disnake.ButtonStyle.gray, custom_id='promo', emoji='🎁')
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        user_id = interaction.user.id
        guild = interaction.guild
        try:
            with connection.cursor() as cursor:
                query = 'SELECT id FROM nrp_players WHERE discord_id=%s'
                cursor.execute(query, (user_id,))
                info = cursor.fetchone()
                
                id = info
                
                upd_info = 'UPDATE nrp_players SET'
                

        except Exception as e:
            print(e)


class promoModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите название промокода', placeholder='Например: 68sjdk1*2d', custom_id='promo', style=disnake.TextInputStyle.short, max_length=10, required=True),
            disnake.ui.TextInput(label='Введите кол-во использований', placeholder='Например: 15', custom_id='column', style=disnake.TextInputStyle.short, max_length=10, required=True),
            disnake.ui.TextInput(label='Введите сумму донат валюты', placeholder='Например: 20000', custom_id='donate', style=disnake.TextInputStyle.short, max_length=10, required=True),
            disnake.ui.TextInput(label='Кол-во жетонов прокачки', placeholder='Например: 15', custom_id='coin', style=disnake.TextInputStyle.short, max_length=10, required=True),
            disnake.ui.TextInput(label='Кол-во жетонов защиты', placeholder='Например: 3', custom_id='save', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Создание промокода МТА', components=components, custom_id='promoModl')
    async def callback(self, interaction: disnake.ModalInteraction):
        promo = interaction.text_values.get('promo')
        column = interaction.text_values.get('column')
        donate = interaction.text_values.get('donate')
        coin = interaction.text_values.get('coin')
        save = interaction.text_values.get('save')

        guild = interaction.guild

        cursor = promodb.cursor()
        cursor.execute('INSERT INTO promocodes (promo_name, column_use, donate, coin, save) VALUES (%s, %s, %s, %s, %s, %s)', (promo, column, donate, coin, save))
        promodb.commit()

        embed = disnake.Embed(title='Успешное создание промокода', color=0x2b2d31)
        embed.description = f'Вы успешно **создали промокод** с названием `{promo}` и `{column}` количеством использований.'
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text=f'Создание промокода -> {interaction.user.name} | {interaction.user.id}')
        await interaction.response.send_message(embed=embed, ephemeral=True)

        channel = disnake.utils.get(guild.text_channels, id=promo_channel)

        memembed = disnake.Embed(title='Появился новый промокод', color=0x2b2d31)
        memembed.description = f'''
        Промокод: `{promo}`
        Кол-во использований: `{column}`
        Кол-во донат валюты: `{donate}`
        Жетонов прокачки оружия: `{coin}`
        Жетонов защиты уровня: `{save}`
        '''
        memembed.add_field(name='Перейти в канал:', value=f'{channel.mention}', inline=False)
        memembed.set_footer(text=f'Проомокод создан -> {interaction.user.name} | ID: {interaction.user.id}')
        for member in guild.members:
            await member.send(embed=embed)

        channelemb = disnake.Embed(title='Появился новый промокод', color=0x2b2d31)
        channelemb.description = f'''
        Промокод: `{promo}`
        Кол-во использований: `{column}`
        Кол-во донат валюты: `{donate}`
        Жетонов прокачки оружия: `{coin}`
        Жетонов защиты уровня: `{save}`
        '''
        channelemb.set_footer(text=f'Проомокод создан -> {interaction.user.name} | ID: {interaction.user.id}')

        await interaction.response.send_message(embed=embed, view=view())

class Promocodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Создать промокод для игроков')
    @commands.has_any_role(*roles)
    async def createpromo(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_modal(promoModal())

def setup(bot):
    bot.add_cog(Promocodes(bot))