import json
import requests
from DBConfig import RedisConfig
from settings import INI_LINK, HEADERS, INIT_KEY, CACH_KEEP, console_logger, root_logger

RedisConfig.cache_keep(CACH_KEEP)


class DownLink(object):

    def __init__(self):
        self.rc = RedisConfig.rc
        self.headers = HEADERS
        self.key_list = INIT_KEY
        self.link = INI_LINK

    def get_link(self, page, keyword, key_type):

        params = {
            'query': keyword,
            'per_page': '30',
            'page': page,
        }
        resp = requests.get(url=self.link, params=params, headers=self.headers)
        content_json = json.loads(resp.text)
        content_num = len(content_json['results'])
        if content_num != 0:
            for block in content_json['results']:
                link = block['urls']['regular']
                self.rc.rpush('unsplash_link', str((link, key_type)))
            console_logger.info('已经向redis中添加{0}类，第{1}页！'.format(keyword, page))
            return False
        else:
            return True

    def run(self):
        for keyword, key_type in self.key_list.items():
            page = 1
            loop_times = 0
            while True:
                try:
                    flag = self.get_link(page=page, keyword=keyword, key_type=key_type)
                    page += 1
                    if flag:
                        break
                except BaseException as exc:
                    root_logger.error(f"关键字：{keyword}，第{page}页，发生错误{exc}")
