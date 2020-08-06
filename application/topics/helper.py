import re
from string import ascii_letters, digits
from random import choice

def create_slug(title, type):
    if type == 'Message':
        if title:
            return title[:3] + ''.join([choice(ascii_letters + digits) for i in range(8)])
        else:
            return ''.join([choice(ascii_letters + digits) for i in range(11)])
    elif type == 'Thread':
        return re.sub(r'[^\w+]', '-', title) + '.' + ''.join([choice(ascii_letters + digits) for i in range(3)])
    elif type == 'Topic':
        return re.sub(r'[^\w+]', '-', title)