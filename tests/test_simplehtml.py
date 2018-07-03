from requests_html import HTML


def test_simplehtml():
    
    doc = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>hello</title></head><body><h1>world</h1></body></html>'
    
    html = HTML(html=doc)
    
    assert html.find('title', first=True).text == 'hello'
    
    assert html.find('h1', first=True).text == 'world'
