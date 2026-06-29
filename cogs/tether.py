# by ztoohn
import disnake, json
from disnake.ext import commands, tasks

from utils.database import connection
from utils.succroles import roles


class TeatherModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Ваш код верификации (F4 -> Главная)', placeholder='Например: XXXXXXXXXX', custom_id='teather', style=disnake.TextInputStyle.short, max_length=10, required=True),
            disnake.ui.TextInput(label='Ваш игровой айди (F4 -> Главная)', placeholder='Например: 6811', custom_id='user_id', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Привязка аккаунта к дискорду', components=components, custom_id='teatherModal')

    async def callback(self, interaction: disnake.ModalInteraction):
        teather = interaction.text_values.get('teather')
        user_id = interaction.text_values.get('user_id')
        try:
            with connection.cursor() as cursor:
                query = 'SELECT teather_code, discord_id FROM nrp_players WHERE id=%s'
                cursor.execute(query, (user_id,))
                info = cursor.fetchone()
                if info:
                    teather_code, discord_id = info

                    if teather == teather_code:
                        if discord_id == '0':
                            add_discord = 'UPDATE nrp_players SET discord_id=%s WHERE id=%s'
                            cursor.execute(add_discord, (str(interaction.user.id), str(user_id)))  # Fixed here

                            account_info = 'SELECT nickname, id, permanent_data FROM nrp_players WHERE id=%s'
                            cursor.execute(account_info, (str(user_id),))
                            info_acc = cursor.fetchone()

                            if info_acc:
                                nickname, id, permanent_data = info_acc

                                data = json.loads(permanent_data)
                                if 'inventory_data' not in data[0]:
                                    data[0]['inventory_data'] = {'136': 15, '154': 3}
                                else:
                                    data[0]['inventory_data']['136'] += 15
                                    data[0]['inventory_data']['154'] += 3

                                upd_json = json.dumps(data)

                                sql = 'UPDATE nrp_players SET permanent_data = %s WHERE id = %s'
                                cursor.execute(sql, (upd_json, user_id))
                                connection.commit()

                                values_coin = data[0]['inventory_data']['136']
                                values_save = data[0]['inventory_data']['154']

                                embed = disnake.Embed(title='Успешная привязка аккаунта к дискорду', color=0x2b2d31)
                                embed.description = f'Вы успешно привязали свой **дискорд аккаунт** к аккаунту {nickname}[`{id}`]\nНа ваш аккаунт было зачислено `15` жетонов **прокачки** оружия и `3` жетона **защиты** уровня. Теперь у вас `{values_coin}` жетонов **прокачки** оружия и `{values_save}` жетонов **защиты** уровня'
                                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                                embed.set_footer(text='Привязка разработана -> | akarumay&holodny source')

                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                return
                        else:
                            embed = disnake.Embed(title='Ошибка при попытке привязки аккаунта', color=0x2b2d31)
                            embed.description = 'У вас уже привязан аккаунт Discord к аккаунту MTA. Обратитесь в техническую поддержку для отвязки аккаунта.'
                            embed.set_thumbnail(url=interaction.user.display_avatar.url)
                            embed.set_footer(text='Привязка разработана -> | akarumay&holodny source')
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                embed = disnake.Embed(title='Произошла ошибка при попытке привязки аккаунта', color=0x2b2d31)
                embed.description = 'При попытке привязки аккаунта произошла ошибка, вы указали неверный код.'
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                embed.set_footer(text='Привязка разработана -> | akarumay&holodny source')

                await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)



class TeatherButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Верифицировать', style=disnake.ButtonStyle.success, custom_id='teather', emoji='🛡')
    async def teather(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        '''Кнопка привязки аккаунта мта и дискорд'''
        try:
            with connection.cursor() as cursor:

                callback = cursor.execute('SELECT discord_id FROM nrp_players')
                user_id = interaction.user.id

                discord_ids = [row[0] for row in cursor.fetchall()]

                if user_id in discord_ids:
                    embed = disnake.Embed(title='Ошибка при попытки привязки аккаунта', color=0x2b2d31)
                    embed.description = 'У вас уже привязан аккаунт дискорд к аккаунту MTA. Напишите в тех.поддержку для того, что бы отвязать аккаунт'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text='Привязка разработана -> | akarumay&holodny source')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await interaction.response.send_modal(TeatherModal())

        except Exception as e:
            print(e)

class Tether(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*roles)
    async def privyaz(self, ctx):
        embed = disnake.Embed(title='Привязка аккаунт дискорд к аккаунту MTA', color=0x2b2d31)
        embed.description = 'Для того, что бы **привязать** аккаунт дискорд к аккаунту МТА, нажмите кнопку ниже.\nПри успешной привязки вы получите: `15` жетонов прокачки оружия, и `3` жетона сохранения уровня'
        embed.set_footer(text='Привязка разработана -> | akarumay&holodny source')

        await ctx.send(embed=embed, view=TeatherButton())

    @privyaz.error
    async def action_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            user = ctx.author
            emb = disnake.Embed(title='Ошибка при выполнение команды', color=0x2b2d31)
            emb.description = 'У вас не хватает прав для выполнения данной команды.'
            emb.set_thumbnail(url=user.display_avatar.url)
            await user.send(embed=emb)

def setup(bot):
    bot.add_cog(Tether(bot))