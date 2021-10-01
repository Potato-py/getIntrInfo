# -*- coding: UTF-8 -*-
import os
import sys 

cmdList={
    #主机类
    "当前用户":"whoami /all",
    "网络信息":"ipconfig /all",
    "计算机版本/补丁编号":"systeminfo",
    "进程列表":"tasklist",
    "补丁信息":"wmic qfe",
    "系统信息":"wmic os",
    "机器运行信息":"net statistics workstation",
    "系统架构":"set process",
    "防火墙配置":"netsh firewall show config",
    "日志修改权限":"wmic nteventlog get path,filename,writeable",
    "当前在线用户":"quser",
    "本地用户":"net user",
    "本机管理员":"net localgroup administrators",
    "已安装软件信息":"wmic product get name,version",
    #杀软类
    "杀软信息":r"WMIC /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName,productState,pathToSignedProductExe",
    #网络类
    "端口信息":"netstat -ano",
    "路由信息":"route print",
    "arp信息":"arp -a",
    "host信息":"type c:\Windows\system32\drivers\etc\hosts",
    "wifi密码":"netsh wlan show profile",
    #计划任务类
    "计划任务":"schtasks",
    #服务类
    "自启服务":"wmic startup get command, caption",
    "已启服务":"net start",
    "本机服务":"wmic service list brief",
    #DNS服务
    "DNS服务器":"nslookup",
    "DNS缓存":"ipconfig /displaydns",
    "DNS服务器":"nslookup",
    #域信息
    "当前域信息":"net config workstation",
    "当前连接":"net use",
    "当前映射":"net share",
    "域环境":"net view",
    "定位域控":"net time",
    "定位域控":"net group \"domain controllers\" /domain",
    "域用户":"net user /domain",
    "域用户详情":"wmic useraccount get /all ",
    "域用户密码策略":"net accounts /domain",
    "本地用户组信息":"net localgroup",
    "域用户组信息":"net group /domain",
    "域用户组成员":"net \"Domain users\" /domain",
    "域管理员用户组成员":"net group \"Domain Admins\" /domain",
    "域管理员用户组成员":"net group \"Enterprise Admins\" /domain",
    "域信任信息":"nltest /domain_trusts",
}
choseList={}
    
def main():#可根据需要把打印数据存xml文档
    #可添加选择性执行，对应数据丢入choseList再执行
    #以下默认全部执行
    for key,value in cmdList.items():
        print('\n\n-------------%s-------------'%key)
        message = os.popen(value).read()
        print(message)
    
if __name__ == "__main__":
    main()