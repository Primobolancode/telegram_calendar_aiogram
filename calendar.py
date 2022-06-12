from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    callback_query, Location
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import date, datetime, time
import calendar
from calendar import monthrange
from dateutil.relativedelta import relativedelta

token = "5462774258:AAEV74hyyQLC6a7p63Rc9i8kLSjiU1GpSvw"
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
dates = []
for i in range (1, 32):
    dates.append(i)

########## START ##########
@dp.message_handler(commands=['start'], state=['*'])
async def start_bot(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           "Выберите дату", reply_markup = create_month_inline(date=today()))


def create_month_inline(date):
    markup = InlineKeyboardMarkup() # Создание ряда
    markup.row_width = 3 # Длина ряда
    markup = row_of_years(date, markup) # Ряд годов
    markup = row_of_months(date, markup) # Ряд месяцев
    markup.row_width = 1 # Длина ряда
    markup.row().add(InlineKeyboardButton(text='■■■■■■■■■■■■■', callback_data='-')) # Разделитель
    markup.row_width = 7 # Длина ряда
    row_of_weekdays(markup) # Дни недели (названия)
    rows_of_weeks(date, markup) # Дни месяца (1-31)
    return markup
###############################################################
########## Приемник + 1 год ##########
@dp.callback_query_handler(lambda event: event.data.startswith('next_year_'))
async def next_year(call: types.CallbackQuery):
    date = call.data.split('next_year_')[1]
    date = datetime.strptime(date, '%Y-%m-%d')
    next_date = date.replace(date.year + 1)
    await call.message.edit_reply_markup(create_month_inline(next_date))
########## Приемник - 1 год ##########
@dp.callback_query_handler(lambda event: event.data.startswith('prev_year_'))
async def prev_year(call: types.CallbackQuery):
    date = call.data.split('prev_year_')[1]
    date = datetime.strptime(date, '%Y-%m-%d')
    next_date = date.replace(date.year - 1)
    await call.message.edit_reply_markup(create_month_inline(next_date))
########## Приемник - 1 месяц ##########
@dp.callback_query_handler(lambda event: event.data.startswith('prev_month_'))
async def prev_month(call: types.CallbackQuery):
    date = call.data.split('prev_month_')[1]
    date = datetime.strptime(date, '%Y-%m-%d')
    next_date = date + relativedelta(months=-1)
    await call.message.edit_reply_markup(create_month_inline(next_date))
########## Приемник + 1 месяц ##########
@dp.callback_query_handler(lambda event: event.data.startswith('next_month_'))
async def next_month(call: types.CallbackQuery):
    date = call.data.split('next_month_')[1]
    date = datetime.strptime(date, '%Y-%m-%d')
    next_date = date + relativedelta(months=1)
    await call.message.edit_reply_markup(create_month_inline(next_date))
########## Приемник даты ##########
@dp.callback_query_handler(lambda event: event.data.startswith('date_'))
async def next_month(call: types.CallbackQuery):
    print(call.data)
###############################################################
def row_of_years(date, markup):
    current_month = date.month
    current_day = date.day
    current_year = date.year
    prev_year = date.year - 1
    next_year = date.year + 1
    next_year_text = str(str(next_year) + '   >')
    prev_year_text = str('<   ' + str(prev_year))
    current_year_button = InlineKeyboardButton(text=current_year, callback_data=f'current_year_{date.year}')
    prev_year_button = InlineKeyboardButton(text=prev_year_text, callback_data=f'prev_year_{date.year}-{date.month}-{date.day}')
    next_year_button = InlineKeyboardButton(text=next_year_text, callback_data=f'next_year_{date.year}-{date.month}-{date.day}')
    return markup.row().add(prev_year_button,current_year_button, next_year_button)
def row_of_months(date, markup):
    current_month = date.month
    prev_month = date.month - 1
    if prev_month > 12:
        prev_month = 1
    elif prev_month < 1:
        prev_month = 12
    next_month = date.month + 1
    if next_month > 12:
        next_month = 1
    elif next_month < 1:
        next_month = 12
    current_month_text = from_num_to_month(current_month)
    next_month_text = from_num_to_month(next_month)
    prev_month_text = from_num_to_month(prev_month)
    next_month_text = next_month_text + '     >'
    prev_month_text = '<     ' + prev_month_text
    current_month_button = InlineKeyboardButton(text=current_month_text, callback_data=f'current_month')
    prev_month_button = InlineKeyboardButton(text=prev_month_text, callback_data=f'prev_month_{date.year}-{date.month}-{date.day}')
    next_month_button = InlineKeyboardButton(text=next_month_text, callback_data=f'next_month_{date.year}-{date.month}-{date.day}')
    return markup.row().add(prev_month_button,current_month_button, next_month_button)
def row_of_weekdays(markup):
    row = []
    weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    for day in weekdays:
        row.append(InlineKeyboardButton(text=f'{day}', callback_data=f'{day}'))
    markup.row().add(*row)
    return markup
def rows_of_weeks(date, markup):
    list_of_weeks = calendar.monthcalendar(date.year, date.month)
    row = []
    print(list_of_weeks)
    print(date.year)
    print(date.month)
    for week in list_of_weeks:
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(text='❌', callback_data='❌'))
            else:
                row.append(InlineKeyboardButton(text=f'{day}',callback_data=f'date_{date.year}-{date.month}-{day}'))
    markup.row().add(*row)
    return markup
def today():
    today = date.today()
    return today
def from_num_to_month(num):
    if num == 1:
        return 'Январь'
    elif num == 2:
        return 'Февраль'
    elif num == 3:
        return 'Март'
    elif num == 4:
        return 'Апрель'
    elif num == 5:
        return 'Май'
    elif num == 6:
        return 'Июнь'
    elif num == 7:
        return 'Июль'
    elif num == 8:
        return 'Август'
    elif num == 9:
        return 'Сентябрь'
    elif num == 10:
        return 'Октябрь'
    elif num == 11:
        return 'Ноябрь'
    elif num == 12:
        return 'Декабрь'
    else:
        return None
###############################################################
executor.start_polling(dp, skip_updates=True)
