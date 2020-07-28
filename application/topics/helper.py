import re
from random import randint

def create_slug_for_thread(title):
    return re.sub(r'[^\w+]', '-', title) + '.' + str(randint(1,100))

def create_slug_for_message():
    return 'msg#' + str(randint(1,100))