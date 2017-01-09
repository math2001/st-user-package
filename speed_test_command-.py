# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin as sp
import time

class ScopeVsSettingsCommand(sp.TextCommand):

    def run(self, edit):
        scope_name = []
        settings = []
        for i in range(500):
            t = time.time()
            self.view.scope_name(0)
            scope_name.append(time.time() - t)
        for i in range(500):
            t = time.time()
            self.view.settings().get('markdown_live_preview_enabled')
            settings.append(time.time() - t)

        msg = ["scope_name: {}".format(sum(scope_name) / len(scope_name))]
        msg += ["settings  : {}".format(sum(settings) / len(settings))]
        msg = '\n'.join(msg)

        sublime.message_dialog(msg)
