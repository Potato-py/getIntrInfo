# -*- coding: UTF-8 -*-
import os
import sys 

cmdList={
    "office数据库文件":'dir /a /s /b "*.mdb"',
    "sql文件":'dir /a /s /b "*.sql"',
    "虚拟光盘文件":'dir /a /s /b "*.mdf"',
    "outlook电子邮件文件":'dir /a /s /b "*.eml"',
    "outlook数据库文件":'dir /a /s /b "*.pst"',
    "配置文件":'dir /a /s /b "*conf*"',
    "备份文件":'dir /a /s /b "*bak*"',
    "密码文件":'dir /a /s /b "*pwd*"',
    "密码文件":'dir /a /s /b "*pass*"',
    #"登录文件":'dir /a /s /b "*login*"',
    #"用户文件":'dir /a /s /b "*user*"',
    "QQ文件"：'dir /a /s /b "Documents/Tencent Files/"|findstr "FileRecv.*\."',
    "微信文件"：'dir /a /s /b "Documents/WeChat Files/"|findstr "FileStorage.*\."',
    "钉钉文件"：'dir /a /s /b "Downloads"',
}
choseList={}
    
def main():#可根据需要把打印数据存xml文档
    #可添加选择性执行，对应数据丢入choseList再执行
    #以下默认全部执行
    #第一次运行比较慢，正常
    for key,value in cmdList.items():
        print('\n\n-------------%s-------------'%key)
        message = os.popen(value).read()
        print(message)
    #可以添加选择性读取某文件---我有。懒
    
if __name__ == "__main__":
    main()