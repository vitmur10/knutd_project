import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from asgiref.sync import sync_to_async
from django.core.wsgi import get_wsgi_application
import random
from Infotron.keybord import *
from Infotron.Const import *
from Infotron.filters import *
from datetime import datetime, timedelta

faculties = [facult[0] for facult in cur.fetchall()]
faculty_list = ",".join(faculties)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knutd_project.settings')
application = get_wsgi_application()
from question.models import Question, Faculty
from cafe_student.views import add_order
from analytic.views import analytics


async def send_message_to_all_users(message_text):
    for chat_id in cur.execute(''):
        try:
            await bot.send_message(chat_id[0], message_text)
        except Exception as e:
            logging.exception(f"Помилка при надсиланні повідомлення у чат {chat_id}: {e}")


class FSMQuestion(StatesGroup):
    text = State()  # State to store the text of the question


class Admin_answer(StatesGroup):
    text = State()  # State to store the text of the answer
    id_user = State()  # State to store the user ID


class Add_mfaq(StatesGroup):
    text = State()  # State to store the text of the new question
    answer = State()  # State to store the text of the answer to the new question
    faculty = State()


faculty_id = None


class Advertisement(StatesGroup):
    text = State()


# Обработчики
@dp.message_handler(state=Add_mfaq.answer, content_types=['text'])
async def add_most_frequently_asked_questions(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Add to FAQ with a button"""
    async with state.proxy() as data:
        data['answer'] = message.text
    await message.answer(f"Введіть факультет.\nОсь перелік доступних: {faculty_list}")
    await Add_mfaq.next()


@dp.message_handler(state=Add_mfaq.faculty)
async def add_most_frequently_asked_questions_faculty(message: aiogram.types.Message,
                                                      state: aiogram.dispatcher.FSMContext):
    """Add to FAQ with a button"""
    async with state.proxy() as data:
        data['faculty'] = message.text
    await state.finish()
    a = Question.objects.all()
    f = Faculty.objects.filter(name=data['faculty'])
    faculty = await sync_to_async(f.first)()
    try:
        faculty_id = faculty.id
        await sync_to_async(a.create)(text=data['text'], answer=data['answer'], type='Найчастіші запитання',
                                      faculty_id=faculty_id)
        await message.reply('✅ Ви успішно додали запитання!')
    except AttributeError:
        await message.reply(f"""Такого факультета немає у базі даних. Добавте його, або вкажіть інший\nОсь перелік '
                            'доступних: {faculty_list}\nПовторіть спробу добавити питання""")


@dp.message_handler(state=Advertisement.text, content_types=['photo', 'text'])
async def add_most_frequently_asked_questions(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'photo':
            data['text'] = message.caption
        else:
            data['text'] = message.text
    await state.finish()
    cur.execute(
        "SELECT chat_id FROM analytic_analytics_user")
    for chat_id in cur.fetchall():
        if message.content_type == 'photo':
            ph = message.photo[0].file_id
            await bot.send_photo(chat_id[0], ph,
                                 caption=data['text'])
        else:
            await bot.send_message(chat_id[0], data['text'])
    await message.answer('Це повідомлення відправлене усім')


@dp.message_handler(state=FSMQuestion.text, content_types=['photo', 'text'])
async def newquestion(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """Processing the question and sending it to the chat for a response"""
    global c
    async with state.proxy() as data:
        if message.text == "Назад":
            await message.answer("Окей", reply_markup=keyboard_menu)
            await state.finish()
        else:
            if message.content_type == 'photo':
                data['text'] = message.caption
            else:
                data['text'] = message.text
            await state.finish()
            if message.chat.username is None:
                who = "Ім'я користувача не встановлено"
            else:
                who = "@" + message.chat.username
            c = message.chat.id
            add_most_frequently_asked_questions_button = aiogram.types.InlineKeyboardButton(text=f" Додати у "
                                                                                                 f"найчастіші "
                                                                                                 f"запитання",
                                                                                            callback_data="add_most_frequently_asked_questions")
            button_answer = aiogram.types.InlineKeyboardButton(text=f" Відповісти для {who}", callback_data=c)
            keyboard_answer = aiogram.types.InlineKeyboardMarkup().add(button_answer).add(
                add_most_frequently_asked_questions_button)
            if message.content_type == 'photo':
                ph = message.photo[0].file_id
                await message.reply(f"{cfg['question_ur_question_sended_message']}")
                await bot.send_photo(cfg['teh_chat_id'], ph,
                                     caption=f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                                     reply_markup=keyboard_answer)
            else:
                await message.reply(f"{cfg['question_ur_question_sended_message']}", reply_markup=keyboard_menu)
                await bot.send_message(cfg['teh_chat_id'],
                                       f"✉ | Нове запитання\nВід: {who}\nПитання: {data['text']}",
                                       reply_markup=keyboard_answer)


@dp.message_handler(commands=['start'])
@analytics
async def start(message: aiogram.types.Message):
    """command start"""
    await message.answer(cfg['welcome_message'],
                         reply_markup=menu_faculty)


@dp.message_handler(commands=['getchatid'])
async def client_getgroupid(message: aiogram.types.Message):
    """receiving a chat id"""
    try:
        await message.answer(f"Chat id is: *{message.chat.id}*\nYour id is: *{message.from_user.id}*")
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")


# ban
@dp.message_handler(IsAdmin(is_admin=True), commands=['ban'], commands_prefix='/')
async def ban(message: aiogram.types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповіддю на повідомлення')
        return

    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


@dp.message_handler(IsAdmin(is_admin=True), commands=['kik'], commands_prefix='/')
async def kik(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ця команда має бути відповіддю на повідомлення')
        return

    await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply(f'Покинув нас')


@dp.message_handler(state=Admin_answer.text, content_types=['photo', 'text'])
async def admin_answer(message: aiogram.types.Message, state: aiogram.dispatcher.FSMContext):
    """The answer to the question"""
    try:
        async with state.proxy() as data:
            if message.content_type == 'photo':
                data['text'] = message.caption
            else:
                data['text'] = message.text
        await state.finish()
        await bot.send_message(data.get('id_user'),
                               f"✉ Нове повідомлення!\nВідповідь від технічної підтримки:\n\n{data['text']}")
        await message.reply('✅ Ви успішно відповіли на запитання!')
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{cfg['error_message']}")
        await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")


@dp.message_handler(content_types=['new_chat_members'])
async def on_user_joiner(message: aiogram.types.Message):
    await message.delete()


# kik


# Mute
@dp.message_handler(IsAdmin(is_admin=True), commands=['mut'], commands_prefix='/')
async def mute(message):
    name1 = message.from_user.get_mention(as_html=True)
    if not message.reply_to_message:
        await message.reply("Ця команда має бути відповіддю на повідомлення!")
        return
    try:
        muteint = int(message.text.split()[1])
        mutetype = message.text.split()[2]
        comment = " ".join(message.text.split()[3:])
    except IndexError:
        await message.reply('Бракує аргументів!\nПриклад:\n`/mut 1 д причина`')
        return
    if mutetype == "г" or mutetype == "годин" or mutetype == "година":
        dt = datetime.now() + timedelta(hours=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(False),
                                       timestamp)
    elif mutetype == "х" or mutetype == "хвилин" or mutetype == "хвилини":
        dt = datetime.now() + timedelta(minutes=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(False),
                                       timestamp)
    elif mutetype == "д" or mutetype == "днів" or mutetype == "день":
        dt = datetime.now() + timedelta(days=muteint)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False),
                                       timestamp)
    await message.reply(
        f' | <b>Рішення було прийняте:</b> {name1}\n | <b>Порушник:</b> <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>\n⏰ | <b>Термін покарання:</b> {muteint} {mutetype}\n | <b>Причина:</b> {comment}',
        parse_mode='html')


@dp.message_handler(content_types=['text'])
@analytics
async def answer_to_the_question(message: aiogram.types.Message):
    a = ['Відпочинь', 'Все буде добре']
    b = ['У тебе дуже гарна посмішка', 'Не думай про погане', 'Все буде добре']
    c = ['У тебе все вийде', 'Все буде добре']
    characters = {
        'z': 'Вийди отсюда розбійник🧏🧏🧏',
        'v': 'Пиздуйте нахуй отсюда йобаниє підараси👨‍🦲👨‍🦲👨‍🦲',
        'vz': 'Пиздець російській федерації⚰️⚰️⚰️',
        'Я втомився': a[random.randrange(0, len(a))],
        'Мені сумно': b[random.randrange(0, len(b))],
        'Я більше не можу': c[random.randrange(0, len(c))],
        'Я втомилася': a[random.randrange(0, len(a))]
    }
    for key in characters:
        if key == message.text:
            await message.reply(
                characters[key])
        elif set(key) == set(message.text.lower()):
            await message.reply(
                characters[key])
    """button processing"""
    global faculty_id
    if message.text == cfg['button_new_question']:
        try:
            button_back = aiogram.types.KeyboardButton("Назад")
            keybord_back = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_back)
            await message.answer(f"{cfg['question_type_ur_question_message']}", reply_markup=keybord_back)
            await FSMQuestion.text.set()
        except Exception as e:
            cid = message.chat.id
            await message.answer(f"{cfg['error_message']}")
            await bot.send_message(cfg['teh_chat_id'], f"Помилка виникла у чаті {cid}\nСтатус помилки: {e}")
    if message.text in dict_answer:
        await message.answer(dict_answer[message.text],
                             reply_markup=create_inline_keyboard(message.text, faculty_id))
    elif message.text == 'Змінити факультет':
        await message.answer('Ось перелік факультетів',
                             reply_markup=menu_faculty)
    elif message.text == 'Головного меню':
        await message.answer("Ось головне меню", reply_markup=keyboard_menu)
    elif message.text == 'Електроне поселення в гуртожиток':
        await message.answer('Заповніть ось цю форму...')
    elif message.text == 'Кафе':
        await message.answer('Ось що є', reply_markup=keybord_kafe())
    elif message.text == 'Зробити оголошення':
        await message.answer('Ок, напишіть у наступному повідомлені текст оголошення')
        await Advertisement.text.set()

    social_keybord = aiogram.types.InlineKeyboardMarkup()
    try:
        cur.execute(
            "SELECT id, name, instagram_link, tg_link, facebook_link, website_link FROM question_faculty")
        for row in cur:
            id, name, instagram_link, tg_link, facebook_link, website_link = row
            list_social = {'Instagram': instagram_link,
                           'Telegram': tg_link,
                           'Facebook': facebook_link,
                           'Cайт': website_link}
            for i in list_social:
                button_social = aiogram.types.InlineKeyboardButton(text=i, url=list_social[i])
                social_keybord.add(button_social)
            if message.text == name:
                faculty_id = id
                await message.answer('🤔', reply_markup=keyboard_menu)
                await message.answer(f"""{name}""", reply_markup=social_keybord)
        cur.execute("SELECT id,type FROM cafe_student_type_Product")
        t = cur.fetchone()
        if message.text in t:
            await message.answer('Ось список позицій які є',
                                 reply_markup=create_inline_keyboard_cafe(t[0]))
        con.commit()
    except pymysql.Error as e:
        print("Помилка бази даних:", e)
        con.rollback()


def extract_arg(arg):
    return arg.split()[1:]


@dp.callback_query_handler(lambda c: True)
@add_order
async def admin_ot(callback_query: aiogram.types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    """processing of inline buttons"""
    global c
    await bot.answer_callback_query(callback_query.id)
    if callback_query.message.chat.id == cfg['teh_chat_id']:
        if callback_query.data == "add_most_frequently_asked_questions":
            await callback_query.message.answer(f"Напишіть відповідь")
            message_index = callback_query.message.text.find('Питання:')
            message = callback_query.message.text[message_index + len("Питання:'"):]
            async with state.proxy() as data:
                data['text'] = message
            await Add_mfaq.answer.set()
        else:
            await callback_query.message.answer(f"Напишіть відповідь")
            async with state.proxy() as data:
                data['id_user'] = callback_query.data
            await Admin_answer.text.set()
    elif "product" in callback_query.data:
        global order
        data_parts = callback_query.data.split(":")
        product_name = data_parts[1]
        product_price = data_parts[2]
        order[product_name] = product_price
        await bot.send_message(callback_query.message.chat.id, order)
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text=f"""Додано {product_name} до кошику за {product_price} грн\nЩоб підтвердити своє замовлення нажміть 
"Підтвердити замовлення" на ..., або можете ще щось добавити у свій кошик """, reply_markup=keyboard_order)
        return order
    elif callback_query.data in dict_order:
        await bot.send_message(callback_query.from_user.id, dict_order[callback_query.data])
    else:
        for reply in cur.execute("SELECT answer FROM question_Question WHERE text = ?",
                                 (callback_query.data,)):
            await bot.send_message(callback_query.from_user.id, f"Ось що мені відомо\n"
                                                                f"{q}\n"
                                                                f"{reply[0]}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
