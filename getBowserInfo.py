import os,sys
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import  datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import browser_cookie3
import requests

#初始化地址
if 'win' in sys.platform:
    BookmarksPath = os.path.expandvars('%LOCALAPPDATA%/Google/Chrome/User Data/Default/Bookmarks') # 存在保存的书签
    localStatePath = os.path.expandvars('%LOCALAPPDATA%/Google/Chrome/User Data/Local State')# 存在AES加密密钥
    loginDataPath = os.path.expandvars('%LOCALAPPDATA%/Google/Chrome/User Data/Default/Login Data')# 存在保存的页面账号密码
    cookiesPath= os.path.expandvars('%LOCALAPPDATA%/Google/Chrome/User Data/Default/Cookies')# 存在cookie
elif 'linux' in sys.platform:
    BookmarksPath = os.path.expanduser('~/.config/google-chrome/Default/Bookmarks')
    localStatePath = os.path.expanduser('~/.config/google-chrome/Local State')
    loginDataPath = os.path.expanduser('~/.config/chromium/Default/Login Data')
    cookiesPath = os.path.expanduser('~/.config/chromium/Default/Cookies')
else:#Mac
    BookmarksPath = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Bookmarks')
    localStatePath = os.path.expanduser('~/Library/Application Support/Google/Chrome/Local State')
    loginDataPath = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Login Data')
    cookiesPath = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies')


def getChromeTime(chromedate):  # 转换时间
    try:
        return str(datetime(1601, 1, 1) + timedelta(microseconds=chromedate))
    except:
        return ''

def getEncKey():    # 获取加密AESkey
    with open(localStatePath, "r", encoding="utf-8") as f:
        localStateTest = f.read()
        localState = json.loads(localStateTest)
    key = base64.b64decode(localState["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

#Chrome专属,可删除使用公用方法
def getDecCookie(encCookie):    # 获取解密后的Cookie
    if sys.platform == 'win32':
        try:
            if encCookie[:4] == b'x01x00x00x00':
                decCookie = dpapiDecrypt(encCookie)
                return decCookie.decode()
            elif encCookie[:3] == b'v10':
                decCookie = aesDecrypt(encCookie)
                return decCookie[:-16].decode()
        except WindowsError:
            return None
    else:
        raise WindowsError

#Chrome专属,可删除使用公用方法
def dpapiDecrypt(encCookie):   # 使用DPAPI解密
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encCookie, len(encCookie))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

#Chrome专属,可删除使用公用方法    
def aesDecrypt(encCookie):  # 使用AESkay解密
    key = getEncKey()
    nonce = encCookie[3:15]
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(encCookie[15:])

def decPassword(password, key): # 解密密码
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def getPassword():  # 获取密码
    key = getEncKey()
    filename = "chromeLoginData.db"
    # 创建新chrome数据库文件，防止正在运行导致数据库锁定
    shutil.copyfile(loginDataPath, filename)
    db = sqlite3.connect(filename)
    db.text_factory = str
    cursor = db.cursor()
    cursor.execute("select origin_url, username_value, password_value, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        password = decPassword(row[2], key)
        dateLastUsed = row[3]        
        if username or password:
            print("\nURL: "+url)
            print("Username: "+username)
            print("Password: "+password)
            print("Last Used: "+getChromeTime(dateLastUsed))
        else:
            continue
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

def formatCookiejar(cookiejar):  # 格式化cookiejar对象并打印
    cookieList = str(cookiejar)[12:-3].split(">, <")
    newCookieList=[]
    for i in range(len(cookieList)):
        temData=[]
        temData.append(cookieList[i].split(" for ")[1])
        temData.append(cookieList[i].split("Cookie ")[1].split("=")[0])
        temData.append(cookieList[i].split("=")[1].split(" for ")[0])
        newCookieList.append(temData)
    [print('\nHost: %s\nName: %s\nCookie: %s'%(newCookieData[0],newCookieData[1],newCookieData[2])) for newCookieData in newCookieList]

def getCookie():    # 获取cookie
    try:
        chromeCookie = browser_cookie3.chrome()
        print('\n\n-------------Chrome浏览器Cookie如下:-------------')
        getChromeCookie()
    except:
        try:
            formatCookiejar(chromeCookie)
        except:
            chromeCookie = []
            print('\n未检测到Chrome浏览器')
    sys.exit()
    try:
        firefoxCookie = browser_cookie3.firefox()
        print('\n\n-------------Firefox浏览器Cookie如下:-------------')
        formatCookiejar(firefoxCookie)
    except:
        firefoxCookie = []
        print('\n未检测到Firefox浏览器')
    try:
        operaCookie =  browser_cookie3.opera()
        print('\n\n-------------Opera浏览器Cookie如下:-------------')
        formatCookiejar(operaCookie)
    except:
        operaCookie = []
        print('\n未检测到Opera浏览器')
    try:
        edgeCookie =  browser_cookie3.edge()
        print('\n\n-------------Edge浏览器Cookie如下:-------------')
        formatCookiejar(edgeCookie)
    except:
        edgeCookie = []
        print('\n未检测到Edge浏览器')
    try:
        chromiumCookie =  browser_cookie3.chromium()
        print('\n\n-------------Chromium浏览器Cookie如下:-------------')
        formatCookiejar(chromiumCookie)
    except:
        chromiumCookie = []
        print('\n未检测到Chromium浏览器')

#Chrome专属,可删除使用公用方法
def getChromeCookie():    # 获取cookie
    filename = "chromeCookieData.db"
    shutil.copyfile(cookiesPath, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select host_key,path,name,encrypted_value,expires_utc from cookies")#需新版sqlite3，否则会报错encrypted_value无法转utf-8
    for row in cursor.fetchall():
        try:
            host = row[0]
            path = row[1]
            name = row[2]
            encrypted_value = row[3]
            expires_utc =getChromeTime(row[4])
            if  encrypted_value:
                print("\nHost: "+host)
                print("Path: "+path)
                print("Name: "+name)
                try:
                    print("Cookie: "+win32crypt.CryptUnprotectData(encrypted_value)[1].decode()) # Chrome80.X版本前解密方式
                except Exception as e:
                    print("Cookie: "+getDecCookie(encrypted_value)) # Chrome80.X版本后解密方式
                print("Expires: "+expires_utc)
        except:
            continue
    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

def forBookmarks(itemData): # 循环书签数据
    for item in itemData:
        type = item['type']
        name = item['name']
        if type == 'url':
            print('\nTitle: ',name, '\nUrl: ',item['url'])
        else:   # 文件夹
            forBookmarks(item['children'])


def getBookmarks(): # 获取书签
    with open(BookmarksPath, 'r',encoding = "utf-8") as f:
        itemData=json.loads(f.read())['roots']['bookmark_bar']['children']
    forBookmarks(itemData)
    

def main():#可根据需要把打印数据存xml文档
    print('\n-------------Chrome浏览器书签如下:-------------')
    getBookmarks()
    print('\n\n-------------Chrome浏览器密码如下:-------------')
    getPassword()
    print('\n\n-------------各浏览器Cookie如下:-------------')
    getCookie()
    
if __name__ == "__main__":
    main()