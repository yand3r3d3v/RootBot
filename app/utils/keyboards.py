from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from app.databases.models import redisClient as client


async def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Купить доступ', callback_data='buy')],
        [InlineKeyboardButton(text='Посмотреть возможности', callback_data='info')]
    ])

    return kb

async def back():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='info')]
    ])

    return kb

async def groups_info():
    kb = InlineKeyboardBuilder()

    groups = await client.connection.keys('group:*')
    maxed_group = max(int(i.split(':')[1]) for i in groups)
    for i in range(1, maxed_group+1):
        kb.add(InlineKeyboardButton(text=f'Группа: №{i}', callback_data=f'info_{i}'))

    kb.add(InlineKeyboardButton(text='Меню', callback_data='main_menu'))

    return kb.adjust(2).as_markup()

