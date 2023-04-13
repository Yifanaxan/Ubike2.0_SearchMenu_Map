import requests

sarea_list = None #建立變數
data_list = None

def getInfo():
    global sarea_list, data_list #The global keyword is used in Python to declare that a variable is a global variable, rather than a local variable within a function or block of code. 
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response = requests.get(url)
    data_list = response.json() #https://jsonviewer.stack.hu/ data_list是一個list裡面很多dictionary
    sarea_temp = set()
    for item in data_list: #請看20230407講義
        sarea_temp.add(item["sarea"])#The line of code sarea_temp.add(item["sarea"]) assumes that item is a dictionary object, and that it has a key named "sarea".
    sarea_list = sorted(list(sarea_temp)) #將sarea_temp轉成排序過的list
    
def getInfoFromArea(areaName):
    filter_data = filter(lambda n:n["sarea"] == areaName, data_list)
    return list(filter_data)

def filter_sbi_warning_data(area_data,numbers) -> list:
    filter_data =filter(lambda n:n["sbi"] <=numbers ,area_data)
    return list(filter_data)

def filter_bemp_warning_data(area_data,numbers) -> list:
    filter_data =filter(lambda n:n["bemp"] <=numbers,area_data)
    return list(filter_data)


getInfo()
#print(type(getInfoFromArea("士林區")))