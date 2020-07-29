import re
from random import randint

def create_slug(title, type):
    if type == 'Message':
        return 'msg#' + str(randint(1, 100))
    elif type == 'Thread':
        return re.sub(r'[^\w+]', '-', title) + '.' + str(randint(1, 100))
    elif type == 'Topic':
        return re.sub(r'[^\w+]', '-', title)