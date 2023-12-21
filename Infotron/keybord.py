import aiogram.types

from Infotron.Const import *

# Creating reply keyboard buttons
button_finansy = aiogram.types.KeyboardButton(text="Фінанси")
button_qat = aiogram.types.KeyboardButton(text="Питання щодо навчання")
button_admissions = aiogram.types.KeyboardButton(text='Питання щодо вступу')
button_mfaq = aiogram.types.KeyboardButton(text='Найчастіші запитання')
button_settlement = aiogram.types.KeyboardButton(text='Електроне поселення в гуртожиток')
button_support = aiogram.types.KeyboardButton(cfg['button_new_question'])
button_back = aiogram.types.KeyboardButton("Змінити факультет")
# Creating a reply keyboard markup and adding buttons to it
keyboard_menu = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_menu.add(button_mfaq).row(button_qat).add(button_finansy, button_admissions).add(button_support, button_back)
# Creating a reply keyboard markup for faculty selection
menu_faculty = aiogram.types.ReplyKeyboardMarkup()
# Adding buttons for each faculty from the database
cafe = aiogram.types.KeyboardButton(text='Кафе')
# Отримати список імен з таблиці question_answer_faculty
cur.execute("SELECT name FROM question_faculty")
menu_faculty = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
for name in cur.fetchall():
    button = aiogram.types.KeyboardButton(text=str(name[0]))
    menu_faculty.add(cafe).add(button)


# Оновлення функції create_inline_keyboard
def create_inline_keyboard(text, f_id):
    """Створення внутрішнього клавішного макету для вибору запитань"""

    menu_question = aiogram.types.InlineKeyboardMarkup()
    # Додавання кнопок для кожного запитання з вказаним типом і факультетом з бази даних
    cur.execute("SELECT text FROM question_question WHERE type = %s and faculty_id = %s", (text, f_id))
    for reply in cur.fetchall():
        button = aiogram.types.InlineKeyboardButton(text=reply[0], callback_data=reply[0])
        menu_question.add(button)
    return menu_question


def keybord_kafe():
    menu_cafe = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = aiogram.types.KeyboardButton("Головного меню")
    cur.execute("SELECT type FROM cafe_student_type_product")
    for type in cur.fetchall():
        button = aiogram.types.KeyboardButton(text=str(type[0]))
        menu_cafe.add(button).add(main_menu)
    return menu_cafe


# Оновлення функції create_inline_keyboard_answer
def create_inline_keyboard_answer(text, f_id):
    """Створення внутрішнього клавішного макету для вибору запитань"""

    keyboard = aiogram.types.InlineKeyboardMarkup()
    # Додавання кнопок для кожного запитання з вказаним типом і факультетом з бази даних
    cur.execute("SELECT text FROM question_question WHERE type = %s and faculty_id = %s", (text, f_id))
    for reply in cur.fetchall():
        button = aiogram.types.InlineKeyboardButton(text=reply[0], callback_data=reply[0])
        keyboard.add(button)
    return keyboard


# Оновлення функції create_inline_keyboard_cafe
def create_inline_keyboard_cafe(text):
    """Створення внутрішнього клавішного макету для вибору запитань"""

    keyboard = aiogram.types.InlineKeyboardMarkup()
    cur.execute("SELECT name, cost FROM cafe_student_product WHERE type_product_id = %s", (text,))
    for name, cost in cur.fetchall():
        button = aiogram.types.InlineKeyboardButton(text=f'{name} = {cost}грн.',
                                                    callback_data=f"product:{name}:{cost}")
        keyboard.add(button)
    return keyboard


keyboard_order = aiogram.types.InlineKeyboardMarkup()
basket = aiogram.types.InlineKeyboardButton(text='Мій кошик', callback_data='my_basket')
confirm_order = aiogram.types.InlineKeyboardButton(text='Підтвердити замовлення', callback_data='confirm_order')
keyboard_order.add(basket, confirm_order)
