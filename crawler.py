from utils.net import *
import yaml


if __name__ == "__main__":
    
    f = open("./config.yml", 'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()
    
    video_list = get_course_info(config['classroom_id'])
    
    for vid in video_list:
        get_caption(config['classroom_id'], vid)
