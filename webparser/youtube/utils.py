import dateparser

def parse_view_count(raw_str):
    return int(raw_str.split(' views')[0].replace(',',''))

def parse_likes(elem):
    if elem:
        return int(elem.text.replace(',',''))
    else:
        return 0

def parse_user_username(raw_str):
    return raw_str.split('/')[-1]

def parse_user_id(raw_str):
    return raw_str.split('/')[-1]

def parse_keywords(raw_str):
    return [x.strip() for x in raw_str.split(',') if x[-3:] != '...']

def parse_str_date(raw_str):
    raw_str = raw_str.replace('Published on ', '').strip()
    raw_str = raw_str.replace('Streamed live on ', '').strip()
    raw_str += ' PST'
    return dateparser.parse(raw_str) # https://productforums.google.com/forum/#!topic/youtube/41autLEJ8xM
