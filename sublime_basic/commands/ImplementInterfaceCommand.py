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

                            class_methods = self.get_class_methods(content)
                            contract_methods = self.get_class_methods(contract)

                            # Here we calculate the difference between the required methods
                            # from the interface and the actual class methods
                            missing_methods = list(set(contract_methods) - set(class_methods))

                            if len(missing_methods) is 0:
                                sublime.message_dialog('Required interface methods already implemented.')

                            for method in missing_methods:
                                class_ending = view.find_all('[}]')

                                if len(class_ending) > 0:
                                    class_ending = class_ending[-1]
                                    row, col = view.rowcol(class_ending.a)

                                    view.insert(edit, view.text_point(row, col), "\n\n\t" + method + "\n\t{\n\n\t}\n")

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
        # @todo get method comments with the following regex: (\/\*([^*]|[\s]|\*+[^*\/]|[\s])*\*\/)
        methods = re.findall('([public |static |abstract |protected |private ]+function [^)]+\))', content, re.MULTILINE)
        result = []

        if len(methods) > 0:
            for match in methods:
                result.append(match.strip())

        return result