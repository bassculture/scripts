# radata.py

class Value:
    def __init__(self, value = None):
        self.value = value
        self.children = dict() # dict of Value indexed by path

    def addChild(self, child_path, child):
        if child_path not in self.children:
            self.children[child_path] = child
        return self.children[child_path]

    def addChild(self, child_path, value):
        if child_path not in self.children:
            self.children[child_path] = Value(value)
        return self.children[child_path]

class Row:
    
    def __init__(self, model):
        self.model = model
        self.values = dict() # of Value indexed by path

    def readFromTabbedText(self, tabbedrow):
        self.rawdata = tabbedrow
        textfields = tabbedrow.split('\t')
        for path in self.model.fields: 
            index = self.model.fields[path].index
            if index != None and \
                index in range(0, len(textfields)) and \
                textfields[index] != '':

                self.values[path] = Value(textfields[index])

            for child_path in self.model.fields[path].children:
                child_index = self.model.fields[path].children[child_path].index
                if child_index != None and \
                    child_index in range(0, len(textfields)) and \
                    textfields[child_index] != '':

                    if path not in self.values:
                        self.values[path] = Value(None)

                    self.values[path].children[child_path] = Value(textfields[child_index])
        return self



