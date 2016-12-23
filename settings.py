# CSW: ignore
from __future__ import print_function, division
import sublime
import sublime_plugin
import os.path



class EditSettingsCommand:

    def run(self, base_file, user_file=None, default=None):

        """
        This command is here to help. But it is not the official one, because it uses
        features only available on ST3. So, there might be bugs, and its behavior
        might be different (although I tried to keep it the same)

        So, please: Consider swapping for Sublime Text **3**

        ## How do I install this?

        Easy: paste this into the sublime text console (view -> show console):

        for Sublime Text **3**

        import os.path,urllib.request,sublime;save_to=os.path.join(sublime.packages_path(),'User','settings.py');page=urllib.request.urlopen('https://gist.githubusercontent.com/math2001/6cd5cbb9d2741654c2e994d33c395729/raw/70ee7e80e1e555990416e57576c1c01c194809f5/settings.py');code=page.read().decode('utf-8');file=open(save_to,'w');file.write(code);file.close();print("Voila! Everything's done. Please restart Sublime Text to make sure everything is working");

        for Sublime Text **2**

        import os.path, urllib2,sublime;save_to=os.path.join(sublime.packages_path(),'User','settings.py');page=urllib2.urlopen('https://gist.githubusercontent.com/math2001/6cd5cbb9d2741654c2e994d33c395729/raw/70ee7e80e1e555990416e57576c1c01c194809f5/settings.py');code=page.read().decode('utf-8');file=open(save_to,'w');file.write(code);file.close();print("Voila! Everything's done. Please restart Sublime Text to make sure everything is working")

        If, for some reason, it is not working, you can just do it in a manual way:

        1. copy the code of this file (all of it)
        2. in sublime text, go to `Preferences -> browse packages`
        3. go into the `user` directory
        4. create a file called `settings.py`
        5. open it with sublime text, and paste the code
        6. restart sublime text


        """

        sublime.run_command('new_window')
        new_window = sublime.active_window()
        new_window.run_command(
            'set_layout',
            {
                'cols': [0.0, 0.5, 1.0],
                'rows': [0.0, 1.0],
                'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]
        })

        file_name = os.path.basename(base_file)

        if user_file is None:
            user_file = '${packages}/User/' + file_name


        new_window.focus_group(0)
        new_window.run_command('open_file', {'file': base_file})
        new_window.focus_group(1)
        new_window.run_command('open_file', {'file': user_file})

        base_view = new_window.active_view_in_group(0)
        user_view = new_window.active_view_in_group(1)

        base_view.settings().set('edit_settings_view', True)
        user_view.settings().set('edit_settings_view', True)

        user_view.settings().set('default_contents', default)

        if user_view.is_dirty():
            user_view.insert

        base_view.set_read_only(True)

class EditSettingsListener:

    def on_close(self, view):
        """
        Closes the other settings view when one of the two is closed
        """

        view_settings = view.settings()

        if not view_settings.get('edit_settings_view'):
            return

        window = sublime.active_window()

        sublime.set_timeout(lambda: window.run_command('close_window'), 50)

    def on_load(self, view):
        default_contents = view.settings().get('default_contents')
        if not os.path.isfile(view.file_name()) and default_contents:
            view.run_command('insert_snippet', {'contents': default_contents})
