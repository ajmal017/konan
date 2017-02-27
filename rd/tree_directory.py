from __future__ import print_function

import datetime as dt

import glob

class Path(object):
    """docstring for Path."""
    def __init__(self, name = '', extension = '', children = []):
        super(Path, self).__init__()
        self._name = name
        self._extension = extension
        if self.extension != '':
            self._full_name =  self.name + '.' + self.extension
        else:
            self._full_name = self.name + '/'
        self._children = children
        #self._family = [] #full tree structure ?

    def __repr__(self):
        if self.extension != '':
            return self.name + '.' + self.extension
        else:
            return self.name + '/'

    def name():
        doc = "The name property."
        def fget(self):
            return self._name
        def fset(self, value):
            self._name = value
        def fdel(self):
            del self._name
        return locals()
    name = property(**name())

    def extension():
        doc = "The extension property."
        def fget(self):
            return self._extension
        def fset(self, value):
            self._extension = value
        def fdel(self):
            del self._extension
        return locals()
    extension = property(**extension())

    def full_name():
        doc = "The full_name property."
        def fget(self):
            return self._full_name
        def fset(self, value):
            self._full_name = value
        def fdel(self):
            del self._full_name
        return locals()
    full_name = property(**full_name())

    def children():
        doc = "The children property."
        def fget(self):
            return self._children
        def fset(self, value):
            self._children = value
        def fdel(self):
            del self._children
        return locals()
    children = property(**children())

    def add_child(self, node):
        if isinstance(node, Path):
            self.children.append(node)

    def showFamily(self, level = 0):
        if level == 0:
            print(self.name, end = '{')

        for child in self.children:
            child.showFamily(level = level -1)
            print(child, end = '{\n')

    def findPath(self, path_base = '', path_name = '', path_extension = ''):
        #TODO:NEED TO GET PARENTS
        """
        public Node findNode(Node n, String s) {
            if (n.name == s) {
                return n;
            } else {
                for (Node child: n.children.values()) {
                    Node result = findNode(child, s);
                    if (result != null) {
                        return result;
                    }
                }
            }
            return null;
        }
        """
        if path_extension != '':
            search_file =  path_name + '.' + path_extension
        else:
            search_file = path_name + '/'

        if self.full_name == search_file:
            path_file = path_base + self.full_name
            print(path_file)
            return path_file# + PARENTS

        # loop structure needs to change for recursion
        for child in self.children:

            child.findPath(path_base = self.full_name, path_name = path_name,
                            path_extension = path_extension)

c = []
for i in xrange(3):
    c.append(Path(name='foo'+str(i), extension='bar'))

p = Path('foo',children = c)
l = p.findPath(path_name='foo2', path_extension='bar')

glob.iglob('/')
