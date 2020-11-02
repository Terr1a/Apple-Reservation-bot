# 版权声明
# tutorial.py - The core part of apple reservation bot
# 本代码仅用作个人学习使用，禁止用于任何违法活动，所产生的后果与代码作者无关
# @author = Wenxiao Pan
# Copyright (c) 2020 Wenxiao Pan

try:
    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.chrome.options import Options
    import prettytable as pt
    import os
except ModuleNotFoundError as e:
    print("缺少依赖模块，正在安装")
    import os
    p = os.popen("pip install selenium")
    print(p.read())
    p = os.popen("pip install prettytable")
    print(p.read())
    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.chrome.options import Options
    import prettytable as pt
import time
import threading

#初始化浏览器
storeOne = webdriver.Chrome()
storeTwo = webdriver.Chrome()
storeThree = webdriver.Chrome()

#初始化状态列表
storeStatus = pt.PrettyTable()
storeStatus.field_names = ["Name","Status"]
statusList = []

#带状态的输出方法
def push(info, flag):
    type = {"SUCCESS":"32","WARNING":"33","FAILED":"31"}
    color = type[flag]
    localtime = time.asctime( time.localtime(time.time()) )
    print("\033[0;%s;40m\t" % color+localtime+": "+info+"\033[0m" )

#判断商店是否可用
def isResAvaliable(b):
    succuss = "立即预约购买你的新 iPhone。"
    try:
        if b.find_element_by_xpath(xpath="//h1").text == succuss:
            return True
    except:
        return False

    return False

#选择手机种类
def purchase(browser:webdriver.Chrome):
    try:
        color = browser.find_element_by_xpath(xpath="//section[@id='product-selector']/fieldset[2]/ul/li[4]/div/label/div")
        color.click()#选择颜色
    except:
        push("COLOR CHOOSE ERROR","FAILED")
        return False
    try:
        capacity = browser.find_element_by_xpath(xpath="//label[@id='capacity-1-label']")
        capacity.click()#选择容量
    except:
        push("CAPACITY CHOOSE ERROR","FAILED")
        return False
    try:
        store = browser.find_element_by_xpath(xpath="//select[@id='anchor-store']")
        Select(store).select_by_value("R493")#选择地区
    except:
        push("STORE UNAVALIABLE","FAILED")
        return False

#南京艾尚天地
def Store_1(table:pt):
    storeOne.get("https://reserve-prime.apple.com/CN/zh_CN/reserve/F/availability?iUP=N")
    time.sleep(3)
    if isResAvaliable(storeOne):
        purchase(browser=storeOne)
        status = storeOne.find_element_by_xpath(xpath="//input[@id='store-R703']").is_enabled()
        if status:
            statusList.append(["南京艾尚天地", "Available"])
        else:
            statusList.append(["南京艾尚天地", "NO"])
    else:
        statusList.append(["南京艾尚天地", "STORE IS CLOSED"])

#南京虹悦城
def Store_2(table:pt):
    storeTwo.get("https://reserve-prime.apple.com/CN/zh_CN/reserve/F/availability?iUP=N")
    time.sleep(3)
    if isResAvaliable(storeTwo):
        purchase(browser=storeTwo)
        status = storeTwo.find_element_by_xpath(xpath="//input[@id='store-R643']").is_enabled()
        if status:
            statusList.append(["南京虹悦城","Available"])
        else:
            statusList.append(["南京虹悦城", "NO"])
    else:
        statusList.append(["南京虹悦城", "STORE IS CLOSED"])

def Store_3(table:pt):
    storeThree.get("https://reserve-prime.apple.com/CN/zh_CN/reserve/F/availability?iUP=N")
    time.sleep(3)
    if isResAvaliable(storeThree):
        purchase(browser=storeThree)
        status = storeThree.find_element_by_xpath(xpath="//input[@id='store-R493']").is_enabled()
        if status:
            statusList.append(["南京金茂汇", "Available"])
        else:
            statusList.append(["南京金茂汇", "NO"])
    else:
        statusList.append(["南京金茂汇", "STORE IS CLOSED"])

def showStores():
    for status in statusList:
        storeStatus.add_row(status)

    while True:
        os.system("CLS")
        push("iphone 12, 蓝色, 128G 实时商店预约状态","WARNING")
        print(storeStatus)
        push("--Update Time","WARNING")
        time.sleep(3)
if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=Store_1,args=(storeStatus,))#商店1线程
    threads.append(t1)#加入线程池
    t2 = threading.Thread(target=Store_2,args=(storeStatus,))#商店2线程
    threads.append(t2)#加入线程池
    t3 = threading.Thread(target=Store_3,args=(storeStatus,))#商店3线程
    threads.append(t3)#加入线程池
    count = 0
    for t in threads:#运行线程
        t.start()
        count+=1
        push("Waiting Server "+str(count)+"returning data","SUCCESS")
        time.sleep(1)

    for t in threads:#在浏览器获得信息之前不刷新表格
        t.join()

    showStores()#输出状态