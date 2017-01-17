# -*- encoding: utf-8 -*-
import os
import sys
import sublime
import sublime_plugin

# fix for import order

sys.path.append(os.path.join(sublime.packages_path(), 'LiveReload'))
LiveReload = __import__('LiveReload')
sys.path.remove(os.path.join(sublime.packages_path(), 'LiveReload'))

class MattSimpleRefresher(LiveReload.Plugin):

    title = "refresh command helper"
    description = "help to create the command matt_simple_refresh"

    def run(self, file):
        self.refresh(file)

class MattSimpleRefreshCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not self.view.file_name():
            return
        self.view.window().run_command('save_all')
        os.path.basename(self.view.file_name())
        MattSimpleRefresher().refresh(os.path.basename(self.view.file_name()))
