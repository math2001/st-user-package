import sublime
import sublime_plugin

class JsonFixerCommand(sublime_plugin.TextCommand):

    """
    fix json trailing comma.
    """

    def remove_trailing_commas(self, edit):
        v = self.view
        if 'json' not in v.settings().get('syntax').lower():
            return
        regions = v.find_all(r',\s*[\]\}]')
        selection = v.sel()
        selection.clear()

        for region in regions:
            if 'punctuation' not in v.scope_name(region.begin()):
                continue
            selection.add(region)

        v.run_command('move', {"by": "characters", "forward": False})
        v.run_command('right_delete')

    def add_needed_comma(self, edit):
        v = self.view
        regions = v.find_all(r'[\}\]"]\s*["\{\[]')
        i = 0
        for region in regions:
            region = sublime.Region(region.begin() + i, region.end() + i)
            if not 'punctuation' in v.scope_name(region.begin()):
                continue
            if (v.substr(region.begin()) == '"' and 'punctuation.definition.'
                'string.end.json' not in v.scope_name(region.begin()) ):
                continue
            text = v.substr(region)
            v.replace(edit, region, text[0] + ',' + text[1:])
            i += 1

    def run(self, edit):

        v = self.view
        initial_colrows = []
        for region in v.sel():
            initial_colrows.append(v.rowcol(region.begin()))

        self.add_needed_comma(edit)
        self.remove_trailing_commas(edit)

        v.sel().clear()
        for col, row in initial_colrows:
            line_length = len(v.substr(v.line(sublime.Region(v.text_point(col, 0)))))
            if row > line_length:
                row = line_length
            v.sel().add(sublime.Region(v.text_point(col, row)))

    def is_enabled(self):
        return 'json' in self.view.settings().get('syntax').lower()

class JsonFixerListener(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.run_command('json_fixer')
