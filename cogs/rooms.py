# by ztoohn
import disnake

from disnake.ext import commands
from datetime import datetime

from utils.succroles import roles
from utils.id import private_channel, private_message, default_room_category_id, default_room_creator_id

room_category = None
room_creator = None

async def delete_channel(guild, channel_id):
    channel = guild.get_channel(channel_id)
    await channel.delete()

async def create_voice_channel(guild, channel_name):
    channel = await guild.create_voice_channel(channel_name, category=room_category)
    return channel

class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='', style=disnake.ButtonStyle.gray, custom_id='hide', emoji='<:hide:1208442132210258010>')
    async def hide(self, button: disnake.ui.Button, interaction: disnake.ApplicationCommandInteraction):
        '''Отобразить/Скрыть комнату'''
        user = interaction.user
        guild = interaction.guild
        voice_state = user.voice

        if voice_state is None or voice_state.channel is None:
            embed = disnake.Embed(title='Скрыть комнату для всех', color=0x2b2d31)
            embed.description = f'{user.mention}, Вы **не находитесь** в голосовом канале!'
            embed.set_thumbnail(url=user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            channel = voice_state.channel
            permissions = channel.permissions_for(user)
            can_edit = permissions.manage_channels

            standartpermissions = channel.permissions_for(guild.default_role)
            can_vision = standartpermissions.read_messages

            if can_edit:
                if can_vision:
                    await channel.set_permissions(guild.default_role, read_messages=False)
                    embed = disnake.Embed(title='Скрыть комнату для всех', color=0x2b2d31)
                    embed.description = f'{user.mention}, Вы успешно **скрыли** Вашу приватную комнату для всех.'
                    embed.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await channel.set_permissions(guild.default_role, read_messages=True)
                    embed = disnake.Embed(title='Скрыть комнату для всех', color=0x2b2d31)
                    embed.description = f'{user.mention}, Вы успешно **открыли** Вашу приватную комнату для всех.'
                    embed.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = disnake.Embed(title='Скрыть комнату для всех', color=0x2b2d31)
                embed.description = f'{user.mention}, У Вас **недостаточно прав** для скрытия комнаты!'
                embed.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)

class Rooms(commands.Cog):
    def __inti__(self, bot):
        self.bot = bot

    @commands.command()
    async def privchannel(self, ctx):
        '''Ембед и кнопки настроек приватной комнатой'''

        settings = disnake.Embed(title='Управление приватной комнатой', color=0x2b2d31)
        settings.description = '**Жми следующие кнопки, чтобы настроить свою приватную комнату.**\nИспользовать их можно только когда у тебя есть приватный канал\n\n'
        settings.add_field(name='', value='\n<:hide:1208442132210258010> — Отобразить/скрыть комнату\n'
                                          '<:edit:1208442130067099678> — Изменить название комнаты\n'
                                          '<:owner:1208442122475413545> — Передать владение комнатой\n'
                                          '<:kick:1208442134265466980> — Выгнать из комнаты\n'
                                          '<:add:1208442128234057768> — Выдать доступ в комнату\n')
        settings.add_field(name='', value='\n<:remove:1208442124459048970> — Забрать доступ в комнату\n'
                                          '<:voice:1208442126493552650> — Выдать право говорить\n'
                                          '<:mutev:1208442119493263441> — Забрать право говорить\n'
                                          '<:limit:1208442136345710632> — Изменить лимит пользователей\n'
                                          '<:lockv:1208442117530058833> — Открыть/закрыть комнату')

        settings.set_footer(text='Управлять приватной комнатой можно через шестерёнкку.')
        await ctx.send(embed=settings, view=ButtonView())

def setup(bot):
    bot.add_cog(Rooms(bot))