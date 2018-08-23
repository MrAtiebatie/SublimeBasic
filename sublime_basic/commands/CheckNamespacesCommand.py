import sublime
import sublime_plugin
from ..classes.Project import Project
from ..classes.PhpIndex import PhpIndex
from ..classes.PhpParser import PhpParser
from ..classes.PhpBuilder import PhpBuilder
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
        self.parser = PhpParser()
        self.builder = PhpBuilder()
        self.index = PhpIndex()

        dependencies = self.parser.get_dependencies(view)
        imported = self.parser.get_imported_classes(view)

        # Compare the used classes vs the imported classes
        unused, unimported = self.generate_difference(dependencies, imported)

        # Find their associated file
        unimported = self.lookup_symbols_unimported(unimported)

        # We separate the single occurrences from the multiple to show a quick panel
        self.single = list(filter(lambda item: isinstance(item[1], str), unimported))
        self.multiple = list(filter(lambda item: isinstance(item[1], list), unimported))

        self.import_or_quick_panel(self.single, self.multiple)

    """Generate the differences between the used dependencies and the imported dependencies"""
    def generate_difference(self, dependencies_r, imported_r):
        dependencies = list()
        imported = list()

        # Convert dependency regions to strings
        for dependency in dependencies_r:
            dependencies.append(self.view.substr(dependency))

        # Convert imported classes regions to strings
        for entity in imported_r:
            imported.append(self.view.substr(entity))

        # Generate the difference in imported classes and
        # used classes and get the regions
        unimported = [dep for dep in dependencies if dep not in imported]
        unimported_regions = [dep for dep in dependencies_r if self.view.substr(dep) in unimported]

        unimported_regions.reverse()

        # Generate the unused classes that are
        # imported at the top of the file
        unused = [dep for dep in imported if dep not in dependencies]
        unused_regions = [dep for dep in imported_r if self.view.substr(dep) in unused]

        return unused_regions, unimported_regions

    """Lookup unimported"""
    def lookup_symbols_unimported(self, unimported):
        results = []

        for entity in unimported:
            entity = self.view.substr(entity)

            # Dit zou eigenlijk hier niet moeten
            # want dan is het geen unimported class
            if entity.startswith("\\"):
                continue

            # Skip relative dependency
            if self.is_relative_dependency(entity):
                continue

            # Find location
            result = self.index.find_symbols(entity)

            results.append([entity, result])

        return results

    """Is it a relative dependency?"""
    def is_relative_dependency(self, entity):
        current = Project.working_dir(True)

        symbols = self.index.find_symbols(entity)

        if symbols is not None:
            designated = [sym for sym in symbols if current in sym]

            return len(designated) > 0
        else:
            return False

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
    def insert_namespace_from_symbol(self, filename, entity):
        filename = self.remove_project_name(filename)

        sublime.active_window().run_command("insert_namespace", { "item": [entity, filename] })

        self.entity = None

        # if self.view.is_dirty():
        #     sublime.active_window().run_command("save")

    """Import or show quick panel"""
    def import_or_quick_panel(self, single, multiple):
        # Import them
        if len(multiple) > 0:
            self.choose_from_occurrences(multiple[0])
        else:
            for result in single:
                self.insert_namespace_from_symbol(result[1], result[0])

    """Show quick panel"""
    def choose_from_occurrences(self, occurences):
        self.entity = occurences[0]

        occurences.pop(0)

        self.definitions = occurences[0]

        sublime.active_window().show_quick_panel(occurences[0], self.on_done)

    """On item selection"""
    def on_done(self, index):
        if index >= 0:
            self.insert_namespace_from_symbol(self.definitions[index], self.entity)

            self.multiple.pop(index)

            self.import_or_quick_panel(self.single, self.multiple)