from aiogram import Router, F

from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery

from app.utils.keyboards import main_menu, groups_info, back
from app.utils.rcon import MinecraftRconClient
from app.databases.models import redisClient as client

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        text='Привет! Это бот для управление сервером Minecraft через протокол RCON',
        reply_markup=await main_menu()
    )


@router.callback_query(F.data == 'info')
@router.callback_query(F.data == 'main_menu')
async def query_info(callback: CallbackQuery):
    await callback.answer()
    if F.data == 'info':
        await callback.message.edit_text(
            text='Выберите нужный вариант:',
            reply_markup=await groups_info()
        )
    else:
        await callback.message.answer(
            text='Привет! Это бот для управление сервером Minecraft через протокол RCON1',
            reply_markup=await main_menu()
        )


@router.callback_query(F.data.startswith('info_'))
async def query_info(callback: CallbackQuery):
    await callback.answer()
    group = callback.data.split('_')[1]
    commands = await client.available_commands(group)
    await callback.message.edit_text(
        text=f'Список доступных команд группе №{group}: \n' + '\n'.join(commands),
        reply_markup=await back()
    )


@router.message(Command('cmd'))
async def run_cmd(message: Message, command: CommandObject):
    id = message.from_user.id
    args = command.args
    if not await client.connection.exists(f'user:{id}'):
        await message.reply(
            text='У вас нет доступа к данной команде',
            reply_markup=await main_menu()
        )
        return

    group = await client.connection.hget(f'user:{id}', 'group')
    available_commands = await client.available_commands(group)

    if args is None:
        await message.reply(text=f'''Правильное использование - /cmd (команда) (аргументы)
        
Список доступных команд:''' + '\n' + '\n'.join(available_commands)
        )
        return

    if args.split()[0] not in available_commands:
        await message.reply(f'{args.split()[0]} используйте доступные команды!')

    rcon = MinecraftRconClient()

    try:
        await rcon.connect()
        response = await rcon.execute(args.replace('/', ''))
    except Exception as e:
        response = None
    finally:
        await rcon.disconnect()

    if response is None:
        await message.reply(text='Произошла ошибка, подождите или сообщите администрации!')
        return

    await message.reply(text=f'''Ответ сервера: {response[0]}''')
