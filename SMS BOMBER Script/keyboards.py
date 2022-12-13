from winreg import KEY_QUERY_VALUE
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from db import get_bomber_history, get_rang


def start_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    kb1 = KeyboardButton("🔥 Начать")
    kb2 = KeyboardButton("👤 Мой аккаунт")
    kb3 = KeyboardButton("❓ FAQ / Помощь")
    kb4 = KeyboardButton("✨ Статистика")
    kb5 = KeyboardButton("💬 О сервисе")
    keyboard.add(kb1).add(kb2, kb4).add(kb3, kb5)
    return keyboard


def back_admin_menu():
    keyboard = InlineKeyboardMarkup()
    kb = InlineKeyboardButton(text="Назад", callback_data="back_adm_menu")
    keyboard.add(kb)
    return keyboard


def admin_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(text="Выдать баланс", callback_data="set_balance")
    kb1 = InlineKeyboardButton(text="Рассылка", callback_data="mailing")
    kb2 = InlineKeyboardButton(text="Забанить", callback_data="ban_user")
    kb3 = InlineKeyboardButton(text="Разбанить", callback_data="unban_user")
    kb4 = InlineKeyboardButton(text="Активные подписки", callback_data="watch_subs")
    kb5 = InlineKeyboardButton(text="Посмотреть профиль", callback_data="watch_profile")
    kb6 = InlineKeyboardButton(
        text="Генератор промокодов", callback_data="promo_generator"
    )
    kb7 = InlineKeyboardButton(text="Обнулить слоты", callback_data="reset_slots")
    keyboard.add(kb, kb1).add(kb2, kb3).add(kb4, kb5).add(kb6, kb7)
    return keyboard


def flood_type():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(text="🤬 Обычный флуд", callback_data="default_flood")
    kb1 = InlineKeyboardButton(
        text="☠️ Бесконечный флуд", callback_data="infinity_flood"
    )
    kb2 = InlineKeyboardButton(text="📝 История", callback_data="history_flood")
    kb3 = InlineKeyboardButton(text="🤍 Белый список", callback_data="whitelist_check")
    kb4 = InlineKeyboardButton(text="❌ Закрыть", callback_data="close_message")
    keyboard.add(kb, kb1).add(kb2, kb3).add(kb4)
    return keyboard


def profile_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="balance_up")
    kb1 = InlineKeyboardButton(text="💵 Подписка", callback_data="sub")
    kb2 = InlineKeyboardButton(text="⚜️ Ранги", callback_data="rangs")
    kb3 = InlineKeyboardButton(text="🎟 Активировать ключ", callback_data="activate_key")
    kb4 = InlineKeyboardButton(
        text="🤝 Партнерская программа", callback_data="partner programm"
    )
    keyboard.add(kb).add(kb1, kb2).add(kb3).add(kb4)
    return keyboard


def buy_sub_confirm(duration, cost):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="☑️ Подтверждаю", callback_data=f"buy_sub_confirm|{duration}|{cost}"
    )
    kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1)
    return keyboard


def buy_sub_kb():
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="🍀 1 час - 9.90 рублей 🍀", callback_data="buy_sub|hour|9.90"
    )
    kb1 = InlineKeyboardButton(
        text="💚 24 часа - 29.90 рублей 💚", callback_data="buy_sub|day|29.90"
    )
    kb2 = InlineKeyboardButton(
        text="💛 7 дней - 69.90 рублей 💛", callback_data="buy_sub|week|69.90"
    )
    kb3 = InlineKeyboardButton(
        text="🔥 30 дней - 169.90 рублей 🔥", callback_data="buy_sub|month|169.90"
    )
    kb4 = InlineKeyboardButton(
        text="🧡 90 дней - 299.90 рублей 🧡",
        callback_data="buy_sub|one_and_half_month|299.90",
    )
    kb5 = InlineKeyboardButton(
        text="🧡 180 дней - 499.90 рублей 🧡", callback_data="buy_sub|half_year|499.90"
    )
    kb6 = InlineKeyboardButton(
        text="💜 365 дней - 999.90 рублей 💜", callback_data="buy_sub|year|999.90"
    )
    kb7 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1, kb2, kb3, kb4, kb5, kb6, kb7)
    return keyboard


def rangs_choose_kb(rang, current_rang):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if rang != current_rang and rang != "🥉 Bronze":
        rang_info = get_rang(rang)
        kb4 = InlineKeyboardButton(
            text=f"💲 Купить этот ранг - {rang_info[4]} ₽ 💲",
            callback_data=f"rang_buy|{rang}",
        )
        keyboard.add(kb4)
    kb = InlineKeyboardButton(text="🥉 Bronze", callback_data="rang_choose|🥉 Bronze")
    kb1 = InlineKeyboardButton(text="🥈 Silver", callback_data="rang_choose|🥈 Silver")
    kb2 = InlineKeyboardButton(text="🥇 Gold", callback_data="rang_choose|🥇 Gold")
    kb3 = InlineKeyboardButton(text="💎 Diamond", callback_data="rang_choose|💎 Diamond")
    kb5 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1, kb2, kb3).add(kb5)
    return keyboard


def balance_up_kb():
    keyboard = InlineKeyboardMarkup(row_width=4)
    kb = InlineKeyboardButton(text="10 ₽", callback_data="balance_up_amount|10")
    kb1 = InlineKeyboardButton(text="30 ₽", callback_data="balance_up_amount|30")
    kb2 = InlineKeyboardButton(text="50 ₽", callback_data="balance_up_amount|50")
    kb3 = InlineKeyboardButton(text="60 ₽", callback_data="balance_up_amount|60")
    kb4 = InlineKeyboardButton(text="100 ₽", callback_data="balance_up_amount|100")
    kb5 = InlineKeyboardButton(text="150 ₽", callback_data="balance_up_amount|150")
    kb6 = InlineKeyboardButton(text="200 ₽", callback_data="balance_up_amount|200")
    kb7 = InlineKeyboardButton(text="300 ₽", callback_data="balance_up_amount|300")
    kb8 = InlineKeyboardButton(text="500 ₽", callback_data="balance_up_amount|500")
    kb9 = InlineKeyboardButton(text="700 ₽", callback_data="balance_up_amount|700")
    kb10 = InlineKeyboardButton(text="1000 ₽", callback_data="balance_up_amount|1000")
    kb11 = InlineKeyboardButton(text="2000 ₽", callback_data="balance_up_amount|2000")
    kb12 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10, kb11).add(kb12)
    return keyboard


def payment_system_choose(summ):
    keyboard = InlineKeyboardMarkup(row_width=3)
    kb = InlineKeyboardButton(
        text="🥝 Qiwi/Банковская карта", callback_data=f"balance_up_system|qiwi|{summ}"
    )
    kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb).add(kb1)
    return keyboard


def create_bill(bill_id, url, amount):
    bill_kb = InlineKeyboardMarkup(row_width=2)
    bill1 = InlineKeyboardButton(text="💳 Перейти к оплате", url=url)
    bill2 = InlineKeyboardButton(
        text="☑️ Проверить оплату",
        callback_data=f"check_bill_status|{bill_id}|{amount}",
    )
    bill3 = InlineKeyboardButton(
        text="🚫 Отменить платеж", callback_data=f"pay_cancel|{bill_id}"
    )
    bill_kb.add(bill1, bill2, bill3)
    return bill_kb


def ref_programm_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(
        text="💰 Запросить вывод", callback_data="withdraw_request"
    )
    kb1 = InlineKeyboardButton(
        text="🔗 Сократить ссылку (clck.ru)", callback_data="link_shorter"
    )
    kb2 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1).add(kb2)
    return keyboard


def withdraw_request_kb(requisites):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="Подтвердить", callback_data=f"withdraw_request_user|{requisites}"
    )
    kb1 = InlineKeyboardButton(text="Отмена", callback_data="back")
    keyboard.add(kb, kb1)
    return keyboard


def withdraw_request_confirm_kb(userid):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="Оплачено", callback_data=f"withdraw_request_admin|{userid}"
    )
    kb1 = InlineKeyboardButton(
        text="Отклонить", callback_data=f"withdraw_request_cancel|{userid}"
    )
    keyboard.add(kb, kb1)
    return keyboard


def whitelist_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(
        text="➕ Добавить номер", callback_data="whitelist_number_add"
    )
    kb1 = InlineKeyboardButton(
        text="❔ Проверить номер", callback_data="check_number_whitelist"
    )
    kb2 = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb, kb1).add(kb2)
    return keyboard


def flood_type_kb(_type):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(text="📨 SMS", callback_data=f"sms_bomber|{_type}")
    kb1 = InlineKeyboardButton(
        text="📞 Авто-звонки", callback_data=f"auto_calls_bomber|{_type}"
    )
    kb2 = InlineKeyboardButton(
        text="☎️ Обратные звонки", callback_data=f"reverse_calls_bomber|{_type}"
    )
    kb3 = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb, kb1, kb2, kb3)
    return keyboard


def flood_mode_kb(_type, bomber):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="🍀 Классический", callback_data=f"bomber_mode|classic|{_type}|{bomber}"
    )
    kb1 = InlineKeyboardButton(
        text="🚧 Мощный", callback_data=f"bomber_mode|powerful|{_type}|{bomber}"
    )
    kb2 = InlineKeyboardButton(
        text="🔥 Легендарный", callback_data=f"bomber_mode|legendary|{_type}|{bomber}"
    )
    kb3 = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb, kb1, kb2, kb3)
    return keyboard


def confirm_rang_buy(rang, cost):
    keyboard = InlineKeyboardMarkup(row_width=1)
    kb = InlineKeyboardButton(
        text="☑️ Подтверждаю", callback_data=f"buy_rang_confirm|{rang}|{cost}"
    )
    kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb, kb1)
    return keyboard


def task_kb(task_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(text="❌ Остановить", callback_data=f"task_stop|{task_id}")
    kb1 = InlineKeyboardButton(
        text="🔄 Обновить", callback_data=f"refresh_task|{task_id}"
    )
    kb2 = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb, kb1).add(kb2)
    return keyboard


def history_kb(userid):
    emojis = {
        "🤬 Обычный флуд": "🤬",
        "☠️ Бесконечный флуд": "☠️",
        "В процессе": "⌛️",
        "📨 SMS": "📨",
        "☎️ Обратные звонки": "☎️",
        "📞 Авто-Звонки": "📞",
        "Завершено": "☑️",
        "Достигнуто максимальное время работы": " ☑️",
    }
    history = get_bomber_history(userid)
    keyboard = InlineKeyboardMarkup(row_width=2)
    for task in history:
        kb = KeyboardButton(
            text=f"{emojis[task[6]]} #{task[8]} {emojis[task[2]]} +{task[1]} {emojis[task[4]]}",
            callback_data=f"refresh_task|{task[8]}",
        )
        keyboard.add(kb)
    kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb)
    return keyboard


def promo_generate_choose_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    kb = InlineKeyboardButton(text="🍀 1 час 🍀", callback_data="generate|sub|hour")
    kb1 = InlineKeyboardButton(text="💚 24 часа 💚", callback_data="generate|sub|day")
    kb2 = InlineKeyboardButton(text="💛 7 дней 💛", callback_data="generate|sub|week")
    kb3 = InlineKeyboardButton(text="🔥 30 дней 🔥", callback_data="generate|sub|month")
    kb4 = InlineKeyboardButton(
        text="🧡 90 дней 🧡",
        callback_data="generate|sub|one_and_half_month",
    )
    kb5 = InlineKeyboardButton(
        text="🧡 180 дней 🧡", callback_data="generate|sub|half_year"
    )
    kb6 = InlineKeyboardButton(text="💜 365 дней 💜", callback_data="generate|sub|year")
    kb7 = InlineKeyboardButton(text="↪️ Назад", callback_data="back_adm_menu")
    kb8 = InlineKeyboardButton(text="🥉 Bronze", callback_data="generate|rang|🥉 Bronze")
    kb9 = InlineKeyboardButton(text="🥈 Silver", callback_data="generate|rang|🥈 Silver")
    kb10 = InlineKeyboardButton(text="🥇 Gold", callback_data="generate|rang|🥇 Gold")
    kb11 = InlineKeyboardButton(
        text="💎 Diamond", callback_data="generate|rang|💎 Diamond"
    )
    keyboard.add(kb, kb1, kb2, kb3, kb4, kb5, kb6, kb8, kb9, kb10, kb11).add(kb7)
    return keyboard
