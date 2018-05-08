# coding=utf8
import sublime
import os
import re
import json
from .classes.Project import Project

class Utils:

    """Return Sublime Text packages path"""
    def packages_path():
        return sublime.packages_path() + '/'

    """Return Sublime Basic package path"""
    def package_path():
        return sublime.packages_path() + '/SublimeBasic/'

    """Get namespaces from composer.json"""
    def get_psr4_namespaces(self):
        content = self.file_get_contents('composer.json')

        if content:
            content = json.loads(content)

            # Check if autoload key exists
            if 'autoload' in content:
                autoload = content['autoload']

                # Check if PSR4 key exists
                if 'psr-4' in autoload:
                    return autoload['psr-4']

        return False

    """Get view contents"""
    def get_full_view(self, view):
        return view.substr(sublime.Region(0, view.size()))

    """Print something"""
    def print(*var):
        print("\t")
        print("\t")
        print(var)
        print("\t")
        print("\t")

    """Print regions to text"""
    def print_regions(*regions):
        for var in regions:
            for region in var:
                print(sublime.active_window().active_view().substr(region))

    """Get the contents of a given filename"""
    def file_get_contents(self, filename, relative=True):
        if relative:
            filename = Project.project_path() + filename

        if os.path.isfile(filename) != True:
            raise Exception("File does not exists")

        with open(filename) as line:
            return line.read()

    """ Get a setting key """
    def settings(key, default, filename=None):
        if filename != None:
            settings = sublime.load_settings(filename)
        else:
            settings = sublime.load_settings("SublimeBasic.sublime-settings")

        return settings.get(key, default)
