#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
#from aliyunsdkvpc.request.v20160428.DescribeForwardTableEntriesRequest import DescribeForwardTableEntriesRequest
from aliyunsdkvpc.request.v20160428.DescribeSnatTableEntriesRequest import DescribeSnatTableEntriesRequest
from aliyunsdkvpc.request.v20160428.DescribeVSwitchAttributesRequest import DescribeVSwitchAttributesRequest
from aliyunsdkvpc.request.v20160428.DescribeRouteTablesRequest import DescribeRouteTablesRequest
from aliyunsdkvpc.request.v20160428.DeleteSnatEntryRequest import DeleteSnatEntryRequest
from aliyunsdkvpc.request.v20160428.DeleteRouteEntryRequest import DeleteRouteEntryRequest
from aliyunsdkvpc.request.v20160428.CreateSnatEntryRequest import CreateSnatEntryRequest

import json
import time
import getopt
import sys
import os


class Get_Nat_Config:
    new_nat_config = None 
    save_RouteTableId = None
    save_RouteEntryName = None
    def __init__(self,NatGatewayId = '',RegionId = '' , accessKeyId = '' ,accessSecret = '', domain = ''):
        self.__RegionId = RegionId
        self.__accessKeyId = accessKeyId
        self.__accessSecret = accessSecret
        self.__domain = domain
        self.NatGatewayId = NatGatewayId

        self.nat_config = self.DescribeNatGateway(self.NatGatewayId)
        self.save('_nat_config',self.nat_config)
        '''
        self.dnat_config = self.DescribeForwardTableEntries()
        self.save('_dnat_config',self.dnat_config)
        '''
        
        
        
        self.vswitch_config = self.DescribeVSwitchAttributes(self.nat_config['PrivateInfo']['VswitchId'])
        self.save('_vswitch_config', self.vswitch_config)
        
        
        self.snat_config = self.DescribeSnatTableEntries(self.nat_config['SnatTable']['SnatTableId'])
        self.save('_snat_config',self.snat_config)
        
        self.routetable_config = self.DescribeRouteTables(self.vswitch_config['RouteTable']['RouteTableId'])
        self.save('_routetable_config',self.routetable_config)
        
        
        #??????????????????
        #======================================================================#
        
    def save(self,name,data):
        with open(self.nat_config['NatGatewayId'] + name + '.json', 'w') as f:
            json.dump(data, f)
            
            
    def DescribeNatGateway(self,NatGatewayId):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(self.__domain)
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2016-04-28')
        request.set_action_name('GetNatGatewayAttribute')
        #======================================================================#
        request.add_query_param('RegionId', self.__RegionId)
        request.add_query_param('NatGatewayId',NatGatewayId)
        #======================================================================#
        response = client.do_action(request)
        return json.loads(str(response, encoding = 'utf-8'))
    
    '''
    def DescribeForwardTableEntries(self):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DescribeForwardTableEntriesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        #======================================================================#
        request.set_ForwardTableId(self.nat_config['ForwardTable']['ForwardTableId'])
        #======================================================================#
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding = 'utf-8'))
    '''
    def DescribeVSwitchAttributes(self,VswitchId):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DescribeVSwitchAttributesRequest()
        request.set_accept_format('json')
        #======================================================================#
        request.set_VSwitchId(VswitchId)
        #======================================================================#
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding = 'utf-8'))
    
    
    def DescribeSnatTableEntries(self,SnatTableId):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DescribeSnatTableEntriesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        #======================================================================#
        request.set_SnatTableId(SnatTableId)
        #======================================================================#
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding = 'utf-8'))       

    
    def DescribeRouteTables(self,RouteTableId):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DescribeRouteTablesRequest()
        request.set_accept_format('json')
        request.set_PageSize(50)
        #======================================================================#
        request.set_RouteTableId(RouteTableId)
        #======================================================================#
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding = 'utf-8')) 
        

 


    def DeleteSnatEntry(self,SnatTableId,SnatEntryId):#??????SNAT??????
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DeleteSnatEntryRequest()
        request.set_accept_format('json')
        #======================================================================#
        request.set_SnatTableId(SnatTableId)
        request.set_SnatEntryId(SnatEntryId)
        #======================================================================#
        response = client.do_action_with_exception(request)
        print(str(response, encoding = 'utf-8'))     
            
    
    def UnassociateEipAddress(self,AllocationId):#EIP??????NAT??????
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(self.__domain)
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2016-04-28')
        request.set_action_name('UnassociateEipAddress')
        #======================================================================#
        request.add_query_param('AllocationId', AllocationId)
        #======================================================================#
        response = client.do_action(request)
        print(str(response, encoding = 'utf-8'))  
        
    
    def DeleteRouteEntry(self,RouteEntryId,NextHopId):#??????????????????
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = DeleteRouteEntryRequest()
        request.set_accept_format('json')
        #======================================================================#
        request.set_RouteEntryId(RouteEntryId)
        request.set_NextHopId(NextHopId)#????????????
        #======================================================================#
        response = client.do_action_with_exception(request)
        print(str(response, encoding = 'utf-8'))    
    
    
    def Delete_All_Snat(self):#????????????SNAT??????
        print('??????????????????SNAT??????')
        for i in range(self.snat_config['TotalCount']):
            SnatTableId = self.snat_config['SnatTableEntries']['SnatTableEntry'][i]['SnatTableId']
            SnatEntryId = self.snat_config['SnatTableEntries']['SnatTableEntry'][i]['SnatEntryId']
            print(i)
            self.DeleteSnatEntry(SnatTableId,SnatEntryId)
            
    def Delete_All_NatEip(self):#????????????NAT???????????????EIP
        print('??????????????????NAT???????????????EIP')
        while True:
            now_snat_config = self.DescribeSnatTableEntries(self.nat_config['SnatTable']['SnatTableId'])
            if now_snat_config['TotalCount']==0:
                for i in range(len(self.nat_config['IpList'])):
                    AllocationId = self.nat_config['IpList'][i]['AllocationId']
                    print(i)
                    self.UnassociateEipAddress(AllocationId)
                break
            else:
                print('????????????SNAT??????')
                time.sleep(0.5)
                continue
            
    def Delete_ALL_Route_Entry(self):#?????????????????????
        print("????????????NAT?????????????????????")
        for i in range(len(self.routetable_config['RouteTables']['RouteTable'])):
            if self.routetable_config['RouteTables']['RouteTable'][i]['RouteTableId'] \
            ==self.vswitch_config['RouteTable']['RouteTableId']:
                    print("????????????????????????")
                    RouteEntrys_list = self.routetable_config['RouteTables']\
                                            ['RouteTable']\
                                            [i]\
                                            ['RouteEntrys']\
                                            ['RouteEntry']
                    for j in range(len(RouteEntrys_list)):
                        if RouteEntrys_list[j]['InstanceId'] == self.nat_config['NatGatewayId']:
                            print('?????????????????????,??????????????????')
                            RouteEntryId = RouteEntrys_list[j]['RouteEntryId']
                            NextHopId = RouteEntrys_list[j]['InstanceId']
                            print('??????RouteTableId')
                            self.save_RouteTableId = RouteEntrys_list[j]['RouteTableId']
                            print(self.save_RouteTableId )
                            
                            print('??????RouteEntryName')
                            self.save_RouteEntryName = RouteEntrys_list[j]['RouteEntryName']
                            print(self.save_RouteEntryName )
                            
                            self.DeleteRouteEntry(RouteEntryId,NextHopId)
                            

    def Create_New_NatGateway(self):
        client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain(self.__domain)
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2016-04-28')
        request.set_action_name('CreateNatGateway')
        #======================================================================#
        request.add_query_param('RegionId', self.__RegionId)
        request.add_query_param('VpcId', self.nat_config['VpcId'])
        try:
            request.add_query_param('Name', self.nat_config['Name'])
        except:
            request.add_query_param('Name', '')
        request.add_query_param('VSwitchId', self.nat_config['PrivateInfo']['VswitchId'])
        request.add_query_param('NatType', self.nat_config['NatType'])#nat??????
        request.add_query_param('InstanceChargeType', "PostPaid")#???????????????
        request.add_query_param('InternetChargeType', "PayByLcu")#???????????????
        #======================================================================#
        response = client.do_action(request)
        out_json = json.loads(str(response, encoding = 'utf-8'))
        if 'Message' in out_json:
            print(out_json['Code'])
            print(out_json['Message'])
            print(out_json['Recommend'])
            print('??????NAT????????????')
            sys.exit(0)
        else:
            while True:
                now_nat_Status = self.DescribeNatGateway(out_json['NatGatewayId'])
                if now_nat_Status['Status'] == 'Available':
                    self.new_nat_config = self.DescribeNatGateway(out_json['NatGatewayId'])
                    break
                time.sleep(1)
                print('.',end=" ")
            print('????????????')
        return json.loads(str(response, encoding = 'utf-8'))
    
    
    def AssociateEipAddress(self,AllocationId ,InstanceId):#NAT????????????EIP
        while True:
            client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
    
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain(self.__domain)
            request.set_method('POST')
            request.set_protocol_type('https') # https | http
            request.set_version('2016-04-28')
            request.set_action_name('AssociateEipAddress')
            #======================================================================#
            request.add_query_param('AllocationId', AllocationId)
            request.add_query_param('InstanceId', InstanceId)
            request.add_query_param('InstanceType', "Nat")
            #======================================================================#
            response = client.do_action(request)
            
            tmp_json = json.loads(str(response, encoding = 'utf-8'))
            if 'Message' in tmp_json:
                print('??????EIP?????????????????????')
                time.sleep(0.9)
            else:
                break
        print(str(response, encoding = 'utf-8'))
    def Nat_bind_All_Eip(self):#NAT??????????????????EIP
        print("??????????????????????????????EIP")
        for i in range(len(self.nat_config['IpList'])):
            self.AssociateEipAddress(self.nat_config['IpList'][i]['AllocationId'], self.new_nat_config['NatGatewayId'])
            print(i)
            
    def CreateSnatEntry(self,new_SnatTableId,VswitchId,SnatIp,SnatEntryName):#??????SNAT??????
        while True:
            try:
                client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
                request = CreateSnatEntryRequest()
                request.set_accept_format('json')
                #======================================================================#
                request.set_SnatTableId(new_SnatTableId)#???????????????NAT??????SNAT
                request.set_SourceVSwitchId(VswitchId)#
                request.set_SnatIp(SnatIp)
                request.set_SnatEntryName(SnatEntryName)
                #======================================================================#
                response = client.do_action_with_exception(request)
                # python2:  print(response) 
                print(str(response, encoding='utf-8'))
                break
            except:
                print('??????EIP?????????????????????????????????SNAT??????')
                time.sleep(0.7)
                pass
    def Create_All_Snat_Entry(self):
        for i in range(len(self.snat_config['SnatTableEntries']['SnatTableEntry'])):
            self.CreateSnatEntry(self.new_nat_config['SnatTable']['SnatTableId'],
                            self.snat_config['SnatTableEntries']['SnatTableEntry'][i]['SourceVSwitchId'],
                            self.snat_config['SnatTableEntries']['SnatTableEntry'][i]['SnatIp'],
                            self.snat_config['SnatTableEntries']['SnatTableEntry'][i]['SnatEntryName'])
    def Create_Route_ntry(self):
        while True:
            client = AcsClient(self.__accessKeyId,self.__accessSecret, self.__RegionId)
            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain(self.__domain)
            request.set_method('POST')
            request.set_protocol_type('https') # https | http
            request.set_version('2016-04-28')
            request.set_action_name('CreateRouteEntry')
            #======================================================================#
    
                
            #======================================================================#    
            request.add_query_param('RouteTableId', self.save_RouteTableId)
            
            request.add_query_param('DestinationCidrBlock', "0.0.0.0/0")
            request.add_query_param('NextHopType', "NatGateway")
            request.add_query_param('RouteEntryName', self.save_RouteEntryName)
            request.add_query_param('NextHopId', self.new_nat_config['NatGatewayId'])
            #======================================================================#
            response = client.do_action(request)
            # python2:  print(response) 
            tmp_json = json.loads(str(response, encoding = 'utf-8'))
            if 'Message' in tmp_json:
                    print('???????????????????????????????????????NAT????????????')
                    time.sleep(0.9)
            else:
                print(tmp_json)
                break
def run(NatGatewayId,RegionId,accessKeyId,accessSecret,domain):
    test = Get_Nat_Config(NatGatewayId = NatGatewayId,
    RegionId = RegionId,#????????????,
    accessKeyId = accessKeyId,#?????????accessKeyId
    accessSecret = accessSecret,#?????????accessSecret
    domain = domain)#?????? ???domain
    '''
test = Get_Nat_Config(NatGatewayId = 'ngw-8vbb0vnxhfnbxoxu16eds',
RegionId = 'cn-shenzhen',#????????????,
accessKeyId = 'LTAI4G9tYWicuudzGv3E3hFU',#?????????accessKeyId
accessSecret = 'Y3F1aDtXlV9G9OFMoqW2mNITRO0OYC',#?????????accessSecret
domain = 'vpc.cn-shenzhen.aliyuncs.com')#?????? ???domain
    '''
    test.Create_New_NatGateway()
    test.Delete_All_Snat()
    test.Delete_All_NatEip()
    test.Delete_ALL_Route_Entry()
    
    test.Nat_bind_All_Eip()
    test.Create_All_Snat_Entry()
    test.Create_Route_ntry()



if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], '-hn:-r:-k:-s:-d', ['help',\
                                                              'NatGatewayId=',\
                                                              'RegionId=',\
                                                              'accessKeyId=',\
                                                              'accessSecret=',\
                                                              'domain=' ])
    NatGatewayId = ''#ngw-8vbwuicn33yy84oniu82k
    RegionId = 'cn-shenzhen'#????????????cn-zhangjiakou
    accessKeyId = os.environ['ACCESS_KEY_ID']#LTAI5t5fiybLUnwRe3KH8fBb
    accessSecret = os.environ['ACCESS_KEY_SECRET']#hBgT2KZWVG8suWH3YWNGrMAfx0VZOM
    domain = 'vpc.aliyuncs.com'#?????????vpc??????vpc.cn-zhangjiakou.aliyuncs.com
    for key, value in opts:
        if key in ['-h', '--help']:
            print('?????????????????????')
            print('???????????????????????????NAT???????????????NAT????????????????????????NAT??????')
            print('?????????????????????SNAT???EIP???NAT????????????')
            print ('?????????')
            print ('-h\t????????????')
            print ('-n\t????????????NAT??????ID')
            print ('-r\t????????????')
            print('-k\t??????accessKeyID')
            print('-s\t??????accessSecret')
            print('-d\t???????????????VPC??????')
            
            sys.exit(0)
        if key in ['-n', '--NatGatewayId']:
            NatGatewayId = value
        if key in ['-r', '--RegionId']:
            RegionId = value
        if key in ['-k', '--accessKeyId']:
            accessKeyId = value
        if key in ['-s', '--accessSecret']:
            accessSecret = value    
        if key in ['-d', '--domain']:
            domain = args[0]
    print('===================================')
    print('??????????????????')
    print('===================================')
    print ('NatGatewayId???'+NatGatewayId, \
           '\n','RegionId???'+ RegionId, \
            '\n', 'accessKeyId???'+accessKeyId,\
              '\n', 'accessSecret???'+accessSecret,\
               '\n',  'domain???'+domain )
    print('===================================')
    print('?????????Y    ????????????')
    print('===================================')
    str_y = input("????????????")
    if str_y == 'Y' or str_y == 'y':
        print('STAR')
        run(NatGatewayId,RegionId,accessKeyId,accessSecret,domain)

'''
test = Get_Nat_Config(NatGatewayId = NatGatewayId,
RegionId = RegionId,#????????????,
accessKeyId = accessKeyId,#?????????accessKeyId
accessSecret = accessSecret,#?????????accessSecret
domain = domain)#?????? ???domain
'''

'''
test.Create_New_NatGateway()

test.Delete_All_Snat()
test.Delete_All_NatEip()
test.Delete_ALL_Route_Entry()

test.Nat_bind_All_Eip()
test.Create_All_Snat_Entry()
test.Create_Route_ntry
'''
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    
