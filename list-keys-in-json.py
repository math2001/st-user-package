# -*- encoding: utf-8 -*-

import json
import sublime

file = 'C:/Users/math/AppData/Roaming/Sublime Text 3/Packages/Default/Default.sublime-commands'
# file = 'C:/Users/math/AppData/Roaming/Sublime Text 3/Packages/User/Main.sublime-menu'

def main():
    try:
        with open(file) as fp:
            obj = sublime.decode_value(fp.read())
    except FileNotFoundError:
        return
    keys = {}

    def add_keys(obj, keys):
        if isinstance(obj, list):
            for item in obj:
                add_keys(item, keys)
        elif isinstance(obj, dict):
            for key, item in obj.items():
                keys[key] = type(item).__name__
                add_keys(item, keys) if key != 'args' else None
        return keys

    add_keys(obj, keys)
