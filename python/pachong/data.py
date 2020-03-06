import openpyxl
 

pro=list(zip([1,2,3,4,5,6],["g","h","i","g","k","l","m"]))
workbook = openpyxl.Workbook()
sheet=workbook.active
tableTitle=['省名','新增确诊','累计确诊','死亡','死亡率','治愈','治愈率']
sheet.append(tableTitle)
for each in pro:
    sheet.append(each)
    
    
workbook.save('疫情数据.xlsx')