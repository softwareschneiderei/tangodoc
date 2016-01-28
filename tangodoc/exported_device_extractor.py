__author__ = 'miq'

from PyTango import DeviceProxy

from documentation import Documentation


class ExportedDeviceExtractor(object):

    def parse(self, device_url):
        device = DeviceProxy(device_url)
        result = Documentation()
        result.name = device.info().dev_class
        result.description = device.description()

        return [result]
