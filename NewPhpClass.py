import sublime
import sublime_plugin
import os
import json

#--------------------------------------------------------
#   New PHP class
#--------------------------------------------------------
class NewPhpClassCommand(sublime_plugin.TextCommand):

    folder = ''

    def run(self, edit):
        view = self.view

        # Path variables
        folders = view.window().folders()
        filename = view.file_name()
        if (len(folders) > 0):
            self.folder = folders[0] + '/'
            filename = filename.replace(self.folder, '')
            print(filename)

        print(self.is_psr4(view))

    def is_psr4(self, view):
        composer = self.folder + 'composer.json'
        content = self.file_get_contents(composer)

        if (content):
            content = json.loads(content)

            # Check if autoload key exists
            if 'autoload' in content:
                autoload = content["autoload"]

                # Check if PSR4 key exists
                if 'psr-4' in autoload:
                    return True

        return False

    def file_get_contents(self, filename):
        if (os.path.isfile(filename) != True):
            return False

        with open(filename) as line:
            return line.read()