__author__ = 'marius.elvert@softwareschneiderei.de'

import xml.etree.ElementTree as ET
from Documentation import Documentation

class XmiParser:

    __type_translation_table = {
        "pogoDsl:VoidType" : "void",
        "pogoDsl:FloatType" : "float",
        "pogoDsl:BooleanType" : "boolean",
        "pogoDsl:StringType": "string",
        "pogoDsl:ConstStringType": "string",
        "pogoDsl:IntType": "integer",
        "pogoDsl:UShortType" : "unsigned short integer",
        "pogoDsl:UIntType" : "unsigned integer",
        "pogoDsl:StateType" : "state",
        "pogoDsl:UIntArrayType" : "unsigned int array"
    }

    def __translate_type(self, type):
        if type in self.__type_translation_table:
            return self.__type_translation_table[type]
        else:
            return type

    def __get_type(self, node, nodename="type"):
        namespace = {'xsi' : 'http://www.w3.org/2001/XMLSchema-instance'}
        return self.__translate_type(node.find(nodename).get("{%s}type" % namespace['xsi']))

    def parse(self, filename):
        tree = ET.parse(filename);
        root = tree.getroot()

        resultlist = []

        for classinfo in root.findall("classes"):

            result = Documentation()
            result.name = classinfo.attrib["name"]

            # Yes, the description is in an attrib called description in a node called description
            descriptionnode = classinfo.find("description")
            if descriptionnode is not None:
                result.description = descriptionnode.get("description")

            print classinfo.attrib["name"]

            for propertyinfo in classinfo.findall("deviceProperties"):
                name = propertyinfo.attrib["name"]
                description = propertyinfo.attrib["description"]
                type = self.__get_type(propertyinfo)
                defaultnode = propertyinfo.find("DefaultPropValue")
                default = defaultnode.text if defaultnode is not None else "-"
                print "\n\nPROPERTY - %s (type=%s, default=%s)" % (name, type, default)
                print "--"
                print ' '.join(description.splitlines())
                result.addproperty(name, description, type, default)

            for commandinfo in classinfo.findall("commands"):
                name = commandinfo.attrib["name"]
                description = commandinfo.attrib["description"]
                print "\n\nCOMMAND -  %s" % name
                print "--"
                print description
                argin = commandinfo.find("argin")
                parameter_description = argin.get("description")
                parameter_type = self.__get_type(argin)
                if parameter_type!="void":
                    print "Parameter: ", parameter_description, parameter_type
                argout = commandinfo.find("argout")
                result_description = argout.get("description")
                result_type = self.__get_type(argout)
                if result_type!="void":
                    print "Result: ", result_description, result_type

                result.addcommand(name, description, parameter_type, parameter_description, result_type, result_description)

            for attributeinfo in classinfo.findall("attributes"):
                name = attributeinfo.get("name")
                description = attributeinfo.find("properties").get("description")
                type = self.__get_type(attributeinfo, "dataType")
                result.addattribute(name, description, type)

            resultlist.append(result)

        return resultlist