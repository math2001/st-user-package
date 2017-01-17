# -*- encoding: utf-8 -*-

import sublime
import sublime_plugin
import re

class Contextr(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        if key != "": return
        if operator != sublime.OP_REGEX_CONTAINS:
            return
        view.settings().get('wo.disabled_keymap')
