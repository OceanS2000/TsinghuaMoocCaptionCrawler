import requests
from bs4 import BeautifulSoup
from utils.net import *
import yaml





def fetch_single_video(url):
    url = 'https://tsinghua.yuketang.cn/pro/lms/8NpUsbr6GZH/3029907/video/2224317'
    cookies = getCookies('./cookies')
    
    response = requests.get("https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid=3029907&sign=8NpUsbr6GZH&term=latest&uv_id=2598", headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
    # response = requests.get("https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/3029907/2224317/?sign=8NpUsbr6GZH&term=latest&uv_id=2598", headers={\
    #                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    #                         'xtbz': 'cloud'},
    #                         cookies = getCookies("./cookies"))
    
    response.encoding = 'utf-8'
    print(response.json())
    # print(response.json()['data']['content_info']['media']['ccid'])
    f = open('./a.txt', 'w+', encoding='utf-8')
    f.write(str(response.json()))

if __name__ == "__main__":
    
    f = open("./config.yml", 'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()
    
    video_list = get_course_info(config['course_id'], config['user_id'])
    
    for vid in video_list:
        get_caption(config['course_id'], config['user_id'], vid)