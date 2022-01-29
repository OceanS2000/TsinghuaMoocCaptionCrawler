import requests

def getCookies(filename):
    f = open(filename)
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    data = f.readline().replace(" ", "").replace("\"", "").replace("\n", "").split(";")
    result = {}
    for entry in data:
        if '=' in entry:
            entryGroup = entry.split("=")
            result[entryGroup[0]] = entryGroup[1]
    return result

def trim(str):
    return str.replace(" ", '')\
              .replace("\n", '')

def get_course_info(cid, sid):
    
    video_list = []
    
    url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid={cid}&sign={sid}&term=latest&uv_id=2598'''
    cookies = getCookies('./cookies')
    response = requests.get(url, headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
    
    data = response.json()
    chapter_list = data['data']['course_chapter']
    
    for chapter in chapter_list:
        leaves = chapter['section_leaf_list']
        for leaf in leaves:
            try:
                video_list.append(leaf['leaf_list'][0]['id'])
            except:
                pass
    
    return video_list

def get_caption(cid, sid, vid):
    url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/{cid}/{vid}/?sign={sid}&term=latest&uv_id=2598'''
    cookies = getCookies('./cookies')
    response = requests.get(url, headers={\
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                            'xtbz': 'cloud'},
                            cookies = getCookies("./cookies"))
    
    data = response.json()
    video_name = data['data']['name']
    
    try:
        ccid = data['data']['content_info']['media']['ccid']
        if not ccid: raise BaseException("HTML Introduction. No video.")
        
        url = f'''https://tsinghua.yuketang.cn/mooc-api/v1/lms/service/subtitle_parse/?c_d={ccid}&lg=0'''
        cookies = getCookies('./cookies')
        response = requests.get(url, headers={\
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                                'xtbz': 'cloud'},
                                cookies = getCookies("./cookies"))
        
        data = response.json()
        data['start'] = [int(s) for s in data['start']]
        caption_list = list(zip(data['start'], data['text']))
        
        f = open(f"./output/[{vid}] {video_name}.txt", 'w+', encoding='utf-8')
        
        for caption in caption_list:
            f.write("%-10d  %s\n" % (caption[0], caption[1]))
        
        f.close()
        
    except:
        pass