import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs

ua = UserAgent().random


phone = "79069246025"


session = requests.session()
req = session.post(
    "https://avtoset.su/",
    headers={
        "User-Agent": ua,
    },
)

cookies = req.cookies.get_dict()


# soup = bs(req.text, "lxml")

# xsrf = soup.find("input", {"name": "CSRFToken"})["value"]
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
    data={"type": "sendCode", "phone": phone[1:], "g-recaptcha-response": "empty"},
)
print(req.text)
