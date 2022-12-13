import phonenumbers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import string
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
from pyqiwip2p import QiwiP2P
import traceback
from os import getenv
import requests
import threading
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
import asyncio, json, os, random, datetime
from pyqiwip2p import QiwiP2P
import pytz
from keyboards import *
from bomber import bomber_active, call_bomber, sms_bomber

from db import *
from cfg import *
from states import *


p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        try:
            if message.from_user.id == admin_id:
                return True
            else:
                return False
        except:
            return False


class IsBanned(BoundFilter):
    async def check(self, message: types.Message):
        try:
            state = get_bans(message.from_user.id)
            if state == None:
                return True
            else:
                return False
        except:
            return False


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def send_profile(userid, _type, _message_id):
    user = get_profile(userid)
    ##registration
    now = datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H")
    diff = datetime.datetime.strptime(
        now, "%d.%m.%Y %S:%M:%H"
    ) - datetime.datetime.strptime(user[4], "%d.%m.%Y %S:%M:%H")
    ##registration
    sub = user[3]
    if sub != "Отсутствует":
        if (
            datetime.datetime.strptime(sub, "%d.%m.%Y %S:%M:%H")
            < datetime.datetime.now()
        ):
            set_default_sub(userid)
            user = get_profile(userid)
            sub = user[3]
        sub_diff = (
            datetime.datetime.strptime(sub, "%d.%m.%Y %S:%M:%H")
            - datetime.datetime.now()
        )

        if sub_diff.days > 0:
            sub = f"{sub_diff.days} дней до окончания подписки"
        elif sub_diff.days == 0:
            sub = f"{int(sub_diff.seconds / 3600)} часов до окончания подписки"
    rang = get_rang(user[5])
    if _type == "message":
        await bot.send_message(
            userid,
            f"<b>👤 Мой аккаунт</b>\n<i>Основная информация </i>\n\n💬 ID: <code>{userid}</code>\n💬 Регистрация: <code>{diff.days} дней назад</code>\n\n🥀 Подписка: <code>{sub}</code>\n💰 Внутренний баланс: <code>{float(user[2])} ₽</code>\n\n⚜️ Твой ранг: <code>{user[5]}</code>\n📞 Слотов занято: <code>{user[6]} из {rang[1]}</code>\n⚙️ Лимит задач в сутки: <code>{user[7]} из {rang[2]}</code>\n🤍 Белый список: <code>{user[8]} из {rang[3]}</code>",
            reply_markup=profile_kb(),
            parse_mode="HTML",
        )
    elif _type == "callback":
        await bot.edit_message_text(
            f"<b>👤 Мой аккаунт</b>\n<i>Основная информация</i>\n\n💬 ID: <code>{userid}</code>\n💬 Регистрация: <code>{diff.days} дней назад</code>\n\n🥀 Подписка: <code>{sub}</code>\n💰 Внутренний баланс: <code>{float(user[2])} ₽</code>\n\n⚜️ Твой ранг: <code>{user[5]}</code>\n📞 Слотов занято: <code>{user[6]} из {rang[1]}</code>\n⚙️ Лимит задач в сутки: <code>{user[7]} из {rang[2]}</code>\n🤍 Белый список: <code>{user[8]} из {rang[3]}</code>",
            chat_id=userid,
            message_id=_message_id,
            reply_markup=profile_kb(),
            parse_mode="HTML",
        )


@dp.message_handler(IsAdmin(), commands=["admin"])
async def admin(message: types.Message):
    await message.answer(
        "<b>admin panel</b>", parse_mode="HTML", reply_markup=admin_kb()
    )


@dp.message_handler(IsBanned(), commands=["start"])
async def start(message: types.Message):
    is_reg = False
    try:
        user = get_profile(message.from_user.id)
        is_reg = True
    except:
        pass
    db_insert(
        message.from_user.id,
        message.from_user.username,
        datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H"),
    )
    if message.text == "/start":
        pass
    else:
        if is_reg == False and str(message.from_user.id) != message.text.split("=")[1]:
            set_referal(message.text.split("=")[1])
        else:
            pass

    await message.answer_sticker(
        r"CAACAgIAAxkBAAEFT71i1jfbiA51Mxtmxb9iUjTY5R4PuAACWzoAAuCjggfPhzDKe5UdFykE"
    )
    await message.answer(start_text, parse_mode="HTML", reply_markup=start_kb())


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_promo_amount)
async def promo_create(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if message.text.isdigit() == False:
        await bot.edit_message_text(
            "Количество промокодов должно быть числом, попробуйте еще раз",
            message.from_user.id,
            data["message_id"],
            reply_markup=back_admin_menu(),
        )
        return FMSAdmin.get_promo_amount.set()
    all_promos = ""
    if data["item"].split("|")[0] == "sub":
        if data["item"].split("|")[1] == "hour":
            sub_text = "1 hour"
        else:
            subs = {
                "day": "1 day",
                "week": "7 day",
                "month": "30 day",
                "one_and_half_month": "90 day",
                "half_year": "180 day",
                "year": "365 day",
            }
            sub_text = subs[data["item"].split("|")[1]]
        for i in range(int(message.text)):
            characters = list(string.ascii_letters + string.digits)
            random.shuffle(characters)
            promo = []
            for i in range(6):
                promo.append(random.choice(characters))
            promo = "".join(promo)
            add_promo(promo, "подписка", sub_text)
            all_promos += f"<code>{promo}</code>\n"
        await bot.edit_message_text(
            f"Вы успешно создали {message.text} промокодов, список:\n{all_promos}",
            message.from_user.id,
            data["message_id"],
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )
    else:
        for i in range(int(message.text)):
            characters = list(string.ascii_letters + string.digits)
            random.shuffle(characters)
            promo = []
            for i in range(6):
                promo.append(random.choice(characters))
            promo = "".join(promo)
            add_promo(promo, f'ранг|{data["item"].split("|")[1]}', "None")
            all_promos += f"<code>{promo}</code>\n"
        await bot.edit_message_text(
            f"Вы успешно создали {message.text} промокодов, список:\n{all_promos}",
            message.from_user.id,
            data["message_id"],
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )

    await state.finish()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_mailing_text)
async def mailing_start(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(
        "<b>📢 Рассылка началась...</b>",
        message.from_user.id,
        data["message_id"],
        parse_mode="HTML",
        reply_markup=back_admin_menu(),
    )
    await state.finish()
    asyncio.create_task(send_message_to_user(message.html_text, message.from_user.id))


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_userid_unban)
async def unban_user(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    try:
        unban(message.text)
        await bot.send_message(message.text, "Администратор разблокировал вас")
    except:
        pass
    await bot.edit_message_text(
        f"Вы разбанили пользователя <code>{message.text}</code>",
        message.from_user.id,
        data["message_id"],
        parse_mode="HTML",
        reply_markup=back_admin_menu(),
    )
    await state.finish()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_reason_ban)
async def ban_reason(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    ban(
        data["userid"],
        message.text,
        datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H"),
    )
    await bot.edit_message_text(
        f'Вы заблокировали пользователя <code>{data["userid"]}</code> по причине: <code>{message.text}</code>',
        message.from_user.id,
        data["message_id"],
        reply_markup=back_admin_menu(),
        parse_mode="HTML",
    )
    try:
        await bot.send_message(
            data["userid"],
            f"Администратор заблокировал вас по причине: {message.text}",
        )
    except:
        pass
    await state.finish()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_userid_ban)
async def ban_userid(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        data["userid"] = message.text
    await bot.edit_message_text(
        "Введите причину блокировки",
        message.from_user.id,
        data["message_id"],
        reply_markup=back_admin_menu(),
    )
    await FMSAdmin.get_reason_ban.set()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_userid_watch_profile)
async def watch_profile(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    try:
        await send_profile(message.from_user.id, "message", data["message_id"])
    except:
        await bot.edit_message_text(
            "<b>Ошибка, данный пользователь не найден</b>",
            message.from_user.id,
            data["message_id"],
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )
    await state.finish()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_amount_set_balance)
async def set_balance_amount(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    if message.text.isdigit() == False and message.text[0] != "-":
        await bot.edit_message_text(
            "Сумма должна быть числом, повторите попытку",
            message.from_user.id,
            data["message_id"],
            reply_markup=back_admin_menu(),
        )
        return FMSAdmin.get_amount_set_balance.set()
    try:
        buy_set_balance(data["userid"], float(message.text))
    except:
        pass
    await bot.edit_message_text(
        f"Вы успешно выдали пользователю <code>{data['userid']}</code> на баланс <code>{float(message.text)} ₽</code>",
        message.from_user.id,
        data["message_id"],
        reply_markup=back_admin_menu(),
        parse_mode="HTML",
    )
    await state.finish()


@dp.message_handler(IsAdmin(), state=FMSAdmin.get_userid_set_balance)
async def set_balance_id(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    async with state.proxy() as data:
        data["userid"] = message.text
    await bot.edit_message_text(
        "Введите баланс, который хотите установить пользователю",
        message.from_user.id,
        data["message_id"],
        reply_markup=back_admin_menu(),
        parse_mode="HTML",
    )
    await FMSAdmin.get_amount_set_balance.set()


@dp.message_handler(state=FSMMain.get_check_number)
async def check_number(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup()
    kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb)
    try:
        phone_num = message.text
        if phone_num[1] != "+" and phone_num[1].isdigit() == True:
            phone_num = f"+{message.text}"
        my_number = phonenumbers.parse(phone_num)
        number = check_phone(f"{my_number.country_code}{my_number.national_number}")
        if number == []:
            await bot.edit_message_text(
                f"""<b>❔ Проверить номер</b>
<i>Результат проверки</i>

<code>📞 +{my_number.country_code}{my_number.national_number}</code>
Флуд ни разу не запускали через нашего бота
    """,
                message.from_user.id,
                data["message_id"],
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await bot.edit_message_text(
                f"""<b>❔ Проверить номер</b>
<i>Результат проверки</i>

<code>📞 +{my_number.country_code}{my_number.national_number}</code>
Флуд запускали несколько раз
    """,
                message.from_user.id,
                data["message_id"],
                parse_mode="HTML",
                reply_markup=keyboard,
            )
    except:
        await bot.edit_message_text(
            """<b>⚠️ Ошибка</b>
<i>Кажется, ты неверно ввёл номер телефона</i>""",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    await state.finish()


@dp.message_handler(state=FSMMain.get_phone_bomber)
async def bomber_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup(row_width=1)
    try:
        phone_num = message.text
        if phone_num[1] != "+" and phone_num[1].isdigit() == True:
            phone_num = f"+{message.text}"
        my_number = phonenumbers.parse(phone_num)
        number = get_whitelist(f"{my_number.country_code}{my_number.national_number}")
        if number != None:
            if int(number[0]) != message.from_user.id:
                kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
                keyboard.add(kb)
                await bot.edit_message_text(
                    "<i>Номер телефона находится в белом списке, это значит что на него нельзя запустить флуд с нашего бомбера.</i>",
                    message.from_user.id,
                    data["message_id"],
                    parse_mode="HTML",
                    reply_markup=keyboard,
                )
                await state.finish()
                return
        characters = list(string.ascii_letters + string.digits)
        random.shuffle(characters)
        task_id = []
        for i in range(6):
            task_id.append(random.choice(characters))
        task_id = "".join(task_id)
        kb = InlineKeyboardButton(
            text="Запустить сейчас",
            callback_data=f"bomber_start|{task_id}",
        )
        kb1 = InlineKeyboardButton(
            text="↪️ Отмена", callback_data=f"bomber_cancel|{task_id}"
        )
        bomber_start_insert(
            message.from_user.id,
            data["tag"],
            data["bomber_type"],
            data["bomber_mode"],
            f"{my_number.country_code}{my_number.national_number}",
            data["work_time"],
            task_id,
        )
        keyboard.add(kb, kb1)
        work_time_text = f"{data['work_time']} минут"
        await bot.edit_message_text(
            f"<b>{data['tag']}</b>\n├ Тип:  <code>{data['bomber_type']}</code>\n├ Режим работы:  <code>{data['bomber_mode']}</code>\n├ Номер:  <code>{my_number.country_code}{my_number.national_number}</code>\n│\n└ Макс. время работы:  <code>{work_time_text if data['tag'] == '🤬 Обычный флуд' else 'Без ограничений'}</code>\n\n<i>❔ Введи номер телефона (в любом формате)</i>",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    except:
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard.add(kb)
        await bot.edit_message_text(
            """<b>⚠️ Ошибка</b>
<i>Кажется, ты неверно ввёл номер телефона. Попробуй еще раз</i>""",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )


@dp.message_handler(state=FSMMain.get_requisites)
async def withdraw_request(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    await bot.edit_message_text(
        f"<b>🤝 Партнёрская программа</b>\n<i>Подтверждение</i>\n\nВаш ID: <code>{message.from_user.id}</code>\nСумма вывода: <code>100.00 ₽</code>\nРеквизиты: <code>{message.text}</code>\nДата и время: <code>{datetime.datetime.today().strftime('%d.%m.%Y %H:%M:%S')}</code>",
        message.from_user.id,
        data["message_id"],
        parse_mode="HTML",
        reply_markup=withdraw_request_kb(100),
    )
    await state.finish()


@dp.message_handler(state=FSMMain.get_whitelist_number)
async def whitelist_add(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    keyboard = InlineKeyboardMarkup()
    kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
    keyboard.add(kb)
    try:
        phone_num = message.text
        if phone_num[1] != "+" and phone_num[1].isdigit() == True:
            phone_num = f"+{message.text}"
        my_number = phonenumbers.parse(phone_num)
        number = get_whitelist(f"{my_number.country_code}{my_number.national_number}")
        if number == None:
            await bot.edit_message_text(
                f"""<b>➕ Добавить номер</b>
    <i>Номер телефона успешно добавлен в белый список</i>
    <code>📞 +{my_number.country_code}{my_number.national_number}</code>
    """,
                message.from_user.id,
                data["message_id"],
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            whitelist_add_db(
                message.from_user.id,
                f"{my_number.country_code}{my_number.national_number}",
            )
        else:
            await bot.edit_message_text(
                f"""<b>➕ Добавить номер</b>
    <i>Номер телефона уже находится в белом списке</i>
    <code>📞 +{my_number.country_code}{my_number.national_number}</code>
    """,
                message.from_user.id,
                data["message_id"],
                parse_mode="HTML",
                reply_markup=keyboard,
            )
    except:
        await bot.edit_message_text(
            """<b>⚠️ Ошибка</b>
<i>Кажется, ты неверно ввёл номер телефона</i>""",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    await state.finish()


@dp.message_handler(state=FSMMain.get_promo)
async def promo_activate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, message.message_id)
    keyboard = InlineKeyboardMarkup()
    kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
    keyboard.add(kb)
    try:
        promo = get_promo(message.text)
        if promo[1].startswith("подписка"):
            if promo[2].split()[1] == "day":
                sub = datetime.datetime.now() + datetime.timedelta(
                    days=int(promo[2].split()[0])
                )
                set_sub(
                    message.from_user.id,
                    sub.strftime("%d.%m.%Y %S:%M:%H"),
                )
                promo_text = f"подписка на {promo[2].split()[0]} дней"
            elif promo[2].split()[1] == "hour":
                sub = datetime.datetime.now() + datetime.timedelta(
                    hours=int(promo[2].split()[0])
                )
                set_sub(
                    message.from_user.id,
                    sub.strftime("%d.%m.%Y %S:%M:%H"),
                )
                promo_text = f"подписка на {promo[2].split()[0]} часов"
        elif promo[1].startswith("ранг"):
            rang = promo[1].split("|")[1]
            set_rang(message.from_user.id, rang)
            promo_text = f"ранг {rang}"
        await bot.edit_message_text(
            f"<b>🎟 Активировать ключ</b>\n<i>Вы активировали промокод: <code>{message.text}</code>.\nЗа этот промокод вы получили: <code>{promo_text}</code></i>",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )

    except:
        await bot.edit_message_text(
            "⚠️ Ошибка, такого ключа нет, либо он уже был активирован ранее",
            message.from_user.id,
            data["message_id"],
            reply_markup=keyboard,
        )
    await state.finish()


@dp.message_handler(state=FSMMain.get_balance_up_amount)
async def get_balance_up_amount(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    data = await state.get_data()
    if message.text.isdigit() == False:
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        await bot.edit_message_text(
            "<b>💰 Пополнить баланс</b>\n<i>Кажется, ты неверно указал сумму пополнения, попробуй ещё раз</i>",
            message.from_user.id,
            data["message_id"],
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        return await FSMMain.get_balance_up_amount.set()
    await bot.edit_message_text(
        f"<b>💰 Пополнить баланс</b>\nСумма:  <code>{message.text}.00 ₽</code>\n\n<i>❔ Выбери способ оплаты</i>",
        message.from_user.id,
        data["message_id"],
        parse_mode="HTML",
        reply_markup=payment_system_choose(message.text),
    )
    await state.finish()


@dp.message_handler(
    IsBanned(),
    text=["👤 Мой аккаунт", "✨ Статистика", "💬 О сервисе", "🔥 Начать"],
)
async def main_handler(message: types.Message):
    if message.text == "🔥 Начать":
        await message.answer(
            """<b>🔥 Начать</b>
<i>Выбери один из вариантов

❔ Больше информации о разнице между обычным и бесконечным флудом есть в разделе «FAQ/Помощь»</i>""",
            parse_mode="HTML",
            reply_markup=flood_type(),
        )
    elif message.text == "👤 Мой аккаунт":
        await send_profile(message.from_user.id, "message", message.message_id)
    elif message.text == "✨ Статистика":
        stats = get_bot_stats()
        all_users = get_all_users()
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        diff = datetime.datetime.strptime(now, "%d.%m.%Y") - datetime.datetime.strptime(
            stats[0], "%d.%m.%Y"
        )
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="❌ Закрыть", callback_data="close_message")
        keyboard.add(kb)
        await message.answer(
            f"<b>✨ Статистика</b>\n<i>От {stats[0]} ({diff.days} дней)</i>\n\n👤 Пользователей: <code>{len(all_users)}</code>\n📵 Номеров уничтожено: <code>{stats[4]}</code>\n📨 Отправлено сообщений:  <code>{stats[5]}</code>\n📞 Сделано звонков: <code>{stats[6]}</code>",
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif message.text == "💬 О сервисе":
        stats = get_bot_stats()
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        diff = datetime.datetime.strptime(now, "%d.%m.%Y") - datetime.datetime.strptime(
            stats[0], "%d.%m.%Y"
        )
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="❌ Закрыть", callback_data="close_message")
        keyboard.add(kb)
        await message.answer(
            f"""<b>💬 О сервисе</b>
<i>Основная информация и ссылки</i>

💬 По всем вопросам/сотрудничество: {admin_username}
💬 Дата запуска:  <code>{stats[0]} ({diff.days} дней)</code>

💬 Сервисов (всего):  <code>{stats[1] + stats[2] + stats[3]} сервисов</code>
├ SMS:  <code>{stats[1]} сервисов</code>
├ Авто-Звонки:  <code>{stats[2]} сервисов</code>
└ Обратные звонки:  <code>{stats[3]} сервисов</code>""",
            parse_mode="HTML",
            reply_markup=keyboard,
        )


@dp.callback_query_handler(IsBanned(), state="*")
async def callback_main(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "default_flood":
        user = get_profile(callback.from_user.id)
        now = datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H")
        if user[3] == "Отсутствует":
            await callback.answer(
                "⚠️ Для продолжения необходимо купить подписку", show_alert=True
            )
            await bot.answer_callback_query(callback.id)
            return
        elif datetime.datetime.strptime(
            user[3], "%d.%m.%Y %S:%M:%H"
        ) < datetime.datetime.strptime(now, "%d.%m.%Y %S:%M:%H"):
            set_default_sub(callback.from_user.id)
            await callback.answer(
                "⚠️ Для продолжения необходимо купить подписку", show_alert=True
            )
            await bot.answer_callback_query(callback.id)
            return
        else:
            await bot.edit_message_text(
                """<b>🤬 Обычный флуд</b>
<i>Выбери тип флуда

❔ Больше информации в разделе «FAQ/Помощь»</i>""",
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=flood_type_kb("default"),
                parse_mode="HTML",
            )
    elif callback.data.startswith("sms_bomber"):
        if callback.data.split("|")[1] == "default":
            tag = "🤬 Обычный флуд"
        elif callback.data.split("|")[1] == "infinity":
            tag = "☠️ Бесконечный флуд"
        await bot.edit_message_text(
            f"""<b>{tag}</b>\n└ Тип:  <code>📨 SMS</code>\n\n<i>❔ Выбери режим работы (влияет на кол-во потоков)</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=flood_mode_kb(callback.data.split("|")[1], "sms"),
        )
    elif callback.data.startswith("bomber_mode"):
        modes = {
            "classic": "🍀 Классический",
            "powerful": "🚧 Мощный",
            "legendary": "🔥 Легендарный",
        }
        bombers = {
            "sms": "📨 SMS",
            "auto_calls": "📞 Авто-Звонки",
            "reverse_calls": "☎️ Обратные звонки",
        }
        if callback.data.split("|")[2] == "default":
            tag = "🤬 Обычный флуд"
        elif callback.data.split("|")[2] == "infinity":
            tag = "☠️ Бесконечный флуд"
        work_time = {"classic": 30, "powerful": 25, "legendary": 20}
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard.add(kb)
        work_time_text = f"{work_time[callback.data.split('|')[1]]} минут"
        await bot.edit_message_text(
            f"<b>{tag}</b>\n├ Тип:  <code>{bombers[callback.data.split('|')[3]]}</code>\n├ Режим работы:  <code>{modes[callback.data.split('|')[1]]}</code>\n│\n└ Макс. время работы:  <code>{work_time_text if tag == '🤬 Обычный флуд' else 'Без ограничений'}</code>\n\n<i>❔ Введи номер телефона (в любом формате)</i>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await FSMMain.get_phone_bomber.set()
        async with state.proxy() as data:
            data["tag"] = tag
            data["bomber_type"] = bombers[callback.data.split("|")[3]]
            data["bomber_mode"] = modes[callback.data.split("|")[1]]
            data["work_time"] = work_time[callback.data.split("|")[1]]
            data["message_id"] = callback.message.message_id
    elif callback.data.startswith("auto_calls_bomber"):
        if callback.data.split("|")[1] == "default":
            tag = "🤬 Обычный флуд"
        elif callback.data.split("|")[1] == "infinity":
            tag = "☠️ Бесконечный флуд"
        await bot.edit_message_text(
            f"""<b>{tag}</b>\n└ Тип:  <code>📞 Авто-Звонки</code>\n\n<i>❔ Выбери режим работы (влияет на кол-во потоков)</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=flood_mode_kb(callback.data.split("|")[1], "auto_calls"),
        )
    elif callback.data.startswith("task_stop"):
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard = InlineKeyboardMarkup().add(kb)
        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        limits_update(callback.from_user.id, -1)
        bomber_stop(callback.data.split("|")[1], now, "Остановлено пользователем")
        bomber = get_bomber_stats(callback.data.split("|")[1])
        bomber_active.remove(bomber[1])
        try:
            bomber = get_bomber_stats(callback.data.split("|")[1])
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
            await bot.edit_message_text(
                f"""<b>{emojis[bomber[6]]}  #{callback.data.split('|')[1]}  {emojis[bomber[2]]}  +{bomber[1]}  {emojis[bomber[4]]}</b>
    <i>Просмотр статистики</i>

👁‍🗨 ID задачи:  <code>{callback.data.split('|')[1]}</code>
├ Тип:  <code>{bomber[2]}</code>
├ Режим работы:  <code>{bomber[3]}</code>
├ Статус:  <code>{bomber[4]}</code>
├ Номер:  <code>+{bomber[1]}</code>
├ Дата запуска:  <code>{bomber[5]} (UTC+03:00)</code>
├ Время работы:  <code>{int((datetime.datetime.strptime(now, "%d.%m.%Y %H:%M:%S") - datetime.datetime.strptime(bomber[5], "%d.%m.%Y %H:%M:%S")).seconds / 60) if bomber[10] == 'None' else int((datetime.datetime.strptime(bomber[10], "%d.%m.%Y %H:%M:%S") - datetime.datetime.strptime(bomber[5], "%d.%m.%Y %H:%M:%S")).seconds / 60)} минут</code>
├ Отправлено успешно:  <code>{bomber[9]}</code>
└ Причина завершения:  <code>{bomber[7]}</code>""",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=task_kb(callback.data.split("|")[1])
                if bomber[4] == "В процессе"
                else keyboard,
            )
        except:
            pass
    elif callback.data.startswith("refresh_task"):
        try:
            kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
            keyboard = InlineKeyboardMarkup().add(kb)
            bomber = get_bomber_stats(callback.data.split("|")[1])
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
            now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            await bot.edit_message_text(
                f"""<b>{emojis[bomber[6]]}  #{callback.data.split('|')[1]}  {emojis[bomber[2]]}  +{bomber[1]}  {emojis[bomber[4]]}</b>
    <i>Просмотр статистики</i>

👁‍🗨 ID задачи:  <code>{callback.data.split('|')[1]}</code>
├ Тип:  <code>{bomber[2]}</code>
├ Режим работы:  <code>{bomber[3]}</code>
├ Статус:  <code>{bomber[4]}</code>
├ Номер:  <code>+{bomber[1]}</code>
├ Дата запуска:  <code>{bomber[5]} (UTC+03:00)</code>
├ Время работы:  <code>{int((datetime.datetime.strptime(now, "%d.%m.%Y %H:%M:%S") - datetime.datetime.strptime(bomber[5], "%d.%m.%Y %H:%M:%S")).seconds / 60) if bomber[10] == 'None' else int((datetime.datetime.strptime(bomber[10], "%d.%m.%Y %H:%M:%S") - datetime.datetime.strptime(bomber[5], "%d.%m.%Y %H:%M:%S")).seconds / 60)} минут</code>
├ Отправлено успешно:  <code>{bomber[9]}</code>
└ Причина завершения:  <code>{bomber[7]}</code>""",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=task_kb(callback.data.split("|")[1])
                if bomber[4] == "В процессе"
                else keyboard,
            )
        except:
            pass

    elif callback.data == "history_flood":
        await bot.edit_message_text(
            "<b>📝 История</b>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=history_kb(callback.from_user.id),
        )
    elif callback.data.startswith("bomber_start"):
        user = get_profile(callback.from_user.id)
        rang = get_rang(user[5])
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard = InlineKeyboardMarkup().add(kb)
        if user[6] >= rang[1]:
            await bot.edit_message_text(
                f"<b>⚠️ Ошибка</b>\n\n<i>Все твои слоты заняты</i>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            await bot.answer_callback_query(callback.id)
            return
        elif user[7] >= rang[2]:
            await bot.edit_message_text(
                f"<b>⚠️ Ошибка</b>\n\n<i>Ты исчерпал лимит задач в сутки</i>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            await bot.answer_callback_query(callback.id)
            return
        limits_update(callback.from_user.id, 1)
        server_phones_update()
        bomber = get_bomber_start(callback.data.split("|")[1])
        bomber_active.append(bomber[4])
        bomber_start_cancel(bomber[6])
        bomber_history_insert(
            callback.from_user.id,
            bomber[4],
            bomber[2],
            bomber[3],
            "В процессе",
            datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            bomber[1],
            "-",
            callback.data.split("|")[1],
            0,
            "None",
        )
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
        if bomber[3] == "🍀 Классический":
            _timer = 30 if bomber[6] == "🤬 Обычный флуд" else 1440
            thread = threading.Thread(
                target=sms_bomber if bomber[2] == "📨 SMS" else call_bomber,
                args=(
                    callback.from_user.id,
                    callback.data.split("|")[1],
                    _timer,
                    bomber[4],
                    callback.message.message_id,
                ),
            )
            thread.start()
        elif bomber[3] == "🚧 Мощный":
            _timer = 25 if bomber[6] == "🤬 Обычный флуд" else 1440
            for i in range(1, 2):
                thread = threading.Thread(
                    target=sms_bomber if bomber[2] == "📨 SMS" else call_bomber,
                    args=(
                        callback.from_user.id,
                        callback.data.split("|")[1],
                        _timer,
                        bomber[4],
                        callback.message.message_id,
                    ),
                )
                thread.start()
        elif bomber[3] == "🔥 Легендарный":
            _timer = 20 if bomber[6] == "🤬 Обычный флуд" else 1440
            for i in range(1, 3):
                thread = threading.Thread(
                    target=sms_bomber if bomber[2] == "📨 SMS" else call_bomber,
                    args=(
                        callback.from_user.id,
                        callback.data.split("|")[1],
                        _timer,
                        bomber[4],
                        callback.message.message_id,
                    ),
                )
                thread.start()
        await bot.edit_message_text(
            f"""<b>{emojis[bomber[1]]}  #{callback.data.split('|')[1]}  {emojis[bomber[2]]}  +{bomber[4]}  {emojis['В процессе']}</b>
<i>Просмотр статистики</i>

👁‍🗨 ID задачи:  <code>{callback.data.split('|')[1]}</code>
├ Тип:  <code>{bomber[2]}</code>
├ Режим работы:  <code>{bomber[3]}</code>
├ Статус:  <code>В процессе</code>
├ Номер:  <code>+{bomber[4]}</code>
├ Дата запуска:  <code>{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")} (UTC+03:00)</code>
├ Время работы:  <code>0 минут</code>
├ Отправлено успешно:  <code>0</code>
└ Причина завершения:  <code>—</code>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=task_kb(callback.data.split("|")[1]),
        )
    elif callback.data.startswith("reverse_calls_bomber"):
        if callback.data.split("|")[1] == "default":
            tag = "🤬 Обычный флуд"
        elif callback.data.split("|")[1] == "infinity":
            tag = "☠️ Бесконечный флуд"
        await bot.edit_message_text(
            f"""<b>{tag}</b>\n└ Тип:  <code>☎️ Обратные звонки</code>\n\n<i>❔ Выбери режим работы (влияет на кол-во потоков)</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=flood_mode_kb(callback.data.split("|")[1], "reverse_calls"),
        )
    elif callback.data.startswith("bomber_cancel"):
        await state.finish()
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
        bomber_start_cancel(callback.data.split("|")[1])
    elif callback.data == "infinity_flood":
        user = get_profile(callback.from_user.id)
        now = datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H")
        if user[3] == "Отсутствует":
            await callback.answer(
                "⚠️ Для продолжения необходимо купить подписку", show_alert=True
            )
            await bot.answer_callback_query(callback.id)
            return
        elif datetime.datetime.strptime(
            user[3], "%d.%m.%Y %S:%M:%H"
        ) < datetime.datetime.strptime(now, "%d.%m.%Y %S:%M:%H"):
            set_default_sub(callback.from_user.id)
            await callback.answer(
                "⚠️ Для продолжения необходимо купить подписку", show_alert=True
            )
            await bot.answer_callback_query(callback.id)
            return
        else:
            await bot.edit_message_text(
                """<b>🤬 Обычный флуд</b>
<i>Выбери тип флуда

❔ Больше информации в разделе «FAQ/Помощь»</i>""",
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=flood_type_kb("infinity"),
                parse_mode="HTML",
            )
    elif callback.data == "close_message":
        await state.finish()
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    elif callback.data == "sub":
        await bot.edit_message_text(
            "<b>💵 Подписка</b>\n<i>Выбери наиболее подходящий для тебя вариант из списка ниже\n❔ Стоимость подписки для всех рангов одинаковая. Больше информации ты сможешь найти в разделе <b>«FAQ / Помощь».</b></i>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=buy_sub_kb(),
        )
    elif callback.data == "back":
        await state.finish()
        await send_profile(
            callback.from_user.id, "callback", callback.message.message_id
        )
    elif callback.data == "rangs":
        user = get_profile(callback.from_user.id)
        rang = get_rang(user[5])
        await bot.edit_message_text(
            f"<b>⚜️ Ранги</b>\n<i>Выбери интересующий тебя ранг с помощью кнопок ниже, после чего нажми на кнопку «Купить этот ранг»</i>\n\n— <code>{user[5]}</code> —\n\n📞 Слотов: <code>{rang[1]} шт.</code>\n⚙️ Суточный лимит:  <code>{rang[2]} задач в день</code>\n🤍 Белый список: <code>{rang[3]} номеров</code>\n💰 Цена: <code>{rang[4]} ₽</code>"
            + "\n\n<i>❗️ У тебя уже есть этот ранг</i>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=rangs_choose_kb(user[5], user[5]),
        )
    elif callback.data.startswith("rang_choose"):
        rang = get_rang(callback.data.split("|")[1])
        user = get_profile(callback.from_user.id)
        if rang[0] == user[5]:
            warn_text = "\n\n<i>❗️ У тебя уже есть этот ранг</i>"
        else:
            warn_text = ""
        try:
            await bot.edit_message_text(
                f"<b>⚜️ Ранги</b>\n<i>Выбери интересующий тебя ранг с помощью кнопок ниже, после чего нажми на кнопку «Купить этот ранг»</i>\n\n— <code>{callback.data.split('|')[1]}</code> —\n\n📞 Слотов: <code>{rang[1]} шт.</code>\n⚙️ Суточный лимит:  <code>{rang[2]} задач в день</code>\n🤍 Белый список: <code>{rang[3]} номеров</code>\n💰 Цена: <code>{rang[4]} ₽</code>"
                + warn_text,
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=rangs_choose_kb(rang[0], user[5]),
            )
        except:
            pass
    elif callback.data == "balance_up":
        msg = await bot.edit_message_text(
            "<b>💰 Пополнить баланс</b>\n<i><u>Отправь мне сумму</u> на которую хочешь пополнить баланс или выбери один из предложенных вариантов</i>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=balance_up_kb(),
            parse_mode="HTML",
        )
        await FSMMain.get_balance_up_amount.set()
        async with state.proxy() as data:
            data["message_id"] = msg.message_id
    elif callback.data.startswith("balance_up_amount"):
        await bot.edit_message_text(
            f"<b>💰 Пополнить баланс</b>\nСумма:  <code>{callback.data.split('|')[1]}.00 ₽</code>\n\n<i>❔ Выбери способ оплаты</i>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=payment_system_choose(callback.data.split("|")[1]),
        )
    elif callback.data.startswith("balance_up_system"):
        amount = callback.data.split("|")[2]
        new_bill = p2p.bill(amount=amount, lifetime=30)
        bill_id = new_bill.bill_id
        pay_keyboard = create_bill(bill_id, new_bill.pay_url, amount)
        await bot.edit_message_text(
            f"<b>💰 Пополнить баланс</b>\nК оплате:  <code>{amount}.00 ₽</code>\n\n<i>❔ Нажми на кнопку ниже чтобы открыть форму оплаты.После оплаты нажми кнопку проверить оплату.</i>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=pay_keyboard,
            parse_mode="HTML",
        )
    elif callback.data.startswith("rang_buy"):
        user = get_profile(callback.from_user.id)
        rang = get_rang(callback.data.split("|")[1])
        keyboard = InlineKeyboardMarkup(row_width=1)
        if user[2] < float(rang[4]):
            kb = InlineKeyboardButton(
                f"💰 Пополнить баланс на {rang[4]}₽",
                callback_data=f"balance_up_amount|{rang[4]}",
            )
            kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
            keyboard.add(kb, kb1)
            await bot.edit_message_text(
                f"<b>⚠️ Недостаточно средств</b>\n<i>Для пополнения баланса нажми на кнопку ниже</i>\nТвой баланс:  <code>{user[2]} ₽</code>",
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await bot.edit_message_text(
                f"""<b>💵 Подтверждение покупки</b>
<i>Для продолжения тебе необходимо подтвердить списание средств, нажав соответствующую кнопку</i>

🔥 Покупка ранга: <code>{rang[0]}</code>
💰 Сумма: <code>{rang[4]} ₽</code>

Твой баланс:  <code>{user[2]} ₽</code>""",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=confirm_rang_buy(rang[0], rang[4]),
            )

    elif callback.data.startswith("buy_rang_confirm"):
        keyboard = InlineKeyboardMarkup(row_width=1)
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        set_rang(callback.from_user.id, callback.data.split("|")[1])
        balance_down(callback.from_user.id, callback.data.split("|")[2])
        await bot.edit_message_text(
            f"<b>⚜️ Ранги</b>\n<i>Ты успешно купил ранг <code>{callback.data.split('|')[1]}</code></i>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif callback.data.startswith("check_bill_status"):
        bill_id = callback.data.split("|")[1]
        amount = callback.data.split("|")[2]
        status = (p2p.check(bill_id=bill_id)).status
        close_kb = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="❌ Закрыть", callback_data="close_message")
        close_kb.add(kb)
        if status == "PAID":
            await bot.edit_message_text(
                f"<b>💰 Пополнить баланс</b>\n<i>Твой баланс был успешно пополнен на сумму <code>{amount}.00 ₽</code></i>",
                callback["message"]["chat"]["id"],
                callback["message"]["message_id"],
                parse_mode="HTML",
                reply_markup=close_kb,
            )
            buy_set_balance(callback.from_user.id, amount)
            user = get_profile(callback.from_user.id)
            await bot.send_message(
                admin_id,
                f"Пользователь @{callback.from_user.username}<code>({callback.from_user.id})</code> пополнил баланс на <code>{amount}₽</code>",
            )
            if user[9] != "None":
                set_ref_balance(user[9], amount / 5)
                await bot.send_message(
                    int(user[9]),
                    f"Вы получили <code>{amount / 5} ₽</code> за пополнение баланса вашим рефералом.",
                    parse_mode="HTML",
                )
        elif status == "WAITING":
            await callback.answer("Статус платежа: Ожидает оплаты")
        elif status == "EXPIRED":
            await bot.edit_message_reply_markup(
                callback.from_user.id, callback.message.message_id
            )
            await callback.answer("Статус платежа: Истекло время оплаты")
    elif callback.data.startswith("pay_cancel"):
        bill_id = callback.data.split("|")[1]
        if bill_id != "0":
            p2p.reject(bill_id=bill_id)
        await bot.edit_message_text(
            "Платёж отменён ✅",
            callback["message"]["chat"]["id"],
            callback["message"]["message_id"],
        )
        await send_profile(
            callback.from_user.id, "message", callback.message.message_id
        )
    elif callback.data == "activate_key":
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        await bot.edit_message_text(
            "<b>🎟 Активировать ключ</b>\n<i>Теперь отправь мне ключ, который ты хочешь активировать</i>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        await FSMMain.get_promo.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data.startswith("buy_sub_confirm"):
        user = get_profile(callback.from_user.id)
        keyboard = InlineKeyboardMarkup(row_width=1)
        if user[2] < float(callback.data.split("|")[2]):
            kb = InlineKeyboardButton(
                f"💰 Пополнить баланс на {callback.data.split('|')[2]}₽",
                callback_data=f"balance_up_amount|{callback.data.split('|')[2]}",
            )
            kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
            keyboard.add(kb, kb1)
            await bot.edit_message_text(
                f"<b>⚠️ Недостаточно средств</b>\n<i>Для пополнения баланса нажми на кнопку ниже</i>\n\nТвой баланс <code>{user[2]} ₽</code>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
            keyboard.add(kb)
            if callback.data.split("|")[1] == "hour":
                sub = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                    "%d.%m.%Y %S:%M:%H"
                )
                sub_text = "1 час"
            else:
                subs = {
                    "day": 1,
                    "week": 7,
                    "month": 30,
                    "one_and_half_month": 90,
                    "half_year": 180,
                    "year": 365,
                }
                sub = (
                    datetime.datetime.now()
                    + datetime.timedelta(days=subs[callback.data.split("|")[1]])
                ).strftime("%d.%m.%Y %S:%M:%H")
                sub_text = f'{subs[callback.data.split("|")[1]]} дней'
            balance_down(callback.from_user.id, callback.data.split("|")[2])
            set_sub(callback.from_user.id, sub)
            await bot.edit_message_text(
                f"<b>💵 Подписка</b>\n<i>Ты успешно купил подписку на <code>{sub_text}</code></i>",
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
    elif callback.data == "reset_slots":
        reset_slots()
        await callback.message.edit_text(
            "Вы успешно обнулили слоты, можете перезапускать бота",
            reply_markup=back_admin_menu(),
        )
    elif callback.data.startswith("buy_sub"):
        user = get_profile(callback.from_user.id)
        keyboard = InlineKeyboardMarkup(row_width=1)
        if user[2] < float(callback.data.split("|")[2]):
            kb = InlineKeyboardButton(
                f"💰 Пополнить баланс на {callback.data.split('|')[2]}₽",
                callback_data=f"balance_up_amount|{callback.data.split('|')[2]}",
            )
            kb1 = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
            keyboard.add(kb, kb1)
            await bot.edit_message_text(
                f"<b>⚠️ Недостаточно средств</b>\n<i>Для пополнения баланса нажми на кнопку ниже</i>\n\nТвой баланс <code>{user[2]} ₽</code>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            subs = {
                "day": 1,
                "week": 7,
                "month": 30,
                "one_and_half_month": 90,
                "half_year": 180,
                "year": 365,
            }
            if callback.data.split("|")[1] == "hour":
                sub = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime(
                    "%d.%m.%Y %S:%M:%H"
                )
                sub_text = "1 час"
            else:
                subs = {
                    "day": 1,
                    "week": 7,
                    "month": 30,
                    "one_and_half_month": 90,
                    "half_year": 180,
                    "year": 365,
                }

                sub_text = (
                    f'{subs[callback.data.split("|")[1]]} дней'
                    if subs[callback.data.split("|")[1]] != 1
                    else f'{subs[callback.data.split("|")[1]]} день'
                )
            await bot.edit_message_text(
                f"""<b>💵 Подтверждение покупки</b>
<i>Для продолжения тебе необходимо подтвердить списание средств, нажав соответствующую кнопку</i>

🔥 Покупка подписки на <code>{sub_text} </code>
💰 Сумма: <code>{callback.data.split('|')[2]} ₽</code>

Твой баланс:  <code>{user[2]} ₽</code>""",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=buy_sub_confirm(
                    callback.data.split("|")[1], callback.data.split("|")[2]
                ),
            )
    elif callback.data == "partner programm":
        user = get_profile(callback.from_user.id)
        ref = get_referals(callback.from_user.id)
        bot_me = await bot.me
        await bot.edit_message_text(
            f"<b>🤝 Партнёрская программа</b>\n<i>Приглашай друзей и зарабатывай!</i>\n\n🔗 <code>t.me/{bot_me['username']}?start={callback.from_user.id}</code>\n├ Рефералов: <code>{len(ref)}</code>\n├ Ставка:  <code>20.00%</code>\n└ Доступно к выводу:  <code>{user[10]} ₽</code>\n\n⁉️ Подробнее узнать о партнёрской программе можно в разделе «FAQ/Помощь»",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=ref_programm_kb(),
        )
    elif callback.data == "link_shorter":
        bot_me = await bot.me
        req = requests.post(
            f"https://clck.ru/--",
            data={
                "json": "true",
                "url": f"t.me/{bot_me['username']}?start={callback.from_user.id}",
            },
        )
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        await bot.edit_message_text(
            f"<b>🤝 Партнёрская программа</b>\n<i>Твоя сокращённая партнёрская ссылка</i>\n\n🔗 <code>{json.loads(req.text)[0]}</code>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    elif callback.data == "withdraw_request":
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        user = get_profile(callback.from_user.id)
        if float(withdraw_limit) > float(user[10]):
            await callback.answer(
                f"⚠️   Суммы на твоем балансе недостаточно для вывода средств ( {float(user[10])} ₽ / {float(withdraw_limit)} ₽ )",
                show_alert=True,
            )
        else:
            msg = await bot.edit_message_text(
                f"<b>🤝 Партнёрская программа</b>\n <i>Введите реквизиты для вывода (например: <code>8-800-555-3535 киви</code>)</i>",
                callback.from_user.id,
                callback.message.message_id,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            await FSMMain.get_requisites.set()
            async with state.proxy() as data:
                data["message_id"] = msg.message_id
    elif callback.data.startswith("withdraw_request_user"):
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        user = get_profile(callback.from_user.id)
        if float(user[10]) < float(100):
            await bot.edit_message_text(
                f"⚠️ Суммы на твоем балансе недостаточно для вывода средств <code>({float(user[10])} ₽ / {float(withdraw_limit)} ₽)</code>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        else:
            await bot.edit_message_text(
                "<b>🤝 Партнёрская программа</b>\n\n<i>Заявка на вывод успешно отправлена</i>",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            ref = get_referals(callback.from_user.id)
            await bot.send_message(
                admin_id,
                f"Заявка на вывод от пользователя @{callback.from_user.username}(<code>{callback.from_user.id}</code>)\n\nТекущий реферальный баланс: <code>{user[10]}</code>\nВсего рефералов: <code>{len(ref)}</code>\nРеквизиты: <code>{callback.data.split('|')[1]}</code>\nДата и время: <code>{datetime.datetime.today().strftime('%d.%m.%Y %H:%M:%S')}</code>",
                parse_mode="HTML",
                reply_markup=withdraw_request_confirm_kb(callback.from_user.id),
            )
    elif callback.data.startswith("withdraw_request_admin"):
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        set_ref_balance(callback.data.split("|")[1], -100)
        await bot.edit_message_text(
            f'Вы подтвердили оплату пользователю <code>{callback.data.split("|")[1]}</code>',
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await bot.send_message(
            callback.data.split("|")[1],
            f"<b>🤝 Партнёрская программа</b>\n\n Администратор подтвердил вывод средств на ваш кошелек. Ваш реферальный баланс обновлен",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    elif callback.data.startswith("withdraw_request_cancel"):
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back")
        keyboard.add(kb)
        await bot.edit_message_text(
            f'Вы отклонили заявку на вывод пользователю <code>{callback.data.split("|")[1]}</code>',
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await bot.send_message(
            callback.data.split("|")[1],
            f"<b>🤝 Партнёрская программа</b>\n\n Администратор отклонил заявку на вывод средств на ваш кошелек",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    elif callback.data == "whitelist_check":
        user = get_profile(callback.from_user.id)
        rang = get_rang(user[5])
        await bot.edit_message_text(
            f"""<b>🤍 Белый список</b>
<i>Белый список - это реестр номеров, которые защищены от флуда через наш сервис, то есть на них нельзя будет запустить флуд SMS или звонками.

📞 Добавлено номеров:  <code>{user[8]} из {rang[3]}</code>

❕ Услуга работает до тех пор, пока активна твоя подписка на бота.

❕ Через нашего бота флуд на добавленные номера сможешь запустить только ты.</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=whitelist_kb(),
        )
    elif callback.data == "back_adm_menu":
        await state.finish()
        await bot.edit_message_text(
            "<b>admin panel</b>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=admin_kb(),
            parse_mode="HTML",
        )
    elif callback.data == "whitelist_number_add":
        user = get_profile(callback.from_user.id)
        rang = get_rang(user[5])
        if int(user[8]) == int(rang[3]):
            await callback.answer(
                "⚠️ Добавлено максимальное кол-во номеров. Увеличить это ограничение можно, повысив свой ранг.",
                show_alert=True,
            )
        else:
            keyboard = InlineKeyboardMarkup()
            kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
            keyboard.add(kb)
            await bot.edit_message_text(
                """<b>➕ Добавить номер</b>
<i>Пришли мне номер телефона (в любом формате), чтобы добавить его в белый список.</i>""",
                callback.from_user.id,
                callback.message.message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
            await FSMMain.get_whitelist_number.set()
            async with state.proxy() as data:
                data["message_id"] = callback.message.message_id

    elif callback.data == "back1":
        await state.finish()
        await bot.edit_message_text(
            """<b>🔥 Начать</b>
<i>Выбери один из вариантов

❔ Больше информации о разнице между обычным и бесконечным флудом есть в разделе «FAQ/Помощь»</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=flood_type(),
        )
    elif callback.data == "check_number_whitelist":
        keyboard = InlineKeyboardMarkup()
        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard.add(kb)
        msg = await bot.edit_message_text(
            """<b>❔ Проверить номер</b>\n
<i>Пришли мне номер телефона (в любом формате) и я скажу, запускали ли на него флуд через этого бота.</i>""",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=keyboard,
        )
        await FSMMain.get_check_number.set()
        async with state.proxy() as data:
            data["message_id"] = msg.message_id
    elif callback.data == "set_balance":
        await bot.edit_message_text(
            "Введите id пользователя, которому хотите установить баланс",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=back_admin_menu(),
        )
        await FMSAdmin.get_userid_set_balance.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data == "watch_profile":
        await bot.edit_message_text(
            "<b>Введите id пользователя</b>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )
        await FMSAdmin.get_userid_watch_profile.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data == "ban_user":
        await bot.edit_message_text(
            "<b>Введите id пользователя, которого хотите забанить</b>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )
        await FMSAdmin.get_userid_ban.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data == "unban_user":
        await bot.edit_message_text(
            "<b>Введите id пользователя, которого хотите разбанить</b>",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=back_admin_menu(),
            parse_mode="HTML",
        )
        await FMSAdmin.get_userid_unban.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data == "watch_subs":
        subs = get_subs()
        with open("subs.txt", "w+") as f:
            f.write(subs)
        with open("subs.txt", "rb") as f:
            await bot.send_document(
                callback.from_user.id, f, caption="Активные подписки"
            )
    elif callback.data == "mailing":
        await bot.edit_message_text(
            "<b>Введите текст рассылки</b>",
            callback.from_user.id,
            callback.message.message_id,
            parse_mode="HTML",
            reply_markup=back_admin_menu(),
        )
        await FMSAdmin.get_mailing_text.set()
        async with state.proxy() as data:
            data["message_id"] = callback.message.message_id
    elif callback.data == "promo_generator":
        await bot.edit_message_text(
            "Выберите, на что будут сгенерированы промокоды",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=promo_generate_choose_kb(),
        )
    elif callback.data.startswith("generate"):
        if callback.data.split("|")[1] == "sub":
            item = f'sub|{callback.data.split("|")[2]}'
        else:
            item = f'rang|{callback.data.split("|")[2]}'
        await bot.edit_message_text(
            "Введите количество промокодов, которое хотите сгенерировать",
            callback.from_user.id,
            callback.message.message_id,
            reply_markup=back_admin_menu(),
        )
        await FMSAdmin.get_promo_amount.set()
        async with state.proxy() as data:
            data["item"] = item
            data["message_id"] = callback.message.message_id
    await bot.answer_callback_query(callback.id)


async def timer():
    reset_limit()


async def send_message_to_user(message, user_id):
    receive_users, block_users = 0, 0
    users = get_all_users()
    for user in users:
        try:
            await bot.send_message(user[0], message, parse_mode="HTML")
            receive_users += 1
        except:
            block_users += 1
            update_status_distribution(user_id=user[0], value="inactive")
        await asyncio.sleep(0.05)
    await bot.send_message(
        user_id,
        f"<b>📢 Рассылка была завершена ☑</b>\n"
        f"👤 Пользователей получило сообщение: <code>{receive_users} ✅</code>\n"
        f"👤 Пользователей не получило сообщение: <code>{block_users} ❌</code>",
        parse_mode="HTML",
        reply_markup=back_admin_menu(),
    )


if __name__ == "__main__":
    # TIMEZONE = getenv("Asia/Novokuznetsk") or "Asia/Novokuznetsk"
    # tz = pytz.timezone(TIMEZONE)
    sched = AsyncIOScheduler()
    # sched.configure(timezone=tz)
    sched.start()
    sched.add_job(
        timer,
        "interval",
        days=3,
    )
    executor.start_polling(dp, skip_updates=True)
