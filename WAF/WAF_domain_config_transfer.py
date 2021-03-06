#!/usr/bin/env python
#coding=utf-8
import json
import os
import csv
import getopt
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkwaf_openapi.request.v20190910.DescribeInstanceInfoRequest import DescribeInstanceInfoRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeDomainNamesRequest import DescribeDomainNamesRequest
from aliyunsdkwaf_openapi.request.v20190910.DescribeProtectionModuleStatusRequest import DescribeProtectionModuleStatusRequest
from aliyunsdkwaf_openapi.request.v20190910.ModifyProtectionModuleStatusRequest import ModifyProtectionModuleStatusRequest
#accessKeyId = os.environ['ACCESS_KEY_ID']#LTAI5t5fiybLUnwRe3KH8fBb
#accessSecret = os.environ['ACCESS_KEY_SECRET']#hBgT2KZWVG8suWH3YWNGrMAfx0VZOM


#获取ak

class WAF:
    def __init__(self):
        self.DefenseTypes = ['waf',
                            'dld',
                            'tamperproof',
                            'dlp',
                            'normalized',
                            'bot_crawler',
                            'bot_intelligence',
                            'antifraud',
                            'bot_algorithm',
                            'bot_wxbb',
                            'bot_wxbb_pkg',
                            'ac_cc',
                            'ac_blacklist',
                            'ac_highfreq',
                            'ac_dirscan',
                            'ac_scantools',
                            'ac_collaborative',
                            'ac_custom']
        
        #self.accessKeyId = 'TMP.3Khh9YKAkZqAcudLCtLHvVdbqHXs5AYjRHYMKWtrEqBJf8UmvooWD2jszupybVAeMNqShu3bHyKcVHxEcWaUWjVepWs23q'
        #self.accessSecret = 'GzNrEWuHGkMXEzoBY5bXFa2gLURSjw7nxfvrUWsEgwyC'
        self.accessKeyId = os.environ['ACCESS_KEY_ID']
        self.accessSecret = os.environ['ACCESS_KEY_SECRET']
        self.region = 'cn-shenzhen'
        self.WAF_InstanceId = self.get_WAF_InstanceId()
        self.WAF_Domains = self.get_WAF_domain()
        self.config = self.exmple_modle_config()
        self.old_config = None
    def get_WAF_InstanceId(self):
        client = AcsClient(self.accessKeyId,\
                           self.accessSecret, self.region)
        
        request = DescribeInstanceInfoRequest()
        request.set_accept_format('json')
        
        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        #print(str(response, encoding='utf-8'))
        tmp_json = json.loads(str(response, encoding = 'utf-8'))
        return tmp_json['InstanceInfo']['InstanceId']
    def get_WAF_domain(self):
        client = AcsClient(self.accessKeyId,\
                           self.accessSecret, self.region)
        request = DescribeDomainNamesRequest()
        request.set_accept_format('json')
        
        request.set_InstanceId(self.WAF_InstanceId)
        
        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        tmp_json = json.loads(str(response, encoding = 'utf-8'))
        return tmp_json['DomainNames']
    def WAF_ProtectionModuleStatus(self,Domain,DefenseType):
        client = AcsClient(self.accessKeyId,\
                           self.accessSecret, self.region)
        request = DescribeProtectionModuleStatusRequest()
        request.set_accept_format('json')
        
        request.set_Domain(Domain)
        request.set_DefenseType(DefenseType)
        request.set_InstanceId(self.WAF_InstanceId)
        
        response = client.do_action_with_exception(request)
        # python2:  print(response) 
        tmp_json = json.loads(str(response, encoding = 'utf-8'))
        return tmp_json['ModuleStatus']
    def out_all_domains_status(self):
        execl_list = []
        for i in range(len(self.WAF_Domains)):
            tmp = []
            tmp.append(self.WAF_Domains[i])
            for j in range(len(self.DefenseTypes)):
                tmp.append(self.WAF_ProtectionModuleStatus(self.WAF_Domains[i],self.DefenseTypes[j]))
            print(str(i)+':'+self.WAF_Domains[i])
            execl_list.append(tmp)
        print("开始写入数据")
        tmp_a = ['domain']
        tmp_a.extend(self.DefenseTypes)
        
        with open("out-status.csv",'w',newline='') as t:#numline是来控制空的行数的
            writer=csv.writer(t)#这一步是创建一个csv的写入器（个人理解）
            writer.writerow(tmp_a)#写入标签
            writer.writerows(execl_list)#写入样本数据
        return execl_list
    def exmple_modle_config(self):
        tmp = []
        for j in range(len(self.DefenseTypes)):
            tmp.append(self.WAF_ProtectionModuleStatus('mall.amway.com.cn',self.DefenseTypes[j]))
        return tmp
    def set_status_modle(self,Domain,DefenseType,set_number):
        client = AcsClient(self.accessKeyId,\
                           self.accessSecret, self.region)
        request = ModifyProtectionModuleStatusRequest()
        request.set_accept_format('json')
        
        request.set_Domain(Domain)
        request.set_DefenseType(DefenseType)
        request.set_InstanceId(self.WAF_InstanceId)
        request.set_ModuleStatus(set_number)
        while True:
            try:
                response = client.do_action_with_exception(request)
                print("-",end="")
                break
            except:
                print("错误",end="")
                tmp_json = json.loads(str(response, encoding = 'utf-8'))
                print(tmp_json)
                
    def set_all_status(self,Domain):
        for i in range(len(self.DefenseTypes)):
            self.set_status_modle(Domain, self.DefenseTypes[i], self.config[i])
    def read_config_csv(self):
        old_config_list = []
        with open('out-status.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                old_config_list.append(list(row))
        self.old_config = old_config_list[1:]
        
    def reset_all_Domains_config(self):
        self.read_config_csv()
        Domains_list = txt2list(file = 'domains.txt')
        for Domain in Domains_list:#先确认domains.txt文件里面的域名
            for old in self.old_config:#先确认out-status.csv文件里面的域名
                
                if Domain in old:#如果domains.txt某一条域名和原先配置域名一直就执行配置还原
                    tmp_config = old[1:]
                    print("回退操作，域名为："+old[0])
                    for i in range(len(self.DefenseTypes)):
                        #print(self.DefenseTypes[i],end=':')
                        #print(tmp_config[i])
                        #pass
                        self.set_status_modle(Domain, self.DefenseTypes[i], int(tmp_config[i]))
                    print("回退操作成功")
                    
def txt2list(file = ''):
    with open(file, "r") as f:  # 打开文件
        data = f.read()  # 读取文件
    return data.split('\n')

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-hd:-sr', ['help','Domains_list=' ,'status=','reset='])
    #print(args)
    Domains_list = []
    for key, value in opts:
        if key in ['-h', '--help']:
            print('联系人：陈柳安')
            print('该脚本参考mall.amway.com.cn网站WAF配置，设置其他网站WAF')
            print('参数：')
            print('-h\t显示帮助')
            print('-d\t输入你的txt文件名，文件一行一个域名数量不限')
            print('-s\t执行输出所有域名的配置开关状态，并且输出到一个CSV文件上')
            print('-r\t根据-s 输出的文件out-status.csv文件来还原原来的配置')
            #print(opts)
            #print(key)
            sys.exit(0)
        if key in ['-d', '--Domains']:
            
            Domains_list = txt2list(file = value)
            #print(Domains_list)
            waf = WAF()
            print("开始执行")

            
            for Domain in Domains_list:
                if Domain == '':
                    continue
                waf.set_all_status(Domain)
                print(Domain+"----完成设置")
            sys.exit(0)
        if key in ['-s', '--status']:
            print("开始查询所有域名功能开关状态")
            waf = WAF()
            waf.out_all_domains_status()
            sys.exit(0)
        if key in ['-r', '--reset']:
            print("选择回退操作")
            waf = WAF()
            waf.reset_all_Domains_config()
            sys.exit(0)
    