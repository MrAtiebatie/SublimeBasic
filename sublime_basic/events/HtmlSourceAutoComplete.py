import os
import re
import glob
import sublime
import sublime_plugin
from ..utils import Utils

class HtmlSourceAutoComplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):

        scope = view.scope_name(view.sel()[0].b).split(' ')
        scopes = ['text.html.basic', 'source.js.embedded.html', 'string.quoted.double.html', 'meta.tag.inline.any.html']

        if not any(x in scope for x in scopes):
            return

        project = Utils.project_path()

        for sel in view.sel():
            line = view.line(sel.end())
            line = view.substr(line).strip()

            row, col  = view.rowcol(sel.begin())
            attribute = view.substr(view.word(view.text_point(row, col - 4)))

            regex = ""
            if attribute == "src":
                regex = re.compile('.*?src=["\']?((?:.(?!["\']?\s+(?:\S+)=|[>"\']))+.)["\']?')
            elif attribute == "href":
                regex = re.compile('.*?href=["\']?((?:.(?!["\']?\s+(?:\S+)=|[>"\']))+.)["\']?')

            search = re.search(regex, line)

            if search.lastindex != None:
                match = search.group(1).split('/')
                prefix = match.pop()

                return self.find(prefix, project + 'public' + '/'.join(match))

        # print(suggestions)

    def find(self, prefix, folder):
        result = []

        if not os.path.isdir(folder):
            return result

        for item in os.listdir(folder):
            if prefix in item.lower() and item != ".DS_Store":
                path = os.path.join(folder, item)
                if os.path.isdir(path):
                    result.append([item + '\tfolder', item])
                else:
                    result.append([item + '\tfile', item])

        return result