# -*- encoding: utf-8 -*-

import sublime_plugin

class TestMeCommand(sublime_plugin.TextCommand):

    def run(self, edit, dico):
        print("delete-me.py:8", dico)
        dico['hello'] = 'world'
        print("delete-me.py:10", dico)
