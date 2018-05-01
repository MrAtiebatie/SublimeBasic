import sublime

"""Project class"""
class Project():

    """Get project path"""
    def project_path():
        folders = sublime.active_window().folders()

        folders = [folder for folder in folders if "Sublime Text" not in folder]

        if (len(folders) > 0):
            folder = folders[0]

        if folder.endswith('/') != True:
            folder += '/'

        return folder

    """Get filename"""
    def filename(relative=False):
        filename = sublime.active_window().active_view().file_name()

        if relative:
            return filename.replace(Project.project_path(), "")
        else:
            return filename

    """Get working directory"""
    def working_dir(relative=False):
        filename = Project.filename(relative)

        filename = filename.split("/")

        filename.pop()

        return "/".join(filename)