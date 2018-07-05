def parse_view_count(raw_str):
    return int(raw_str.split(' views')[0].replace(',',''))

def parse_user_username(raw_str):
    return raw_str.split('/')[-1]

def parse_user_id(raw_str):
    return raw_str.split('/')[-1]
