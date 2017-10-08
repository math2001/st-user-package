# -*- encoding: utf-8 -*-

import time
import sublime
import sublime_plugin

class InsertTimestamp(sublime_plugin.TextCommand):
    
    def run(self, edit):
        for region in self.view.sel():
            self.view.erase(edit, region)
            self.view.insert(edit, region.begin(), str(time.time() * 1000))
