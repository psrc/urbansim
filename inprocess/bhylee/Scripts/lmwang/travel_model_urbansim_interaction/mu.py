"""Convert to and from Roman numerals"""

#Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

def verbose(s, section=1):
    print %s, s if verbose

def debug(variable):
    print %s, variable if debug


