# -*- coding: UTF-8 -*-
import os,sys
import csv

cmdList={
    "QQ文件":'dir /a /s /b "C:/Users/Administrator/Documents/Tencent Files/"|findstr "FileRecv.*\."',
    "微信文件":'dir /a /s /b "C:/Users/Administrator/Documents/WeChat Files/"|findstr "FileStorage.*\."',
    "下载文件":'dir /a /s /b "C:/Users/Administrator/Downloads"',
    "office数据库文件":'c: & dir /a /s /b "*.mdb" & d: & dir /a /s /b "*.mdb" & e: & dir /a /s /b "*.mdb"',
    "sql文件":'c: & dir /a /s /b "*.sql" & d: & dir /a /s /b "*.sql" & e: & dir /a /s /b "*.sql"',
    "虚拟光盘文件":'c: & dir /a /s /b "*.mdf" & d: & dir /a /s /b "*.mdf" & e: & dir /a /s /b "*.mdf"',
    "outlook电子邮件文件":'c: & dir /a /s /b "*.eml"',
    "outlook数据库文件":'c: & dir /a /s /b "*.pst"',
    "配置文件":'c: & dir /a /s /b "*.conf*" & d: & dir /a /s /b "*.conf*" & e: & dir /a /s /b "*.conf*"',
    "备份文件":'c: & dir /a /s /b "*bak*" & d: & dir /a /s /b "*bak*" & e: & dir /a /s /b "*bak*"',
    "密码文件":'c: & dir /a /s /b "*pwd*" & d: & dir /a /s /b "*pwd*" & e: & dir /a /s /b "*pwd*"',
    "密码文件":'c: & dir /a /s /b "*pass*" & d: & dir /a /s /b "*pass*" & e: & dir /a /s /b "*pass*"',
    #"登录文件":'c: & dir /a /s /b "*login*" & d: & dir /a /s /b "*login*" & e: & dir /a /s /b "*login*"',
    #"用户文件":'c: & dir /a /s /b "*user*" & d: & dir /a /s /b "*user*" & e: & dir /a /s /b "*user*"',
}
choseList={}
    
def main():
    #可添加选择性执行，对应数据丢入choseList再执行
    #以下默认全部执行
    #第一次运行比较慢，正常
    id=0
    for key,value in cmdList.items():
        id = id + 1
        print('\n\n-------------%s-------------'%key)
        message = os.popen(value).read()
        print(message)
        csv_writer.writerow([ id, key, message])
    #可以添加选择性读取某文件---我有。懒

if __name__ == "__main__":
    filename='./Result/sensitiveFile.csv'
    with open(filename, 'w', encoding='utf-8', newline='') as q:
        csv_writer = csv.writer(q)
        csv_writer.writerow([ 'ID','类型', '路径'])
        main()