from xml.etree.ElementTree import ElementTree

__author__ = 'marius.elvert@softwareschneiderei.de'

import xml.etree.ElementTree as ElemTree
from documentation import Documentation


class XmiParser(object):

    __type_translation_table = {
        "pogoDsl:VoidType": "void",
        "pogoDsl:FloatType": "float",
        "pogoDsl:DoubleType": "double",
        "pogoDsl:BooleanType": "boolean",
        "pogoDsl:StringType": "string",
        "pogoDsl:ConstStringType": "string",
        "pogoDsl:IntType": "int",
        "pogoDsl:UCharType": "unsigned char",
        "pogoDsl:UShortType": "unsigned short",
        "pogoDsl:UIntType": "unsigned int",
        "pogoDsl:StateType": "state",
        "pogoDsl:UIntArrayType": "unsigned int array"
    }

    def __translate_type(self, data_type):
        if data_type in self.__type_translation_table:
            return self.__type_translation_table[data_type]
        else:
            return data_type

    def __get_type(self, node, nodename="type"):
        namespace = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        return self.__translate_type(node.find(nodename).get("{%s}type" % namespace['xsi']))

    def parse(self, filename):
        tree = ElemTree.parse(filename)
        root = tree.getroot()

        resultlist = []

        for classinfo in root.findall("classes"):

            result = Documentation()
            result.name = classinfo.attrib["name"]

            # Yes, the description is in an attrib called description in a node called description
            descriptionnode = classinfo.find("description")
            if descriptionnode is not None:
                result.description = descriptionnode.get("description")

            for propertyinfo in classinfo.findall("deviceProperties"):
                name = propertyinfo.attrib["name"]
                description = propertyinfo.attrib["description"]
                type = self.__get_type(propertyinfo)
                defaultnode = propertyinfo.find("DefaultPropValue")
                default = defaultnode.text if defaultnode is not None else "-"
                result.addproperty(name, description, type, default)

            for commandinfo in classinfo.findall("commands"):
                name = commandinfo.attrib["name"]
                description = commandinfo.attrib["description"]
                argin = commandinfo.find("argin")
                parameter_description = argin.get("description")
                parameter_type = self.__get_type(argin)
                argout = commandinfo.find("argout")
                result_description = argout.get("description")
                result_type = self.__get_type(argout)

                result.addcommand(name, description, parameter_type, parameter_description, result_type, result_description)

            for attributeinfo in classinfo.findall("attributes"):
                name = attributeinfo.get("name")
                description = attributeinfo.find("properties").get("description")
                type = self.__get_type(attributeinfo, "dataType")
                result.addattribute(name, description, type)

            resultlist.append(result)

        return resultlist