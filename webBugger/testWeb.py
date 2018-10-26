from selenium import webdriver
from PIL import Image, ImageEnhance
from pytesseract import *


#
# browser = webdriver.Chrome()
# browser.get("http://localhost:8091/#/")
# # browser.
# login_button = browser.find_element_by_link_text('登   录')
# login_button.click()
# html = browser.page_source
# print(html)


# 定义调试类
class TroubleMan():
    def __init__(self, host='http://localhost:8091/#/', user='qiaokuoyuan', password='123456',
                 temp_dir='d:/d/debugger/'):
        self.browser = webdriver.Chrome()
        self.host = host
        self.user = user
        self.password = password
        self.temp_dir = temp_dir

    # 自动登陆，relogin代表是否需要重复登陆，即已经登陆了退出重新登陆
    def login(self, relogin=False):
        self.browser.get(self.host)
        # 如果需要退出登录
        if (relogin):
            try:
                logout_btn = self.browser.find_element_by_link_text('退出')
                logout_btn.click()
            except:
                pass
        # 找到登陆按钮
        login_button = self.browser.find_element_by_link_text('登   录')

        login_button.click()
        self.browser.find_element_by_id('name').send_keys(self.user)
        self.browser.find_element_by_id('pass').send_keys(self.password)

        # 网页截图
        self.browser.save_screenshot(self.temp_dir + 'screen.png')

        # 找到验证码 元素
        vcode = self.browser.find_element_by_id('img_chk')

        # 找到验证码位置
        left = vcode.location['x']
        top = vcode.location['y']
        right = vcode.location['x'] + vcode.size['width']
        bottom = vcode.location['y'] + vcode.size['height']

        # 从屏幕截图中截取验证码
        img = Image.open(self.temp_dir + 'screen.png')
        img = img.crop((left, top, right, bottom))

        img = img.convert('L')  # 图像加强，二值化

        sharpness = ImageEnhance.Contrast(img)  # 对比度增强

        img = sharpness.enhance(2.0)

        # sharp_img.save(self.temp_dir + "newVerifyCode.png")
        #
        # newVerify = Image.open(self.temp_dir + 'newVerifyCode.png')

        # 使用image_to_string识别验证码
        vcodeStr = image_to_string(img).strip()  # 使用image_to_string识别验证码
        # text1 = image_to_string('newVerifyCode.png').strip()
        print('识别验证码为', vcodeStr)

        vcode.send_keys(vcodeStr)

        self.browser.find_element_by_id('登    录').click()


# 测试  点击“登录”按钮，跳转到登录页。
def test_login_jump(self):
    pass


t = TroubleMan()
t.login(True)
