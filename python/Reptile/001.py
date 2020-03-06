# -*- coding: utf-8 -*-

"""
@File    : JsonCrawlerRelativeData.py
@Author  : fungis@163.com
@Time    : 2020/2/10 19:10
"""
#导入爬虫requests库和json解析库
import json
import requests

#爬取丁香园数据页面
url = 'https://raw.githubusercontent.com/BlankerL/DXY-2019-nCoV-Data/master/json/DXYArea.json'
response = requests.get(url)
# 将响应信息进行json格式化
versionInfo = response.text
print(versionInfo)#打印爬取到的数据
print("------------------------")#重要数据分割线↓

#一个从文件加载，一个从内存加载#json.load(filename)#json.loads(string)
jsonData = json.loads(versionInfo)

#用于存储数据的集合
dataSource = []
provinceShortNameList = []
confirmedCountList = []
curedCount = []
deadCountList = []
#遍历对应的数据存入集合中
for k in range(len(jsonData['results'])):
    if(jsonData['results'][k]['country'] == '中国'):
        provinceShortName = jsonData['results'][k]['provinceShortName']
        if("待明确地区" == provinceShortName):
            continue;
        confirmedCount = jsonData['results'][k]['confirmedCount']
        # 存储数据为键值对点形式（[['江苏', 492], ['安徽', 830]]）
        dataSource.append("['"+provinceShortName+"',"+str(confirmedCount)+"]")
        provinceShortNameList.append(provinceShortName)#省份名称简称
        confirmedCountList.append(confirmedCount)
        curedCount.append(jsonData['results'][k]['curedCount'])
        deadCountList.append(jsonData['results'][k]['deadCount'])
        # print(jsonData['results'][k]['provinceName'])#打印省份全称

print("data = "+str(dataSource).replace('"',''))#省份，确认人数集合data =[省份,确诊人数],[省份,确诊人数]...]
print("columns = "+str(provinceShortNameList))#省份集合
print("confirmedCount = "+str(confirmedCountList))#确诊人数集合
print("curedCount = "+str(curedCount))#治愈人数集合
print("deadCount = "+str(deadCountList))#死亡人数集合

