from PyTango._PyTango import DevLong, DevUChar, DevUShort, DevString, DevBoolean, DevDouble, DevFloat, DevVoid, DevULong, \
    DevVarULongArray, DevLong64, DevShort, DevULong64, SPECTRUM, IMAGE
from PyTango import CmdArgType

__author__ = 'miq'

from PyTango import DeviceProxy

from documentation import Documentation



class ExportedDeviceExtractor(object):

    __type_translation_table = {
        DevVoid: "void",
        DevFloat: "float",
        DevDouble: "double",
        DevBoolean: "boolean",
        DevString: "string",
        DevLong: "int",
        DevLong64: "long",
        DevUChar: "unsigned char",
        DevShort: "short",
        DevUShort: "unsigned short",
        DevULong: "unsigned int",
        DevULong64: "unsigned long",
        19: "state",
        DevVarULongArray: "unsigned int array"
    }

    argument_type_translation_table = {
        CmdArgType.DevVoid: 'void'
    }

    def translate(self, data_type, data_format):
        format = '' # for SCALAR
        if data_format == SPECTRUM:
            format = ' array'
        if data_format == IMAGE:
            format = ' 2D-array'
        if data_type in self.__type_translation_table:
            return self.__type_translation_table[data_type] + format
        else:
            return str(data_type) + format

    def translate_command_argument(self, argument_type):
        if argument_type in self.argument_type_translation_table:
            return self.argument_type_translation_table[argument_type]
        else:
            return str(argument_type)

    def parse(self, device_url):
        device = DeviceProxy(device_url)
        result = Documentation()
        result.name = device.info().dev_class
        result.description = device.description()
        # FIXME: perhaps need to query the database about the propertiess
        propertyNames = device.get_property_list('*')
        for propertyName in propertyNames:
            result.addproperty(propertyName, 'TODO description', 'TODO type name', 'TODO default')
        attributeInfos = device.attribute_list_query()
        for attributeInfo in attributeInfos:
            result.addattribute(attributeInfo.name, attributeInfo.description, self.translate(attributeInfo.data_type, attributeInfo.data_format))
        commandInfos = device.command_list_query()
        for commandInfo in commandInfos:
            result.addcommand(
                commandInfo.cmd_name,
                'TODO command description',
                self.translate_command_argument(commandInfo.in_type),
                commandInfo.in_type_desc,
                self.translate_command_argument(commandInfo.out_type),
                commandInfo.out_type_desc)
        return [result]

