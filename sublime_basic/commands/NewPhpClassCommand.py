import sublime
import sublime_plugin
import os
from ..utils import Utils

#--------------------------------------------------------
# New PHP class
#--------------------------------------------------------
class NewPhpClassCommand(sublime_plugin.WindowCommand):

    def run(self, paths = []):
        self._paths = paths
        window = sublime.active_window()
        view = window.active_view()

        window.run_command('hide_panel')
        window.show_input_panel('File Name:', '', self.create_file, None, None)

    def create_file(self, filename):
        filename = self._paths[0] + '/' + filename

        if filename.endswith('.php') != True:
            filename += '.php'

        if os.path.isfile(filename):
            sublime.error_message('File already exists.')
            return

        with open(filename, 'a'):
            os.utime(filename, None)
            view = sublime.active_window().open_file(filename)

            # v = self.window.new_file()
            # v.settings().set('default_dir', self._paths[0])
            # v.set_syntax_file('Packages/PHP/PHP.tmLanguage')
            # v.set_name(filename)

            self.insert_template(view)

    def insert_template(self, view):
        if not view.is_loading():
            print("Insert template")
            view.run_command('insert_file_template', { 'template': Utils().package_path() + '/class.sublime-snippet' })

        else:
            sublime.set_timeout(lambda: self.insert_template(view), 10)