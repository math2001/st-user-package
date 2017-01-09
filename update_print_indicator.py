# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
from os.path import basename

class UpdatePrintIndicatorCommand(sublime_plugin.TextCommand):

    def run(self, edit, lines=[]):
        v = self.view
        # CSW: ignore
        regions = v.find_all(r'print\("[\w\-]+\.py:\d+",')
        for region in regions:
            # CSW: ignore
            text = 'print("{}:{}",'.format(basename(v.file_name()),
                                           v.rowcol(region.begin())[0] + 1)
            v.replace(edit, region, text)
