import traceback
from spider import Spider
import time

# 主url
page_url = 'https://www.95mm.net/'
# 待拼接url
module_maps = {
    '1': 'qingchun',
    '2': 'sifang',
    '3': 'xinggan',
    '4': 'tag/黑丝',
    '5': 'tag/杨晨晨'
}


def main():
    while True:
        module = input("请输入你要抓取的模块代号\n\t清纯唯美\t->\t1 \n\t摄影私房\t->\t2 "
                       "\n\t性感妖姬\t->\t3 \n\t黑丝\t->\t4 \n\t杨晨晨->\t5  \n输入数字即可：")
        try:
            url = page_url + module_maps[module]
            # 如果上面输入错了,就抛出错误,然后再输入数量
            require_number = int(input("你要抓取的写真数量（考虑到健康以及速度问题，"
                                       "请不要输入过大的数据！因为一个写真里的图片数量不唯一！建议输入24的倍数）："))
            # print(url)
            # print(url, require_number)
            s = Spider(url, require_number)
            print("正在下载中。。。图片均保存在当前目录下")
            start = time.time()
            s.start()
            end = time.time()
            print("共计耗时：{}秒".format(end - start))
            return
        except Exception as e:
            print(traceback.print_exc())
            print("请按照提示输入代号！")


if __name__ == '__main__':
    main()
