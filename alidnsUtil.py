import json
import sys
import os
from datetime import datetime

#import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest, \
    AddDomainRecordRequest, DescribeDomainsRequest, DeleteDomainRecordRequest, SetDomainRecordStatusRequest

#pip install aliyun-python-sdk-core-v3
#pip install aliyun-python-sdk-domain
#pip install aliyun-python-sdk-alidns


ACCESS_KEY=os.environ['ACCESS_KEY']
SECRET_KEY=os.environ['SECRET_KEY']
client = AcsClient(ACCESS_KEY,SECRET_KEY,"cn-hangzhou");

#get domamin name list
def list_domain():
    DomainList = DescribeDomainsRequest.DescribeDomainsRequest()
    DomainList.set_accept_format('json')
    DNSListJson = json.loads(client.do_action_with_exception(DomainList))
    domainList=[]
    for i in DNSListJson['Domains']['Domain']:
        domainList.append(i['DomainName'])
        print(i['DomainName'])
    #print DNSListJson
    return domainList



#get record name list by domain name
def list_dns_record(DomainName):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    pageSize=100
    recordsAll=[]
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecords.set_PageSize(pageSize)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    #print(DomainRecordsJson['PageNumber'])
    #print(DomainRecordsJson['PageSize'])
    totalCounts=DomainRecordsJson['TotalCount']
    if(totalCounts % pageSize == 0):
        pageCounts=int(totalCounts / pageSize)
    else:
        pageCounts=int(totalCounts / pageSize) + 1

    print("get page counts:"+str(pageCounts))
    for count in range(pageCounts):
        print("\nget records from pagenumber: "+str(count+1)+" \n")
        DomainRecords.set_PageNumber(count+1)
        DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
        for x in DomainRecordsJson['DomainRecords']['Record']:
            recordsAll.append(x)
            RecordId = x['RecordId']
            RR = x['RR']
            Type = x['Type']
            Line = x['Line']
            Value = x['Value']
            TTL = x['TTL']
            Status = x['Status']
            txt =  RR+' '+Type+' '+Line+' '+Value+' '+str(TTL)+' '+Status
            print(txt)

    print("\nall records number: "+str(len(recordsAll)))
    return recordsAll

    #for item in recordsAll:
    #    RecordId = item['RecordId']
    #    RR = item['RR']
    #    Type = item['Type']
    #    Line = item['Line']
    #    Value = item['Value']
    #    TTL = item['TTL']
    #    Status = item['Status']
    #    txt =  RR+' '+Type+' '+Line+' '+Value+' '+str(TTL)+' '+Status
    #    print(txt)




#update record
def edit_dns_record(DomainName, hostname, hostname_new, Types, IP):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
            UpdateDomainRecord.set_accept_format('json')
            UpdateDomainRecord.set_RecordId(RecordId)
            UpdateDomainRecord.set_RR(hostname_new)
            UpdateDomainRecord.set_Type(Types)
            UpdateDomainRecord.set_TTL('600')
            UpdateDomainRecord.set_Value(IP)
            UpdateDomainRecordJson = json.loads(client.do_action_with_exception(UpdateDomainRecord))
            print(UpdateDomainRecordJson)


#add new record
def add_dns_record(DomainName, hostname, Types, IP):
    AddDomainRecord = AddDomainRecordRequest.AddDomainRecordRequest()
    AddDomainRecord.set_DomainName(DomainName)
    AddDomainRecord.set_RR(hostname)
    AddDomainRecord.set_Type(Types)
    AddDomainRecord.set_TTL('600')
    AddDomainRecord.set_Value(IP)
    AddDomainRecordJson = json.loads(client.do_action_with_exception(AddDomainRecord))
    print(AddDomainRecordJson)



#delete record
def delete_dns_record(DomainName, hostname):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
            RecordId = x['RecordId']
            DeleteDomainRecord = DeleteDomainRecordRequest.DeleteDomainRecordRequest()
            DeleteDomainRecord.set_RecordId(RecordId)
            DeleteDomainRecordJson = json.loads(client.do_action_with_exception(DeleteDomainRecord))
            print(DeleteDomainRecordJson)


#set record status
def set_dns_record(DomainName, hostname, status):
    DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    DomainRecords.set_accept_format('json')
    DomainRecords.set_DomainName(DomainName)
    DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
    for x in DomainRecordsJson['DomainRecords']['Record']:
        if hostname == x['RR']:
                RecordId = x['RecordId']
                SetDomainRecord = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
                SetDomainRecord.set_accept_format('json')
                SetDomainRecord.set_RecordId(RecordId)
                SetDomainRecord.set_Status(status)
                SetDomainRecordJson = json.loads(client.do_action_with_exception(SetDomainRecord))
                print(SetDomainRecordJson)


#check record if exists
def checkRecord(recordName):
    domainNameOne=recordName.rsplit(".",2)[-1]
    domainNameTwo=recordName.rsplit(".",2)[-2]
    recordRR=recordName.rsplit(".",2)[0]
    domainName=domainNameTwo+"."+domainNameOne
    #print("get this recods domamin name: " +domainName)

    DomainList = DescribeDomainsRequest.DescribeDomainsRequest()
    DomainList.set_accept_format('json')
    DNSListJson = json.loads(client.do_action_with_exception(DomainList))
    domainList=[]
    for i in DNSListJson['Domains']['Domain']:
        domainList.append(i['DomainName'])

    if(domainName not in domainList):
        print("error: this domain: "+ domainName +" is Not yours")
        sys.exit
    else:
        #print("the domain is yours")
        DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        pageSize=100
        recordsAll=[]
        DomainRecords.set_accept_format('json')
        DomainRecords.set_DomainName(domainName)
        DomainRecords.set_PageSize(pageSize)
        DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
        #print(DomainRecordsJson['PageNumber'])
        #print(DomainRecordsJson['PageSize'])
        totalCounts=DomainRecordsJson['TotalCount']
        if(totalCounts % pageSize == 0):
            pageCounts=int(totalCounts / pageSize)
        else:
            pageCounts=int(totalCounts / pageSize) + 1

        for count in range(pageCounts):
            DomainRecords.set_PageNumber(count+1)
            DomainRecordsJson = json.loads(client.do_action_with_exception(DomainRecords))
            for x in DomainRecordsJson['DomainRecords']['Record']:
                recordsAll.append(x)
        #print("all records number: "+str(len(recordsAll)))
        RRList=[]

        for x in recordsAll:
            #RecordId = x['RecordId']
            RR = x['RR']
            RRList.append(RR)

        if(recordRR in RRList):
            print(recordRR + " : already existed in "+ recordName)
            return True
        else:
            print(recordRR + " : NOT exists in "+recordName)
            return False


list_domain()

#add_dns_record('freidenker.tech', 'test1', 'A', '10.12.1.0')

#list_dns_record("freidenker.tech")
checkRecord("freidenker.freidenker.tech")

