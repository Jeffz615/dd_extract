import requests
import math
import json


def getStat(vmid):
    burp0_url = f"https://api.bilibili.com/x/relation/stat?vmid={vmid}&jsonp=jsonp"
    burp0_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Accept": "*/*", "Sec-Fetch-Site": "same-site",
                     "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "script", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    response = requests.get(burp0_url, headers=burp0_headers)
    print(response.json())
    return response.json()


def getFollowings(vmid, count):
    l = []
    burp0_headers = {"Connection": "close", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Accept": "*/*", "Sec-Fetch-Site": "same-site",
                     "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "script", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    for i in range(1, min(math.ceil(count/50)+1, 6)):
        burp0_url = f"https://api.bilibili.com:443/x/relation/followings?vmid={vmid}&pn={i}&ps=50&order=desc&jsonp=jsonp"
        response = requests.get(burp0_url, headers=burp0_headers)
        l += response.json().get('data').get('list')
    for i in range(1, min(math.ceil((count-250)/50)+1, 6)):
        burp0_url = f"https://api.bilibili.com:443/x/relation/followings?vmid={vmid}&pn={i}&ps=50&order=asc&jsonp=jsonp"
        response = requests.get(burp0_url, headers=burp0_headers)
        l += response.json().get('data').get('list')
    return l


def getInfo(mid):
    burp0_url = f"https://api.bilibili.com:443/x/space/acc/info?mid={mid}&jsonp=jsonp"
    burp0_headers = {"Connection": "close", "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68", "DNT": "1", "Origin": "https://space.bilibili.com",
                     "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://space.bilibili.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"}
    response = requests.get(burp0_url, headers=burp0_headers)
    print(response.json())
    return response.json()


def getVtbs():
    url = "https://api.vtbs.moe/v1/short"
    response = requests.get(url)
    # print(response.json())
    return response.json()


if __name__ == "__main__":
    vmid = int(input("[+] 请输入您的uid："))
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
