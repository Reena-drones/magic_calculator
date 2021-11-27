from math import *
from . import Exceptions

def check_two_error(func):
    def inner(args):
        if not isinstance(args, tuple):
            raise Exceptions.TwoArgumentNeeded
        elif len(args) != 2:
            raise Exceptions.TwoArgumentNeeded
        else:
            return func(args)
    return inner


def check_one_error(func):
    def inner(args):
        if isinstance(args , tuple):
            raise Exceptions.OneArgumentNeeded
        elif isinstance(args, float):
            raise Exceptions.IntgerAllowed
        else:
            return func(args)
    return inner


@check_two_error
def subtract(args):
    return args[0] - args[1]


@check_two_error
def multiply(args):
    return args[0] * args[1]


@check_two_error
def divide(args):
    print('divide')
    return args[0]/args[1]

@check_one_error
def navg(n):
    return sum([a for a in range(n)])/n


@check_one_error
def nsum(n):
    return sum([a for a in range(n)])


@check_one_error
def nsquaresum(n):
    print(n)
    return sum([a*a for a in range(n+1)])


def operate_math(method, *args):
    try:
        m = eval(method)
        if len(args) == 1:
            try:
                return m(args[0])
            except TypeError:
                return m(args)
        try:
            return m(args)
        except TypeError:
            return m(args[0])

    except Exceptions.TwoArgumentNeeded:
        raise Exceptions.TwoArgumentNeeded

    except Exception as e:
        print(type(e))
        raise e


