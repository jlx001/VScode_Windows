import time, json, requests
import jsonpath
from pyecharts.charts import Map
import pyecharts.options as opts
import openpyxl
#%%

# 全国疫情地区分布(各省确诊病例)
def catch_cn_disease_dis():
    timestamp = '%d'%int(time.time()*1000)
    url_area = ('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
               '&callback=&_=') + timestamp
    world_data = json.loads(requests.get(url=url_area).json()['data'])
    china_data = jsonpath.jsonpath(world_data, 
                                   expr='$.areaTree[0].children[*]')
    ls_province_names = jsonpath.jsonpath(china_data, expr='$[*].name')
    Is_newConfirm_vals=jsonpath.jsonpath(china_data, expr='$[*].today.confirm')
    ls_confirm_vals = jsonpath.jsonpath(china_data, expr='$[*].total.confirm')
    Is_dead_vals=jsonpath.jsonpath(china_data, expr='$[*].total.dead')
    Is_deadRate_vals=jsonpath.jsonpath(china_data, expr='$[*].total.deadRate')
    Is_heal_vals=jsonpath.jsonpath(china_data, expr='$[*].total.heal')
    Is_healRate_vals=jsonpath.jsonpath(china_data, expr='$[*].total.healRate')
    ls_province_confirm = list(zip(ls_province_names, ls_confirm_vals))        
    Is_province_vals=list(zip(ls_province_names,Is_newConfirm_vals, ls_confirm_vals,Is_dead_vals,Is_deadRate_vals,Is_heal_vals,Is_healRate_vals)) 
    return ls_province_confirm,Is_province_vals,world_data

#%%
ls_province_cfm,Is_province_vals,dic_world_data = catch_cn_disease_dis()
print(ls_province_cfm)

# 输出到excel

workbook = openpyxl.Workbook()
sheet=workbook.active
tableTitle=['省名','新增确诊','累计确诊','死亡','死亡率','治愈','治愈率']
sheet.append(tableTitle)
for each in Is_province_vals:
    sheet.append(each)
workbook.save('疫情数据.xlsx')


#%%

# 绘制全国疫情地图
def map_cn_disease_dis() -> Map:
    c = (
        Map()
        .add('中国', ls_province_cfm, 'china')
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
print('完成')