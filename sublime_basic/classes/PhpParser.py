import re
import sublime
import inspect
from ..utils import Utils

class PhpParser:

    """Get imported class from a view"""
    def get_imported_classes(self, view):
        regions = view.find_by_selector("meta.use.php")
        usages = list()

        for region in regions:
            usage = view.word(sublime.Region(region.b - 1, region.b))

            usages.append(usage)

        return usages

    """Get used classes in code"""
    def get_dependencies(self, view):

        # Get all dependencies
        classes = view.find_by_selector("meta.path.php support.class.php")
        classes += view.find_by_selector("meta.path.php support.class.builtin.php")
        extensions = view.find_by_selector("meta.path.php entity.other.inherited-class.php")

        view.erase_regions("usages")
        view.erase_regions("classes")
        view.erase_regions("extensions")
        view.erase_regions("imported")

        # List of dependencies
        classes.reverse()
        dependencies = extensions + classes

        # Grab imported classes to filter them
        imported = self.get_imported_classes(view)

        dependencies = self.filter_duplicate_regions(dependencies, imported)

        # Include a possible namespace in the dependencies
        return list(map(lambda dep: self.include_namespace(view, dep), dependencies))

    """Include namespace"""
    def include_namespace(self, view, region):
        extended = sublime.Region(region.a - 1, region.b)
        string = view.substr(extended)

        # Loop until we find one of the characters in this list
        if string[0] in [" ", "(", "[", "{"]:
            return region
        else:
            return self.include_namespace(view, extended)

    """Filter duplicate regions"""
    def filter_duplicate_regions(self, regions1, regions2):
        return [region for region in regions1 if region not in regions2]

    """Get namespace from file"""
    def get_namespace_from_file(self, filename, classname):
        contents = Utils().file_get_contents(filename)

        namespace = re.findall("namespace ([^\s]+);", contents, re.MULTILINE)

        if namespace:
            return namespace[0] + "\\" + classname
        else:
            return classname