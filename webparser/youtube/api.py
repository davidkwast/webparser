from urllib.parse import urljoin

import webparser.api
from . import utils

def get_search_list(url):
    '''Gets vided if from search URL'''
    
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

def _search_generator(url, limit):
    if limit < 1:
        limit == 1
    count = 0
    videos = 1
    next_page_link = url
    while count < limit:
        if not next_page_link:
            break
        d = get_search_list(next_page_link)
        videos = d['videos']
        yield videos
        next_page_link = d['next_page_link']
        count += 1

def search(query, limit=60):
    '''Searches a query string
    
    Args:
        query (str): query string.
        limit (int): number of search pages to process.

    Returns:
        list: video id
    '''
    URL = 'https://www.youtube.com/results?search_query='
    r = []
    for videos in _search_generator(URL + query, limit):
        r += videos
    return r

def get_video_info(video_id):
    '''Gets video data
    
    Args:
        query (str): video id

    Returns:
        dict: video data
    '''
    COOKIES = {'PREF': 'f1=50000000&gl=BR&hl=en'}
    YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v='
    url = YOUTUBE_VIDEO_URL + video_id
    response = webparser.api.request(url, cookies=COOKIES)
    html = response.html
    title_raw = html.find('.watch-title',first=1).text
    keywords_raw = html.find('meta[name="keywords"]', first=1).attrs['content']
    publish_date_raw = html.find('.watch-time-text', first=1).text
    description_raw = html.find('#eow-description', first=1)
    view_count_raw = html.find('.watch-view-count', first=1).text
    likes_raw = html.find('.like-button-renderer-like-button span', first=1)
    dislikes_raw = html.find('.like-button-renderer-dislike-button span', first=1)
    user_id_raw = html.find('.yt-user-info',first=1).find('a', first=1).attrs['href']
    user_username_raw = html.find('span[itemprop="author"] link', first=1).attrs['href']
    category_raw, license_raw = [x.text for x in html.find('.watch-info-tag-list')][:2]
    return {
        'title': title_raw.strip(),
        'keywords': utils.parse_keywords(keywords_raw),
        'publish_date': utils.parse_str_date(publish_date_raw),
        'category': category_raw,
        'license': license_raw,
        'view_count': utils.parse_view_count(view_count_raw),
        'likes': utils.parse_likes(likes_raw),
        'dislikes': utils.parse_likes(dislikes_raw),
        'user_id': utils.parse_user_id(user_id_raw),
        'user_username': utils.parse_user_username(user_username_raw),
        'description_text': str(description_raw.text),
        'description_html': str(description_raw.html),
        '_video_id': video_id,
        '_url': url,
        '_response_obj': response,
    }
