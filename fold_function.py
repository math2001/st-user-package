import sublime, sublime_plugin
import os

def md(*t, **kwargs):
    t = kwargs.get('sep', ' ').join([str(el) for el in t])
    sublime.message_dialog(t)

def sm(*t, **kwargs):
    t = kwargs.get('sep', ' ').join([str(el) for el in t])
    sublime.status_message(t)

def em(*t, **kwargs):
    t = kwargs.get('sep', ' ').join([str(el) for el in t])
    sublime.error_message(t)

class FoldFunctionCommand(sublime_plugin.TextCommand):

    def run(self, edit, *args, **kwargs):
        v = self.view
        v.selection.clear()
        view_size = v.size()
        for region in v.find_by_selector('entity.name.function'):
            base_indentation = v.indentation_level(region.begin())
            line = v.full_line(region.end())
            region = sublime.Region(line.end() - 1)
            while True:

                line = v.full_line(line.end())
                if line.end() >= view_size:
                    region = region.cover(line)
                    break

                indentation = v.indentation_level(line.begin())
                stripped = v.substr(line).strip()
                if indentation <= base_indentation and stripped not in ['', '{']:
                    break
                elif indentation > base_indentation + 1 and 'parameter' in v.scope_name(line.begin()):
                    region = v.full_line(line.end())
                    region = sublime.Region(region.begin() - 1, region.b)
                else:
                    region = region.cover(line)

            v.selection.add(region)
            continue

            last_line = v.substr(region).splitlines(keepends=True)[-1]
            print("fold_function.py:44", repr(last_line))
            striped = last_line.strip()
            if striped == '':
                print("fold_function.py:47", region)
                region = sublime.Region(region.begin(), region.end() - len(last_line) - 1)
            elif striped == '}':
                print("fold_function.py:48", last_line)
                region = sublime.Region(region.begin(), region.end() - len(last_line))
            else:
                print("fold_function.py:53", repr(v.substr(v.full_line(region.end()))))

            # v.fold(region)
            v.selection.add(region)
