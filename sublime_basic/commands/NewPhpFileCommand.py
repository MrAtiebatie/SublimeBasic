import sublime
import sublime_plugin
import os
from ..utils import Utils

#--------------------------------------------------------
# New PHP file
#--------------------------------------------------------
class NewPhpFileCommand(sublime_plugin.WindowCommand):

    def run(self, file, paths = []):
        self._paths = paths
        self._file = file
        window = sublime.active_window()
        view = window.active_view()

        window.run_command('hide_panel')
        window.show_input_panel('File Name:', '', self.create_file, None, None)

    def create_file(self, filename):
        filename = self._paths[0] + '/' + filename

        if filename.endswith('.php') != True:
            filename += '.php'

        if self._file == 'test.sublime-snippet' and not filename.endswith('Test.php'):
            filename = filename.replace('.php', 'Test.php')


        if os.path.isfile(filename):
            sublime.error_message('File already exists.')
            return

        with open(filename, 'a'):
            os.utime(filename, None)
            view = sublime.active_window().open_file(filename)

            self.insert_template(view)

    def insert_template(self, view):
        if not view.is_loading():
            view.run_command('insert_file_template', { 'template': Utils.package_path() + '/sublime_basic/templates/' + self._file })
        else:
            sublime.set_timeout(lambda: self.insert_template(view), 10)