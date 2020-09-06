import time

from selenium import webdriver
from selenium.webdriver import ActionChains


class LoginSlide:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options, executable_path='./driver/chromedriver')
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.driver.maximize_window()

    def get_login(self):
        # self.driver.get('https://passport.tujia.com/PortalSite/LoginPage/?originUrl=https%3A%2F%2Fwww.tujia.com')
        # self.driver.get('https://www.xiaozhu.com/')
        # self.driver.get('https://www.qcc.com/user_login')
        self.driver.get('https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d91IOQcc&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F')
        time.sleep(3)
        # self.driver.find_element_by_xpath('//a[@class="logindialog"]').click()
        # self.driver.find_element_by_xpath('//a[@id="normalLogin"]').click()
        self.driver.find_element_by_xpath('//input[@id="fm-login-id"]').send_keys('000000')

        time.sleep(3)
        self.driver.find_element_by_xpath('//input[@id="fm-login-password"]').send_keys('123456')
        # self.driver.find_element_by_xpath('//a[@id="normalLogin"]').click()
        time.sleep(5)
        # slide = self.driver.find_element_by_xpath('//span[@class="nc_iconfont btn_slide"]')
        # slide = self.driver.find_element_by_xpath('//span[@id="nc_5_n1z"]')
        slide = self.driver.find_element_by_xpath('//span[@id="nc_1_n1z"]')
        ActionChains(self.driver).drag_and_drop_by_offset(slide, 360, 0).perform()
        time.sleep(30)


if __name__ == '__main__':
    LoginSlide().get_login()