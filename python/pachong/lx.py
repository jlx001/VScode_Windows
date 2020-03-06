# —*— coding: utf-8 —*—
import requests
import json
import time
import pandas as pd
from pyecharts.charts import Map   # 画图模块
import pyecharts.options as opts
# 请求的URL
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'

# 伪装请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'referer': 'https://news.qq.com/zt2020/page/feiyan.htm?from=timeline&isappinstalled=0'
}

# 抓取数据
r = requests.get(url % time.time(), headers=headers)

data = json.loads(r.text)
# print (r.text)

data = json.loads(data['data'])

lastUpdateTime = data['lastUpdateTime']
print('数据更新时间 ' + str(lastUpdateTime))


# 采集当日数据
areaTree = data['areaTree']

print('采集当日省市数据...')

# 创建空 dataframes
col_names =  ['省', '市', '新增确诊','累计确诊', '死亡', '治愈','死亡率','治愈率']
col_names_p = ['省', '新增确诊', '累计确诊', '死亡', '治愈', '死亡率', '治愈率']

# 创建空列表用于画图
Is_province_name=list()  # 省
Is_province_confirm=list() # 累计确诊数

my_df  = pd.DataFrame(columns = col_names)
my_df_p = pd.DataFrame(columns = col_names_p)

for item in areaTree:
    if item['name'] == '中国':
        item_ps = item['children']

        # 遍历省级数据
        for item_p in item_ps:
            province = item_p['name']
            # print(province)
            # print(item_p['total'])
            confirm = item_p['total']['confirm']
            death = item_p['total']['dead']
            heal = item_p['total']['heal']
            new_confirm = item_p['today']['confirm']
            deadRate =item_p['total']['deadRate']
            healRate =item_p['total']['healRate']

            # 向df添加数据
            data_dict = {'省': province,'新增确诊':new_confirm,'累计确诊': confirm,
                         '死亡': death, '治愈': heal, '死亡率': deadRate, '治愈率': healRate}
            # print (data_dict)
            my_df_p.loc[len(my_df_p)] = data_dict
            
            # 添加画图需要的数据
            Is_province_name.append(item_p['name'])  # 省 转换数据格式 
            Is_province_confirm.append(confirm) # 累计确诊

            # 遍历地级数据
            item_cs = item_p['children']
            for item_c in item_cs:
                prefecture = item_c['name']
                # print('  ' + prefecture)
                # print('  ' + str(item_c['total']))
                new_confirm = item_c['today']['confirm']
                confirm = item_c['total']['confirm']
                # suspect = item_c['total']['suspect']
                death = item_c['total']['dead']
                heal = item_c['total']['heal']
                deadRate = item_c['total']['deadRate']
                healRate = item_c['total']['healRate']

                # 向df添加数据
                data_dict = {'省': province, '市':prefecture, '新增确诊':new_confirm,'累计确诊': confirm,
                             '死亡': death, '治愈': heal, '死亡率': deadRate, '治愈率': healRate}
                my_df.loc[len(my_df)] = data_dict

# 循环结束 组合“省”与“累计确诊”
Is_province_cfm = list(zip(Is_province_name,Is_province_confirm))
# 画图
def map_cn_disease_dis() -> Map:
    c = (
        Map()
        .add('中国', Is_province_cfm, 'china')
        .set_global_opts(
            title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
            visualmap_opts=opts.VisualMapOpts(is_show=True,
                                              split_number=6,
                                              is_piecewise=True,  # 是否为分段型
                                              pos_top='center',
                                              pieces=[
                                                   {'min': 10000, 'color': '#7f1818'},  #不指定 max
                                                   {'min': 1000, 'max': 10000},
                                                   {'min': 500, 'max': 999},
                                                   {'min': 100, 'max': 499},
                                                   {'min': 10, 'max': 99},
                                                   {'min': 0, 'max': 5} ],                                              
                                              ),
        )
    )
    return c
map_cn_disease_dis().render('全国疫情地图.html')

# 保存数据
my_df.index += 1   # 使index从1开始
my_df_p.index += 1
my_df.to_csv(r'./china_prefecture_status_{}.csv'.format(str(lastUpdateTime).split()[0]), encoding='utf_8_sig', header='true')
my_df_p.to_csv(r'./china_province_status_{}.csv'.format(str(lastUpdateTime).split()[0]), encoding='utf_8_sig', header='true')

#for each in my_df_p:

print('Success')