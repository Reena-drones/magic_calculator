import math
from .functions import *


def available_operations():
    temp = dir(math)
    general_operations = ['sum', 'subtract', 'multiply', 'divide', 'float', 'max', 'min', 'abs', 'round']
    math_operations = temp[5:]
    manual_operations = ['nsum', 'nsquaresum', 'navg']
    out = {'operations': general_operations, 'math_operations': math_operations, 'manual_operations': manual_operations}
    return out


def wrap_available_operations():
    result = available_operations()
    out = []
    for elem in result.values():
        out += elem
    return out
