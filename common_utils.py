import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime


# 发送邮件提醒打卡结果
def sendInfo(receiver, result, user):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    if result == "未填报":
        message = MIMEText('小助手提醒您，您的体温上报结果为：<font color="red">上报失败，请及时手动上报！</font>', 'html', 'utf-8')
    else:
        message = MIMEText('小助手提醒您，您的体温上报结果为：<font color="blue">成功上报！体温是 ' + result + '。</font>', 'html', 'utf-8')
    message['From'] = Header("小助手", 'utf-8')  # 发送者
    message['To'] = Header("测试", 'utf-8')  # 接收者

    subject = str(user) + '自动体温上报结果'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # windows 下这样写
        # smtpObj = smtplib.SMTP()
        # smtpObj.connect('smtp.qq.com', 25)  # 25 为 SMTP 端口号
        
		# Linux 下这样写
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect('smtp.qq.com', 465)  # 阿里云指定 465 为 SSL 端口号
		
        smtpObj.login('发件人邮箱账号', 'SMTP授权码')
        smtpObj.sendmail('发件人邮箱账号', receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


# 判断当前时间是哪个时间段（晨检/午检/晚检）
def getTime():
    now_time = datetime.datetime.now()
    # 获取小时和分钟
    time_list = str(now_time).split(' ')[1].split(':')
    h_time = int(time_list[0])
    m_time = int(time_list[1])

    if 19 <= h_time < 21 and m_time >= 5:
        return 3
    if 12 <= h_time < 14 and m_time >= 5:
        return 2
    if 7 <= h_time < 9 and m_time >= 5:
        return 1

    return 0
