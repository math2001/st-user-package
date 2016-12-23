# -*- encoding: utf-8 -*-

import json


file = 'C:/Users/math/AppData/Roaming/Sublime Text 3/Packages/Default/Main.sublime-menu'
# file = 'C:/Users/math/AppData/Roaming/Sublime Text 3/Packages/User/Main.sublime-menu'

with open(file) as fp:
    obj = json.load(fp)


keys = []

def add_keys(obj, keys):
    if isinstance(obj, list):
        for item in obj:
            add_keys(item, keys)
    elif isinstance(obj, dict):
        for key, item in obj.items():
            keys.append(key) if key not in keys else None
            add_keys(item, keys) if key != 'args' else None


add_keys(obj, keys)
