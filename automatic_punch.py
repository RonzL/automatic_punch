from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from common_utils import *


class Clock:

    def __init__(self):
        self.usrList = ['用户A','用户B']
        self.pwdList = ['密码A','密码B']
        self.receiverList = ['邮箱A','邮箱B']
        self.chrome_options = Options()

        # Linux 下需要开启无头模式
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')

    # 执行打卡动作
    def clockIn(self, driver):
		# 获取当前时间
        now_time = datetime.datetime.now()
        print('当前时间是：' + str(now_time))
        now_time = getTime()

        # 判断进入哪个页面
        if now_time == 1:
            # 进入晨检
            print('进入晨检页面')
            driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/div").click()
        elif now_time == 2:
            # 进入午检
            print('进入午检页面')
            driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/div").click()
        elif now_time == 3:
            # 进入晚检
            print('进入晚检页面')
            driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div").click()

        elif now_time == 0:
            print('还未到打卡时间')

        time.sleep(2)

    # 查询打卡结果
    def findResult(self, driver):
        # 回到打卡主页面
        driver.get("https://e-report.neu.edu.cn/inspection/items")
        now_time = getTime()
        clock_result = ''
        print('查询打卡结果')
        # 判断读取哪个模块
        if now_time == 1:
            # 进入晨检
            clock_result = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/div/p")
        elif now_time == 2:
            # 进入午检
            clock_result = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/div/p")
        elif now_time == 3:
            clock_result = driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div/div/p")
        return clock_result.text

    # 开始为每个人打卡
    def clockForAll(self):
        for i in range(len(self.usrList)):
            global all_driver
            try:
                print('===============================')
                print(self.usrList[i] + '开始填报...')
                # 打开谷歌浏览器
                driver = webdriver.Chrome(chrome_options=self.chrome_options)
                all_driver = driver
                print('已打开谷歌浏览器')

                # 来到登录页面
                driver.get('xxxxxxxx')
                print('来到登录页面')
                # 延时加载
                time.sleep(2)

                # 输入用户名和密码
                driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[1]/input[1]").send_keys(self.usrList[i])
                driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[1]/input[2]").send_keys(self.pwdList[i])
                # 模拟点击登录
                driver.find_element_by_xpath("/html/body/div[2]/div/form/div/div[1]/span/input").click()
                print('登录成功')
                # 延时加载
                time.sleep(2)
				
				# 来到打卡主页面
                driver.get('xxxxxxxxx')
                time.sleep(2)

                # 进入具体时间段的打卡页面（晨检/午检/晚检）
                self.clockIn(driver)

                # 点击提交打卡
                driver.find_element_by_xpath("/html/body/div[2]/form/div[5]/input").click()
                print('体温上报成功')
                time.sleep(2)

                # 读取结果
                sendInfo(self.receiverList[i], self.findResult(driver), self.usrList[i])
                time.sleep(2)

                # 退出驱动
                driver.quit()
                print("谷歌浏览器退出成功")
                # 退出程序

            except Exception:
                print('体温上报失败')
                sendInfo(self.receiverList[i], "未填报", self.usrList[i])
                all_driver.quit()
                print("谷歌浏览器退出成功")
                # 退出程序


if __name__ == '__main__':
    clock = Clock()
    clock.clockForAll()
    exit(0)

