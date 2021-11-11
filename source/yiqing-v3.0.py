#!/usr/bin/env python
# coding: utf-8

# In[1]:


# encoding:utf-8
import os
import selenium
import time
import json
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# In[2]:

# 打卡账号
username = ""
# 打卡账号的密码
password = ""
# 打卡尝试次数
timesToRepeat = 5
# 打卡网址
url = 'https://newcas.gzhu.edu.cn/cas/login?service=http%3A%2F%2Fyqtb.gzhu.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fyqtb.gzhu.edu.cn%252Finfoplus%252Foauth2%252Fauthorize%253Fx_redirected%253Dtrue%2526scope%253Dprofile%252Bprofile_edit%252Bapp%252Btask%252Bprocess%252Bsubmit%252Bprocess_edit%252Btriple%252Bstats%252Bsys_profile%252Bsys_enterprise%252Bsys_triple%252Bsys_stats%252Bsys_entrust%252Bsys_entrust_edit%2526response_type%253Dcode%2526redirect_uri%253Dhttp%25253A%25252F%25252Fyq.gzhu.edu.cn%25252Ftaskcenter%25252Fwall%25252Fendpoint%25253FretUrl%25253Dhttp%2525253A%2525252F%2525252Fyq.gzhu.edu.cn%2525252Ftaskcenter%2525252Fworkflow%2525252Findex%2526client_id%253D1640e2e4-f213-11e3-815d-fa163e9215bb'
# 邮箱服务器地址
emailServerAddress = 'smtp.qq.com'
# 邮箱服务器端口号
emailServerPort = 25
# 接收打卡提示的邮箱
userEmail = ''
# 发送打卡提示的邮箱（需开启STMP/POP协议）
senderEmail = ''
# 发送打卡提示邮箱的验证码（开启STMP/POP协议时给的验证码）
senderEmailPasswd = ''
# 邮件正文内容（HTML）(打卡成功)
successMsg = '''
    <h2>打开程序提示您：打卡成功了！！！</h2>
    <p>又是美好的一天[doge]</p>
    '''
# 邮件正文内容（HTML）(打卡失败)
failMsg = '''
    <h2>打卡程序警告：打卡失败了！！！</h2>
    <p>请手动打卡！！！[doge]</p>
    '''
failMsgChormeDirverError = '''
    <h2>打卡程序警告：打卡失败了！！！</h2>
    <p>此ChormeDriver版本无法支持Chrome浏览器，无法正常启动自动打卡程序，请检查ChromeDriver与Chrome版本是否兼容！！！</p>
    '''

# message: 邮件正文，subject:邮箱主题
def sendQQMail(message,subject):
    ret=True
    try:
        msg=MIMEText(message,'html','utf-8')
        msg['From']=formataddr(["打卡程序小助手",senderEmail])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["打卡程序用户",userEmail])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']=subject                # 邮件的主题，也可以说是标题
 
        server=smtplib.SMTP(emailServerAddress, emailServerPort)  # 发件人邮箱中的SMTP服务器
        server.login(senderEmail, senderEmailPasswd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(senderEmail,[userEmail,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception: 
        ret=False
        print("邮件发送失败")
        
    return ret

# 获取爱词霸每日鸡汤
def get_iciba_everyday_chicken_soup():
    url = 'http://open.iciba.com/dsapi/'  # 爱词霸网站地址
    r = requests.get(url) 
    all = json.loads(r.text) # 获取到json格式的内容，内容很多
    English = all['content']  # 提取json中的英文鸡汤
    Chinese = all['note']  # 提取json中的中文鸡汤
    Voice = all['tts']  # 提取音频链接
    image_url = all["fenxiang_img"] # 提取json中的图片链接
    out = '<br/><h3>每日一句</h3><p>%s</p><p>%s</p><p><p><video controls="" autoplay="" name="media"><source src="%s" type="audio/mpeg"></video></p><img src="%s" alt="每日一句"></p>'%(English, Chinese, Voice, image_url)
    return out

# 获取当天天气
def get_weather(city):
    url = 'http://wthrcdn.etouch.cn/weather_mini?city={}'.format(city)
    f=requests.get(url)
    wea_dict1=json.loads(f.text)
    #print(jsons['data']['forecast'])
    # for i in jsons['data']['forecast']:
    #     print(i['date'])
    #     print(i['high'])
    #     print(i['low'])
    #     print(i['fengli'])
    #     print(i['type'])
    if wea_dict1['status'] != 1000 :
        return "<br/><h3>天气预报</h3><p>天气api出错！！！无法查看天气！！！</p>"

    format_str = "<br/><h3>天气预报</h3><p><b>日期：</b>%s</p><p><b>坐标：</b>%s</p><p><b>天气：</b>%s</p><p><b>温度：</b>%s</p><p><b>风力：</b>%s</p>"
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    wea_dict =  wea_dict1['data']['forecast'][0]
    wea_type = wea_dict['type']
    wind = wea_dict['fengli'].split('CDATA[')[1][:2]
    temp = wea_dict['low'] + '~' + wea_dict['high']
    out = format_str % (date, city, wea_type, temp, wind)
    return out


# 打卡程序运行逻辑
for i in range(timesToRepeat):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        # global driver
        driver = webdriver.Chrome(options= chrome_options)
        print("打开自动测试浏览器！！")

        driver.get(url)
    except BaseException:
        print("ChromeDriver版本无法支持Chrome浏览器！")
        sendQQMail(failMsgChormeDirverError+get_weather('广州')+get_iciba_everyday_chicken_soup(),'打卡助手警告：打卡失败了！！！')
        os._exit(0)

    time.sleep(3)

    
    '''提交账户名跟密码'''
    try:
        driver.find_element_by_name("un").send_keys(username)
        driver.find_element_by_name("pd").send_keys(password)
        print("账户名及密码成功输入！！")
    
    except BaseException:
        print("无法输入账户名、密码？？")
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue
    
    '''触发成功登录按钮'''
    try:
        driver.find_element_by_class_name("login-btn").click()
        print("成功登录！！")
        
    except BaseException:
        print("登录失败？？")
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue

    '''触发学生健康状况申报按钮'''
    time.sleep(2)
    try:
        driver.find_element_by_link_text("学生健康状况申报").click()
        print("成功点击'学生健康状况申报'按钮！！")
    except BaseException:
        print("无法点击'学生健康状况申报'按钮？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue

    '''切换弹窗'''
    time.sleep(2)
    try:
        windows = driver.window_handles   # 获取该会话所有的窗口
        driver.switch_to.window(windows[-1])  # 跳转到最新的窗口
        print("窗口切换成功！！")
    except BaseException:
        print("窗口切换失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue
        
    '''触发开始上报按钮'''
    time.sleep(2)
    try:
        driver.find_element_by_id("preview_start_button").click()
        print("点击开始上报按钮！！")
    except BaseException:
        print("点击上报按钮失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue

    '''触发开疫情申报按钮1'''
    time.sleep(2)
    try:
        driver.find_element_by_id("V1_CTRL46").click()
        print("点击是否接触过半个月内有疫情重点地区旅居史的人员按钮成功！！")
    except BaseException:
        print("点击是否接触过半个月内有疫情重点地区旅居史的人员按钮失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue

    '''触发开疫情申报按钮1'''
    time.sleep(2)
    try:
        driver.find_element_by_id("V1_CTRL262").click()
        print("点击粤康码是否为绿码按钮成功！！")
    except BaseException:
        print("点击粤康码是否为绿码按钮失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue
    
    time.sleep(2)
    try:
        driver.find_element_by_id("V1_CTRL37").click()
        print("点击半个月内是否到过国内疫情重点地区成功！！")
    except BaseException:
        print("点击半个月内是否到过国内疫情重点地区失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue
        
    # 进行确认勾选
    time.sleep(2)
    try:
        driver.find_element_by_xpath("//*[@id='V1_CTRL82']").click()
        print("勾选最后的确认按钮！！")
    except BaseException:
        print("确认按钮勾选失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue
        
    '''确认提交按钮'''
    time.sleep(2)
    try:
        driver.find_element_by_class_name("command_button_content").click()
        print("提交表单！！")
    except BaseException:
        print("表单提交失败？？")
        
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器
        
        # 跳出当前循环
        continue

    time.sleep(4)
    try:
        txt = driver.find_element_by_class_name("form_do_action_error").text
        if txt != "打卡成功":
            print("可能提示会话已过期")
            driver.close() # 关闭当前窗口
            driver.quit()  # 退出Chrome浏览器  
            
            continue
        else:
            print("页面提示打卡成功！")
    except BaseException:
        print("打卡失败？？")
        # 退出
        driver.close() # 关闭当前窗口
        driver.quit()  # 退出Chrome浏览器

        # 最后提交的一次如果提交失败则发送邮件
        if i == timesToRepeat-1 :
            sendQQMail(failMsg+get_weather('广州')+get_iciba_everyday_chicken_soup(),'打卡助手警告：打卡失败了！！！')
        # 跳出当前循环
        continue
    
    time.sleep(2)
    driver.close() # 关闭当前窗口
    driver.quit()  # 退出Chrome浏览器
    print("打卡成功")

    # 若打卡成功一定会收到邮件提示，否则打卡失败（打卡失败有可能没有发送邮件）
    sendQQMail(successMsg+get_weather('广州')+get_iciba_everyday_chicken_soup(),'打开助手提示您：打卡成功了！！！')
    break

