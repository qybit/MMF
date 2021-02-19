import re


class Tools:
    @staticmethod
    def filter_filename(text):
        """
        过滤傻逼中文字符 一律用 '-' 代替
        :param text:
        :return:
        """
        try:
            return re.sub(
                "[\u0060|\u0021-\u002c|\u002e-\u002f|\u003a-\u003f|\u2200-\u22ff|\uFB00-\uFFFD|\u2E80-\u33FF]",
                '-', text)
        except Exception as e:
            print(e)
            return text
