import re
import sublime
from ..utils import Utils

class PhpBuilder:

    def clear_use_statements(self, view, edit):
        uses = []
        regions = view.find_by_selector("meta.use.php meta.path.php support.class.php")
        regions = regions + view.find_by_selector("meta.use.php meta.path.php support.class.builtin.php")

        for region in regions:
            uses.append(view.full_line(region))

        # Remove the whole block at once
        if (len(uses) > 0):
            view.replace(edit, sublime.Region(uses[0].a, uses[-1].b), "")

    """Insert namespace from symbol"""
    def insert_namespace_from_symbol(self, view, namespace):
        print(view)
        regions = view.find_all(r"^(use\s+.+[;])", 0)

        if len(regions) > 0:
            region = regions[0]
            for r in regions:
                region = region.cover(r)

            view.replace(edit, region, self.build_uses(view, namespace))
        else:
            region = view.find_by_selector("keyword.other.namespace.php")

            row, col = view.rowcol(region[0].begin())
            region   = view.text_point(row + 2, col)

            view.insert(edit, region, self.build_uses(view, namespace) + "\n\n")

        sublime.status_message("Successfully imported " + namespace)

    """Build use statements"""
    def build_uses(self, view, namespace):
        uses = []
        use_stmt = "use " + namespace + ";"

        view.find_all(r"^(use\s+.+[;])", 0, "$1", uses)
        uses.append(use_stmt)
        uses = list(set(uses))
        uses.sort(key = len)

        return "\n".join(uses)


