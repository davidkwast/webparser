import requests_html

def request(url, cookies=None):
    s = requests_html.HTMLSession(mock_browser=False)
    return s.get(url, cookies=cookies)
