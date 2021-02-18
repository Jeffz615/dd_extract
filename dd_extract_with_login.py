import math
import requests
from urllib import parse
import time
import os
from http.cookiejar import MozillaCookieJar
from PIL import Image


class bilibiliQRLogin():
    def __init__(self):
        self.uid = 0
        self.login_session = ''
        self.global_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        self.qr_login_url = 'http://passport.bilibili.com/qrcode/getLoginUrl'
        self.qr_login_info_url = 'http://passport.bilibili.com/qrcode/getLoginInfo'
        self.user_info_url = 'https://api.bilibili.com/x/space/myinfo'
        self.times = 3  # 超时时间 times*10 秒
        self.cookie_path = './cookie.txt'
        self.qr_path = './qr.png'
        self.load_cookie_from_local()
        if not self.check_expire():
            self.get_login_session()

    def qr_scan(self):
        h = requests.get(self.qr_login_url)

        json_data = h.json()

        oauthKey = json_data['data']['oauthKey']
        qr_image_url = json_data['data']['url']

        self.save_qr_img(qr_image_url)

        return oauthKey

    def save_qr_img(self, qr_image_url):
        try:
            import qrcode
            qr_image = qrcode.make(qr_image_url)
            qr_image.save('qr.png')
            return
        except ImportError:
            print("本地没有qrcode库,采用api生成二维码")

        try:
            qr_image = requests.get(
                'http://qr.topscan.com/api.php?text='+qr_image_url).content
            with open('qr.png', 'wb') as f:
                f.write(qr_image)
        except:
            print("网站api失效，无法生成二维码")
            raise Exception("网站api失效，无法生成二维码")

    def get_qr_scan_status(self, oauthKey):
        data = {
            'oauthKey': oauthKey
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        session = requests.Session()
        session.cookies = MozillaCookieJar(self.cookie_path)
        h = session.post(self.qr_login_info_url, headers=headers, data=data)
        status = h.json()['status']
        if status:
            return status, session
        else:
            return status, None

    def check_expire(self):
        if not self.login_session:
            return False
        h = self.login_session.get(
            self.user_info_url, headers=self.global_headers)
        j = h.json()
        if j['code'] == 0:
            self.uid = j['data']['mid']
            return self.uid
        return False

    def get_login_session(self):
        if self.login_session and self.check_expire():
            return self.login_session
        oauthKey = self.qr_scan()
        print("请扫描二维码")
        img = Image.open(self.qr_path)
        img.show()
        for i in range(self.times):
            time.sleep(10)
            status, session = self.get_qr_scan_status(oauthKey)
            if not status:
                print("等待二维码扫描")
            else:
                print("登录成功")
                self.login_session = session
                self.save_cookie_to_local()
                return session
            if i == self.times - 1:
                print('未扫码超时')
                raise TimeoutError("登录超时")
        return None

    def save_cookie_to_local(self):
        self.login_session.cookies.save(
            ignore_discard=True, ignore_expires=True)

    def load_cookie_from_local(self):
        if os.path.exists(self.cookie_path):
            s = MozillaCookieJar(self.cookie_path)
            s.load(self.cookie_path, ignore_discard=True, ignore_expires=True)
            session = requests.Session()
            session.cookies = s
            self.login_session = session
        else:
            pass


def getStat(vmid):
    burp0_url = f"https://api.bilibili.com/x/relation/stat?vmid={vmid}&jsonp=jsonp"
    burp0_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Accept": "*/*", "Sec-Fetch-Site": "same-site",
                     "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "script", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    response = session.get(burp0_url, headers=burp0_headers)
    print(response.json())
    return response.json()


def getFollowings(vmid, count):
    l = []
    burp0_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Accept": "*/*", "Sec-Fetch-Site": "same-site",
                     "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "script", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    for i in range(1, math.ceil(count/50)+1):
        burp0_url = f"https://api.bilibili.com:443/x/relation/followings?vmid={vmid}&pn={i}&ps=50&order=desc&jsonp=jsonp"
        response = session.get(burp0_url, headers=burp0_headers)
        l += response.json().get('data').get('list')
    return l


def getInfo(mid):
    burp0_url = f"https://api.bilibili.com:443/x/space/acc/info?mid={mid}&jsonp=jsonp"
    burp0_headers = {"Connection": "close", "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Origin": "https://space.bilibili.com",
                     "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    response = session.get(burp0_url, headers=burp0_headers)
    print(response.json())
    return response.json()


def getVtbs():
    url = "https://api.vtbs.moe/v1/short"
    response = session.get(url)
    # print(response.json())
    return response.json()


if __name__ == "__main__":
    lg = bilibiliQRLogin()
    session = lg.get_login_session()
    vmid = lg.uid
    stat = getStat(vmid)
    following = stat.get('data').get('following')
    print(f"[+] 已关注人数：{following}")
    print('[+] 关注列表提取中...')
    followList = getFollowings(vmid, following)
    mids = set()
    for user in followList:
        mids.add(user.get("mid"))
    print(mids)
    print(f"[+] 已获取最新关注的 {len(mids)} 个up主")
    print("[+] 正在从vtbs.moe获取vtbs列表...")
    vtbs = getVtbs()
    dd = []
    print("[+] 检测并输出dd列表...")
    for user in vtbs:
        if user.get("mid") in mids:
            uname = user.get('uname')
            roomid = user.get('roomid')
            print(f"{uname} : {roomid}")
            if roomid:
                dd.append(str(roomid))
    print("=============================================")
    print(" ".join(dd))
    os.system('pause')