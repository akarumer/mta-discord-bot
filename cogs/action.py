# by ztoohn
import disnake, json
from disnake.ext import commands
from datetime import datetime

from utils.database import connection
from utils.succroles import roles

class virtualMoney(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите количество валюты', placeholder='Например: 1999999', custom_id='amount', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Устаноовить виртуальную валюту', components=components, custom_id='virtulModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET mney = %s WHERE id = %s'
                    cursor.execute(sql, (int(amount), int(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, money FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET money = %s WHERE nickname = %s'
                    cursor.execute(sql, (int(amount), str(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, money FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)

                nickname, id, money = info

                updinfo = disnake.Embed(title=f'Установка виртуальной валюты - {nickname}[{id}]', color=0x2b2d31)
                updinfo.description = f'Вы успешно изменили **виртуальную валюту** игроку {nickname}. Теперь у него `{money}` виртуальной валюты.'
                updinfo.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class donateMoney(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите количество доната', placeholder='Например: 1999999', custom_id='amount', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Установить донатную валюту', components=components, custom_id='donateModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET donate = %s WHERE id = %s'
                    cursor.execute(sql, (int(amount), int(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, donate FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET donate = %s WHERE nickname = %s'
                    cursor.execute(sql, (int(amount), str(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, donate FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)

                nickname, id, donate = info

                updinfo = disnake.Embed(title=f'Установка донатной валюты - {nickname}[{id}]', color=0x2b2d31)
                updinfo.description = f'Вы успешно изменили **донатную валюту** игроку {nickname}. Теперь у него `{donate}` донатной валюты.'
                updinfo.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class adminLevel(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите уровень прав', placeholder='Например: 11', custom_id='amount', style=disnake.TextInputStyle.short, max_length=3, required=True)
        ]
        super().__init__(title='Установить права админитсратора', components=components, custom_id='adminModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET accesslevel = %s WHERE id = %s'
                    cursor.execute(sql, (int(amount), int(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, accesslevel FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET accesslevel = %s WHERE nickname = %s'
                    cursor.execute(sql, (int(amount), str(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id, accesslevel FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)

                nickname, id, accesslevel = info

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

                updinfo = disnake.Embed(title=f'Установка уровня прав - {nickname}[{id}]', color=0x2b2d31)
                updinfo.description = f'Вы успешно изменили **уровень прав администратора** игроку {nickname}. Теперь у него `{adminname}[{accesslevel}]`.'
                updinfo.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=updinfo, ephemeral=True)

        except Exception as e:
            print(e)

class socailModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите социальный рейтинг', placeholder='Например: от -1000 до 1000', custom_id='amount', style=disnake.TextInputStyle.short, max_length=5, required=True)
        ]
        super().__init__(title='Изменить социальный рейтинг', components=components, custom_id='socialModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = int(interaction.text_values.get('amount'))
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if amount >= 1000:
                    embed = disnake.Embed(title='Ошибка при изменении социального рейтинга', color=0x2b2d31)
                    embed.description = 'Вы можете **установить** максимум `1000` социального рейтинга на один аккаунт'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif amount <= -1000:
                    embed = disnake.Embed(title='Ошибка при изменении социального рейтинга', color=0x2b2d31)
                    embed.description = 'Вы можете **установить** минимум `-1000` социального рейтинга на один аккаунт'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if ident.isdigit():
                        sql = 'UPDATE nrp_players SET social_rating = %s WHERE id = %s'
                        cursor.execute(sql, (amount, int(ident)))
                        connection.commit()
                        cursor.execute('SELECT nickname, id, social_rating FROM nrp_players WHERE id = %s', (int(ident),))
                    else:
                        sql = 'UPDATE nrp_players SET social_rating = %s WHERE nickname = %s'
                        cursor.execute(sql, (amount, ident))
                        connection.commit()
                        cursor.execute('SELECT nickname, id, social_rating FROM nrp_players WHERE nickname = %s', (ident,))

                    info = cursor.fetchone()

                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                        embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed, ephemeral=True)

                    nickname, id, social_rating = info

                    updinfo = disnake.Embed(title=f'Изменение социального рейтинга - {nickname}[{id}]', color=0x2b2d31)
                    updinfo.description = f'Вы успешно изменили **социальный рейтинг** игроку {nickname}. Теперь у него `{social_rating}` социального рейтинга.'
                    updinfo.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=updinfo, ephemeral=True)

        except Exception as e:
            print(e)

class nickModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите новый никнейм', placeholder='Например: Максим Гангшутер', custom_id='amount', style=disnake.TextInputStyle.short, max_length=50, required=True)
        ]
        super().__init__(title='Изменить никнейм игроку', components=components, custom_id='nickModal')
    
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET nickname = %s WHERE id = %s'
                    cursor.execute(sql, (str(amount), int(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET nickname = %s WHERE nickname = %s'
                    cursor.execute(sql, (str(amount), str(ident)))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    nickname, id = info

                    updinfo = disnake.Embed(title=f'Изменение никнейма игроку - {nickname}[{id}]', color=0x2b2d31)
                    updinfo.description = f'Вы успешно изменили **никнейм** игроку с ID `{id}` на **{amount}**.'
                    updinfo.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class maleModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True)
        ]
        super().__init__(title='Изменить пол игроку на мужской', components=components, custom_id='maleModal')
    
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET gender = 0 WHERE id = %s'
                    cursor.execute(sql, int(ident))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET gender = 0 WHERE nickname = %s'
                    cursor.execute(sql, str(ident))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    nickname, id = info

                    updinfo = disnake.Embed(title=f'Изменение пола игроку - {nickname}[{id}]', color=0x2b2d31)
                    updinfo.description = f'Вы успешно пол игрока **{nickname}**[`{id}`] на мужской.'
                    updinfo.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class femaleModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True)
        ]
        super().__init__(title='Изменить пол игроку на женский', components=components, custom_id='femaleModal')
    
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'UPDATE nrp_players SET gender = 1 WHERE id = %s'
                    cursor.execute(sql, int(ident))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE id = %s', (int(ident),))
                else:
                    sql = 'UPDATE nrp_players SET gender = 1 WHERE nickname = %s'
                    cursor.execute(sql, str(ident))
                    connection.commit()
                    cursor.execute('SELECT nickname, id FROM nrp_players WHERE nickname = %s', (str(ident),))

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    nickname, id = info

                    updinfo = disnake.Embed(title=f'Изменение пола игроку - {nickname}[{id}]', color=0x2b2d31)
                    updinfo.description = f'Вы успешно пол игрока **{nickname}**[`{id}`] на женский.'
                    updinfo.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class removePlayer(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True)
        ]
        super().__init__(title='Удалить аккаунт игроку', components=components, custom_id='removeModal')
    
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        user = interaction.user
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'DELETE FROM nrp_players WHERE id = %s'
                    cursor.execute(sql, int(ident))
                    connection.commit()
                else:
                    sql = 'DELETE FROM nrp_players WHERE nickname = %s'
                    cursor.execute(sql, str(ident))
                    connection.commit()

                info = cursor.fetchone()

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:

                    updinfo = disnake.Embed(title=f'Удаление аккаунта - {ident}', color=0x2b2d31)
                    updinfo.description = f'Вы успешно удалили аккаунт `{ident}`'
                    updinfo.set_thumbnail(url=user.display_avatar.url)
                    await interaction.response.send_message(embed=updinfo, ephemeral=True)
        except Exception as e:
            print(e)

class GenderSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label='Мужской', description='Установить мужской пол игроку', emoji='♂'),
            disnake.SelectOption(label='Женский', description='Установить женский пол игроку', emoji='♀')
        ]
        super().__init__(placeholder='Выберите пол >', min_values=1, max_values=1, options=options)
    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        if not interaction.values:
            await interaction.response.defer()
        elif interaction.values[0] == 'Мужской':
            await interaction.response.send_modal(maleModal())
        elif interaction.values[0] == 'Женский':
            await interaction.response.send_modal(femaleModal())

class newJeton(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите количество жетончиков', placeholder='Например: 160', custom_id='amount', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Изменить количество жетонов', components=components, custom_id='JetonModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'SELECT nickname, id, permanent_data FROM nrp_players WHERE id = %s'
                    cursor.execute(sql, int(ident))
                    info = cursor.fetchone()
                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                        embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        nickname, id, permanent_data = info
                        json_data = permanent_data
                        data = json.loads(json_data)
                        data[0]['inventory_data']['136'] = amount
                        upd_json = json.dumps(data)
                        sql = 'UPDATE nrp_players SET permanent_data = %s WHERE id = %s'
                        cursor.execute(sql, (upd_json, ident,))
                        connection.commit()

                        values_coin = data[0]['inventory_data'].get('136', 0)

                        if values_coin is None:
                            values_coin = 0

                        embed = disnake.Embed(title=f'Изменить жетоны прокачки оружия - {nickname}[{id}]', color=0x2b2d31)
                        embed.description = f'Вы успешно изменили количество жетонов прокачки оружия на аккаунте **{nickname}**[`{id}`]. Теперь у него `{values_coin}` жетонов.'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    sql = 'SELECT nickname, id, permanent_data FROM nrp_players WHERE nickname = %s'
                    cursor.execute(sql, str(ident))
                    info = cursor.fetchone()
                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                        embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        nickname, id, permanent_data = info
                        json_data = permanent_data
                        data = json.loads(json_data)
                        data[0]['inventory_data']['136'] = amount
                        upd_json = json.dumps(data)
                        sql = 'UPDATE nrp_players SET permanent_data = %s WHERE nickname = %s'
                        cursor.execute(sql, (upd_json, str(ident),))
                        connection.commit()

                        values_coin = data[0]['inventory_data'].get('136', 0)

                        if values_coin is None:
                            values_coin = 0

                        embed = disnake.Embed(title=f'Изменить жетоны прокачки оружия - {nickname}[{id}]', color=0x2b2d31)
                        embed.description = f'Вы успешно изменили количество жетонов прокачки оружия на аккаунте **{nickname}**[`{id}`]. Теперь у него `{values_coin}` жетонов.'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)

                        await interaction.response.send_message(embed=embed, ephemeral=True)

                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)

class newJetonDef(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Введите ID или НИКНЕЙМ игрока', placeholder='Например: 3 | Максим Самопсих', custom_id='ident', style=disnake.TextInputStyle.short, max_length=50, required=True),
            disnake.ui.TextInput(label='Введите количество жетончиков', placeholder='Например: 160', custom_id='amount', style=disnake.TextInputStyle.short, max_length=10, required=True)
        ]
        super().__init__(title='Изменить количество жетонов', components=components, custom_id='JetonDefModal')
    async def callback(self, interaction: disnake.ModalInteraction):
        ident = interaction.text_values.get('ident')
        amount = interaction.text_values.get('amount')
        try:
            with connection.cursor() as cursor:
                if ident.isdigit():
                    sql = 'SELECT nickname, id, permanent_data FROM nrp_players WHERE id = %s'
                    cursor.execute(sql, int(ident))
                    info = cursor.fetchone()
                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                        embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        nickname, id, permanent_data = info
                        json_data = permanent_data
                        data = json.loads(json_data)
                        data[0]['inventory_data']['154'] = amount
                        upd_json = json.dumps(data)
                        sql = 'UPDATE nrp_players SET permanent_data = %s WHERE id = %s'
                        cursor.execute(sql, (upd_json, ident,))
                        connection.commit()

                        values_save = data[0]['inventory_data'].get('154', 0)

                        if values_save is None:
                            values_save = 0

                        embed = disnake.Embed(title=f'Изменить количество жетонов защиты уровня - {nickname}[{id}]', color=0x2b2d31)
                        embed.description = f'Вы успешно изменили количество жетонов защиты уровня на аккаунте **{nickname}**[`{id}`]. Теперь у него `{values_save}` жетонов.'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    sql = 'SELECT nickname, id, permanent_data FROM nrp_players WHERE nickname = %s'
                    cursor.execute(sql, str(ident))
                    info = cursor.fetchone()
                    if info is None:
                        embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                        embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)
                        embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        nickname, id, permanent_data = info
                        json_data = permanent_data
                        data = json.loads(json_data)
                        data[0]['inventory_data']['154'] = amount
                        upd_json = json.dumps(data)
                        sql = 'UPDATE nrp_players SET permanent_data = %s WHERE nickname = %s'
                        cursor.execute(sql, (upd_json, str(ident),))
                        connection.commit()

                        values_save = data[0]['inventory_data'].get('154', 0)

                        if values_save is None:
                            values_save = 0

                        embed = disnake.Embed(title=f'Изменить количество жетонов защиты уровня - {nickname}[{id}]', color=0x2b2d31)
                        embed.description = f'Вы успешно изменили количество жетонов защиты уровня на аккаунте **{nickname}**[`{id}`]. Теперь у него `{values_save}` жетонов.'
                        embed.set_thumbnail(url=interaction.user.display_avatar.url)

                        await interaction.response.send_message(embed=embed, ephemeral=True)


                if info is None:
                    embed = disnake.Embed(title='Ошибка при поиске аккаунта', color=0x2b2d31)
                    embed.description = 'Аккаунт не найден, попробуйте ввести другой айди'
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f'Команду вызвал: {interaction.user.name} || {interaction.user.id}')

                    await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            print(e)

class actionSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label='Виртуальная валюта', description='Вы установите определённое количество валюты'),
            disnake.SelectOption(label='Донатная валюта', description='Вы установите определённое количество донатной валюты'),
            disnake.SelectOption(label='Права Администратора', description='Вы установите определённые права администратора'),
            disnake.SelectOption(label='Социальный рейтинг', description='Вы установите определённое количество социального рейтинга'),
            disnake.SelectOption(label='Уровень аккаунта', description='Вы установите определённое уровень'),
            disnake.SelectOption(label='Никнейм игрока', description='Вы измените никнейм игроку'),
            disnake.SelectOption(label='Пол игрока', description='Вы измените пол игроку'),
            disnake.SelectOption(label='Жетоны прокачки оружия', description='Изменить количество жетонов', emoji='⚡'),
            disnake.SelectOption(label='Жетоны сохранения уровня', description='Изменить количетсво жетонов', emoji='⚡'),
            disnake.SelectOption(label='Удалить аккаунт', description='Вы полностью удалите аккаунт с игры', emoji='❌')
        ]
        super().__init__(placeholder='Выберите действие над игрком >', min_values=0, max_values=1, options=options)
    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        if not interaction.values:
            await interaction.response.defer()
        elif interaction.values[0] == 'Виртуальная валюта':
            await interaction.response.send_modal(virtualMoney())
        elif interaction.values[0] == 'Донатная валюта':
            await interaction.response.send_modal(donateMoney())
        elif interaction.values[0] == 'Права Администратора':
            await interaction.response.send_modal(adminLevel())
        elif interaction.values[0] == 'Социальный рейтинг':
            await interaction.response.send_modal(socailModal())
        elif interaction.values[0] == 'Никнейм игрока':
            await interaction.response.send_modal(nickModal())
        elif interaction.values[0] == 'Пол игрока':
            embed = disnake.Embed(title=f'Установить пол игроку - {interaction.user.name}', color=0x2b2d31)
            embed.description = 'Для того, что бы продолжить, выберите пол для изменения.'
            embed.set_thumbnail(url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed, view=SelectGender(), ephemeral=True)
        elif interaction.values[0] == 'Удалить аккаунт':
            await interaction.response.send_modal(removePlayer())
        elif interaction.values[0] == 'Жетоны прокачки оружия':
            await interaction.response.send_modal(newJeton())
        elif interaction.values[0] == 'Жетоны сохранения уровня':
            await interaction.response.send_modal(newJetonDef())

class SelectAction(disnake.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__()
        self.add_item(actionSelect())

class SelectGender(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GenderSelect())

class ActionPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Меню управления игроком')
    @commands.has_any_role(*roles)
    async def action(self, interaction: disnake.ApplicationCommandInteraction, *, identifier: str):
        '''Вызов панели управления игроком'''
        user = interaction.user

        try:
            with connection.cursor() as cursor:

                if identifier.isdigit():
                    sql = 'SELECT id, nickname FROM nrp_players WHERE id = %s'
                    cursor.execute(sql, (int(identifier),))
                else:
                    sql = 'SELECT id, nickname FROM nrp_players WHERE nickname = %s'
                    cursor.execute(sql, (identifier,))

                for info in cursor:
                    id, nickname = info

                time = datetime.now()
                formatted_time = disnake.utils.format_dt(time, style='R')
                emb = disnake.Embed(title=f'Меню управления игроком - {nickname}[{id}]', color=0x2b2d31)
                emb.description = f'Меню открыто: {formatted_time}. Для того, что бы продолжить, выберите один из пунктов ниже.'
                emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/1031255562819752031/1110225142212218961/118.png')
                emb.set_footer(text=f'Открыто: {user.name} | ID: {user.id}')

                await interaction.response.send_message(embed=emb, view=SelectAction(), ephemeral=True)
        except Exception as e:
            print(e)

    @action.error
    async def action_error(self, interaction: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingAnyRole):
            user = interaction.user
            emb = disnake.Embed(title='Ошибка при выполнение команды', color=0x2b2d31)
            emb.description = 'У вас не хватает прав для выполнения данной команды.'
            emb.set_thumbnail(url=user.display_avatar.url)
            await interaction.response.send_message(embed=emb, ephemeral=True)

def setup(bot):
    bot.add_cog(ActionPlayer(bot))