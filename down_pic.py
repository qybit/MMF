import uuid
import requests
import os


class PicDownload:
    """
    图片下载类
    参数1：url
    参数2：file_location default:current directory
    """

    def __init__(self, url='', location_prefix='images', folder_name='img', file_name=uuid.uuid1()):
        """
        基于当前目录的DIY图片下载
        :param url: 下载的url
        :param location_prefix: 目前前缀
        :param folder_name: 文件夹名称
        :param file_name: 文件名称
        """
        if len(url) == 0:
            print("请传一个合法的参数！")
            return
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "en-us",
                        "Connection": "keep-alive",
                        "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}
        self.url = url
        self.folder_name = folder_name
        self.location_prefix = location_prefix
        self.file_name = file_name

    def make_directory(self):
        """
        先检查是否存在目录
        :return:
        """
        p = '{}/{}'.format(self.location_prefix, self.folder_name)
        if not os.path.exists(p):
            os.makedirs(p)
            print("文件夹<{}>创建成功".format(self.folder_name))

    def download(self):
        """
        下载功能
        :return:
        """
        self.make_directory()
        r = requests.get(self.url, headers=self.headers)
        p = '{}/{}/{}.jpg'.format(self.location_prefix, self.folder_name, self.file_name)
        if os.path.exists(p):
            return
        with open(p, 'wb') as f:
            f.write(r.content)
