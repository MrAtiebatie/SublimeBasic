# coding=utf8
import sublime
import os
import re
import json

class Basic:

    # def __init__(self):
    #     print(self)

    # Get project path
    def project_path(self):
        folders = sublime.active_window().folders()

        if (len(folders) > 0):
            folder = folders[0]

        if folder.endswith('/') != True:
            folder += '/'

        return folder

    # Return Sublime Text packages path
    def packages_path(self):
        return sublime.packages_path() + '/'

    # Return Sublime Basic package path
    def package_path(self):
        return sublime.packages_path() + '/SublimePlus/'

    # Get namespaces from composer.json
    def get_psr4_namespaces(self):
        composer = self.project_path() + 'composer.json'
        content = self.file_get_contents(composer)

        if (content):
            content = json.loads(content)

            # Check if autoload key exists
            if 'autoload' in content:
                autoload = content['autoload']

                # Check if PSR4 key exists
                if 'psr-4' in autoload:
                    return autoload['psr-4']

        return False

    # Get the contents of a given filename
    def file_get_contents(self, filename):
        if (os.path.isfile(filename) != True):
            return False

        with open(filename) as line:
            return line.read()