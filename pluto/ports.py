import re
import serial.tools.list_ports

class PortUtil(object):
    """Helper class that scan serial port automatically"""
    comports = [p[0] for p in serial.tools.list_ports.comports()]
    num_ports = len(comports)
    auto_port = None
    keywords = []
    patterns = []
    '''
    def __init__(self):
        pass
    '''

    @classmethod
    def count_ports(cls):
        return cls.num_ports
    
    @classmethod
    def scan(cls, *args, **kwargs):
        if len(args) == 0:
            cls.keywords = ['usb', 'serial']
        else:
            for index, val in enumerate(args):
                cls.keywords.append(val)

        for keyword in cls.keywords:
            p = re.compile('(/dev/)((tty)|(cu)|.*).({0})\w*[\d]'.format(keyword))
            cls.patterns.append(p)
                
        for port in cls.comports:
            for pattern in cls.patterns:
                m = pattern.match(port)
                if m:
                    cls.auto_port = m.group()
                else:
                    pass

        return cls.auto_port


        
            
            

        
        
