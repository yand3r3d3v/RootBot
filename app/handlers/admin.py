from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from app.databases.models import redisClient as client

router = Router()


@router.message(Command('admin'))
async def cmd_admin(message: Message, command: CommandObject):
    id = message.from_user.id

    if not await client.connection.exists(f'user:{id}') or not await client.connection.hget(f'user:{id}', 'admin'):
        return

    if command.args is None:
        await message.reply(text='Используйте /admin add/remove/update/info')
        return

    args = command.args.split()
    match args[0]:
        case 'add':
            if not await client.exists(f'group:{args[1]}'):
                await message.reply(f'Группы {args[1]} не существует')
                return

            for command in args[2:]:

                await client.lpush(f'group:{args[1]}', command)

            await message.reply(text=f'''Вы добавили команду/ы: {args[2:]} в группу {args[1]}''')

        case 'remove':
            if await client.exists(f'user:{args[1]}'):
                await client.delete(f'user:{args[1]}')
                await message.reply(f'Пользователь {args[1]} был удален!')
                return
            await message.reply('Пользователь не найден, проверьте правильность ввода')

        case 'update':
            pass

        case 'info':
            data = await client.lrange(f'user:{args[1]}', 0, -1)
            await message.reply(f'''{data}''')
            pass

        case _:
            await message.reply(text='Используйте /admin add/remove/update/info')
