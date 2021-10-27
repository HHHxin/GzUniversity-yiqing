# 广大疫情自动打卡程序
### 广大疫情自动打卡程序（在Windows和Linux下均可使用）；本程序仅供学习使用，不用于任何商业用途。请勿将本程序进行非法使用。大家一定要听从学校组织安排，不要心存侥幸，瞒报自己真实情况妨碍疫情防护，危害他人生命健康。

### 特此声明：如有人使用本程序用于非法用途，均与本人无关。



### 注：本程序使用Python语言所编写，需要进行相应的环境配置。所需要的类库包括有selenium、time、smtplib、email

selenium需要在本机环境中进行一定的配置，相关的配置可自行百度即可。本程序所使用的是ChromeDriver（谷歌自动化测试浏览器）

#### Requirement

The code was tested on:

- selenium
- time
- smtplib
- email

To install requirement:

```
pip install -r requirements
```

~~本程序包括有两个模块，验证码识别模块及相关按钮触发提交模块。~~

### 使用步骤

（yiqing-v3.0.py 使用方式）

**1、配置ChromeDriver**

略(自行百度)

* [参考（Windows为例）](https://blog.csdn.net/qq_22200671/article/details/108638836)

  

**2、配置邮件客户端，开启STMP/POP协议(本程序使用qq邮箱作为发送邮件服务端)，获取响应的验证码，在代码响应部分填写自己的信息**

略(自行百度)

* [如何打开POP3/SMTP/IMAP功能？_QQ邮箱帮助中心](https://service.mail.qq.com/cgi-bin/help?subtype=1&&no=166&&id=28)

**note： 开启IMAP/SMTP服务**

**3、填写yiqing-v3.0.py 里的配置信息**

* 打卡账号
  username = ""

* 打卡账号的密码
  password = ""

* 接收打卡提示的邮箱
  userEmail = ''

* 发送打卡提示的邮箱（需开启STMP/POP协议）
  senderEmail = ''

* 发送打卡提示邮箱的验证码（开启STMP/POP协议时给的验证码）
  senderEmailPasswd = ''

**4、测试程序**（Windows系统为例）
（1）配置有python环境，直接双击执行（可能出现报错的情况看不到）

（2）Win+R，输入cmd，跳转到程序所在目录，采用 

 ```
python yiqing-v3.0.py
 ```

**5、设置定时任务**

* 设置后每天可自行启动打卡程序

**备注**

可能出现错误的情况包括以下：

~~1、本程序验证码的识别采用截图保存到本地的形式，可能存在保存不成功或权限问题。需要根据报错情况对路径或权限进行修改~~

2、本程序并不是每次都能执行成功，有时候会出现执行失败的情况。可能会出现第一次执行失败，第二次执行成功。哪个步骤执行失败，都有相关的错误提示，一般出现这种错误时为网页端更新使得程序无法处理某些选项，可自行打卡一次后解决，也有可能需要更新代码解决。

3、可能出现因Chrome自动更新使得ChromeDriver无法导致错误，配置对应Chrome版本的ChromeDriver即可解决，配置方式可自行百度。



## 再次声明：本程序仅供学习使用，并无其他意图，如有非法使用，均与本人无关。









