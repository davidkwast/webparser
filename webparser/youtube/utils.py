import dateparser

def parse_view_count(raw_str):
    return int(raw_str.split(' views')[0].replace(',',''))

def parse_likes(raw_str):
    return int(raw_str.replace(',',''))

def parse_user_username(raw_str):
    return raw_str.split('/')[-1]

def parse_user_id(raw_str):
    return raw_str.split('/')[-1]

def parse_keywords(raw_str):
    return [x.strip() for x in raw_str.split(',') if x[-3:] != '...']

def parse_str_date(raw_str):
    return dateparser.parse(raw_str.split('Published on ')[-1] + ' PST') # https://productforums.google.com/forum/#!topic/youtube/41autLEJ8xM
