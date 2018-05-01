import sublime
import sublime_plugin
from ..classes.Project import Project
from ..classes.PhpParser import PhpParser
from ..utils import Utils

#--------------------------------------------------------
# Check namespaces
#--------------------------------------------------------
class CheckNamespacesCommand(sublime_plugin.TextCommand):

    results = []
    definitions = []
    entity = None

    """Constructor"""
    def run(self, edit):
        view = self.view
        php = PhpParser()

        dependencies = php.get_dependencies(view)
        imported = php.get_imported_classes(view)

        # Include a possible namespace in the dependencies
        dependencies = list(map(lambda dep: php.include_namespace(view, dep), dependencies))

        # Compare the used classes vs the imported classes
        unused, unimported = php.get_unimported(view, dependencies, imported)

        # Find their associated file
        unimported = self.lookup_unimported(unimported)

        # We separate the single occurrences from the multiple to show a quick panel
        single = list(filter(lambda item: isinstance(item[1], str), unimported))
        multiple = list(filter(lambda item: isinstance(item[1], list), unimported))

        # Import them
        for result in single:
            self.insert_namespace_from_symbol(result[1], result[0])

        if len(multiple) > 0:
            self.choose_from_occurrences(multiple[0])

    """Show quick panel"""
    def choose_from_occurrences(self, occurences):
        self.entity = occurences[0]

        occurences.pop(0)

        self.definitions = occurences[0]

        sublime.active_window().show_quick_panel(occurences[0], self.on_done)

    """Lookup unimported"""
    def lookup_unimported(self, unimported):
        results = []

        for entity in unimported:
            entity = self.view.substr(entity)

            if not entity.startswith("\\"):

                # Check if it's a relative dependency
                if not self.is_relative_dependency(entity):
                    result = self.find_existence(entity)

                    results.append([entity, result])

        return results

    """Is it a relative dependency?"""
    def is_relative_dependency(self, entity):
        current = Project.working_dir(True)
        symbols = self.find_existence(entity)
        designated = [sym for sym in symbols if current in sym]

        return len(designated) > 0

    """Find existence"""
    def find_existence(self, entity):
        symbols = sublime.active_window().lookup_symbol_in_index(entity)
        symbols = [entity for entity in symbols if ".php" in entity[0]]

        if len(symbols) == 1:
            return symbols[0][1]
        elif len(symbols) > 1:
            symbols = list(map(lambda item: item[1], symbols))

            return symbols

    """On item selection"""
    def on_done(self, index):
        if index >= 0:
            self.insert_namespace_from_symbol(self.definitions[index], self.entity)

            self.view.run_command("check_namespaces")

    """Remove project name from filename"""
    def remove_project_name(self, filename):
        # For some reason Sublime Text only prepends the project
        # folder name if it has more than 2 project folders
        if len(sublime.active_window().folders()) == 1:
            return filename

        filename = filename.split("/")

        filename.pop(0)

        return "/".join(filename)

    """Insert namespace from symbol"""
    # PhpBuilder
    def insert_namespace_from_symbol(self, filename, entity):
        filename = self.remove_project_name(filename)

        sublime.active_window().run_command("insert_namespace", { "item": [entity, filename] })

        self.entity = None

        if self.view.is_dirty():
            sublime.active_window().run_command("save")