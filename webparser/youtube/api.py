from urllib.parse import urljoin

import webparser.api
from . import utils

def get_search_list(url):
    COOKIES = {'PREF': 'f1=50000000&gl=BR&hl=en'}
    SPLIT = '/watch?v='
    response = webparser.api.request(url, cookies=COOKIES)
    html = response.html
    links = [x.find('a',first=1).attrs['href'] for x in html.find('.yt-lockup-video')]
    videos = [x.split(SPLIT)[-1] for x in links if SPLIT in x]
    next_page_link__list = [x for x in html.find('span.yt-uix-button-content') if x.text == 'Next »']
    if next_page_link__list:
        link = next_page_link__list[0].element.getparent().attrib['href']
        next_page_link = urljoin(response.url, link)
    else:
        next_page_link = None
    return {
        'videos': videos,
        'next_page_link': next_page_link,
        '_response_obj': response,
    }

def search(query):
    URL = 'https://www.youtube.com/results?search_query='
    return get_search_list(URL + query)

def get_video_info(video_id):
    COOKIES = {'PREF': 'f1=50000000&gl=BR&hl=en'}
    YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
    url = YOUTUBE_VIDEO_URL + video_id
    response = webparser.api.request(url, cookies=COOKIES)
    html = response.html
    title_raw = html.find('.watch-title',first=1).text
    view_count_raw = html.find('.watch-view-count',first=1).text
    likes_raw = html.find('button[title="I like this"]',first=1).text
    dislikes_raw = html.find('button[title="I dislike this"]',first=1).text
    user_id_raw = html.find('.yt-user-info',first=1).find('a',first=1).attrs['href']
    user_username_raw = html.find('span[itemprop="author"]',first=1).find('link',first=1).attrs['href']
    return {
        'title': title_raw.strip(),
        'view_count': utils.parse_view_count(view_count_raw),
        'likes': int(likes_raw),
        'dislikes': int(dislikes_raw),
        'user_id': utils.parse_user_id(user_id_raw),
        'user_username': utils.parse_user_username(user_username_raw),
        '_url': url,
        '_response_obj': response,
    }
