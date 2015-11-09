import sublime
import sublime_plugin
import os
import json
from xml.etree import ElementTree

#--------------------------------------------------------
#   New PHP class
#--------------------------------------------------------
class NewPhpClassCommand(sublime_plugin.TextCommand):

    folder = ''
    packages = ''

    def run(self, edit):
        view = self.view

        self.packages = sublime.packages_path() + '/'

        # Path variables
        folders = view.window().folders()
        filename = view.file_name()
        if (len(folders) > 0):
            self.folder = folders[0] + '/'
            filename = filename.replace(self.folder, '')

        namespaces = self.get_psr4_namespaces(view)

        print(namespaces)

        if namespaces:
            for namespace, folder in namespaces.items():
                if folder in filename:
                    namespace = namespace.replace('\\', '/')
                    filename = filename.replace(folder, namespace)

                    # Now extract the namespace and classname
                    namespace = os.path.dirname(filename).replace('/', '\\')
                    classname = os.path.basename(filename).replace('.php', '')

                    xml = ElementTree.parse(self.packages + 'SublimePlus/class.sublime-snippet')
                    snippet = xml.getroot().find('content').text
                    view.window().run_command('insert_snippet', dict(contents=snippet, NAMESPACE=namespace, CLASSNAME=classname))

    def get_psr4_namespaces(self, view):
        composer = self.folder + 'composer.json'
        content = self.file_get_contents(composer)

        if (content):
            content = json.loads(content)

            # Check if autoload key exists
            if 'autoload' in content:
                autoload = content["autoload"]

                # Check if PSR4 key exists
                if 'psr-4' in autoload:
                    return autoload['psr-4']

        return False

    def file_get_contents(self, filename):
        if (os.path.isfile(filename) != True):
            return False

        with open(filename) as line:
            return line.read()