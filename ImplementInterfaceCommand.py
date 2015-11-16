import re
import sublime
import sublime_plugin
from .SublimeBasic import Basic

#--------------------------------------------------------
# Implement Interface Plugin
#--------------------------------------------------------
class ImplementInterfaceCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view

        project_path = Basic().project_path()
        content = Basic().get_full_view(view)
        interfaces = self.get_interface(content)

        for interface in interfaces:
            if isinstance(interface, str):
                # @todo implement the check by namespace
                # interface_namespace = self.get_interface_namespace(content, interface)

                tags = open(project_path + '.tags', 'r', newline='', encoding='utf-8')
                with tags as inF:
                    for line in inF:
                        if 'interface ' + interface in line:
                            filename = line.strip().split()[1]
                            contract = Basic().file_get_contents(filename)

                            print(self.get_class_methods(contract))

                            return

    # Get class name
    def get_class_name(self, content):
        return re.findall('class ([a-zA-Z]+)', content, re.MULTILINE)

    # Find interface
    def get_interface(self, content):
        matches = re.findall('implements([\s\w,]+)', content, re.MULTILINE)
        interfaces = []

        if len(matches) > 0:
            for match in matches[0].split(','):
                interfaces.append(match.strip())

            return interfaces
        else:
            return None

    # Get interface namespace
    def get_interface_namespace(self, content, interface):
        regex = r'use ([a-zA-Z\\]+(' + interface + '));'
        matches = re.findall(regex, content)

        if len(matches) > 0:
            return matches[0][0]
        else:
            return None

    # Get first element
    def get_first(self, array):
        if len(array) > 0:
            return array[0]

    # Get class methods
    def get_class_methods(self, content):
        matches = re.findall('([public |static |abstract |protected |private ]+function [^)]+\))', content, re.MULTILINE)
        methods = []

        if len(matches) > 0:
            for match in matches:
                methods.append(match.strip())

        return methods