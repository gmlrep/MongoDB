from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from utils.utils import async_get_pay

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer(text=f'Hi [{message.from_user.first_name}](https://t.me/{message.from_user.username})!',
                         parse_mode='Markdown',
                         disable_web_page_preview=True)


@router.message(F.text)
async def get_input_data(message: Message):
    error_text = ('Невалидный запрос. Пример запроса:'
                  '{"dt_from": "2022-09-01T00:00:00", '
                  '"dt_upto": "2022-12-31T23:59:00", '
                  '"group_type": "month"}')
    try:
        input_data = eval(message.text)
        output_data = await async_get_pay(data=input_data)
        if output_data is None:
            await message.answer(text=error_text)
        else:
            new_output_data = f"{output_data}"
            new_output_data = new_output_data.replace("'", '"')
            await message.answer(text=new_output_data)
    except NameError:
        await message.answer(text=error_text)
