from urllib.parse import urljoin

import webparser.api

def search(query):
    COOKIES = {'PREF': 'f1=50000000&gl=BR&hl=en'}
    URL = 'https://www.youtube.com/results?search_query='
    SPLIT = '/watch?v='
    response = webparser.api.request(URL + query, cookies=COOKIES)
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
    }
