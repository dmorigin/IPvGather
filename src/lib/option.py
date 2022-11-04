
"""
"""
class Option:

    """
    """
    def __init__(self, value):
        self._value = value


    """
    """
    def some(self) -> bool:
        return self._value != None


    """
    """
    def none(self) -> bool:
        return self._value == None


    """
    """
    def get(self):
        return self._value

# // class Option

"""
"""
def none() -> Option:
    return Option(None)


"""
"""
def some(value) -> Option:
    return Option(value)
