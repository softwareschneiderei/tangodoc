__author__ = 'marius.elvert@softwareschneiderei.de'


class Documentation:
    class PropertyInfo:
        def __init__(self, name, description, type, default):
            self.name = name
            self.description = description
            self.type = type
            self.default = default

    class CommandInfo:
        def __init__(self, name, description, parameter_type, parameter_description, result_type, result_description):
            self.name = name
            self.description = description
            self.parametertype = parameter_type
            self.parameterdescription = parameter_description
            self.resulttype = result_type
            self.resultdescription = result_description

    class AttributeInfo:
        def __init__(self, name, description, type_name):
            self.name = name
            self.description = description
            self.type = type_name

    def __init__(self):
        self.name = ""
        self.description = ""
        self.properties = []
        self.commands = []
        self.attributes = []

    def addproperty(self, name, description, type_name, default):
        self.properties.append(Documentation.PropertyInfo(name, description, type_name, default))

    def addcommand(self, name, description, parameter_type, parameter_description, result_type, result_description):
        self.commands.append(
            Documentation.CommandInfo(name, description, parameter_type, parameter_description, result_type,
                                      result_description))

    def addattribute(self, name, description, type_name):
        self.attributes.append(Documentation.AttributeInfo(name, description, type_name))
