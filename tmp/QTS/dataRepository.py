from __future__ import print_function

import sys
import os
import traceback

class dataRepository(object):
    def __init__(self, dir_root = '/', project = 'test/', data_file = 'test.txt'):
        self._root = dir_root #find users Dropbox folder
        self._projects = os.listdir(self.root)
        self._current_project = self.selectProject(project = project)
        self._current_file = data_file

    def selectProject(self, project = ''):
        if project not in self.projects:
            try:
                os.mkdir(self.root + project) # try for mkdirs
            except:
                print(traceback.format_exc()+'\n')
                return ''
        return project

    def checkData(self, path = ''):
        if not os.path.exists(path):
            # decide which to use
            return False
            '''raise IOError('The file: ' + path +
                        ' does not exist or could not be found.')'''
        else:
            return True

    def root():
        doc = "The root property."
        def fget(self):
            return self._root
        def fset(self, value):
            self._root = value
        def fdel(self):
            del self._root
        return locals()
    root = property(**root())

    def projects():
        doc = "The projects property."
        def fget(self):
            return self._projects
        def fset(self, value):
            self._projects = value
        def fdel(self):
            del self._projects
        return locals()
    projects = property(**projects())

    def current_project():
        doc = "The current_project property."
        def fget(self):
            return self._current_project
        def fset(self, value):
            self._current_project = value
        def fdel(self):
            del self._current_project
        return locals()
    current_project = property(**current_project())

    def current_file():
        doc = "The current_file property."
        def fget(self):
            if self.checkData(self._current_file):
                return self._current_file
            else:
                return self.checkData(self._current_file)
        def fset(self, value):
            self._current_file = value
        def fdel(self):
            del self._current_file
        return locals()
    current_file = property(**current_file())

    def project_path():
        doc = "The project_path property."
        def fget(self):
            return self._root + self._current_project
        return locals()
    project_path = property(**project_path())

    def file_path():
        doc = "The file_path property."
        def fget(self):
            return self._root + self._current_project + self._current_file
        return locals()
    file_path = property(**file_path())
