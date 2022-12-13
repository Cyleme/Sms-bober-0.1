from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMMain(StatesGroup):
    get_balance_up_amount = State()
    get_promo = State()
    get_requisites = State()
    get_whitelist_number = State()
    get_check_number = State()
    get_phone_bomber = State()


class FMSAdmin(StatesGroup):
    get_userid_set_balance = State()
    get_amount_set_balance = State()
    get_userid_watch_profile = State()
    get_userid_ban = State()
    get_reason_ban = State()
    get_userid_unban = State()
    get_mailing_text = State()
    get_promo_amount = State()
