# -*- coding: UTF-8 -*-
import os
import importlib,sys 
importlib.reload(sys)
 
 
# 获取电脑连接过的所有wifi名称和密码
def checkWIFI():
    list = []
    # 获取所有的wifi名称
    message = os.popen('netsh wlan show profiles').readlines()
    for i in message:
        result = i.strip().encode().decode("utf-8")

        if result.find(u"所有用户配置文件 : ") != -1:
            command = 'netsh wlan show profiles name="' + result[11:] + '" key=clear'
            print(command)
            try:
                per_wifi = os.popen(command).readlines()
            except:
                per_wifi = []
            
            for j in per_wifi:
                passwd = j.strip().encode().decode("utf-8")
 
                if passwd.find(u"关键内容            :") != -1:# 密码字符串不为空时
                    if passwd[18:] != '':
                        list_temp = []
                        list_temp.append(result[11:])
                        list_temp.append(passwd[18:])
                        list.append(list_temp)
    return list

list = checkWIFI()
print("返回结果如下：")
i = 0
for j in list:
    i = i + 1
    print(str(i) + "、wifi名称：" + j[0] + "，密码：" + j[1])