import time
import traceback
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities
from down_pic import PicDownload
from tools import Tools


class Spider:
    """
    获得根据main传来的url,开启虚拟chrome 拿到当前页面的写真模块，把每一个写真模块div，
    根据div可以计算所有图片的数量   然后交给ParseModule类处理
    """
    total_div_cnt = 0
    total_pic_cnt = 0

    def __init__(self, _url='https://www.baidu.com', _require_number=1):
        """
        :param _url: 模块url
        :param _require_number: 要抓取的写真数量。默认是1个写真
        """
        self.url = _url
        self.require_number = _require_number
        self.options = ChromeOptions()
        # 无界 Chrome 运行
        # options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument(
            'user-agent=" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/84.0.4147.89 Safari/537.36"')

        self.driver = webdriver.Chrome(options=self.options)
        # 最大化窗口
        self.driver.maximize_window()
        # 控制循环
        self.flag = True
        self.module_set = set()

    def parser(self, module=None):
        if module is None:
            return
        # 解析模块
        # 1 获得模块的图片总数量
        total_pic = int(module.find_element_by_css_selector("[class='list-tag']") \
                        .find_element_by_tag_name('span').get_attribute('innerHTML')[:-1])
        self.total_pic_cnt += total_pic
        # 获得模块的 title+url
        target_module = module.find_element_by_css_selector("[class='list-body']") \
            .find_element_by_tag_name('a')
        # title 用于创建文件夹，需要格式化一下，否则会创建失败
        module_title = Tools.filter_filename(target_module.get_attribute('innerHTML'))
        time.sleep(1)
        # 点击下一页
        self.driver.execute_script("arguments[0].click();", target_module)

        # 跳转页面
        self.driver.switch_to.window(self.driver.window_handles[-1])
        for i in range(1, total_pic + 1):
            # 获取当前页面的url  /html/body/main/div/div[2]/div/div[3]/div[1]/div/p/a/img
            center_img = self.driver.find_element_by_css_selector("[class='nc-light-gallery-item']") \
                .find_element_by_tag_name('img')
            img_url = center_img.get_attribute('src')
            download = PicDownload(img_url, folder_name=module_title, file_name=i)
            download.download()
            self.driver.execute_script("arguments[0].click();", center_img)
        # 关闭窗口
        self.driver.close()
        # 回档
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def start(self):
        """
        获得所有的模块，然后把每个模块传递给 parse中ModuleParser解析
        :return:
        """
        try:
            self.driver.get(self.url)
            scroll_to_bottom = "var q=document.documentElement.scrollTop=10000"
            while self.flag:
                def f():
                    # 下滑请求数据
                    self.driver.execute_script(scroll_to_bottom)
                    #  等资源加载
                    time.sleep(1)
                    # 点击加载更多请求数据
                    btn = self.driver.find_element_by_css_selector(
                        "[class='dposts-ajax-load btn btn-light btn-block']")
                    self.driver.execute_script("arguments[0].click();", btn)
                    module_divs = self.driver.find_elements_by_css_selector("[class='col-6 col-md-3 d-flex']")
                    # print(len(module_divs))
                    for module in module_divs:
                        if module in self.module_set:
                            continue
                        self.module_set.add(module)
                        if self.total_div_cnt == self.require_number:
                            # 模块数量够了，退出函数,以及退出外层循环
                            self.flag = False
                            return
                        self.parser(module)
                        self.total_div_cnt += 1
                        # print(module)
                f()
            print("一共下载了{}张图片。所有图片均保存在当前目录下".format(self.total_div_cnt * self.total_pic_cnt))
            self.driver.quit()
        except Exception as e:
            # 释放内存
            self.driver.quit()
            print(traceback.print_exc())
