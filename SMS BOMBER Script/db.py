import sqlite3
from time import time
from threading import Lock

lock = Lock()


con = sqlite3.connect("db.db", check_same_thread=False)

cur = con.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS "users" (
	"userid"	INTEGER,
	"username"	TEXT,
	"balance"	INTEGER DEFAULT 0,
	"sub"	TEXT DEFAULT Отсутствует,
	"reg"	TEXT,
	"rang"	INTEGER DEFAULT '🥉 Bronze',
	"slots"	INTEGER DEFAULT 0,
	"tasks_limit"	INTEGER DEFAULT 0,
	"whitelist"	INTEGER DEFAULT 0,
	"referal"	TEXT DEFAULT None,
	"ref_bal"	REAL DEFAULT 0,
	"status"	TEXT DEFAULT 'active',
	PRIMARY KEY("userid")
);"""
)


cur.execute(
    """CREATE TABLE IF NOT EXISTS "banlist" (
	"userid"	INTEGER,
	"ban_reason"	TEXT,
	"date"	TEXT,
	PRIMARY KEY("userid")
);"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS "rangs" (
	"rang"	TEXT,
	"slots"	INTEGER,
	"daily_limit"	INTEGER,
	"whitelist"	INTEGER,
	"price"	REAL
);"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS "promocodes" (
	"name"	TEXT,
	"item"	TEXT,
	"duration"	TEXT,
	PRIMARY KEY("name")
);"""
)


cur.execute(
    """CREATE TABLE IF NOT EXISTS "bot_stats" (
	"start_date"	TEXT,
	"sms_services"	INTEGER,
	"auto_calls_servces"	INTEGER,
	"reverse_calls_services"	INTEGER,
	"number_destroyed"	INTEGER,
	"sms_sent"	INTEGER,
	"calls_sent"	INTEGER
);"""
)


cur.execute(
    """CREATE TABLE IF NOT EXISTS "whitelist" (
	"added_by"	INTEGER,
	"number"	TEXT,
	PRIMARY KEY("number")
);"""
)


cur.execute(
    """CREATE TABLE IF NOT EXISTS "bomber_start" (
	"userid"	INTEGER,
	"method"	TEXT,
	"type"	TEXT,
	"mode"	TEXT,
	"phone"	TEXT,
	"worktime"	INTEGER,
	"id"	TEXT,
	PRIMARY KEY("id")
);"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS "history" (
	"userid"	INTEGER,
	"phone"	TEXT,
	"type"	TEXT,
	"mode"	TEXT,
	"status"	TEXT,
	"date"	TEXT,
	"method"	TEXT,
	"stop_reason"	TEXT,
	"id"	TEXT,
	"success_sent"	INTEGER,
	"time_stop"	TEXT,
	PRIMARY KEY("id")
);"""
)


def db_insert(userid, username, reg):
    try:
        lock.acquire(True)
        cur.execute(
            "INSERT OR IGNORE INTO `users` (userid, username, reg) VALUES (?, ?, ?)",
            (userid, username, reg),
        )
        con.commit()
    finally:
        lock.release()


def get_profile(userid):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `users` WHERE `userid` = ?", (userid,)
        ).fetchall()[0]
        return res
    finally:
        lock.release()


def buy_set_balance(userid, balance):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `balance` = `balance` + ? WHERE `userid` = ?",
            (
                balance,
                userid,
            ),
        )
        con.commit()
    finally:
        lock.release()


def set_default_sub(userid):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `sub` = ? WHERE `userid` = ?", ("Отсутствует", userid)
        )
        con.commit()
    finally:
        lock.release()


def set_referal(userid, referal):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `referal` = ? WHERE `userid` = ?", (referal, userid)
        )
        con.commit()
    finally:
        lock.release()


def get_rang(rang):
    try:
        lock.acquire(True)
        res = cur.execute("SELECT * FROM `rangs` WHERE `rang` = ?", (rang,)).fetchall()[
            0
        ]
        return res
    finally:
        lock.release()


def get_promo(promo):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `promocodes` WHERE `name` = ?", (promo,)
        ).fetchall()[0]
        cur.execute("DELETE FROM `promocodes` WHERE `name` = ?", (promo,))
        con.commit()
        return res
    finally:
        lock.release()


def set_sub(userid, sub):
    try:
        lock.acquire(True)
        cur.execute("UPDATE `users` SET `sub` = ? WHERE `userid` = ?", (sub, userid))
        con.commit()
    finally:
        lock.release()


def set_rang(userid, rang):
    try:
        lock.acquire(True)
        cur.execute("UPDATE `users` SET `rang` = ? WHERE `userid` = ?", (rang, userid))
        con.commit()
    finally:
        lock.release()


def balance_down(userid, balance):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `balance` = `balance` - ? WHERE `userid` = ?",
            (balance, userid),
        )
        con.commit()
    finally:
        lock.release()


def set_ref_balance(userid, balance):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `ref_bal` = `ref_bal` + ? WHERE `userid` = ?",
            (balance, userid),
        )
        con.commit()
    finally:
        lock.release()


def get_referals(userid):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `users` WHERE `referal` = ?", (userid,)
        ).fetchall()
        return res
    finally:
        lock.release()


def get_bot_stats():
    try:
        lock.acquire(True)
        res = cur.execute("SELECT * FROM `bot_stats`").fetchall()[0]
        return res
    finally:
        lock.release()


def get_all_users():
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `users` WHERE `status` = ?", ("active",)
        ).fetchall()
        return res
    finally:
        lock.release()


def whitelist_add_db(userid, number):
    try:
        lock.acquire(True)
        cur.execute("INSERT OR IGNORE INTO `whitelist` VALUES (?, ?)", (userid, number))
        cur.execute(
            "UPDATE `users` SET `whitelist` = `whitelist` + ? WHERE `userid` = ?",
            (1, userid),
        )
        con.commit()
    finally:
        lock.release()


def get_whitelist(number):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `whitelist` WHERE `number` = ?", (number,)
        ).fetchone()
        return res
    finally:
        lock.release()


def check_phone(number):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `history` WHERE `phone` = ?", (number,)
        ).fetchall()
        return res
    finally:
        lock.release()


def bomber_stats_update(task_id, stats):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `history` SET `success_sent` = `success_sent` + ? WHERE `id` = ?",
            (stats, task_id),
        )
        con.commit()
    finally:
        lock.release()


def bomber_start_insert(userid, method, type, mode, phone, work_time, id):
    try:
        lock.acquire(True)
        cur.execute(
            "INSERT INTO `bomber_start` VALUES(?, ?, ?, ?, ?, ?, ?)",
            (userid, method, type, mode, phone, work_time, id),
        )
        con.commit()
    finally:
        lock.release()


def get_bomber_start(task_id):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `bomber_start` WHERE `id` = ?", (task_id,)
        ).fetchone()
        return res
    finally:
        lock.release()


def bomber_start_cancel(task_id):
    try:
        lock.acquire(True)
        cur.execute("DELETE FROM `bomber_start` WHERE `id` = ?", (task_id,))
        con.commit()
    finally:
        lock.release()


def reset_limit():
    try:
        lock.acquire(True)
        cur.execute("UPDATE `users` SET `tasks_limit` = ?", (0,))
        con.commit()
    finally:
        lock.release()


def bomber_history_insert(
    userid,
    phone,
    _type,
    mode,
    status,
    date,
    work_time,
    stop_reason,
    id,
    succ_sent,
    time_start,
):
    try:
        lock.acquire(True)
        cur.execute(
            "INSERT INTO `history` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                userid,
                phone,
                _type,
                mode,
                status,
                date,
                work_time,
                stop_reason,
                id,
                succ_sent,
                time_start,
            ),
        )
        con.commit()
    finally:
        lock.release()


def get_bomber_stats(task_id):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `history` WHERE `id` = ?", (task_id,)
        ).fetchone()
        return res
    finally:
        lock.release()


def get_bomber_history(userid):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `history` WHERE `userid` = ?", (userid,)
        ).fetchall()
        return res
    finally:
        lock.release()


def bomber_stop(task_id, stop_time, stop_reason):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `history` SET `status` = ?, `stop_reason` = ?, `time_stop` = ? WHERE `id` = ?",
            ("Завершено", stop_reason, stop_time, task_id),
        )
        con.commit()
    finally:
        lock.release()


def server_phones_update():
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `bot_stats` SET `number_destroyed` = `number_destroyed` + 1"
        )
        con.commit()
    finally:
        lock.release()


def limits_update(userid, value):
    try:
        lock.acquire(True)
        if value == 1:
            cur.execute(
                "UPDATE `users` SET `slots` = `slots` + ?, `tasks_limit`= `tasks_limit` + ? WHERE `userid` = ?",
                (value, value, userid),
            )
        elif value == -1:
            cur.execute(
                "UPDATE `users` SET `slots` = `slots` + ? WHERE `userid` = ?",
                (value, userid),
            )
        con.commit()
    finally:
        lock.release()


def server_sms_update(sms):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `bot_stats` SET `sms_sent` = `sms_sent` + ?",
            (sms,),
        )
        con.commit()
    finally:
        lock.release()


def server_call_update(call):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `bot_stats` SET `calls_sent` = `calls_sent` + ?",
            (call,),
        )
        con.commit()
    finally:
        lock.release()


def ban(userid, reason, date):
    try:
        lock.acquire(True)
        cur.execute(
            "INSERT OR IGNORE INTO `banlist` VALUES (?, ?, ?)", (userid, reason, date)
        )
        con.commit()
    finally:
        lock.release()


def unban(userid):
    try:
        lock.acquire(True)
        cur.execute("DELETE FROM `banlist` WHERE `userid` = ?", (userid,))
        con.commit()
    finally:
        lock.release()


def get_bans(userid):
    try:
        lock.acquire(True)
        res = cur.execute(
            "SELECT * FROM `banlist` WHERE `userid` = ?", (userid,)
        ).fetchone()
        return res
    finally:
        lock.release()


def get_subs():
    try:
        lock.acquire(True)
        txt = ""
        res = cur.execute(
            "SELECT `userid`, `username`, `status` FROM `users` WHERE `sub` != ?",
            ("Отсутствует",),
        ).fetchall()
        for z, res in enumerate(res, 1):
            if res[2] == "active":
                txt += f"{z}. {res[0]} @{res[1]}\n"
            else:
                pass
        return txt
    finally:
        lock.release()


def update_status_distribution(user_id: int, value: str):
    try:
        lock.acquire(True)
        cur.execute(
            "UPDATE `users` SET `status` = ? WHERE userid = ?", (value, user_id)
        )
        con.commit()
    finally:
        lock.release()


def add_promo(name, item, duration):
    try:
        lock.acquire(True)
        cur.execute("INSERT INTO `promocodes` VALUES (?, ?, ?)", (name, item, duration))
        con.commit()
    finally:
        lock.release()


def reset_slots():
    cur.execute("UPDATE `users` SET `slots` = 0")
    con.commit()
